import argparse
import time
from collections import deque
import numpy as np
import serial
import joblib
from features import extract_features

def distance_z(feat, mean, std):
    z = (feat - mean) / std
    return float(np.sqrt(np.sum(z * z)))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--port", default="/dev/ttyACM0")
    ap.add_argument("--baud", type=int, default=115200)
    ap.add_argument("--model", default="model.joblib")
    ap.add_argument("--threshold", type=float, default=6.0,
                    help="Más bajo = más estricto")
    args = ap.parse_args()

    model = joblib.load(args.model)
    fs = int(model["fs"])
    win_s = float(model["win"])
    step_s = float(model["step"])
    mean = model["mean"]
    std = model["std"]

    win_n = int(fs * win_s)
    step_n = int(fs * step_s)

    buf = deque(maxlen=win_n)
    since = 0

    ser = serial.Serial(args.port, args.baud, timeout=1)
    time.sleep(1.0)

    print("=== REALTIME AUTH STARTED ===")
    print(f"window={win_s}s step={step_s}s threshold={args.threshold}")

    try:
        while True:
            line = ser.readline().decode(errors="ignore").strip()
            if not line.startswith("S,"):
                continue

            parts = line.split(",")
            if len(parts) != 3:
                continue

            try:
                adc = float(parts[2])
            except ValueError:
                continue

            buf.append(adc)
            since += 1

            if len(buf) == win_n and since >= step_n:
                since = 0

                feat = extract_features(
                    np.array(buf, dtype=np.float32)
                )
                dist = distance_z(feat, mean, std)

                auth = 1 if dist < args.threshold else 0
                ser.write(f"AUTH,{auth}\n".encode())

                print(f"distance={dist:.2f} AUTH={auth}")

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        ser.close()

if __name__ == "__main__":
    main()
