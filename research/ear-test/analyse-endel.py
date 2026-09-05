#!/usr/bin/env python3
"""Deep analysis of ref02 (Endel "Deeper Focus", iPhone screen recording).

Same conventions as measure-clips.py: band shares are POWER-domain, LRA is the
honest constancy figure, and no listening judgement is made anywhere -- the
agent that ran this cannot hear.  Everything is a number or arithmetic on one.

Prerequisites (run once, outside the repo):
    ffmpeg -i ref02....m4a -ar 44100 -ac 2 ref02.wav
    python -m demucs -n htdemucs -o stems --filename "{stem}.{ext}" ref02.wav

Usage:
    python analyse-endel.py --work <analysis dir> --plots <repo plot dir>

Writes results.json into the work dir and PNGs into the plot dir.
Audio never enters the repo; only JSON summary + plots leave the work dir.
"""
import argparse, json, os, subprocess, re
import numpy as np
import scipy.signal as sig
import librosa
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

SR = 44100
N_FFT = 8192
HOP = 2048                      # 46 ms, as in measure-clips.py
BANDS = [(0, 60), (60, 150), (150, 500), (500, 2000), (2000, 8000), (8000, None)]
BAND_NAMES = ["<60 Hz", "60-150 Hz", "150-500 Hz", "500 Hz-2 kHz", "2-8 kHz", ">8 kHz"]
STEMS = ["drums", "bass", "other", "vocals"]
# NOTE (lyria-stems-2026-09-02.md): htdemucs is trained on band music.  On synthetic
# techno the deep sub lands in `drums` and `bass` is really the 60-150 Hz body.
# Stem *labels* below are Demucs's, not musical truth.


# --------------------------------------------------------------------------
# 1. CLICK ARTEFACTS -- Daniel's own screen taps on the iPhone recording
# --------------------------------------------------------------------------
def find_clicks(y, sr, step=0.125):
    """Screen taps = short HF transients that do NOT sit on the musical grid.

    Two stages, because stage 1 alone is useless here:

    1. 4 kHz high-pass -> short-frame RMS envelope -> peaks standing >=14 dB over
       a 4 s running-median HF floor.  This finds 755 events, but they are NOT
       taps: the track has real percussive HF content.
    2. RHYTHM TEST, which is what actually separates them.  For each transient,
       ask whether ANY other transient sits at a lag that is a whole multiple of
       a 16th note (0.125 s at the settled 120 BPM), within +-20 ms, anywhere in
       a +-8.5 s neighbourhood.  A musical element repeats on the grid; a
       fingertip does not.  Only the events with no such partner survive.

    Measured on this file: 755 transients -> 747 are grid-periodic (they cluster
    at exactly 0.125 / 0.25 / 0.5 / 0.75 / 2.0 s spacings) and 8 are isolated.
    """
    sos = sig.butter(8, 4000, btype="highpass", fs=sr, output="sos")
    hf = sig.sosfilt(sos, y)
    fl, hp = 512, 128                                    # 12 ms frame / 2.9 ms hop
    env = librosa.feature.rms(y=hf, frame_length=fl, hop_length=hp)[0]
    t = librosa.frames_to_time(np.arange(len(env)), sr=sr, hop_length=hp)
    db = 20 * np.log10(np.maximum(env, 1e-12))
    w = int(round(4.0 * sr / hp)) | 1
    floor = sig.medfilt(db, kernel_size=min(w, len(db) - (1 - len(db) % 2)))
    excess = db - floor
    thr = 14.0
    peaks, props = sig.find_peaks(excess, height=thr, distance=int(0.12 * sr / hp))
    T, H = t[peaks], props["peak_heights"]

    lags = [step * k for k in range(1, 65)]              # up to 4 bars of 16ths
    tol = 0.020
    clicks = []
    for i in range(len(T)):
        d = np.abs(T - T[i])
        d = d[(d > 0.05) & (d < 8.5)]
        periodic = len(d) and any(np.any(np.abs(d - L) < tol) for L in lags)
        if not periodic:
            clicks.append(dict(t=round(float(T[i]), 3),
                               excess_db=round(float(H[i]), 1)))
    return clicks, dict(hf_cutoff_hz=4000, threshold_db_over_local_floor=thr,
                        grid_step_s=step, lag_tolerance_ms=20,
                        neighbourhood_s=8.5,
                        transients_total=int(len(T)),
                        transients_grid_periodic=int(len(T) - len(clicks)))


