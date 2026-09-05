# Verified Live-control pitfalls

Observed locally in Ableton Live 12 on 2026-09-05. Rediscover capabilities before assuming another bridge exposes the same API.

- Save the original Live Set before experiments and verify the current file name. Browser/native UI interaction uses the installed computer-use surface.
- Enumerate device parameters; normalized values are not display units. Operator Attack has a different curve from Decay/Release. Set and read back **milliseconds**, filter **Hz**, level **dB**, and enum labels.
- Operator's [official instrument reference](https://www.ableton.com/en/live-manual/12/live-instrument-reference/#operator) confirms its partial editor, output-normalization context option and modeled filter drive. Its global Time parameter is an adjustment around zero; inspect the actual range before mistaking 0% for zero envelope duration.
- Native Operator has one internal LFO; independent continuous modulators can be external LFO devices. An envelope that restarts on every note is not an independent slow drift.
- External LFO exposes duplicate `Rate` names for frequency and sync. Select the correct enumerated parameter and verify its displayed units. A name-to-parameter dictionary can silently select the wrong one.
- Verify a modulation mapping by the visible target label and a rendered effect; merely having an LFO device or Map checkbox does not prove it is mapped.
- Local OSC writes are queued. An OSC read barrier before TCP inspection prevented stale snapshots. Some TCP mutation responses reflected pre-change state; use subsequent readback.
- The installed bridge's `duplicate_session_clip_to_arrangement` uses `destination_time`, not `time`; the wrong key silently placed clips at zero. Read every resulting clip start/end.
- Export dialogs may cache the previous selection length and regenerate accessibility IDs. Read the actual export start, duration, track selection, and current IDs.
- In the local native UI, export-length sliders did not support accessibility setValue; click and type worked. Live appended the selected track name to the supplied export basename. Discover the actual output filename instead of assuming the typed name is final.
- A muted Main Utility can make the main export silent while individual tracks export normally with Main FX excluded. Summed stems do not include Main processing; label them accordingly.
- Output-meter values are not automatically linear amplitude. Use rendered audio for loudness/peak measurement.
- Keep synth evidence, audio renders, and listening verdicts together. A correctly loaded patch is operational proof; it is not proof of a good sound.
