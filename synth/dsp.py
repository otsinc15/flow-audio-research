"""Small DSP toolbox for the offline focus-music renderer.

Everything here is numpy/scipy only and fully deterministic: no global RNG,
no wall-clock, no audio input. Buffers are float32 mono unless stated.
"""

import numpy as np
from scipy.signal import lfilter, lfilter_zi, fftconvolve

SR = 44100


def db2lin(d):
    return float(10.0 ** (d / 20.0))


# ---------------------------------------------------------------- oscillators

def sine(freq, n, sr=SR, phase0=0.0):
    """Sine. `freq` may be a scalar or an array of length n (phase-integrated)."""
    if np.isscalar(freq):
        t = np.arange(n, dtype=np.float64) / sr
        return np.sin(2 * np.pi * freq * t + phase0).astype(np.float32)
    ph = phase0 + 2 * np.pi * np.cumsum(np.asarray(freq, dtype=np.float64)) / sr
    return np.sin(ph).astype(np.float32)


def saw(freq, n, sr=SR, max_hz=6000.0, phase0=0.0):
    """Additive band-limited saw, harmonics truncated at `max_hz`.

    Truncating at 6 kHz rather than Nyquist is deliberate: the references are
    startlingly dark above 2 kHz and a full-bandwidth saw blows that budget.
    """
    t = np.arange(n, dtype=np.float64) / sr
    nyq = min(max_hz, sr * 0.45)
    kmax = max(1, int(nyq // freq))
    out = np.zeros(n, dtype=np.float64)
    for k in range(1, kmax + 1):
        out += np.sin(2 * np.pi * freq * k * t + phase0 * k) / k
    return (out * (2.0 / np.pi)).astype(np.float32)


def fm(carrier_hz, ratio, index, n, sr=SR, phase0=0.0):
    """Two-operator FM (sine modulating sine). `index` may be an array."""
    t = np.arange(n, dtype=np.float64) / sr
    mod = np.sin(2 * np.pi * carrier_hz * ratio * t)
    return np.sin(2 * np.pi * carrier_hz * t + np.asarray(index) * mod + phase0).astype(np.float32)


def noise(rng, n):
    return rng.standard_normal(n).astype(np.float32)


# ------------------------------------------------------------------- filters

def _rbj_lp(f0, q, sr=SR):
    f0 = float(np.clip(f0, 20.0, sr * 0.45))
    w0 = 2 * np.pi * f0 / sr
    alpha = np.sin(w0) / (2 * q)
    cw = np.cos(w0)
    b = np.array([(1 - cw) / 2, 1 - cw, (1 - cw) / 2])
    a = np.array([1 + alpha, -2 * cw, 1 - alpha])
    return b / a[0], a / a[0]


def _rbj_bp(f0, q, sr=SR):
    f0 = float(np.clip(f0, 20.0, sr * 0.45))
    w0 = 2 * np.pi * f0 / sr
    alpha = np.sin(w0) / (2 * q)
    cw = np.cos(w0)
    b = np.array([alpha, 0.0, -alpha])
    a = np.array([1 + alpha, -2 * cw, 1 - alpha])
    return b / a[0], a / a[0]


def _rbj_hp(f0, q, sr=SR):
    f0 = float(np.clip(f0, 20.0, sr * 0.45))
    w0 = 2 * np.pi * f0 / sr
    alpha = np.sin(w0) / (2 * q)
    cw = np.cos(w0)
    b = np.array([(1 + cw) / 2, -(1 + cw), (1 + cw) / 2])
    a = np.array([1 + alpha, -2 * cw, 1 - alpha])
    return b / a[0], a / a[0]


def lowpass(x, f0, q=0.707, sr=SR):
    b, a = _rbj_lp(f0, q, sr)
    return lfilter(b, a, x).astype(np.float32)


def highpass(x, f0, q=0.707, sr=SR):
    b, a = _rbj_hp(f0, q, sr)
    return lfilter(b, a, x).astype(np.float32)


def bandpass(x, f0, q=1.0, sr=SR):
    b, a = _rbj_bp(f0, q, sr)
    return lfilter(b, a, x).astype(np.float32)


def tv_lowpass(x, cutoff, q=1.0, sr=SR, block=256):
    """Resonant low-pass whose cutoff moves. `cutoff` is an array of len(x).

    Processed in short blocks with the biquad state carried across, so a slow
    LFO on the cutoff is smooth and there is no per-block click.
    """
    x = np.asarray(x, dtype=np.float64)
    cutoff = np.asarray(cutoff, dtype=np.float64)
    n = len(x)
    out = np.empty(n, dtype=np.float64)
    zi = np.zeros(2)
    for s in range(0, n, block):
        e = min(n, s + block)
        b, a = _rbj_lp(float(cutoff[s]), q, sr)
        seg, zi = lfilter(b, a, x[s:e], zi=zi)
        out[s:e] = seg
    return out.astype(np.float32)


def onepole_lp(x, fc, sr=SR):
    a = 1.0 - np.exp(-2 * np.pi * float(fc) / sr)
    return lfilter([a], [1.0, -(1.0 - a)], x).astype(np.float32)


# ---------------------------------------------------------------- envelopes

def exp_decay(n, tau, sr=SR):
    t = np.arange(n, dtype=np.float64) / sr
    return np.exp(-t / tau).astype(np.float32)


def ar_env(n, attack, release, sr=SR):
    t = np.arange(n, dtype=np.float64) / sr
    a = np.clip(t / max(attack, 1e-4), 0, 1)
    r = np.exp(-np.clip(t - attack, 0, None) / max(release, 1e-4))
    return (a * r).astype(np.float32)


def add_at(buf, pos, sig, gain=1.0):
    """Add `sig` into `buf` at sample `pos`, truncating at the buffer end."""
    pos = int(pos)
    if pos >= len(buf):
        return
    if pos < 0:
        sig = sig[-pos:]
        pos = 0
    e = min(len(buf), pos + len(sig))
    buf[pos:e] += gain * sig[: e - pos]


def smooth_steps(values, n, sr=SR, tau=0.02):
    """One-pole smoothing of a stepped control signal (kills note-change clicks)."""
    a = 1.0 - np.exp(-1.0 / (tau * sr))
    return lfilter([a], [1.0, -(1.0 - a)], values).astype(np.float32)


# -------------------------------------------------------------------- delay

def dub_delay(x, delay_s, feedback, hicut_hz, wow_depth_s, wow_hz,
              repeats=14, sr=SR, pingpong=True, wow_phase=0.0):
    """Tempo-synced tape-style echo, expanded into its repeats.

    A feedback delay with an LTI damping filter is mathematically the sum of
    K delayed copies, each damped one more time than the last. Expanding it
    that way keeps everything vectorised (no per-sample Python loop) and, as a
    bonus, lets each successive repeat drift a little further - which is what a
    real tape echo does. Returns (left, right).
    """
    x = np.asarray(x, dtype=np.float32)
    n = len(x)
    t = np.arange(n, dtype=np.float64) / sr
    left = np.zeros(n, dtype=np.float32)
    right = np.zeros(n, dtype=np.float32)
    src_idx = np.arange(n, dtype=np.float64)
    tap = x.astype(np.float64)
    for k in range(1, repeats + 1):
        g = feedback ** k
        if g < 1e-4:
            break
        wob = wow_depth_s * k * np.sin(2 * np.pi * wow_hz * t + wow_phase + 0.7 * k)
        read = src_idx - k * delay_s * sr - wob * sr
        rep = np.interp(read, src_idx, tap, left=0.0, right=0.0)
        # damping: one pole per repeat, so repeat k is k-times darker
        rep = rep.astype(np.float32)
        for _ in range(min(k, 6)):
            rep = onepole_lp(rep, hicut_hz, sr)
        if pingpong and (k % 2 == 1):
            left += g * rep
            right += 0.35 * g * rep
        elif pingpong:
            right += g * rep
            left += 0.35 * g * rep
        else:
            left += g * rep
            right += g * rep
    return left, right


# ------------------------------------------------------------------- reverb

def reverb_ir(rng, seconds=2.6, damp_hz=2200.0, sr=SR, predelay_s=0.02):
    """Exponentially-decaying filtered-noise impulse response, stereo."""
    n = int(seconds * sr)
    t = np.arange(n) / sr
    env = np.exp(-t / (seconds / 5.0))
    ir = []
    for _ in range(2):
        h = rng.standard_normal(n).astype(np.float32) * env.astype(np.float32)
        h = onepole_lp(h, damp_hz, sr)
        h = highpass(h, 90.0, 0.707, sr)
        pre = np.zeros(int(predelay_s * sr), dtype=np.float32)
        ir.append(np.concatenate([pre, h]))
    ir = np.stack(ir)
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True)) + 1e-12
    return ir


def convolve_stereo(x, ir):
    l = fftconvolve(x, ir[0])[: len(x)]
    r = fftconvolve(x, ir[1])[: len(x)]
    return l.astype(np.float32), r.astype(np.float32)


# ----------------------------------------------------------------- dynamics

def soft_clip(x, threshold):
    return (threshold * np.tanh(x / threshold)).astype(np.float32)


def true_peak_db(x, sr=SR, oversample=4):
    from scipy.signal import resample_poly
    up = resample_poly(np.asarray(x, dtype=np.float64), oversample, 1, axis=0)
    p = float(np.max(np.abs(up)))
    return 20 * np.log10(p + 1e-12)