def click_mask(clicks, n, sr, pad=0.150):
    """Boolean sample mask: True = keep.  +-150 ms around every click is dropped."""
    keep = np.ones(n, bool)
    for c in clicks:
        a = max(0, int((c["t"] - pad) * sr))
        b = min(n, int((c["t"] + pad) * sr))
        keep[a:b] = False
    return keep


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------
def band_shares(y, sr):
    S = np.abs(librosa.stft(y, n_fft=N_FFT, hop_length=HOP)) ** 2
    fb = librosa.fft_frequencies(sr=sr, n_fft=N_FFT)
    tot = S.sum()
    out = {}
    for (lo, hi), name in zip(BANDS, BAND_NAMES):
        m = (fb >= lo) & ((fb < hi) if hi else np.ones_like(fb, bool))
        out[name] = round(float(S[m].sum() / tot * 100), 3) if tot else 0.0
    return out


def rms_1s(y, sr):
    """RMS in dBFS on 1-second non-overlapping frames."""
    n = sr
    k = len(y) // n
    r = np.array([np.sqrt((y[i * n:(i + 1) * n] ** 2).mean()) for i in range(k)])
    return 20 * np.log10(np.maximum(r, 1e-10))


def smooth(x, w):
    w = max(1, int(w))
    return np.convolve(x, np.ones(w) / w, mode="same")


def dominant_periods(x, dt, min_s=4.0, max_s=200.0, n=4):
    """Autocorrelation of a (detrended) trajectory -> dominant modulation periods.

    x is sampled every dt seconds.  Returns the strongest local autocorrelation
    peaks inside [min_s, max_s], with their normalised correlation height.
    """
    x = np.asarray(x, float)
    x = x - x.mean()
    if x.std() == 0:
        return []
    ac = np.correlate(x, x, mode="full")[len(x) - 1:]
    ac /= ac[0]
    lags = np.arange(len(ac)) * dt
    m = (lags >= min_s) & (lags <= max_s)
    if m.sum() < 5:
        return []
    idx = np.where(m)[0]
    pk, pr = sig.find_peaks(ac[idx], height=0.05)
    order = np.argsort(pr["peak_heights"])[::-1][:n]
    return [dict(period_s=round(float(lags[idx[pk[i]]]), 2),
                 acf=round(float(ac[idx[pk[i]]]), 3)) for i in order]


def hz_to_note(f):
    if f is None or not np.isfinite(f) or f <= 0:
        return None
    return librosa.hz_to_note(float(f), unicode=False)


