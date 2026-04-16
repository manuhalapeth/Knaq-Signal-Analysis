# Exploratory Analysis: Key Observations
### Part 2 Signal Characterization

## 1. The Sensor Geometry Is Accidentally Perfect for Dynamics Analysis

The long term gravity decomposition (derived from 52.66M samples, zero gyroscope) recovers **g = 9.792 m/s² against standard 9.807 m/s², a 0.146% error**. That is calibration quality you would expect from a lab instrument, not raw firmware output. It validates that the long term mean approach is reliable and that the sensor has negligible bias.

What it reveals about mounting: X carries 95.8% of gravitational load (mean 9.399 m/s², 16.30 degrees from vertical), Y carries 28.0% (mean 2.748 m/s², 73.70 degrees from vertical), and Z carries **0.7%** (mean 0.070 m/s², 89.59 degrees from vertical, effectively perfectly horizontal). Pitch is +73.70 degrees, roll +88.53 degrees.

The consequence for signal analysis is significant: **Z requires zero gravity compensation**. Its RMS = 2.756 m/s², std = 2.755 m/s², 100% dynamic content by definition. X, by contrast, is 91.1% gravity and only 8.9% dynamics. For any real time event classifier or anomaly detector, Z is the channel to watch: no DC removal, no tilt correction, no orientation model needed. Y sits in between at 32.1% dynamic content.

One further detail worth noting: the Y axis mean is persistently **2.748 m/s²**, and its p99 is 0.273 m/s², meaning **99% of all Y samples are negative**. The Y axis almost never crosses zero. This confirms a fixed, hardware level mounting offset, not a transient orientation effect. Any downstream classifier needs to treat Y's sign convention as an immutable constant for this device.

## 2. The Sample Clock Is Jittering at 44%. This Is a Firmware Problem.

The median sample interval is exactly 1.2500 ms (confirming 800 Hz), but the **standard deviation is 0.5557 ms, 44.5% of the nominal interval**. This is not quantization noise. At a true 800 Hz hardware clock, interval jitter should be sub microsecond. At 44%, the acquisition firmware is almost certainly running a **software polling loop**, not a hardware interrupt driven timer.

Why this matters analytically: every spectral method in this notebook, Welch PSD, STFT, the spectrogram, assumes uniform sampling. The frequency resolution claimed (0.195 Hz for Welch, 0.391 Hz for the spectrogram) is computed from sample count and nominal fs. With real jitter of 0.56 ms, each FFT window contains phase noise that broadens spectral peaks and raises the effective noise floor. The "drifting vs stable" classification of resonances is therefore less reliable than the numbers suggest. A genuinely stable resonance could appear to drift due to non uniform time steps.

For a product shipping firmware: this is a one line fix (hardware timer interrupt instead of polling) that would improve all downstream spectral analysis quality materially. The timestamp anomalies in Part 1, 1,119,928 monotonicity violations and 2,385,639 duplicate timestamps (4.5% of the dataset), are almost certainly a symptom of the same root cause: a soft clock that occasionally stalls, duplicates, or reverses under interrupt pressure.

## 3. The Kurtosis Values Are Consistent Across All Axes. That Consistency Is the Observation.

All three axes return kurtosis in the range **4.38 to 4.49**, tightly clustered around 4.43. This uniformity across geometrically independent axes rules out axis specific artifacts. The elevated kurtosis (around 48% above the Gaussian baseline of 3.0) is a property of the system's dynamics, not the sensor.

Kurtosis in this range is the fingerprint of **moderate impulsive content**: recurring short duration, high amplitude events layered on top of a broadly Gaussian vibration background. Not catastrophic (kurtosis above 10 would indicate structural distress), not clean (kurtosis = 3.0 would indicate pure background vibration noise). Think surface impacts, step transitions, mechanical transitions. Events that last milliseconds but happen regularly enough over 18 hours to systematically fatten all three tail distributions.

The product implication is direct: kurtosis is cheap to compute (one pass over a 1 second buffer), orientation independent in the sense that all three axes are equally elevated, and sits at a value (around 4.4) that is actionable as a deployment baseline. A system where kurtosis climbs above 6 to 8 on the Z axis over time is telling you something changed: surface conditions, mounting wear, or component condition.

## 4. The Skewness Values Reveal a Paradox Worth Resolving

