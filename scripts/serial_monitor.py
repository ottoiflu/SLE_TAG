#!/usr/bin/env python3
"""串口日志采集脚本：从 CH340 (BS21 Tag) 读取串口输出，实时追加到本地日志文件。

用法:
    python3 scripts/serial_monitor.py [--port /dev/ttyUSB0] [--baud 115200] [--log tag_serial.log]

默认参数:
    --port  /dev/ttyUSB0
    --baud  115200
    --log   tag_serial.log

输出:
    - 所有串口数据实时追加到日志文件（每行带毫秒级时间戳）
    - 同时打印到 stdout
"""

import argparse
import os
import sys
import time
from datetime import datetime

try:
    import serial
    import serial.tools.list_ports
except ImportError:
    print("错误: 需要 pyserial，请执行: pip install pyserial")
    sys.exit(1)


def list_ports():
    """列出所有可用串口"""
    ports = serial.tools.list_ports.comports()
    if not ports:
        print("未检测到任何串口设备")
        return []
    print("可用串口:")
    for p in ports:
        print(f"  {p.device} - {p.description} [{p.hwid}]")
    return [p.device for p in ports]


def monitor(port: str, baud: int, log_path: str):
    """打开串口并持续读取，追加到日志文件"""
    log_dir = os.path.dirname(os.path.abspath(log_path))
    os.makedirs(log_dir, exist_ok=True)

    print(f"串口监视器启动")
    print(f"  端口: {port}")
    print(f"  波特率: {baud}")
    print(f"  日志文件: {os.path.abspath(log_path)}")
    print(f"  按 Ctrl+C 停止")
    print("-" * 60)

    try:
        ser = serial.Serial(
            port=port,
            baudrate=baud,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE,
            timeout=0.5,
        )
    except serial.SerialException as e:
        print(f"错误: 无法打开串口 {port}: {e}")
        print()
        available = list_ports()
        if available:
            print(f"\n提示: 使用 --port 指定正确的串口，例如:")
            print(f"  python3 scripts/serial_monitor.py --port {available[0]}")
        sys.exit(1)

    line_buf = bytearray()
    start_time = time.time()

    try:
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n=== 串口监视器启动 {datetime.now().isoformat()} ===\n")
            log_file.write(f"=== 端口: {port} 波特率: {baud} ===\n\n")

            while True:
                try:
                    data = ser.read(ser.in_waiting or 1)
                except serial.SerialException as e:
                    print(f"\n串口读取错误: {e}")
                    break

                if not data:
                    continue

                elapsed_ms = int((time.time() - start_time) * 1000)

                for byte in data:
                    ch = chr(byte) if 0x20 <= byte < 0x7F or byte == 0x0A else ''

                    if byte == 0x0A:  # LF - 换行
                        line = line_buf.decode("utf-8", errors="replace").strip()
                        line_buf.clear()
                        if line:
                            ts = datetime.now().strftime("%H:%M:%S.%f")[:-3]
                            out = f"[{ts} +{elapsed_ms:07d}ms] {line}"
                            print(out, flush=True)
                            log_file.write(out + "\n")
                            log_file.flush()
                    elif ch:
                        line_buf.append(byte)

    except KeyboardInterrupt:
        print("\n\n监视器已停止")
    finally:
        ser.close()
        with open(log_path, "a", encoding="utf-8") as log_file:
            log_file.write(f"\n=== 串口监视器停止 {datetime.now().isoformat()} ===\n")


def main():
    parser = argparse.ArgumentParser(
        description="BS21 Tag 串口日志采集器",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python3 scripts/serial_monitor.py                          # 自动检测 /dev/ttyUSB0
  python3 scripts/serial_monitor.py --port /dev/ttyUSB1      # 指定端口
  python3 scripts/serial_monitor.py --log ./logs/tag.log     # 指定日志路径
  python3 scripts/serial_monitor.py --baud 921600            # 自定义波特率
        """,
    )
    parser.add_argument("--port", default="/dev/ttyUSB0", help="串口设备路径 (默认: /dev/ttyUSB0)")
    parser.add_argument("--baud", type=int, default=115200, help="波特率 (默认: 115200)")
    parser.add_argument("--log", default="tag_serial.log", help="日志输出文件 (默认: tag_serial.log)")
    parser.add_argument("--list", action="store_true", help="仅列出可用串口")

    args = parser.parse_args()

    if args.list:
        list_ports()
        return

    if not os.path.exists(args.port):
        print(f"警告: 串口 {args.port} 不存在")
        list_ports()
        sys.exit(1)

    monitor(args.port, args.baud, args.log)


if __name__ == "__main__":
    main()