# --------------------------------------------------------------------------
# 2. GLOBAL: tempo, key, bass fundamental
# --------------------------------------------------------------------------
def global_metrics(y, sr, keep):
    out = {}
    yk = y[keep]                                       # click-excluded copy
    onset_env = librosa.onset.onset_strength(y=yk, sr=sr)
    tempo, beats = librosa.beat.beat_track(onset_envelope=onset_env, sr=sr)
    out["librosa_bpm_default_prior"] = round(float(np.atleast_1d(tempo)[0]), 1)

    # prior-free tempogram: which periodicity actually dominates?
    tg = librosa.feature.tempogram(onset_envelope=onset_env, sr=sr)
    agg = tg.mean(axis=1)
    freqs = librosa.tempo_frequencies(tg.shape[0], sr=sr)
    v = np.isfinite(freqs) & (freqs > 30) & (freqs < 300)
    a, f = agg[v], freqs[v]
    order = np.argsort(a)[::-1]
    picked = []
    for i in order:
        if all(abs(f[i] - q) > 5 for q, _ in picked):
            picked.append((float(f[i]), float(a[i] / a.max())))
        if len(picked) == 5:
            break
    out["tempogram_candidates_bpm_relstrength"] = [(round(b, 1), round(s, 3)) for b, s in picked]
    out["tempo_peak_over_median"] = round(float(a.max() / np.median(a)), 1)
    bt = librosa.frames_to_time(beats, sr=sr)
    ibi = np.diff(bt)
    out["beat_interval_cv"] = round(float(ibi.std() / ibi.mean()), 3)

    # chroma over the whole track, and over the bass region only (<200 Hz)
    ch = librosa.feature.chroma_cqt(y=yk, sr=sr, hop_length=HOP)
    prof = ch.mean(axis=1)
    names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]
    out["chroma_full"] = {n: round(float(p), 3) for n, p in zip(names, prof)}
    out["chroma_full_rank"] = [names[i] for i in np.argsort(prof)[::-1]]
    lp = sig.sosfilt(sig.butter(8, 200, btype="lowpass", fs=sr, output="sos"), yk)
    chl = librosa.feature.chroma_cqt(y=lp, sr=sr, hop_length=HOP, fmin=librosa.note_to_hz("C1"),
                                     n_octaves=4)
    pl = chl.mean(axis=1)
    out["chroma_low200"] = {n: round(float(p), 3) for n, p in zip(names, pl)}
    out["chroma_low200_rank"] = [names[i] for i in np.argsort(pl)[::-1]]
    return out


def bass_pitch_track(y_bassish, sr):
    """pyin on a low-passed signal -> bass fundamental in Hz / note over time."""
    lp = sig.sosfilt(sig.butter(8, 300, btype="lowpass", fs=sr, output="sos"), y_bassish)
    f0, voiced, vprob = librosa.pyin(lp, fmin=30.0, fmax=300.0, sr=sr,
                                     frame_length=8192, hop_length=2048)
    t = librosa.frames_to_time(np.arange(len(f0)), sr=sr, hop_length=2048)
    good = np.isfinite(f0) & voiced
    res = dict(voiced_frac=round(float(good.mean()), 3))
    if good.sum():
        fv = f0[good]
        res.update(median_hz=round(float(np.median(fv)), 2),
                   p10_hz=round(float(np.percentile(fv, 10)), 2),
                   p90_hz=round(float(np.percentile(fv, 90)), 2),
                   median_note=hz_to_note(np.median(fv)),
                   semitone_std=round(float(np.std(12 * np.log2(fv / np.median(fv)))), 2))
        # note histogram: how much time on each pitch class / octave
        notes = [hz_to_note(x) for x in fv]
        hist = {}
        for n in notes:
            hist[n] = hist.get(n, 0) + 1
        res["note_hist_pct"] = {k: round(v / len(notes) * 100, 1)
                                for k, v in sorted(hist.items(), key=lambda kv: -kv[1])[:8]}
        res["track"] = [(round(float(tt), 2), round(float(ff), 2))
                        for tt, ff in zip(t[good], f0[good])][::10]   # decimated
    return res


