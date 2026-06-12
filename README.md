# BS21 星闪高精度防丢追踪器

本目录是项目总工程，负责硬件设计、项目级文档和跨仓库协作。固件与烧录工具分别保存在两个独立 Git 仓库中，提交和版本管理必须分开进行。

## 当前状态

| 子系统 | 路径/工程 | 当前状态 |
| --- | --- | --- |
| 硬件 | 嘉立创 EDA `赫哥不要/BS21_1`，`Board1/P1/PCB1` | 原理图已加入 0402 调试 LED；原理图 DRC 尚有 25 个警告；PCB 待复核 |
| 固件 | `sle_local/` | BS21E FBB SDK，使用 uv 管理 Python 构建环境 |
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
- `sle_local/`：固件源码、构建环境、实验数据和固件归档。
- `hisiflash/`：烧录工具源码。
- `Docs/fbb_bs2x/`：FBB BS2X SDK 参考快照，本地普通目录，不纳入版本管理；在线文档为 https://docs.hisilicon.com/repos/fbb_bs2x/zh-CN/master/ ，快照丢失时从 HiSpark 官方仓库重新获取。

不要在根仓库中直接提交 `sle_local/`、`hisiflash/`、虚拟环境、编译缓存或构建目录。
