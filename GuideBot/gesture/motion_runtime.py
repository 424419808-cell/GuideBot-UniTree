"""Own the local motion server for one conversation session."""
import subprocess
import time

from .catalog import MOTION_ROOT
from GuideBot.hardware.g1_motion.client import request as socket_request, SOCKET_NAME


class MotionRuntime:
    def __init__(self, *, request=None, popen=subprocess.Popen, clock=time.monotonic,
                 sleep=time.sleep):
        if request is None:
            request = lambda payload: socket_request(SOCKET_NAME, payload)
        self.request = request
        self.popen = popen
        self.clock = clock
        self.sleep = sleep
        self.process = None

    def _status(self):
        return self.request({'状态': True})['status']

    def _wait(self, ownership, timeout):
        deadline = self.clock() + timeout
        while self.clock() < deadline:
            if self.process.poll() is not None:
                raise RuntimeError(f'Motion server exited: {self.process.returncode}')
            status = self._status()
            if status['ownership'] == ownership:
                return status
            if ownership == 'owned' and status['ownership'] == 'released':
                raise RuntimeError('Motion server rejected upper-body acquire')
            self.sleep(.1)
        raise TimeoutError(f'Motion server did not reach {ownership}')

    def start(self):
        binary = MOTION_ROOT / 'build/motion_library_server'
        if not binary.is_file():
            raise FileNotFoundError(f'{binary}; build the motion library first')
        # The fixed socket must be free; an existing controller is never taken over.
        try:
            self._status()
        except OSError:
            pass
        else:
            raise RuntimeError('A motion server is already running')
        self.process = self.popen([str(binary), '--start-released'], cwd=MOTION_ROOT,
                                  stdin=subprocess.PIPE, text=True)
        try:
            self.process.stdin.write('RUN\n')
            self.process.stdin.flush()
            self.process.stdin.close()
            deadline = self.clock() + 15
            while True:
                if self.process.poll() is not None:
                    raise RuntimeError(f'Motion server exited: {self.process.returncode}')
                try:
                    status = self._status()
                    break
                except OSError:
                    if self.clock() >= deadline:
                        raise TimeoutError('Motion server startup timed out')
                    self.sleep(.1)
            if status['ownership'] != 'released':
                raise RuntimeError('Motion server did not start released')
            self.sleep(1.5)
            self.request({'接管': True})
            self._wait('owned', 15)
        except BaseException:
            self.stop()
            raise

    def stop(self):
        process = self.process
        self.process = None
        if process is None or process.poll() is not None:
            return
        try:
            status = self._status()
            if status['ownership'] == 'owned':
                self.request({'停止': True})
                self.request({'释放': True})
            if status['ownership'] != 'released':
                deadline = self.clock() + 30
                while self.clock() < deadline:
                    if self._status()['ownership'] == 'released':
                        break
                    self.sleep(.1)
                else:
                    raise TimeoutError('Upper-body release timed out')
            self.request({'退出': True})
            process.wait(timeout=10)
        except (OSError, ValueError, subprocess.TimeoutExpired, TimeoutError):
            process.terminate()
            try:
                process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                process.kill()
                process.wait()
