# G1 EDU+ 29 自由度：本机测试入口

本机环境为 `~/.conda/envs/GuideBot`（Python 3.10）。Python 依赖依据
`/home/kwx/requirements.txt`，安装副本位于
`~/.config/guidebot/requirements-portable.txt`，仅将原机器不可访问的
`file:///home/conda/feedstock_root/...` 构建路径改为包名。模型和原生库保存在
`~/.local/share/guidebot/deps/`；密钥仍在 `~/.config/guidebot/conversation.env`。

在仓库根目录运行：

```bash
bash tools/guidebot.sh check
bash tools/guidebot.sh evaluate --case open_question_expanded
```

`check` 只做本地检查，不连接 DDS、不录音、不运动。`evaluate` 会调用 DeepSeek，
但不驱动机器人。脚本使用 GuideBot 环境绝对路径，无需先激活 Conda；也可手动
`source ~/.bashrc` 后 `conda activate GuideBot`。

## 先验收单动作

机器人停稳、现场具备操作条件后，由操作员手动执行：

```bash
bash tools/guidebot.sh preview greet_open --no-confirm
```

试播会接管并播放，随后返回并释放。`--no-confirm` 避免修改已有动作验收状态。
仅离线检查时追加 `--check`。单次试播与常驻运动服务不可同时运行。

## 语音与动作联动

先同步项目已有的知识文档（会上传到配置的阶跃账户），并在模拟模式下验证对话：

```bash
GUIDEBOT_GESTURE_EXECUTION_MODE=simulation bash tools/guidebot.sh conversation --sync-knowledge
```

按 Enter 才开始录放音，再按 Enter 停止。后续已同步且内容未改变时可省略
`--sync-knowledge`。模拟阶段检查会话目录中的 `gesture.jsonl`，区分 planned、
command、skipped 和 execution_error；模型选中动作不代表动作已发送。

真机联动只需一个终端。机器人停稳后运行：

```bash
GUIDEBOT_GESTURE_EXECUTION_MODE=robot python GuideBot/conversation/conversation.py
```

第一次按 Enter 后程序自动启动运动服务并接管上半身；第二次按 Enter 后自动停止动作、释放控制权并退出服务。已有运动服务时会拒绝启动，避免接管其他进程。动作依据机器人播报文本规划。需要中止当前动作时：

```bash
bash tools/guidebot.sh motion stop
```

## 限位来源与验证边界

`GuideBot/hardware/g1_motion/config/arm_joint_limits.json` 中 14 个上肢关节的范围来自宇树官方仓库
`unitreerobotics/unitree_ros/robots/g1_description/g1_29dof.urdf`。
配置记录来源 URL、下载文件 SHA256、核验人/方式、时间与范围。已逐项核对关节顺序、
有限数值区间，以及全部 10 个录制资产的所有帧。`verified=true` 仅表示这项配置与
录制数据核验通过，不代表现场标定、碰撞检测或物理试播。

生产流程还未向 GestureService 接入 navigation、scene、asr/dialogue、task 状态源。
因此跟随、展示、澄清、等待动作在缺少对应可信状态时会被拒绝，不能以评测文件中的
模拟状态代替真实状态。`gesture.released` 只释放调度器记录，不主动收回手臂；
基础姿态仍需状态机显式请求。
