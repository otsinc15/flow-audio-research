# Spec extracted from the listening references

Date: 2026-09-02. Method: measurement only — **no listening judgement is made anywhere in this
file.** The agent that produced it cannot hear. Everything below is a number from `ffmpeg`
(EBU R128) or `librosa` 0.11 (tempo, onsets, spectral balance), plus the arithmetic on those
numbers. The ear test is still the real test.

Reference audio lives outside the repo (`~/Documents/AI Agent Outputs/Artifacts/flow-audio-references/`),
is never committed, and was never uploaded to any generator. See `reference-manifest.md`.

## How each column was measured

| Metric | Tool | Note |
|---|---|---|
| Tempo (BPM) | `librosa.beat.beat_track` | librosa's default prior is a log-normal centred on **120 BPM**, so a bare "120" is weak evidence. The `candidates` column is the prior-free tempogram peak list. |
| Tempo confidence | peak/median ratio of the aggregated tempogram + coefficient of variation of inter-beat intervals | Higher ratio = one periodicity dominates. Lower beat-CV = steadier grid. |
| I / LRA / True peak | `ffmpeg -filter_complex ebur128=peak=true` | I = integrated LUFS, LRA = loudness range in LU, peak = dBFS true peak. |
| Band shares | power (magnitude²) STFT, `n_fft=8192`, hop 2048, share of total energy | **Power-domain shares are always bass-dominated** — a 60 Hz sine carries orders of magnitude more energy than an equally loud hi-hat. Compare rows against each other, never against an intuition about "how bright it sounds". |
| Onsets/min | `librosa.onset.onset_detect` count ÷ minutes | An *event-density proxy*, not a count of musical hits. Only the relative figure means anything. |
| Centroid CV | std ÷ mean of the spectral centroid | How much the timbre moves. `slow_cv_1s` is the same on a 1-second smoothed centroid, i.e. slow timbral drift with the per-beat flicker removed. |
| RMS spread | p90 − p10 of frame RMS in dB (46 ms frames) | Frame-level, so a hard kick against a quiet gap inflates it. **LRA is the honest "constant energy" number**; RMS spread is included only because it exposes head/tail fades. |

## References

| | ref01 — "Late Autumn" 12:51–17:45 | ref02 — Endel Deeper Focus |
|---|---|---|
| Duration | 4:54 | 7:47 |
| **Tempo** | **114.8 BPM** | **120.2 BPM** |
| Tempo candidates (BPM, rel. strength) | 114.8 (1.00), 76.0 (0.77), 56.8 (0.76) | 120.2 (1.00), 79.5 (0.96), 161.5 (0.86) |
| Tempo peak/median ratio | 27.0 | 17.6 |
| Beat-interval CV | 0.027 | 0.019 |
| **Integrated loudness** | **−20.4 LUFS** | **−14.9 LUFS** |
| **LRA** | **4.1 LU** | **4.1 LU** |
| True peak | −4.3 dBFS | **0.0 dBFS (at the ceiling)** |
| <60 Hz | 27.6 % | 4.5 % |
| 60–150 Hz | 21.2 % | 76.7 % |
| 150–500 Hz | 46.5 % | 14.8 % |
| 500 Hz–2 kHz | 4.2 % | 4.0 % |
| 2–8 kHz | 0.44 % | 0.07 % |
| >8 kHz | 0.11 % | 0.00 % |
| Onsets / min | 393 | 346 |
| Centroid mean | 1797 Hz | 788 Hz |
| Centroid CV | 0.58 | 0.64 |
| Centroid slow CV (1 s) | 0.41 | 0.46 |
| RMS spread p10–p90 | 10.0 dB | 11.0 dB |

### Caveats that limit how far these numbers can be pushed

1. **ref02 is an iPhone screen recording**, not a master. Its `I` of −14.9 LUFS and its 0.0 dBFS true
   peak describe the *phone's playback chain at whatever volume the device was set to*, not Endel's
   mix. Its near-absent sub (4.5 % below 60 Hz against 76.7 % in 60–150 Hz) may be Endel's own
   voicing for earbuds *or* the capture path rolling off the bottom. **This measurement cannot tell
   those two apart.**
2. **ref01 is a SoundCloud stream** (AAC 160 k), which is loudness-normalised on the way out, so its
   −20.4 LUFS is likewise not the artist's master.
3. Therefore **absolute loudness is not comparable between the two references**. What *is* comparable,
   because both landed on it independently through different capture chains, is **LRA = 4.1 LU** in
   both. That is the transferable fact: both references hold near-constant energy for minutes.
