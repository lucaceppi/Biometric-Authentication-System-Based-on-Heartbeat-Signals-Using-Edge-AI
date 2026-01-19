import argparse
import csv
import time
from pathlib import Path
import serial

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="/dev/ttyACM0")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--label", type=int, required=True, help="1=me, 0=other")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out_path = Path(args.out)
    is_new = not out_path.exists()

    ser = serial.Serial(args.port, args.baud, timeout=1)

    with out_path.open("a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["ts_unix", "ms_arduino", "adc", "label"])

        print("Collecting... Ctrl+C to stop")
        try:
            while True:
                line = ser.readline().decode(errors="ignore").strip()
                if not line.startswith("S,"):
                    continue
                parts = line.split(",")
                if len(parts) != 3:
                    continue
                ms = parts[1]
                adc = parts[2]
                w.writerow([time.time(), ms, adc, args.label])
        except KeyboardInterrupt:
            print("\nStopped.")
        finally:
            ser.close()

if __name__ == "__main__":
    main()