# --------------------------------------------------------------------------
# 5. DRUMS: kick grid, decay, spectral peak
# --------------------------------------------------------------------------
def drum_metrics(yd, sr, bpm, clicks):
    out = {}
    # kick = low-passed drums stem (Demucs puts the sub here, see lyria note).
    # librosa's onset_detect over-triggers badly on a sustained sub (2583 hits,
    # 0.20 s median gap = not musical), so pick peaks on the level envelope with a
    # prominence floor and a minimum spacing instead.
    lp = sig.sosfilt(sig.butter(8, 120, btype="lowpass", fs=sr, output="sos"), yd)
    hp = 128
    e = librosa.feature.rms(y=lp, frame_length=1024, hop_length=hp)[0]
    edb = 20 * np.log10(np.maximum(e, 1e-10))
    tt = librosa.frames_to_time(np.arange(len(edb)), sr=sr, hop_length=hp)
    pk, _ = sig.find_peaks(edb, prominence=6.0, distance=int(0.35 * sr / hp))
    on = np.array([tt[p] for p in pk
                   if all(abs(tt[p] - c["t"]) > 0.15 for c in clicks)])
    out["kick_onsets"] = int(len(on))
    if len(on) > 3:
        d = np.diff(on)
        d = d[d > 0.05]
        out["kick_ioi_median_s"] = round(float(np.median(d)), 4)
        out["kick_ioi_cv"] = round(float(d.std() / d.mean()), 3)
        out["kick_bpm_from_ioi"] = round(60.0 / float(np.median(d)), 2)
        vals, cnts = np.unique(np.round(d, 2), return_counts=True)
        o = np.argsort(cnts)[::-1][:10]
        out["kick_ioi_hist_s"] = {str(float(vals[i])): int(cnts[i]) for i in o}
        # 16-step grid occupancy at the settled tempo
        beat = 60.0 / bpm
        bar = 4 * beat
        step = bar / 16
        phase = ((on - on[0]) % bar) / step
        steps = np.round(phase).astype(int) % 16
        occ = np.bincount(steps, minlength=16)
        out["kick_grid_16"] = occ.tolist()
        out["kick_grid_16_pct"] = [round(x / len(on) * 100, 1) for x in occ]
        out["kick_grid_dev_ms_std"] = round(float(np.std((phase - np.round(phase)) * step) * 1000), 1)

    # kick decay: median time from onset to -20 dB on the low-passed stem
    decays, peaks = [], []
    for t in on[:400]:
        i = int(t * sr)
        seg = lp[i:i + int(1.5 * sr)]
        if len(seg) < sr // 4:
            continue
        e = librosa.feature.rms(y=seg, frame_length=1024, hop_length=128)[0]
        e = 20 * np.log10(np.maximum(e, 1e-10))
        pk = e.max()
        below = np.where(e < pk - 20)[0]
        if len(below):
            decays.append(below[0] * 128 / sr)
        sp = np.abs(np.fft.rfft(seg[:int(0.25 * sr)] * np.hanning(int(0.25 * sr))))
        fr = np.fft.rfftfreq(int(0.25 * sr), 1 / sr)
        peaks.append(float(fr[np.argmax(sp[(fr < 250)])]))
    if decays:
        out["kick_decay_to_-20dB_ms_median"] = round(float(np.median(decays)) * 1000, 1)
        out["kick_decay_to_-20dB_ms_p10_p90"] = [round(float(np.percentile(decays, 10)) * 1000, 1),
                                                 round(float(np.percentile(decays, 90)) * 1000, 1)]
    if peaks:
        out["kick_spectral_peak_hz_median"] = round(float(np.median(peaks)), 1)
        out["kick_spectral_peak_hz_p10_p90"] = [round(float(np.percentile(peaks, 10)), 1),
                                                round(float(np.percentile(peaks, 90)), 1)]

    # hats / claps: is there ANY content above 4 kHz (hat) or 1-4 kHz (clap body)?
    for name, lo, hi in [("hat_4k+", 4000, None), ("clapband_1k_4k", 1000, 4000)]:
        s = sig.sosfilt(sig.butter(8, [lo, hi] if hi else lo,
                                   btype="bandpass" if hi else "highpass",
                                   fs=sr, output="sos"), yd)
        e = librosa.onset.onset_strength(y=s, sr=sr, hop_length=512)
        det = librosa.onset.onset_detect(onset_envelope=e, sr=sr, hop_length=512, units="time")
        det = [t for t in det if all(abs(t - c["t"]) > 0.15 for c in clicks)]
        out[name + "_onsets"] = len(det)
        out[name + "_rms_dbfs"] = round(20 * np.log10(max(float(np.sqrt((s ** 2).mean())), 1e-10)), 1)
        if len(det) > 3:
            beat = 60.0 / bpm; bar = 4 * beat; step = bar / 16
            ph = ((np.array(det) - det[0]) % bar) / step
            out[name + "_grid_16"] = np.bincount(np.round(ph).astype(int) % 16,
                                                 minlength=16).tolist()
    return out


