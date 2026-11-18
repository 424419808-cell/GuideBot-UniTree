# G1 上肢动作模块

`GuideBot.gesture` 负责动作选择与调度；本模块负责录制资产校验、本地 socket 协议和
已批准轨迹的执行。

- `client.py`：运行时 UNIX socket 客户端。
- `assets.py`：运行时和离线工具共用的目录、轨迹、元数据及时间配置校验。
- `motion_library_server.cpp` 和头文件：G1 控制服务及轨迹逻辑。
- `config/`：物理动作清单与关节限位。
- `assets/motions/`、`assets/poses/`、`assets/metadata/`：录制数据与验收记录。
  清单中也包含尚未录制的动作。

在仓库根目录构建：
`cmake -S GuideBot/hardware/g1_motion -B GuideBot/hardware/g1_motion/build`
和 `cmake --build GuideBot/hardware/g1_motion/build -j 4`。
`build/` 是生成目录，不纳入版本控制。录制、试播、验收和时间编辑工具在
`tools/motions/`；现场操作流程见 `docs/motions/motion-library.md`。

C++ 源码及动作资产整合自独立的 `g1-arm-teach-play` 项目；许可文本保留在 `LICENSE`。
