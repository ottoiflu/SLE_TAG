# 基于 BS21 星闪平台的高精度低成本室内协同定位系统

本目录是项目总工程，负责硬件设计、项目级文档和跨仓库协作。固件、应用和烧录工具分别保存在独立 Git 仓库中，提交和版本管理必须分开进行。

## 项目简介

工业车间、仓储物流等场景长期面临室内定位难题：GPS 无法穿透建筑，UWB 成本过高，传统 BLE 信标依赖 RSSI 在多径和金属遮挡下精度严重退化，众包方案则因缺少终端覆盖而失效。

本项目基于 BS21 星闪芯片，利用 SLE 信道探测的多频点相位测量实现精准测距。硬件成本仅为 UWB 的五分之一，标定后精度优于 1 米，配合 ESPRIT 算法与空间平滑抑制多径干扰，在工业环境中表现远超传统蓝牙。

系统采用去中心化协同定位架构：任意设备获取坐标后即可作为参考节点，节点数无上限。标签通过 GTTT 调度与周围多个节点同时测距，最小二乘三边解算实时求解坐标，全部本地计算，无需云端或运营商网络，满足保密场景的离线安全需求。

标签集成加速度计、NFC、蜂鸣器，采用多级低功耗策略适配纽扣电池长续航。应用层规划电子围栏告警、设备查找、轨迹回溯等功能，可应用于工业仓储资产定位、医院设备追踪、地下人员安全、保密安防、畜牧业无缝定位等场景。为室内定位提供一套低成本、高精度、可独立部署、纯本地运行的解决方案。

## 当前状态

| 子系统 | 路径/工程 | 当前状态 |
| --- | --- | --- |
| 硬件 | 嘉立创 EDA `赫哥不要/BS21_1`，`Board1/P1/PCB1` | 原理图已加入 0402 调试 LED；原理图 DRC 尚有 25 个警告；PCB 待复核 |
| 固件 | `sle_local/` | BS21E FBB SDK，使用 uv 管理 Python 构建环境 |
| 应用 | `location_app/` | Android/HarmonyOS 定位演示应用 |
| 烧录 | `hisiflash/` | BS2X 实验性 SEBOOT/YMODEM 支持，使用 UART_L0 |
| 项目文档 | `Docs/` | 硬件、软件、测试、焊接和工程管理文档 |

## 快速开始

### 构建固件

```bash
cd sle_local
UV_CACHE_DIR=.uv-cache uv sync
UV_CACHE_DIR=.uv-cache CCACHE_DIR=.ccache \
  uv run --directory src python build.py -ninja standard-bs21e-1100e
```

固件输出：

```text
sle_local/src/output/bs21e/fwpkg/standard-bs21e-1100e/bs21e_all_in_one.fwpkg
```

### 烧录并监控串口

```bash
./hisiflash/target/release/hisiflash \
  -c bs2x -p /dev/ttyUSB0 -b 460800 \
  flash sle_local/src/output/bs21e/fwpkg/standard-bs21e-1100e/bs21e_all_in_one.fwpkg \
  --monitor --monitor-baud 115200
```

### 查看工程状态

```bash
./scripts/project-status.sh
```

## 文档入口

- [文档中心](Docs/README.md)
- [工程管理](Docs/工程管理.md)
- [硬件设计](Docs/硬件设计.md)
- [软件仓库与构建烧录](Docs/软件仓库.md)
- [测试方案](Docs/测试方案.md)
- [焊接与调试指南](Docs/焊接与调试指南.md)

## 仓库边界

- 根仓库：项目管理、硬件文档、项目级变更记录。
- `sle_local/`：固件源码、构建环境、实验数据和固件归档；根仓库以子模块固定提交。
- `location_app/`：Android/HarmonyOS 应用源码、测试和应用专属文档；根仓库以子模块固定提交。
- `hisiflash/`：烧录工具源码。当前为独立嵌套仓库，根仓库不固定其提交；发布或复现时必须记录其 commit。
- `Docs/fbb_bs2x/`：FBB BS2X SDK 参考快照，本地普通目录，不纳入版本管理；在线文档为 https://docs.hisilicon.com/repos/fbb_bs2x/zh-CN/master/ ，快照丢失时从 HiSpark 官方仓库重新获取。

不要在根仓库中直接提交子仓库源码、虚拟环境、编译缓存或构建目录；子仓库必须在各自仓库中提交。
