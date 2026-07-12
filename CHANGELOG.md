# Changelog

## [Unreleased]

### Added

- `.github/workflows/ci.yml`: 主 CI 流水线（子模块校验、hisiflash Rust 构建测试、location_app Android 构建、文档链接校验）。
- `.github/workflows/firmware-build.yml`: 固件批量构建流水线（需自托管 Runner + HiSilicon SDK）。
- Tag 固件新增电池电压/电量监测：每次定位帧通过 BLE 上报 `batteryMv` 和 `batteryPct`，APP 端显示实时电压和电量百分比。
- `scripts/serial_monitor.py`: 串口日志实时采集脚本，带毫秒级时间戳，支持自定义端口和波特率。
- `Docs/硬件参考_BearPi_Pico_H2821E.md`: BearPi Pico H2821E 开发板硬件参考。

### Changed

- 项目目录整理：`app_logo.png` 移入 `Docs/assets/`。
- 清理 `submit_materials/` 冗余文件（旧版视频 v1、旧版文档 v2、模板、未签名授权书）。
- `.gitignore` 统一子模块忽略规则（补充 `location_app`），新增 `submit_materials/` 大文件排除规则。

### Fixed

- Kconfig 修复多余的 `endif` 导致构建失败。
- `sle_locate_adc.c` 补充缺失的 `pinctrl.h` 头文件。

### Changed

- 构建脚本 `build_locate_firmwares.py` Tag 构建时显式启用 ADC 和 BLE。
- `standard_bs21e_1100e.config` 默认启用 `CONFIG_SLE_LOCATE_ENABLE_ADC`。

## [0.2.0] - 2026-06-10

### Added

- `peripheral/sle_locate_nfc.c/h`: NFC-A Tag 驱动，支持 NDEF 文本配置、RF 场检测和低功耗休眠唤醒
- `peripheral/sle_locate_i2c.c/h`: I2C0 主机驱动（GPIO_14/SCL, GPIO_15/SDA），支持读写和总线扫描
- `peripheral/sle_locate_button.c/h`: GPIO 按键驱动（P0.25），支持短按/长按/双击检测和去抖动
- `peripheral/sle_locate_pm.c/h`: 低功耗管理框架，支持 IDLE/LIGHT/DEEP 三级休眠，集成电量监测和定时唤醒
- Kconfig 新增 `SLE_LOCATE_ENABLE_NFC`、`SLE_LOCATE_ENABLE_BUTTON`、`SLE_LOCATE_ENABLE_PM` 开关

### Fixed

- **ADC 引脚错误 (P0)**: `BOARD_PIN_BAT_ADC` 从 S_MGPIO4 修正为 S_MGPIO2，匹配原理图 P1 中 BAT_ADC 的实际连接 (U1.4 GPIO_02/AIN0)
- **CMakeLists 缺失**: 将 peripheral/ 下所有外设源文件按 Kconfig 条件加入编译列表，并添加 peripheral/ 头文件搜索路径
- **蜂鸣器/ADC 仅初始化未调用**: Tag 主循环从空 `osal_msleep(1000)` 改为周期性电量监测 (5s)、上电蜂鸣自检、低电量告警和空闲休眠逻辑
- Kconfig 中 ADC 帮助文本从 GPIO_04 更正为 GPIO_02/AIN0

### Changed

- `sle_locate.c`: 重构 Tag 主循环，集成电量采集、蜂鸣器自检、按钮回调、低功耗管理和低电量告警
- CMakeLists.txt: 通用化外设源文件编译逻辑，按 Kconfig 开关增量链接

## [0.1.0] - 2026-06-08

### Added

- 初始化项目版本，完成原理图设计、PCB 布局和核心文档框架。
- AGENTS.md 项目说明、参考资料和 MCP 工具规范
- Docs/硬件设计.md（16 章完整硬件审查报告）
- Docs/软件仓库.md（SDK 目录结构和构建烧录说明）
- Docs/测试方案.md（4 阶段测试计划）
- Docs/文档审查-团队报告.md（团队文档交叉审查报告）

### Changed

- 根据硬件审查修正 AGENTS.md 中 XC1 端点表述（不需要额外电容）
- 测试方案补充外设测试前置条件说明和低功耗测试章节