All three axes have skewness within **0.013 to 0.016**, nearly perfectly symmetric distributions. For a system dynamics signal, this says the physical system encounters statistically equal positive and negative excursions on every axis over 18 hours, which is physically coherent: as much lateral motion in one direction as the other, as much acceleration as deceleration, similar upward and downward environmental inputs.

Now compare that to the vector **magnitude** distribution, which is heavily right skewed: mean = 10.194 m/s², median = 9.809 m/s². The mean is pulled +0.385 m/s² above the median by a long right tail of high magnitude transient events. Yet the median is **9.809 m/s², within 0.002 m/s² of standard g (9.807)**. The median sample, the "typical" observation in this dataset, is essentially the physical system at rest at exactly gravitational acceleration.

This is not a contradiction. It is a signal about the dataset's structure. The **typical sample is quiet, but the distribution has a heavy upper tail from impact events**. The per axis symmetry means those impacts come from all directions equally over time. The magnitude asymmetry means when impacts happen, they add to the vector magnitude rather than cancelling across axes, which is physically expected. You cannot have a "negative" impact that reduces total acceleration.

For feature engineering: the median magnitude is a far more stable baseline than the mean. Any drift in the median over time is a meaningful signal about sensor calibration or system orientation change.

## 5. The Z Axis Extremes Are Asymmetric and the Physics Explains Why

Z minimum = **22.975 m/s²**, Z maximum = **+26.954 m/s²**. With a near zero mean (0.070 m/s²), the peak to peak of 49.929 m/s² is roughly symmetrically distributed around zero but not exactly. The positive extreme is **3.98 m/s² larger** than the negative extreme in absolute terms.

For a near horizontal axis in this mounting configuration, positive Z likely corresponds to the upward direction relative to the physical system. The asymmetry means the largest recorded events were **compressions in the positive direction** (contact with a raised obstacle, mechanical damping compression) rather than extensions in the negative direction (system dropping away from a surface, damping extension). This is consistent with typical impact distributions: raised obstacles and hard surface contacts are more common and sharper than gradual downward extensions.

The Z peak to peak of 49.929 m/s² is **3.5x larger than X (13.666 m/s²)** and **3.3x larger than Y (15.012 m/s²)**. This axis carries the system's full vertical dynamics, uncontaminated by gravity bias. For any surface classification or impact detection model, **Z is the only axis that matters**.

## 6. The 3g Event Happened During the Calmest Active Phase. That Is the Point.

The maximum vector magnitude is **29.35 m/s² (2.99x g)** at **3.43 hours into the recording**. The per hour intensity analysis for hour 3 shows only 77 p95 threshold bins, well below the expected 180 and among the lowest of any active hour. The max bin std for hour 3 is 1.526 m/s², unremarkable.

The 3g event is **discrete and isolated**: a single 32.91 second analysis bin containing an extreme excursion surrounded by hours of normal operation. This is exactly the failure mode that per hour p95 counting cannot detect. You can be in the calmest hour of the recording and still hit 3g once.

This has direct product design implications. **Any event detection system built only on rolling standard deviation or per minute bin statistics will miss this class of event entirely.** You need a parallel high frequency trigger, something like "any sample exceeding N times local RMS within a short window", running simultaneously alongside the trend analysis. The two approaches are complementary and not interchangeable. The 3g event argues for streaming processing at native 800 Hz, not just windowed aggregates.

## 7. The Session Structure Tells a Specific Story

The 15 stationary segments reconstruct the full session timeline with surprising granularity:

- **0 to 1.13h**: initial continuous active phase (around 68 minutes)
- **1.13 to 1.25h**: brief stop cluster. 4 micro segments totaling around 400 seconds (scheduled stops, loading, or servicing)
- **1.25 to 8.44h**: the dominant feature. **7.19 hours of continuous operation without a single stop**
- **8.44h**: a 76 second pause (two back to back segments of 60s and 16s)
- **8.46 to 11.79h**: continued active operation (around 3.33 hours)
- **11.79 to 12.58h**: fragmented wind down. 6 short segments (4 to 120 seconds each) interspersed with brief active phases
- **12.70 to 13.25h**: 33 minute stationary period (motor off, mean bin std = 0.026 m/s²)
- **13.25 to 13.37h**: brief 7 minute return phase (only 425 active seconds in the entire hour)
- **13.37 to 18.28h**: terminal 4.92 hour standby (motor off, mean bin std = 0.022 m/s²)

