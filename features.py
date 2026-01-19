import numpy as np

def extract_features(window_adc: np.ndarray) -> np.ndarray:
    """
    Features robustas sin SciPy:
    - mean, std, min, max, range
    - energy (mean square)
    - zero crossings (cambios de signo)
    - slope stats (derivada discreta)
    """
    x = window_adc.astype(np.float32)
    x = x - float(np.mean(x))

    mean = float(np.mean(x))
    std  = float(np.std(x))
    minv = float(np.min(x))
    maxv = float(np.max(x))
    rng  = maxv - minv
    energy = float(np.mean(x * x))

    # Zero crossings
    s = np.sign(x)
    zero_cross = float(np.sum((s[1:] * s[:-1]) < 0)) if len(x) > 1 else 0.0

    # Slope stats
    dx = np.diff(x) if len(x) > 1 else np.array([0.0], dtype=np.float32)
    dx_mean = float(np.mean(dx))
    dx_std  = float(np.std(dx))
    dx_abs_mean = float(np.mean(np.abs(dx)))

    return np.array([
        mean, std, minv, maxv, rng, energy,
        zero_cross, dx_mean, dx_std, dx_abs_mean
    ], dtype=np.float32)