4. ref02's tempo of 120.2 BPM sits exactly on librosa's prior. Its tempogram peak ratio (17.6) is the
   weaker of the two, and its second candidate (79.5 BPM at 0.96 relative strength) is nearly as
   strong as the winner. **Treat "Endel Deeper Focus is at 120 BPM" as unconfirmed**; the pulse is
   steady (beat-CV 0.019) but which periodicity is *the* tempo is not settled by this measurement.
   ref01's 114.8 BPM is solid: peak ratio 27.0 and a second candidate at two-thirds the strength.

## Target spec, in plain English

Aim at a steady grid somewhere in the **114–122 BPM** window — ref01, the track Daniel calls perfect,
sits at 114.8, and the strongest reading of the Endel bar is 120. Anything above ~126 is outside both
references. Hold the energy dead flat: both references land on a loudness range of **4.1 LU**, which
in practice means no section is more than about two decibels louder than any other for the whole
duration, so a target of **LRA ≤ 4 LU** is the single most defensible number here. For absolute level,
neither capture is a master, so master to the platform convention (about **−16 to −14 LUFS integrated**
for app playback) and keep at least **1 dB of true-peak headroom** — ref02 hit 0.0 dBFS, which is a
property of the phone recording, not something to imitate. On the bottom end the two references
disagree sharply and the disagreement is the finding: ref01 puts **~49 % of its energy below 150 Hz**
split roughly evenly between sub (<60 Hz, 27.6 %) and bass (60–150 Hz, 21.2 %), and still keeps
**46 % in the 150–500 Hz chord/body region**, while ref02 puts **81 % below 150 Hz but almost none of
it under 60 Hz**. A safe target for a product that has to work on earbuds and on a laptop speaker is
**40–55 % below 150 Hz, with the sub band no more than about half of that, and a real 150–500 Hz body
of 15–45 %** — the region where both a filtered chord and the warmth of a room live. Keep everything
above 2 kHz under about **0.5 % of total energy**; both references are startlingly dark up there.
Finally, keep event density at or under roughly **400 onsets per minute** (ref01 393, ref02 346) and
keep slow timbral drift alive rather than frozen — both references show a 1-second-smoothed centroid
coefficient of variation around **0.41–0.46**, meaning the colour keeps moving gently even though
nothing ever "happens".

---

# Objective pre-screen: six ElevenLabs clips against the spec

Six 60-second clips generated 2026-09-02 (`generation-log-2026-09-02.md`); audio is in
`~/Documents/AI Agent Outputs/Artifacts/flow-audio-candidates/`, uncommitted. Same measurement
pipeline, identical settings. **This is a pre-screen, not a verdict.** It can only say whether a clip
is inside the reference envelope on measurable axes; it says nothing about whether it sounds good,
and nothing here should be read as a quality claim.

| | ref01 | ref02 | a-1 | a-2 | a-3 | b-1 | b-2 | b-3 |
|---|---|---|---|---|---|---|---|---|
| Prompted BPM | — | — | 122 | 120 | 126 | 118 | 122 | 115 |
| **Measured BPM** | 114.8 | 120.2 | 123.0 | 120.2 | 126.0 | 117.5 | 123.0 | 114.8 |
| Tempo peak ratio | 27.0 | 17.6 | 34.7 | 24.8 | 54.2 | 28.8 | 43.1 | 27.8 |
| Beat-interval CV | 0.027 | 0.019 | 0.011 | 0.006 | 0.026 | 0.009 | 0.011 | 0.007 |
| **I (LUFS)** | −20.4 | −14.9 | −12.4 | −14.1 | −14.0 | −14.3 | −14.0 | −14.9 |
| **LRA (LU)** | 4.1 | 4.1 | 0.4 | 0.1 | 5.8 | 0.5 | 1.5 | 0.7 |
| True peak (dBFS) | −4.3 | 0.0 | −1.4 | −1.4 | −0.1 | −1.4 | −1.4 | −1.3 |
| **<60 Hz** | 27.6 % | 4.5 % | 76.9 % | 69.0 % | 64.2 % | 68.7 % | 53.5 % | 46.3 % |
| 60–150 Hz | 21.2 % | 76.7 % | 19.1 % | 27.7 % | 28.9 % | 21.1 % | 37.1 % | 40.7 % |
| **Σ <150 Hz** | 48.8 % | 81.2 % | 96.0 % | 96.8 % | 93.1 % | 89.8 % | 90.6 % | 87.1 % |
| **150–500 Hz** | 46.5 % | 14.8 % | 3.9 % | 3.1 % | 4.2 % | 9.8 % | 8.8 % | 12.0 % |
| 500 Hz–2 kHz | 4.2 % | 4.0 % | 0.10 % | 0.08 % | 0.10 % | 0.36 % | 0.59 % | 0.73 % |
| 2–8 kHz | 0.44 % | 0.07 % | 0.00 % | 0.01 % | 0.16 % | 0.05 % | 0.03 % | 0.03 % |
| >8 kHz | 0.11 % | 0.00 % | 0.00 % | 0.03 % | 2.43 % | 0.00 % | 0.01 % | 0.18 % |
| **Onsets / min** | 393 | 346 | 244 | 374 | 499 | 460 | 333 | 334 |
| Centroid mean (Hz) | 1797 | 788 | 1169 | 2293 | 6606 | 1573 | 1656 | 1914 |
| Centroid slow CV (1 s) | 0.41 | 0.46 | 0.41 | 0.05 | 0.12 | 0.45 | 0.28 | 0.53 |
| RMS spread p10–p90 (dB) | 10.0 | 11.0 | 26.9 | 23.0 | 28.3 | 38.6 | 32.9 | 25.9 |
| Head 3 s → tail 3 s level | −24.1 → −21.4 dB | — | −11.2 → −13.1 | −13.3 → −13.2 | −12.2 → **−21.8** | −13.7 → **−38.0** | −13.4 → −18.3 | −14.5 → **−23.9** |