# --------------------------------------------------------------------------
# 3/4. ARRANGEMENT + HYPNOTIC MOVEMENT
# --------------------------------------------------------------------------
def movement(y, sr, label):
    """Centroid + rolloff trajectories (1 s smoothing) and their modulation periods."""
    cen = librosa.feature.spectral_centroid(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP)[0]
    rol = librosa.feature.spectral_rolloff(y=y, sr=sr, n_fft=N_FFT, hop_length=HOP,
                                           roll_percent=0.85)[0]
    dt = HOP / sr
    w = int(round(1.0 / dt))
    cs, rs = smooth(cen, w), smooth(rol, w)
    lo, hi = np.percentile(cs, 10), np.percentile(cs, 90)
    out = dict(label=label,
               centroid_mean_hz=round(float(cs.mean())),
               centroid_p10_p90_hz=[round(float(lo)), round(float(hi))],
               centroid_slow_cv_1s=round(float(cs.std() / cs.mean()), 3),
               centroid_sweep_octaves=round(float(np.log2(hi / lo)), 2) if lo > 0 else None,
               rolloff85_mean_hz=round(float(rs.mean())),
               rolloff85_p10_p90_hz=[round(float(np.percentile(rs, 10))),
                                     round(float(np.percentile(rs, 90)))],
               centroid_periods=dominant_periods(cs, dt),
               rolloff_periods=dominant_periods(rs, dt),
               _cen_traj=cs[::10].tolist(), _dt=dt * 10)
    # amplitude modulation (tremolo-like level movement) on the 1 s RMS curve
    r = rms_1s(y, sr)
    out["rms_1s_mean_db"] = round(float(r.mean()), 1)
    out["rms_1s_p10_p90_db"] = [round(float(np.percentile(r, 10)), 1),
                                round(float(np.percentile(r, 90)), 1)]
    out["am_depth_db_p10_p90"] = round(float(np.percentile(r, 90) - np.percentile(r, 10)), 1)
    out["am_periods"] = dominant_periods(r, 1.0)
    return out


def delay_structure(y, sr, bpm):
    """Tempo-synced echo test: autocorrelation of the onset envelope at musical lags."""
    env = librosa.onset.onset_strength(y=y, sr=sr, hop_length=512)
    env = env - env.mean()
    ac = np.correlate(env, env, mode="full")[len(env) - 1:]
    ac /= ac[0]
    dt = 512 / sr
    beat = 60.0 / bpm
    names = {"16th": 0.25, "dotted-16th": 0.375, "8th": 0.5, "triplet-8th": 1 / 3,
             "dotted-8th": 0.75, "quarter": 1.0, "dotted-quarter": 1.5,
             "half": 2.0, "bar": 4.0, "2 bars": 8.0}
    out = {}
    for n, mult in names.items():
        lag = beat * mult
        i = int(round(lag / dt))
        if i < len(ac):
            lo, hi = max(0, i - 3), min(len(ac), i + 4)
            out[n] = dict(lag_s=round(lag, 3), acf=round(float(ac[lo:hi].max()), 3))
    return out


