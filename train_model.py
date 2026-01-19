import argparse
import csv
from pathlib import Path
import numpy as np
import joblib
from features import extract_features

FS = 100
WIN_S = 8.0
STEP_S = 2.0

def load_adc_from_csv(path: Path) -> np.ndarray:
    adc_vals = []
    with path.open() as f:
        r = csv.DictReader(f)
        for row in r:
            try:
                adc_vals.append(float(row["adc"]))
            except Exception:
                pass
    return np.array(adc_vals, dtype=np.float32)

def build_windows(adc: np.ndarray, fs: int, win_s: float, step_s: float):
    win = int(win_s * fs)
    step = int(step_s * fs)
    for start in range(0, len(adc) - win + 1, step):
        yield adc[start:start+win]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--me", required=True, help="CSV de tus datos (label=1)")
    ap.add_argument("--out", default="model.joblib")
    ap.add_argument("--fs", type=int, default=FS)
    ap.add_argument("--win", type=float, default=WIN_S)
    ap.add_argument("--step", type=float, default=STEP_S)
    args = ap.parse_args()

    adc = load_adc_from_csv(Path(args.me))
    if len(adc) < int(args.fs * args.win):
        raise SystemExit("No hay suficientes muestras en me.csv. Graba al menos 1-2 minutos.")

    feats = []
    for w in build_windows(adc, args.fs, args.win, args.step):
        feats.append(extract_features(w))

    X = np.array(feats, dtype=np.float32)
    mean = X.mean(axis=0)
    std = X.std(axis=0) + 1e-6  # evita division por cero

    model = {
        "fs": args.fs,
        "win": args.win,
        "step": args.step,
        "mean": mean,
        "std": std
    }

    joblib.dump(model, args.out)
    print(f"OK: modelo guardado en {args.out}")
    print("features_dim =", X.shape[1], "windows =", X.shape[0])

if __name__ == "__main__":
    main()