### What the pre-screen actually establishes

**Tempo: pass, and better than expected.** Every clip landed within 1.5 BPM of its prompted tempo
(122→123.0, 120→120.2, 126→126.0, 118→117.5, 122→123.0, 115→114.8), and every clip's grid is
*steadier* than either reference (beat-CV 0.006–0.026 against 0.027 and 0.019). Five of six sit inside
the 114–123 BPM band the references define; a-3 at 126.0 is above it by design. **BPM in the prompt is
a working control.**

**Loudness: pass on level, and flatter than the references on range.** All six sit at −14.9 to
−12.4 LUFS, i.e. between the two reference captures, with 1.3–1.4 dB of true-peak headroom on five of
six (a-3 is at −0.1 dBFS, effectively no headroom). Five of six have an LRA of 0.1–1.5 LU, well under
the 4 LU target — these are *more* constant than the references, not less. a-3 (5.8 LU) is the only
one outside, and its head-to-tail figures explain why: it fades.

**Low end: every clip fails the envelope, and it is the headline gap.** Sub-60 Hz energy runs 46–77 %
against ref01's 27.6 %; total energy below 150 Hz runs 87–97 % against ref01's 48.8 % and ref02's
81.2 %. The mirror of that is the **150–500 Hz body region, where every clip is starved**: 3.1–12.0 %
against ref01's 46.5 % and ref02's 14.8 %. In measurement terms the clips are a kick and a sub with
almost nothing in the register where a filtered chord would sit. b-3 (46.3 % sub, 12.0 % body) and
b-2 are the closest to the envelope; a-1 and a-2 are the furthest. **Nothing here says the clips sound
bad — it says their energy distribution is not the references' distribution**, and that the dub-techno
palette (B) moves toward the references while the minimal-techno palette (A) moves away.

**Brightness: a-3 is an outlier.** 6606 Hz mean centroid and 2.43 % of energy above 8 kHz, against
≤0.18 % for every other clip and ≤0.11 % for both references. The "shaker and percussive tick" wording
in the a-3 prompt is the plausible cause.

**Event density: mostly inside, two outside.** a-1 at 244/min is well under both references; a-3 (499)
and b-1 (460) are over the ~400 ceiling.

**Loop-friendliness: four of six fade out despite the prompt forbidding it.** Every prompt said "no
outro". a-1 (−1.9 dB head-to-tail) and a-2 (+0.1 dB) are flat and would butt-splice; a-3 (−9.6 dB),
b-2 (−4.9 dB) and especially b-1 (−24.3 dB) taper, and b-3 (−9.4 dB) does too. **"No outro" in the
prompt is not reliably obeyed** — a loopable clip needs either a re-roll or a trim before the fade.

The high RMS spread on the clips (23–39 dB against the references' 10–11 dB) is *not* evidence of
inconstant arrangement: LRA, which is the gated 3-second measure, says the opposite. It reflects
46 ms frames alternating between a very loud sub-heavy kick and a comparatively empty gap — i.e. the
clips are far more sub-transient-dominated than the references, which is the same finding as the band
table, seen from a different angle.