def arrangement(stems, sr, bpm, dur):
    """Per-stem 1 s RMS -> which layers are audible in each 8-bar block."""
    bar = 4 * 60.0 / bpm
    block = 8 * bar
    rows, curves = [], {}
    for k, y in stems.items():
        curves[k] = rms_1s(y, sr)
    n = int(dur // block)
    for b in range(n):
        t0, t1 = b * block, (b + 1) * block
        row = dict(block=b + 1, bars=f"{b*8+1}-{b*8+8}", t0=round(t0, 1), t1=round(t1, 1))
        for k, c in curves.items():
            seg = c[int(t0):int(min(t1, len(c)))]
            row[k] = round(float(seg.mean()), 1) if len(seg) else None
        rows.append(row)
    # relative level: dB below that stem's own loudest block (so "is it in or out")
    for k in curves:
        vals = [r[k] for r in rows if r[k] is not None]
        mx = max(vals) if vals else 0
        for r in rows:
            if r[k] is not None:
                r[k + "_rel"] = round(r[k] - mx, 1)
    return rows, curves, bar


def ssm(y, sr, bpm):
    """Self-similarity on MFCC+chroma, beat-ish downsampled, plus lag-profile
    (mean similarity as a function of time-lag) to read loop length in bars."""
    mf = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20, hop_length=HOP)
    ch = librosa.feature.chroma_cqt(y=y, sr=sr, hop_length=HOP)
    F = np.vstack([librosa.util.normalize(mf, axis=0), librosa.util.normalize(ch, axis=0)])
    # downsample to ~0.5 s columns to keep the matrix small
    k = int(round(0.5 * sr / HOP))
    m = F.shape[1] // k
    F = F[:, :m * k].reshape(F.shape[0], m, k).mean(axis=2)
    F = librosa.util.normalize(F, axis=0)
    S = F.T @ F
    dt = 0.5
    # lag profile: average similarity at each lag
    lags = np.arange(1, m)
    prof = np.array([np.mean(np.diagonal(S, offset=int(l))) for l in lags])
    bar = 4 * 60.0 / bpm
    pk, pr = sig.find_peaks(prof, height=np.percentile(prof, 60))
    top = np.argsort(pr["peak_heights"])[::-1][:6]
    loops = [dict(lag_s=round(float(lags[pk[i]] * dt), 2),
                  bars=round(float(lags[pk[i]] * dt / bar), 2),
                  sim=round(float(prof[pk[i]]), 3)) for i in top]
    return S, dt, loops, prof, lags * dt