A 7.19 hour uninterrupted active operation is an extended deployment session, consistent with a long distance transit run, a multi stop service route, or continuous asset operation. The structure (one long active phase, brief stops, progressive wind down, extended standby) is a clean behavioral archetype that a session segmentation algorithm should be able to reproduce exactly from this data.

## 8. The Bin Std Is a Proxy for Motor State, Not Just Motion State

The mean within bin std across stationary segments follows a clear gradient:

| Segment | Duration | Mean bin std | Motor interpretation |
|---------|----------|-------------|----------------------|
| Long standby (1, 2) | 4.92h, 33min | 0.022 to 0.026 m/s² | Motor off, at/near sensor noise floor |
| Medium stops (3 to 5) | 1.7 to 4.6 min | 0.046 to 0.066 m/s² | Likely motor off, not fully settled |
| Short stops (6 to 15) | 4 to 60 seconds | 0.063 to 0.085 m/s² | Motor likely active, brief stop |

The theoretical sensor noise floor at 800 Hz is around 0.02 to 0.05 m/s². The long standby periods at 0.022 m/s² are sitting at the absolute floor, these are dead silent observations. The 60 second stops at 0.065 m/s² carry enough residual vibration energy to suggest the motor had not been switched off.

This means **bin std alone can discriminate motor on from motor off stationary states**, no additional sensor needed, no external data bus integration required. The threshold sits somewhere between 0.030 and 0.050 m/s². For a product that wants to infer standby time, energy consumption, or emissions during stops, this is a derivable signal from the accelerometer alone.

## 9. Gate B Is Doing All the Work in Stationary Detection. Gate A Is Nearly Redundant.

The two gate stationary detector: Gate A (|mean_mag minus g| < 0.30 m/s²) passes **20,528 bins**. Gate B (bin_std < 0.10 m/s²) passes **20,445 bins**. The intersection is **20,445 bins**, identical to Gate B alone. Only **83 bins pass Gate A but fail Gate B**.

Gate A is contributing almost nothing. When the system is truly stationary, the mean magnitude is essentially always within 0.30 m/s² of g. The std threshold is the binding discriminator, not the magnitude proximity. The physical reason: a system at rest with its motor active is more likely to have a mildly elevated mean magnitude than to have elevated within bin std. The motor vibration is structured and narrow band, which raises std measurably before it meaningfully shifts the bin mean.

For a production implementation: **a single gate on within bin std (< 0.10 m/s²) would give identical results** to the two gate system, at half the compute cost. The magnitude gate adds fault tolerance in edge cases (sensor tilting mid stop, etc.) but does not change the output on this dataset. This is worth knowing if this algorithm gets ported to a resource constrained MCU.

## 10. The Vibration Intensity Distribution Is Strikingly Compressed

During active operation (45,380 bins, 12.61 hours): p50 std = 1.231 m/s², p95 = 1.330 m/s², p99 = 1.377 m/s². The **entire range from the median to the 99th percentile is only 0.146 m/s²**, a 11.9% spread.

This is unusually tight for 12+ hours of operation across presumably varied surface conditions. It tells you several things simultaneously: the system's mechanical damping is doing its job (absorbing variation in surface roughness before it reaches the sensor), the recording covers a homogeneous operational environment (no sudden transitions between radically different surface types), and the operation style is consistent (no sustained periods of high speed rough surface operation that would shift the whole distribution upward).

The consequence for thresholding: **there is no natural gap in the active bin std distribution that an absolute threshold can exploit**. A threshold at 1.0 m/s² catches everything; at 1.35 m/s² catches almost nothing. This is why the analysis correctly uses session relative percentiles (p95, p99) rather than absolute values. The signal structure demands it and any future model trained on this data should respect that.

## 11. The Intensity Escalation Pattern Has a Double Peak Structure That Suggests Operational Phase Shifts

The per hour p95 counts trace a specific shape:

- Hours 0 to 4: **66 to 85** (consistent low baseline)
- Hours 5 to 7: **208 to 248 to 335** (progressive ramp, +304% from baseline by hour 7)
- Hour 8: **169** (sudden drop, 76 second stop at 8.44h)
- Hours 9 to 10: **181 to 228** (renewed climb)
- Hour 11: **381** (session peak, 2.12x expected)
- Hours 12 to 13: rapid collapse into standby

