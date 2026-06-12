# 项目说明

针对传统蓝牙定位器（AirTag等）在室内环境下定位精度较低、抗干扰能力弱及发现延迟高等痛点，本项目研发一款基于BS21星闪芯片的高精度防丢追踪器。利用星闪SLE（SparkLink Low Energy）技术的高带宽、精细测距特性，实现亚米级室内精准寻物。系统采用多径抑制算法优化定位数据，结合低功耗休眠策略，在保证极高连接成功率的同时延长续航。具备物联组网功能，可与星闪网关或智能手机协同工作，支持遗忘提醒、实时轨迹查询及反向寻找手机等功能。

# 参考资料

## 核心参考：BS2XV100 硬件指南

`Docs/BS2XV100 硬件指南_02.pdf` 是 BS21/Hi2821 芯片的官方硬件设计手册（70 页），**所有硬件判断的第一参考资料**。关键章节：

| 章节 | 页码范围 | 内容 | 本项目对应模块 |
| --- | --- | --- | --- |
| 引脚定义 | 6-15 | 48 引脚功能、复用、电气特性 | U1 全部引脚 |
| 电源设计 | 16-25 | VDD1/VDD2/VDDIO1 供电、DEC 去耦、DCC BUCK 电感 | 电池输入、SLE_3V3 去耦、L1 电感 |
| 时钟电路 | 26-30 | 32MHz 晶体选型、CL=8pF、XC2 串 39pF | X1 晶体、C9 电容 |
| RF 设计 | 31-45 | 50Ω 阻抗、PI 匹配网络、天线净空 | C11/C12/R5/R8/ANT1 |
| NFC 接口 | 46-55 | NFC1/NFC2 外接线圈、调谐电容 | NFC线圈、C13/C14 |
| PCB 布局 | 56-65 | 层叠、走线、地平面、晶振/RF/电源区域 | PCB1 布局约束 |
| 参考设计 | 66-70 | 推荐 BOM、典型应用电路 | 整体方案核对 |

## 其他参考资料

- `Docs/fbb_bs2x` -- 星闪 BS20/BS21E/BS22 解决方案代码仓，搭载 LiteOS，FBB 统一开发框架
- 软件文档在线：https://docs.hisilicon.com/repos/fbb_bs2x/zh-CN/master/
- `sle_local/` -- 本项目软件仓库（测距+定位）

# 工程结构

| 项 | 值 |
| --- | --- |
| EDA 工程名 | `赫哥不要/BS21_1` |
| 原理图 | P1 (A4), 单页, V1.0 |
| PCB | PCB1 (Board1) |
| 主控 | BS21E (hi2821), QFN-48 |
| SDK 目标平台 | standard-bs21e-1100e |
| 供电 | CR2032 纽扣电池 |
| 烧录方式 | USB-to-TTL 转 TX/RX/GND，使用本地 `hisiflash`，BS2X/460800，日志 115200 |

# 边界约束

- 原理图使用嘉立创 EDA 设计，所有硬件判断优先通过 MCP 实时读取 EDA 工程，不依赖 Markdown 文档或记忆
- 对 BS21 关键电路的结论必须同时核对 `Docs/BS2XV100 硬件指南_02.pdf` 和 MCP 读取到的真实网络
- NFC 线圈已购买实物，符号占位需在打板前更新为实际器件
- XC2 已有 39pF 负载电容，XC1 端按手册无需额外电容
- 烧录走 USB-to-TTL 转 TX/RX，不依赖 USB_N/P 数据线
- 软件代码位于 `sle_local/`，基于 FBB BS2X SDK，需在该目录下执行构建和烧录操作

# MCP 工具

嘉立创 EDA MCP Hub 已注册为 `mcp__jlceda__*` 系列工具，8 个工具全部可用。

MCP 服务器关闭时需要重新注册：`claude mcp add --transport http jlceda http://127.0.0.1:7655/mcp`

## 使用原则

1. 只查看当前打开图页用 `schematic_read`；跨页/全局网表/BOM/跨页信号追踪用 `schematic_review`
2. 修改原理图前先读取现状并说明修改目标；修改后必须重新读取或 DRC 验证
3. 新增器件：先 `component_select` 搜索确认，再 `component_place` 放置
4. 透传 API（`api_search`/`api_invoke`）仅基础工具无法满足时使用，调用前先查签名
5. 修改已有器件/网络：先 `eda_context` 确认页面类型，再 `api_search` 查 API，最后 `api_invoke`

## 原理图审查输出要求

- 检查范围：当前页还是全工程，MCP 工具名称和检查时间
- 关键网络：VBAT、SLE_3V3、VDD*、GND、XC1、XC2、RF、NFC1、NFC2、USB_N、USB_P、I2C、UART、按键和LED
- 器件核对：位号、Value、Footprint、Manufacturer Part、Supplier Part
- DRC 结果：错误、警告和需人工确认的未连接管脚
- 设计风险：区分"MCP已验证"和"只能到PCB阶段验证"


# 渐进式文档索引

| 文档 | 内容 |
| --- | --- |
| `README.md` | 项目总览、当前状态、快速开始、仓库边界 |
| `Docs/README.md` | 文档中心：使用顺序、参考资料管理策略、文档同步规则 |
| `Docs/硬件设计.md` | 完整的硬件设计审查：各模块拓扑、器件清单、整改项、验证清单 |
| `Docs/软件仓库.md` | 软件目录结构、核心应用、构建烧录流程、预编译固件、实验数据 |
| `Docs/测试方案.md` | 五阶段测试计划：单板、单链路测距、多基站定位、外设、低功耗 |
| `Docs/焊接与调试指南.md` | 焊接顺序、上电检查、板级故障排查 |
| `Docs/工程管理.md` | 仓库边界、权威信息源、构建产物、变更流程与发布门禁 |
| `sle_local/README.md` | 软件项目目标、定位原理、算法链路、实验结论 |
| `sle_local/tools/` | 构建脚本和烧录说明 |