# --------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--work", required=True, help="dir with ref02.wav + stems/htdemucs/")
    ap.add_argument("--plots", required=True)
    a = ap.parse_args()
    os.makedirs(a.plots, exist_ok=True)
    R = {}

    mix, sr = librosa.load(os.path.join(a.work, "ref02.wav"), sr=SR, mono=True)
    dur = len(mix) / sr
    R["duration_s"] = round(dur, 2)

    # --- 1. clicks --------------------------------------------------------
    clicks, cfg = find_clicks(mix, sr)
    keep = click_mask(clicks, len(mix), sr)
    R["clicks"] = dict(config=cfg, count=len(clicks),
                       excluded_s=round(float((~keep).sum() / sr), 2),
                       excluded_pct=round(float((~keep).mean() * 100), 2),
                       events=clicks)
    print(f"[clicks] {len(clicks)} found, {(~keep).mean()*100:.2f}% of audio excluded")

    # --- 2. global --------------------------------------------------------
    R["global"] = global_metrics(mix, sr, keep)
    R["global"]["bands_pct_mix"] = band_shares(mix[keep], sr)

    # stems
    sd = os.path.join(a.work, "stems", "htdemucs")
    stems = {}
    for s in STEMS:
        p = os.path.join(sd, s + ".wav")
        if os.path.exists(p):
            stems[s], _ = librosa.load(p, sr=SR, mono=True)
    R["stems_found"] = list(stems)

    # settle the tempo using kick inter-onset intervals on the drums stem
    cand = R["global"]["tempogram_candidates_bpm_relstrength"]
    bpm0 = cand[0][0]
    dm = drum_metrics(stems["drums"], sr, bpm0, clicks) if "drums" in stems else {}
    bpm = dm.get("kick_bpm_from_ioi", bpm0)
    # a kick IOI is usually one beat or one bar; fold into a musical range
    folded = bpm
    while folded < 80: folded *= 2
    while folded > 180: folded /= 2
    R["tempo_settled_bpm"] = round(float(folded), 2)
    R["tempo_settle_note"] = ("kick IOI median %.4f s -> %.2f BPM, folded to %.2f"
                              % (dm.get("kick_ioi_median_s", 0), bpm, folded))
    bpm = folded
    # redo the grid at the settled tempo
    if "drums" in stems:
        dm = drum_metrics(stems["drums"], sr, bpm, clicks)
    R["drums"] = dm

    # --- 3. per stem ------------------------------------------------------
    tot = float((mix ** 2).sum())
    R["per_stem"] = {}
    for k, y in stems.items():
        r = rms_1s(y, sr)
        R["per_stem"][k] = dict(
            rms_dbfs=round(20 * np.log10(max(float(np.sqrt((y ** 2).mean())), 1e-10)), 1),
            energy_pct_of_mix=round(float((y ** 2).sum() / tot * 100), 2),
            bands_pct=band_shares(y, sr),
            rms_1s_p10_p90_db=[round(float(np.percentile(r, 10)), 1),
                               round(float(np.percentile(r, 90)), 1)],
            centroid_mean_hz=round(float(librosa.feature.spectral_centroid(
                y=y, sr=sr, n_fft=N_FFT, hop_length=HOP)[0].mean())))

    # --- 4. movement ------------------------------------------------------
    R["movement"] = {k: movement(stems[k], sr, k) for k in ("other", "bass") if k in stems}
    R["delay_structure_other"] = delay_structure(stems["other"], sr, bpm) if "other" in stems else {}
    R["delay_structure_mix"] = delay_structure(mix, sr, bpm)

    # --- 5. arrangement ---------------------------------------------------
    rows, curves, bar_s = arrangement(stems, sr, bpm, dur)
    R["bar_seconds"] = round(bar_s, 3)
    R["arrangement_8bar_blocks"] = rows
    S, sdt, loops, prof, lag_t = ssm(mix[:int(dur * sr)], sr, bpm)
    R["ssm_loop_candidates"] = loops

    # --- 6. bass ----------------------------------------------------------
    if "bass" in stems:
        b = stems["bass"]
        R["bass"] = bass_pitch_track(b, sr)
        sub = sig.sosfilt(sig.butter(8, 60, btype="lowpass", fs=sr, output="sos"), b)
        body = sig.sosfilt(sig.butter(8, [60, 250], btype="bandpass", fs=sr, output="sos"), b)
        e = float((b ** 2).sum())
        R["bass"]["sub_vs_body_pct"] = dict(sub_lt60=round(float((sub ** 2).sum() / e * 100), 1),
                                            body_60_250=round(float((body ** 2).sum() / e * 100), 1))
        # is the bass tied to the kick?  cross-correlate the two 1 s-ish envelopes
        eb = librosa.onset.onset_strength(y=b, sr=sr, hop_length=512)
        ed = librosa.onset.onset_strength(y=stems["drums"], sr=sr, hop_length=512)
        n = min(len(eb), len(ed))
        eb, ed = eb[:n] - eb[:n].mean(), ed[:n] - ed[:n].mean()
        cc = np.correlate(eb, ed, mode="full") / (np.linalg.norm(eb) * np.linalg.norm(ed))
        mid = n - 1
        win = int(0.3 * sr / 512)
        R["bass"]["xcorr_with_drums_max"] = round(float(cc[mid - win:mid + win].max()), 3)
        R["bass"]["xcorr_lag_ms"] = round(float((np.argmax(cc[mid - win:mid + win]) - win)
                                                * 512 / sr * 1000), 1)
        # sustain: fraction of 1 s frames within 3 dB of the stem median (drone test)
        rb = rms_1s(b, sr)
        R["bass"]["frames_within_3dB_of_median_pct"] = round(
            float((np.abs(rb - np.median(rb)) < 3).mean() * 100), 1)

    # --- 7. plots ---------------------------------------------------------
    plots(a.plots, mix, sr, stems, curves, R, S, sdt, loops, clicks, bar_s, prof, lag_t)

    with open(os.path.join(a.work, "results.json"), "w") as f:
        json.dump(R, f, indent=2)
    print("wrote", os.path.join(a.work, "results.json"))


