# BearPi Pico H2821E 硬件参考

## 芯片
- BS21E (Hi2821E)，RISC-V 32bit，64MHz，浮点
- 160KB SRAM，1MB Flash

## Pin 映射（与自定义 Tag 对比）

| 功能 | 自定义 Tag | BearPi Pico | 差异 |
|------|-----------|-------------|------|
| 蜂鸣器 | GPIO_06 | **无** | BearPi 无蜂鸣器 |
| 电池 ADC | GPIO_02 (AIN0) | GPIO_02 (与按键共用) | 相同 |
| LED Boot | GPIO_03 | — | BearPi 无 |
| LED SLE | GPIO_04 | — | BearPi 无 |
| LED ACC | GPIO_05 | — | BearPi 无 |
| 用户 LED | — | GPIO_30 (蓝色) | BearPi 特有 |
| 电源 LED | — | GPIO_31 (红色，硬件固定) | BearPi 特有 |
| NFC | GPIO_09/10 | 可复用 | 未焊 |
| I2C | GPIO_14/15 | 可复用 | |
| 加速度计 INT | GPIO_18 | 无 | BearPi 未焊 |
| UART 调试 | GPIO_19(TX)/20(RX) | GPIO_19(TX)/20(RX) | **完全相同** |
| USB | GPIO_07/08 | GPIO_07/08 | 相同 |
| SWD | GPIO_25/26 | GPIO_25/26 | 相同 |
| 按键 | — | GPIO_02 | 与 ADC 共用 |
| Reset | — | 板载复位按键 | |

## 关键结论
- UART 调试串口引脚完全相同 (P0.19/P0.20)，无需改板级配置
- BearPi 无蜂鸣器、无加速度计、无外接 LED→需禁用对应 Kconfig
- 用户 LED 在 GPIO_30，与自定义 Tag 的 S_MGPIO3~5 不同
- BS21E 芯片相同，SLE/BLE 射频相同，CS/GTTT/IQ 逻辑完全复用
