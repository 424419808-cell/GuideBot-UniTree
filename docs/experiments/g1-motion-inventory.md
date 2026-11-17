# G1 动作库盘点

日期：2026-11-17。源仓库 /home/kwx/g1-arm-teach-play 的 main 工作区干净；仅只读扫描。使用原库 tools/motion_library.py 的 catalog_entries、inspect、parse_motion、validate_metadata 和 SHA256 校验。目标库复制后数据文件与 metadata 逐文件一致。

| 已录制动作 | 物理类型 | 帧数 | 关节数 | metadata | 模型可用 |
|---|---|---:|---:|---|---|
| neutral | pose | 1 | 14 | approved / 校验通过 | 是 |
| greet_open | motion | 1 | 14 | approved / 校验通过 | 是，规划为 pose |
| greet_wave | motion | 3 | 14 | approved / 校验通过 | 是 |
| invite_follow | motion | 4 | 14 | approved / 校验通过 | 是 |
| present_center | motion | 1 | 14 | approved / 校验通过 | 是 |
| present_left | motion | 1 | 14 | approved / 校验通过 | 是，规划为 pose |
| present_right | motion | 1 | 14 | approved / 校验通过 | 是，规划为 pose |
| please_wait | motion | 1 | 14 | approved / 校验通过 | 是，规划为 pose |
| request_repeat | motion | 1 | 14 | approved / 校验通过 | 是，规划为 pose |
| emphasize_once | motion | 3 | 14 | approved / 校验通过 | 是 |

未录制的 12 项：invite_question、indicate_forward、indicate_left、indicate_right、acknowledge_question、answer_open、refer_staff、emphasize_twice、thanks、elevator_indicate_panel、elevator_button_prepose、elevator_boarding_invite。均缺少物理 .dat，未生成假数据，也未暴露给模型。

数据校验失败：无。present_center 已在 2026-11-17 完成真机试播验收，metadata 状态为 approved。关节限位配置仍为 verified=false，因此当前 Sequence 真机播放仍受限位门禁阻止。