def plots(pdir, mix, sr, stems, curves, R, S, sdt, loops, clicks, bar_s, prof, lag_t):
    # spectrogram, log-f, 0-2 kHz
    D = librosa.amplitude_to_db(np.abs(librosa.stft(mix, n_fft=8192, hop_length=4096)), ref=np.max)
    plt.figure(figsize=(13, 5))
    librosa.display.specshow(D, sr=sr, hop_length=4096, x_axis="time", y_axis="log", cmap="magma")
    plt.ylim(20, 2000); plt.colorbar(format="%+2.0f dB")
    for c in clicks:
        plt.axvline(c["t"], color="cyan", lw=0.6, alpha=0.7)
    plt.title("ref02 Endel Deeper Focus - log spectrogram 20 Hz-2 kHz (cyan = detected taps)")
    plt.tight_layout(); plt.savefig(os.path.join(pdir, "spectrogram-0-2k.png"), dpi=130); plt.close()

    # per-stem RMS timelines
    plt.figure(figsize=(13, 6))
    for i, (k, c) in enumerate(curves.items()):
        plt.subplot(len(curves), 1, i + 1)
        plt.plot(np.arange(len(c)), c, lw=0.9)
        plt.ylabel(k + "\ndBFS", fontsize=8); plt.grid(alpha=.3)
        for b in np.arange(0, len(c), bar_s * 8):
            plt.axvline(b, color="k", lw=0.3, alpha=.25)
        if i < len(curves) - 1:
            plt.xticks([])
    plt.xlabel("seconds (grey lines = 8-bar blocks)")
    plt.suptitle("Per-stem 1 s RMS (htdemucs; labels are Demucs's, sub sits in `drums`)")
    plt.tight_layout(); plt.savefig(os.path.join(pdir, "stem-rms.png"), dpi=130); plt.close()

    # centroid trajectory of `other` with modulation period annotated
    if "other" in R["movement"]:
        m = R["movement"]["other"]
        t = np.arange(len(m["_cen_traj"])) * m["_dt"]
        plt.figure(figsize=(13, 4))
        plt.plot(t, m["_cen_traj"], lw=1.0)
        if m["centroid_periods"]:
            p = m["centroid_periods"][0]["period_s"]
            for x in np.arange(0, t[-1], p):
                plt.axvline(x, color="r", ls="--", lw=0.7, alpha=.6)
            plt.title(f"`other` spectral centroid (1 s smooth) - dominant modulation "
                      f"period {p:.1f} s = {p/bar_s:.2f} bars (red)")
        plt.xlabel("seconds"); plt.ylabel("Hz"); plt.grid(alpha=.3)
        plt.tight_layout(); plt.savefig(os.path.join(pdir, "other-centroid.png"), dpi=130); plt.close()

    # self-similarity matrix
    plt.figure(figsize=(7, 6))
    plt.imshow(S, origin="lower", cmap="magma",
               extent=[0, S.shape[0] * sdt, 0, S.shape[0] * sdt])
    plt.colorbar(); plt.xlabel("s"); plt.ylabel("s")
    plt.title("Self-similarity (MFCC+chroma)")
    plt.tight_layout(); plt.savefig(os.path.join(pdir, "ssm.png"), dpi=130); plt.close()

    # lag profile (loop length)
    plt.figure(figsize=(11, 3.5))
    plt.plot(lag_t / bar_s, prof, lw=1)
    plt.xlabel("lag (bars)"); plt.ylabel("mean self-similarity"); plt.grid(alpha=.3)
    plt.title("Repeat-length profile: peaks = loop lengths in bars")
    plt.xlim(0, 80)
    plt.tight_layout(); plt.savefig(os.path.join(pdir, "loop-lag-profile.png"), dpi=130); plt.close()

    # arrangement heatmap
    rows = R["arrangement_8bar_blocks"]
    keys = [k for k in STEMS if k in curves]
    M = np.array([[r.get(k + "_rel", -60) for r in rows] for k in keys], float)
    plt.figure(figsize=(13, 2.6))
    plt.imshow(M, aspect="auto", cmap="viridis", vmin=-24, vmax=0)
    plt.yticks(range(len(keys)), keys)
    plt.xticks(range(0, len(rows), 2), [rows[i]["bars"] for i in range(0, len(rows), 2)],
               rotation=45, fontsize=7)
    plt.colorbar(label="dB below that stem's loudest block")
    plt.title("Arrangement: relative level per 8-bar block")
    plt.tight_layout(); plt.savefig(os.path.join(pdir, "arrangement.png"), dpi=130); plt.close()


if __name__ == "__main__":
    main()