This is a double peak with a trough at hour 8. Two plausible interpretations: the system transitioned between two distinct operational environments (smooth surface phase 1, brief stop, different conditions in phase 2), or operational speed increased progressively in both phases with the stop marking a waypoint. Either way, **hours 5 to 7 and 9 to 11 are not the same kind of rough**. Hour 7's peak is driven by a high single second max (1.550 m/s²) while hour 11's peak is driven by sustained count (381 p95 bins) with a lower max (1.460 m/s²). Discrete hard impacts vs. consistent high vibration grinding. Different surface dynamics, different implications for system wear.

The 3g isolated impact at 3.43h occurs during the **quiet baseline phase (hours 0 to 4)**, reinforcing that transient discrete events and sustained vibration intensity are independent signals that must be tracked separately.

## 12. The Dominant Spectral Peak May Be Interpretable as an Operational Speed

The spectrogram analysis over a 30 minute clip (4.59 to 5.09h, within the 7.19h continuous active phase) returns 5 peaks, all operationally speed dependent (drift std > 1.0 Hz). The strongest: **52.35 Hz at 22.49 dB with prominence 10.41 dB**, nearly 3 dB above the next strongest peak and more than 8 dB above the weakest. This peak dominates the system's vibrational signature.

More interesting is the **8.20 Hz peak** (28.78 dB, prominence 7.82, drift std 1.04 Hz, the lowest drift in the table, nearly at the stable/drifting boundary). If this is a rotating component frequency (such as a wheel or drive shaft), back calculating operational speed with an assumed effective diameter of around 650 mm gives: f = v / (pi x d), so v = 8.20 x pi x 0.65, approximately **16.7 m/s**. That is one plausible interpretation. Without knowing the physical system type, it cannot be confirmed.

The 52.35 Hz and 47.27 Hz pair (5 Hz apart) are worth noting as a potential near harmonic relationship. If the fundamental were around 24 Hz, these would sit near the 2nd harmonic. The 23.83 Hz peak supports this. **23.83 Hz, 47.27 Hz, and the vicinity of 52.35 Hz could represent a 1st/2nd harmonic series from a drivetrain or surface spatial frequency**, with the 52.35 Hz peak being independently excited by a structural mode that happens to align nearby. Without additional context about the physical system this cannot be confirmed, but it is a testable hypothesis on the next recording.

## 13. No Fixed Structural Resonances Is Itself the Baseline. And It Is Fragile.

Every detected spectral peak fails the structural stability test (all drift std > 1.0 Hz). The absence of fixed frequency resonances means the physical system is not exhibiting self excited ringing or fatigue mode vibration. This is baseline healthy.

But it is also worth understanding what "no structural resonances" means in this analysis: the spectrogram covers one **30 minute clip** out of 7.19 hours of continuous active operation. Structural resonances that only appear at specific operational speed ranges, or under specific load conditions, would be missed. The analysis is suggestive, not exhaustive.

The operational value of establishing this baseline is forward looking: a deployment platform that indexes "no prominent stable resonances" for a new device can detect structural fatigue or component wear by monitoring for the **emergence** of new stable frequencies in future recordings. The anomaly is the signal. The baseline is this recording.

## Summary: The Signal From the Signal

This dataset is 52.66 million samples of a single physical system completing what appears to be an **extended operational session**: 7+ hours of continuous operation, a full day active phase, progressive wind down, and an extended standby period. Mechanically normal. Dynamically well behaved. One isolated 3g impact. Two distinct high vibration phases that appear operationally distinct from each other.

The five findings that would directly inform a product roadmap:

1. **Fix the firmware clock.** 44% timing jitter undermines every spectral analysis and corrupts event timestamps at the 2.4M sample scale. This is upstream of everything else.

2. **Z axis only for event detection.** Pure dynamics, no compensation required, 3.5x the amplitude range of the other axes. Everything else is redundant for impact/surface quality scoring.

3. **Use within bin std as a motor state proxy.** The below 0.030 m/s² floor identifies motor off states without external data bus integration, a meaningful capability for standby time and emissions inference.

4. **Run two parallel detectors.** A 1 second windowed std tracker for sustained intensity patterns (hours 7 and 11) and a sample level threshold trigger for discrete impacts (the 3g event at 3.43h). These signals are structurally independent and one cannot substitute for the other.

5. **Intensity thresholds must be session relative, not absolute.** The 11.9% spread from p50 to p99 of active vibration means no fixed threshold cleanly separates vibration intensity tiers. Deployment scoring requires percentile relative normalization per device, per route, or per session.
