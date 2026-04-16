"""
Build ManuHalapeth_Knaq_TakeHome.pdf   black and white
IOV Accelerometer Signal Analysis Take-Home Exercise
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib import colors
import os

# ── Strictly black and white palette ────────────────────────────────────────
BLK       = HexColor('#000000')
NEAR_BLK  = HexColor('#111111')
DARK      = HexColor('#222222')
MID       = HexColor('#555555')
LIGHT     = HexColor('#888888')
RULE_CLR  = HexColor('#aaaaaa')
BG_LIGHT  = HexColor('#f2f2f2')
BG_MID    = HexColor('#e0e0e0')
WHITE     = HexColor('#ffffff')

PAGE_W, PAGE_H = A4
L_MAR = R_MAR = 2.2 * cm
T_MAR = 2.6 * cm
B_MAR = 2.2 * cm

# ── Styles ───────────────────────────────────────────────────────────────────
base = getSampleStyleSheet()

def _s(name, **kw):
    return ParagraphStyle(name, parent=base['Normal'], **kw)

S = {
    'title'   : _s('Title',   fontSize=24, textColor=BLK,   fontName='Helvetica-Bold',
                              leading=30,  spaceAfter=6,    alignment=TA_CENTER),
    'subtitle': _s('Sub',     fontSize=12, textColor=DARK,  fontName='Helvetica',
                              leading=17,  spaceAfter=4,    alignment=TA_CENTER),
    'author'  : _s('Author',  fontSize=11, textColor=MID,   fontName='Helvetica',
                              leading=16,  spaceAfter=2,    alignment=TA_CENTER),
    'date'    : _s('Date',    fontSize=10, textColor=LIGHT,  fontName='Helvetica-Oblique',
                              leading=14,  spaceAfter=0,    alignment=TA_CENTER),

    'h1'      : _s('H1',      fontSize=14, textColor=WHITE, fontName='Helvetica-Bold',
                              leading=19,  spaceBefore=16,  spaceAfter=6,
                              backColor=BLK,
                              leftIndent=-0.4*cm, rightIndent=-0.4*cm,
                              borderPadding=(5, 8, 5, 8)),
    'h2'      : _s('H2',      fontSize=11, textColor=BLK,   fontName='Helvetica-Bold',
                              leading=15,  spaceBefore=12,  spaceAfter=3),
    'h3'      : _s('H3',      fontSize=10, textColor=DARK,  fontName='Helvetica-Bold',
                              leading=14,  spaceBefore=8,   spaceAfter=2),

    'body'    : _s('Body',    fontSize=9.5, textColor=DARK, fontName='Helvetica',
                              leading=14.5, spaceBefore=2,  spaceAfter=4,
                              alignment=TA_JUSTIFY),
    'bullet'  : _s('Bullet',  fontSize=9.5, textColor=DARK, fontName='Helvetica',
                              leading=14,   spaceBefore=1,  spaceAfter=2,
                              leftIndent=14, bulletIndent=4),
    'mono'    : _s('Mono',    fontSize=8.5, textColor=DARK, fontName='Courier',
                              leading=12,   spaceBefore=1,  spaceAfter=1,
                              leftIndent=10, backColor=BG_LIGHT,
                              borderPadding=(3, 5, 3, 5)),
    'caption' : _s('Caption', fontSize=8.5, textColor=LIGHT, fontName='Helvetica-Oblique',
                              leading=12,   spaceBefore=2,  spaceAfter=6,
                              alignment=TA_CENTER),
    'callout' : _s('Callout', fontSize=9.5, textColor=DARK, fontName='Helvetica',
                              leading=14,   spaceBefore=4,  spaceAfter=4,
                              leftIndent=10, borderPadding=(5, 8, 5, 8),
                              backColor=BG_LIGHT),
    'note'    : _s('Note',    fontSize=8.5, textColor=LIGHT, fontName='Helvetica-Oblique',
                              leading=12,   spaceBefore=2,  spaceAfter=4,
                              leftIndent=10),
    'finding' : _s('Finding', fontSize=9.5, textColor=DARK, fontName='Helvetica',
                              leading=14,   spaceBefore=3,  spaceAfter=3,
                              leftIndent=12, borderPadding=(4, 8, 4, 8),
                              backColor=BG_MID),
    'tradeoff': _s('TO',      fontSize=9.5, textColor=DARK, fontName='Helvetica',
                              leading=14,   spaceBefore=3,  spaceAfter=3,
                              leftIndent=12, borderPadding=(4, 8, 4, 8),
                              backColor=BG_LIGHT),
    'exec'    : _s('Exec',    fontSize=9.5, textColor=DARK, fontName='Helvetica',
                              leading=14.5, spaceBefore=2,  spaceAfter=3,
                              alignment=TA_JUSTIFY),
}

def P(text, style='body'):   return Paragraph(text, S[style])
def B(text):                 return Paragraph(f'&#8226; {text}', S['bullet'])
def H1(text):                return Paragraph(text, S['h1'])
def H2(text):                return Paragraph(text, S['h2'])
def H3(text):                return Paragraph(text, S['h3'])
def SP(n=6):                 return Spacer(1, n)
def HR():                    return HRFlowable(width='100%', thickness=0.5,
                                               color=RULE_CLR, spaceAfter=6)
def Callout(text):           return Paragraph(text, S['callout'])
def Finding(text):           return Paragraph(text, S['finding'])
def Note(text):              return Paragraph(text, S['note'])
def Tradeoff(text):          return Paragraph(f'<b>Trade-off:</b> {text}', S['tradeoff'])

def metric_table(rows, col_widths=None):
    data = [[Paragraph(f'<b>{r[0]}</b>', S['mono']),
             Paragraph(str(r[1]), S['mono'])] for r in rows]
    w = col_widths or [8.5*cm, 8*cm]
    t = Table(data, colWidths=w, hAlign='LEFT')
    t.setStyle(TableStyle([
        ('ROWBACKGROUNDS', (0,0), (-1,-1), [BG_LIGHT, WHITE]),
        ('FONTNAME', (0,0), (-1,-1), 'Courier'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('TEXTCOLOR', (0,0), (-1,-1), DARK),
        ('GRID', (0,0), (-1,-1), 0.3, RULE_CLR),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
    ]))
    return t

def section_table(headers, rows, col_widths=None):
    hdr_style = ParagraphStyle('TH', parent=S['mono'], textColor=WHITE,
                               fontName='Helvetica-Bold', fontSize=8.5, leading=12)
    hdr_cells = [Paragraph(f'<b>{h}</b>', hdr_style) for h in headers]
    body_rows = [[Paragraph(str(c), S['mono']) for c in r] for r in rows]
    all_rows = [hdr_cells] + body_rows
    t = Table(all_rows, colWidths=col_widths, hAlign='LEFT', repeatRows=1)
    t.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, 0), BLK),
        ('TEXTCOLOR',    (0, 0), (-1, 0), WHITE),
        ('FONTNAME',     (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE',     (0, 0), (-1,-1), 8),
        ('GRID',         (0, 0), (-1,-1), 0.3, RULE_CLR),
        ('VALIGN',       (0, 0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING',   (0, 0), (-1,-1), 3),
        ('BOTTOMPADDING',(0, 0), (-1,-1), 3),
        ('LEFTPADDING',  (0, 0), (-1,-1), 4),
        ('ROWBACKGROUNDS',(0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    return t



# =============================================================================
#  STORY
# =============================================================================
story = []

# ── Cover ──────────────────────────────────────────────────────────────────────
story += [
    SP(70),
    P('IOV Accelerometer Signal Analysis', 'title'),
    SP(6),
    P('Take-Home Exercise: Technical Report', 'subtitle'),
    SP(22),
    P('Manu Halapeth', 'author'),
    SP(4),
    P('April 2026', 'date'),
    SP(50),
    HR(),
    SP(10),
    P(
        'Complete analysis of a 3-axis accelerometer log from an IOV device: '
        '800 Hz over an 18.28-hour session, 52.66 million samples. '
        'Three parts: data cleaning and validation (Part 1), signal characterisation (Part 2), '
        'and systematic anomaly detection (Part 3). '
        'Every threshold, window size, and design decision is documented with '
        'explicit reasoning and trade-off analysis. '
        'No values are hard-coded from prior inspection — everything is derived from the data.',
        'body'),
    PageBreak(),
]

# ── Executive Summary ─────────────────────────────────────────────────────────
story += [
    H1('Executive Summary'),
    SP(6),

    H2('The Data'),
    P(
        'A single 18.28-hour acquisition session from an IOV-mounted 3-axis accelerometer '
        '(800 Hz, 52.66 million samples, iov.log_2025_10_26). '
        'The session is structurally complete: an initial 68-minute drive, a 7.19-hour '
        'uninterrupted active phase, a progressive wind-down, and a 4.92-hour overnight park. '
        'Raw firmware output with no preprocessing — separators, jitter, and timestamp '
        'anomalies are part of the signal.',
        'body'),

    SP(6),
    H2('Key Findings'),
    B(
        '<b>Z-axis is pure dynamics.</b> Only 0.7% gravitational load (89.59° from vertical). '
        'Its RMS equals its std to three decimal places. Z can be fed directly into any event '
        'detector with no orientation model, no tilt correction, and no gravity compensation. '
        'It has 3.3x the standard deviation of the X and Y axes.'),
    B(
        '<b>44.5% sample clock jitter from a software polling loop.</b> The firmware '
        'acquires on a soft poll rather than a hardware timer interrupt. This causes '
        '4.5% timestamp anomalies (monotonicity violations and duplicates) and broadens '
        'every spectral peak. One firmware change fixes all of it.'),
    B(
        '<b>A 3g peak event occurred during the calmest hour of the session.</b> '
        'At hour 3.43, when per-hour vibration intensity was at its session minimum (p95 count = 77), '
        'a 19.55 m/s² (2.99g) transient hit. Any window-based intensity metric '
        'would have completely missed it. A parallel sample-level trigger is not optional.'),
    B(
        '<b>6,019 transient events detected; two are structural near-twins.</b> '
        'Events E04 and E05 have cosine similarity 0.995 across six feature dimensions, '
        'appearing 1.92 hours apart during the continuous drive — the same physical excitation '
        'source encountered twice. E06 (1,050 ms) has 2.8x the total impulse of any other '
        'detected event despite a moderate peak.'),
    B(
        '<b>Session vibration intensity is unusually compressed.</b> '
        'Active bin-std spans only 11.9% of the median from p50 to p99. '
        'No fixed absolute threshold can cleanly separate vibration intensity tiers — '
        'session-relative percentile thresholds are required by the data structure.'),

    SP(6),
    H2('Most Important Anomaly'),
    Finding(
        'E03  |  Hour 3.43  |  19.55 m/s² (3g)  |  Kurtosis 26.0  |  250 ms\n\n'
        'The sharpest single mechanical event in 18 hours of recording, occurring when '
        'everything else in the session looks completely unremarkable. '
        'Virtually all energy concentrates in a sub-instant spike with trailing ring-down — '
        'kurtosis 26.0, the highest in the 10-event set. '
        'Peak exceeds the 2g plausibility flag threshold, occurs at the 100th population percentile '
        'on both peak magnitude and duration, and would be invisible to any window-based detector '
        'operating at a 1-minute or even 1-second granularity. '
        'Only a real-time sample-level trigger running in parallel catches it.'),

    SP(6),
    H2('Product Insights'),
    B(
        '<b>Fix the firmware clock first.</b> Replace the software polling loop with a '
        'hardware timer interrupt. This is the highest-leverage single change: '
        'it eliminates 44.5% jitter, resolves 4.5% timestamp anomalies, and makes '
        'spectral analysis reliable. Everything else in this report is built on a '
        'soft-clock foundation that should not exist in a production device.'),
    B(
        '<b>Use Z-axis only for real-time event detection.</b> '
        'It is pure dynamics with no gravity contamination, requires no orientation model, '
        'and has 3.3x the amplitude range of the lateral axes. '
        'A single-axis Z-threshold trigger is simpler, faster, and more sensitive than '
        'any multi-axis approach for vertical impact detection.'),
    B(
        '<b>Bin-std below 0.030 m/s² means motor off — no CAN bus required.</b> '
        'The overnight park sits at 0.022 m/s² (sensor noise floor); '
        'traffic stops with motor running sit at 0.063–0.085 m/s². '
        'Motor state is directly readable from the accelerometer alone, '
        'enabling standby time tracking and emissions inference without additional sensors.'),

    PageBreak(),
]

# ── Dataset selection ─────────────────────────────────────────────────────────
story += [
    H1('Dataset Selection: Why One File Out of 48'),
    SP(4),
    P(
        'The shared drive had 48 compressed log files ranging from 462 MB to 591 MB each. '
        'I picked one: '
        '<font face="Courier" size="9">iov.log_2025_10_26</font>. '
        'That choice was not arbitrary.',
        'body'),
    SP(4),
    H3('Why this session'),
    P(
        'The October 26 file contains a structurally complete 18.28-hour session: '
        'system startup, a 7.19-hour uninterrupted drive, wind-down, park, and overnight standby. '
        'That is a coherent unit of analysis with a clear beginning, middle, and end — '
        'everything needed to characterise the signal, build a detection methodology, '
        'and validate it against real events.',
        'body'),
    P(
        'Concatenating all 48 files would be a mistake. Files from different dates represent '
        'different sessions with different ambient conditions, possibly different operators, '
        'different firmware revisions, and different system states. Stitching them creates '
        'cross-session artefacts — sensor mounting angle changes, firmware clock resets — '
        'that are indistinguishable from genuine signal anomalies. '
        'You lose interpretability for the sake of volume.',
        'body'),
    B('<b>Why October 26 specifically?</b> It is the earliest available file — the cleanest '
      'baseline with no prior-session effects — and it contains a structurally complete session '
      '(verified during analysis). Later files may be partial sessions or start mid-journey. '
      'The single file also occupies 1,053 MB in memory; processing all 48 simultaneously '
      'would require ~50 GB of RAM and hours of I/O time.'),
    SP(4),
    Callout(
        'The methodology is fully generalisable. The same detect_header, clean, characterise, '
        'and detect pipeline runs unchanged on any of the other 47 files. '
        'October 26 is simply the most appropriate single-session starting point.'),
    PageBreak(),
]

# =============================================================================
#  PART 1
# =============================================================================
story += [H1('Part 1: Data Loading and Cleaning')]

story += [
    SP(4),
    H2('1.1  What the Raw File Looks Like'),
    P(
        'The source file is firmware-generated text with no preprocessing. '
        'Each data row has four comma-separated floats: '
        '<font face="Courier" size="9">acc_x, acc_y, acc_z, unix_timestamp</font> '
        '(acceleration in m/s², timestamp as Unix epoch float64). '
        'Before the data rows there is a metadata preamble of unknown length; '
        'throughout the file the firmware injects periodic structural artefacts '
        '(separator dots, blank lines); at the end is a log-rotate footer.',
        'body'),
    SP(4),
    metric_table([
        ('Total file lines',              '52,667,096'),
        ('Header lines (auto-detected)',  '25'),
        ('Valid rows loaded',             '52,660,592'),
        ('Corrupt rows',                  '6,479  (0.01230%)'),
        ('Recording duration',            '18.2841 hours'),
        ('Recording start (UTC)',         '2025-10-25  18:14:25'),
        ('Recording end (UTC)',           '2025-10-26  12:29:52'),
        ('Specified sample rate',         '800 Hz'),
        ('Derived sample rate',           '800.036 Hz  (verified match)'),
        ('Median sample interval',        '1.2500 ms'),
        ('Interval std dev',              '0.5557 ms  (44.5% of nominal)'),
        ('In-memory footprint',           '1,053 MB'),
    ]),
    SP(6),
    P(
        'Two things stand out immediately. The corrupt row count of 6,479 (0.012%) is trivial. '
        'More significant is the 44.5% timing jitter: median interval is exactly 1.25 ms '
        'as expected, but the std dev is 0.5557 ms. '
        'That is not sensor noise — it is a firmware clock running on a software polling loop '
        'instead of a hardware interrupt, and it has consequences for every spectral '
        'analysis in Part 2.',
        'body'),
]

story += [
    SP(10),
    H2('1.2  Loading Pipeline: Every Decision Explained'),

    H3('Auto-detecting the header length'),
    P(
        'The preamble length is undocumented. A forward scanner walks the file line by line '
        'and stops at the first row that parses cleanly as four floats. '
        'That line index becomes the skip count (result: 25 lines, in 0.001 seconds). '
        'Hard-coding <font face="Courier" size="9">skiprows=25</font> would silently break '
        'if the firmware ever changes the preamble length. The scanner costs milliseconds '
        'and works on all 48 files regardless of preamble length.',
        'body'),

    H3('Why the typed load fails in pandas 2.x'),
    P(
        'Passing '
        '<font face="Courier" size="9">dtype={\'acc_x\': \'float32\'}</font> '
        'directly to <font face="Courier" size="9">read_csv</font> with '
        '<font face="Courier" size="9">on_bad_lines=\'skip\'</font> '
        'raises a ValueError on the first separator dot. In pandas 2.x the C engine '
        'applies dtype conversion before the bad-line filter runs, so the dot hits '
        'the float32 cast before it can be discarded. '
        'The fix: load untyped, coerce with '
        '<font face="Courier" size="9">pd.to_numeric(errors=\'coerce\')</font>, '
        'drop NaN rows, then cast.',
        'body'),
    Tradeoff(
        'The Python engine avoids this entirely but runs 4x slower on a 52M-row file. '
        'The two-pass C-engine approach is the right balance of correctness and speed.'),

    H3('float32 for axes, float64 for timestamps'),
    P(
        'Acceleration at ±30 m/s² needs ~0.001 m/s² precision; float32 (7 decimal digits) '
        'is more than sufficient and halves the memory cost of the three axis columns. '
        'Timestamps are different: Unix epoch values in 2025 are ~1.76 billion seconds. '
        'float32 maxes at 2²⁴ = 16.7 million, so it would corrupt every inter-sample interval. '
        'float64 is mandatory for timestamps.',
        'body'),
    Tradeoff(
        'Storing timestamps as int64 microseconds would be cleaner and eliminate floating-point '
        'precision issues. The raw firmware encodes them as floats and the clock has 44.5% jitter '
        'anyway — converting to microseconds would imply precision the clock does not have.'),

    H3('Verifying the sample rate before anything else'),
    P(
        '<font face="Courier" size="9">EXPECTED_HZ = 800</font> is the only external constant '
        'in the pipeline, taken directly from the problem specification. '
        'The derived rate came back at 800.036 Hz — a pass. '
        'Running this check early surfaces a mismatch immediately rather than letting it '
        'corrupt the frequency axis of every downstream spectral analysis.',
        'body'),
]

story += [
    SP(10),
    H2('1.3  What the Corrupt Rows Actually Are'),
    P(
        'The 6,479 corrupt rows are not degraded sensor readings — they are firmware write-loop '
        'artefacts inserted between samples. That distinction drives the handling decision.',
        'body'),
    SP(4),
    section_table(
        ['Corruption Type', 'Est. Count', 'What it is'],
        [
            ['Separator dot',     '~5,800', 'Periodic flush/heartbeat marker written by firmware between samples'],
            ['Blank line',        '~600',   'File management artefact with no sensor content'],
            ['Log-rotate footer', '~79',    'Session-end marker appended at the tail of the file'],
        ],
        [4*cm, 2.8*cm, 10*cm]
    ),
    SP(4),
    Note('Categorisation used a 500,000-line bounded scan over the first ten minutes of the recording — '
         'large enough to encounter every artefact category. Counts scaled proportionally to the full file.'),
]

story += [
    SP(10),
    H2('1.4  How I Handled the Corrupt Rows'),
    P('<b>Decision: drop all 6,479.</b>', 'body'),
    SP(2),
    H3('Interpolate (rejected)'),
    P(
        'Interpolation fabricates acceleration values at positions where no measurement was taken. '
        'The separator dots sit between real samples. If any real event coincided with a separator '
        'boundary, synthesising values there would corrupt it.',
        'body'),
    H3('Flag as NaN (rejected)'),
    P(
        'Flagging keeps the index positions but marks them invalid, forcing every downstream '
        'operation (rolling windows, FFT, peak detection) to handle NaN explicitly. '
        'The complexity cost is real; the benefit is zero — these positions contain no sensor '
        'information to preserve.',
        'body'),
    H3('Drop (chosen)'),
    P(
        'Dropping is lossless here because the artefacts are outside the sample stream, '
        'not in place of samples. The post-drop effective rate is 800.036 Hz — '
        'statistically identical to spec. If dropping had created real gaps, the rate '
        'would be measurably lower.',
        'body'),
    Tradeoff(
        'If any corrupt rows had contained partial sensor data (e.g., three of four fields parseable), '
        'flagging or interpolation could be justified. In this file they do not — '
        'all corruption is structural markers with zero sensor content. The decision is unambiguous.'),
]

story += [
    SP(10),
    H2('1.5  Timestamp Problems and the 2g Check'),

    H3('1,119,928 monotonicity violations and 2,385,639 duplicate timestamps'),
    P(
        'This is 4.5% of the dataset — too large to be coincidental, too small to be '
        'a hardware failure. The most likely cause is the same software polling loop '
        'responsible for the 44.5% jitter. When the OS scheduler preempts the acquisition '
        'thread mid-loop, the next timestamp can land at or before the previous one. '
        'Or the soft clock stalls for one scheduler time-slice and two samples get the same tick. '
        'At 4.5%, this is consistent with a polling loop running near a 10 ms scheduler boundary.',
        'body'),
    P(
        'Action taken: sort by timestamp, retain duplicates.',
        'body'),
    Tradeoff(
        'Deduplication requires choosing which duplicated row to keep. Without hardware logs or '
        'a ground-truth reference there is no principled basis for that choice — both duplicated '
        'samples may represent real readings that shared a soft-clock tick. Sort-and-retain is the '
        'conservative, information-preserving choice. Downstream analysis uses windowed statistics '
        'rather than sample-by-sample differences, so it is robust to duplicates.'),

    H3('37 samples exceed the 2g plausibility ceiling'),
    P(
        'A sensor on a physical system in normal operation should not routinely exceed 2g '
        '(19.62 m/s²) on any single axis. These 37 samples were flagged rather than dropped '
        'because at this stage it is unknown whether they are saturation, corruption, or '
        'genuine extreme impacts. Part 3 confirms they are real: the Z-axis extremes of '
        '+26.95 and −22.98 m/s² correspond to actual transient events.',
        'body'),
    Tradeoff(
        'A 3g or 4g ceiling would flag fewer samples but reduce sensitivity to genuine saturation. '
        '2g was chosen as it sits well above normal operation (0–0.5g) while remaining below '
        'hard-contact impact or saturation territory. The 37 flagged samples all proved legitimate.'),
]

story += [
    SP(10),
    H2('1.6  Data Quality Summary'),
    metric_table([
        ('Axis', 'min  /  max  /  mean  /  std  (m/s²)'),
        ('acc_x', '2.658  /  16.324  /  9.398  /  0.839'),
        ('acc_y', '-10.726  /  4.286  /  -2.748  /  0.933'),
        ('acc_z', '-22.975  /  26.954  /  0.070  /  2.755'),
    ]),
    SP(6),
    P(
        'The X-axis mean of 9.399 m/s² is almost exactly g — X is pointing roughly downward, '
        'carrying most of the gravitational load. '
        'The Z-axis mean is 0.070 m/s², effectively zero: Z is nearly horizontal and carries '
        'no gravity, making it 100% dynamic content by definition. '
        'The Y-axis mean of −2.748 m/s² is persistently negative — a fixed mounting offset, '
        'not noise. Any classifier that treats Y as zero-mean will be systematically wrong '
        'from the first sample.',
        'body'),
    SP(4),
    P(
        '<b>Figures:</b> '
        '<font face="Courier" size="9">fig_signal_overview.png</font> (first 30 seconds), '
        '<font face="Courier" size="9">fig_corrupt_row_types.png</font> (corruption breakdown), '
        '<font face="Courier" size="9">fig_quality_summary.png</font> (sampling intervals and box plots).',
        'body'),
    PageBreak(),
]

# =============================================================================
#  PART 2
# =============================================================================
story += [H1('Part 2: Exploratory Signal Characterisation')]

story += [
    SP(4),
    P(
        'Part 2 re-runs the Part 1 cleaning pipeline at the top of its own notebook. '
        'This is deliberate: any notebook should run in isolation and produce correct results '
        'without hidden dependencies on prior state. The cost is ~20 seconds of reload time.',
        'body'),
]

story += [
    SP(6),
    H2('2.1  Time and Frequency Domain Visualisation'),

    H3('Visualising 52 million samples: envelope subsampling'),
    P(
        'Plotting 52M samples directly would take minutes, crash most viewers, and show nothing '
        'useful — overplotting turns the waveform into a solid black rectangle. '
        'Instead, the signal is split into 2,000 equal-width time bins. '
        'For each bin the per-axis mean, max, and min are computed; the figure plots the mean '
        'as a line and shades the min-to-max range as an envelope. '
        'This is lossless: every peak and trough across 18 hours is visible.',
        'body'),
    Tradeoff(
        'Three alternatives: (1) random subsampling at 1/100 drops a 1-sample impact event '
        'with 99% probability. (2) Fixed stride subsampling has the same peak-loss problem '
        'plus aliasing at the stride frequency. (3) Max-envelope is slightly slower but '
        'guarantees no amplitude information is lost — the only correct choice for a signal '
        'where the extremes are the point.'),

    H3('Welch PSD instead of a raw FFT'),
    P(
        'A single FFT over all 52M samples yields 26 million frequency bins at 0.000015 Hz '
        'resolution — dominated by non-stationary content from speed changes and gear shifts, '
        'producing an uninterpretable smear. '
        'Welch averages 116 overlapping 5-minute segments with a Hann window, giving '
        '0.195 Hz resolution with dramatically reduced variance.',
        'body'),
    Tradeoff(
        'Welch trades frequency resolution for variance reduction. At 0.195 Hz resolution, '
        'two peaks closer than that merge. For this signal that is acceptable: meaningful '
        'spectral features have bandwidths of at least 0.5 Hz. The variance reduction from '
        'averaging 116 segments is what makes the peaks visible — a raw periodogram '
        'of operational data buries them completely.'),
    P(
        'The PSD was computed on a 30-minute clip from hours 4.59 to 5.09, within the '
        '7.19-hour continuous drive. This clip is assumed representative of the dominant '
        'operational regime, but spectral content changes with speed and surface conditions. '
        'A full-session rolling spectrogram would be more complete.',
        'body'),
]

story += [
    SP(10),
    H2('2.2  Basic Statistics per Axis'),
    section_table(
        ['Statistic', 'acc_x', 'acc_y', 'acc_z'],
        [
            ['n samples',    '52,660,592', '52,660,592', '52,660,592'],
            ['mean (m/s²)',   '9.3984',    '-2.7477',    '0.0704'],
            ['median (m/s²)', '9.3900',   '-2.7440',    '0.0430'],
            ['std (m/s²)',    '0.8392',    '0.9325',     '2.7551'],
            ['min (m/s²)',    '2.658',     '-10.726',    '-22.975'],
            ['max (m/s²)',    '16.324',    '4.286',      '26.954'],
            ['peak-to-peak', '13.666',    '15.012',     '49.929'],
            ['RMS (m/s²)',   '9.4358',    '2.9016',     '2.7560'],
            ['skewness',     '0.016',     '0.012',      '0.013'],
            ['kurtosis',     '4.466',     '4.494',      '4.381'],
        ],
        [4.2*cm, 3.8*cm, 3.8*cm, 4.7*cm]
    ),
    SP(6),
    P(
        'The Z-axis std of 2.755 m/s² is roughly 3x that of X (0.839) and Y (0.933). '
        'Combined with its near-zero mean, Z is carrying the full vertical dynamics with '
        'nothing else mixed in — making it by far the most useful axis for event detection.',
        'body'),
    P(
        'Kurtosis values of 4.38–4.49 across all three axes are tightly clustered at '
        '48% above Gaussian (3.0). The fact that all three axes show the same elevation '
        'rules out any axis-specific sensor artefact — this is a property of the system '
        'dynamics. It is the fingerprint of moderate impulsive content: regular short '
        'sharp events layered on a broadly normal vibration background.',
        'body'),
    P(
        'Skewness near zero across all axes tells you the system encounters roughly '
        'symmetric excursions over 18 hours. Yet the vector magnitude distribution is '
        'right-skewed (mean 10.194 vs median 9.809 m/s²): impacts add to the magnitude '
        'rather than cancelling across axes, and the median is within 0.002 m/s² of '
        'standard g — confirming the most common state is the system at rest or cruising smoothly.',
        'body'),
    P(
        'One detail worth flagging: Y-axis p99 is −0.273 m/s², meaning 99% of all Y samples '
        'are negative. That is a permanent hardware mounting offset, not noise. '
        'Any model assuming zero-mean Y is wrong on every single sample.',
        'body'),
]

story += [
    SP(10),
    H2('2.3  Sensor Orientation'),

    H3('How orientation was determined without a mounting diagram'),
    P(
        'Over a complete 18-hour session with varied operation, system dynamics average to zero. '
        'What remains in the long-term per-axis mean is its static gravitational component — '
        'exactly the gravity vector in sensor coordinates, which is orientation.',
        'body'),
    metric_table([
        ('X gravity component', '+9.3986 m/s²  (95.8% of g)'),
        ('Y gravity component', '-2.7477 m/s²  (28.0% of g)'),
        ('Z gravity component', '+0.0704 m/s²  (0.7% of g)'),
        ('Recovered magnitude', '9.7923 m/s²  vs standard 9.8066 m/s²'),
        ('Error',               '0.146%  (calibration-quality accuracy)'),
        ('X inclination',       '16.30° from vertical'),
        ('Y inclination',       '73.70° from vertical'),
        ('Z inclination',       '89.59° from vertical'),
    ]),
    SP(6),
    P(
        'The 0.146% error on recovered gravity magnitude validates the approach and confirms '
        'negligible sensor bias drift over 18 hours.',
        'body'),
    P(
        'The Z inclination of 89.59° from vertical is the key result. Z carries 0.7% '
        'gravitational load — essentially perfectly horizontal. Its RMS equals its std '
        'to three decimal places, which only happens when the mean is effectively zero. '
        'Z is pure dynamics: no gravity compensation, no tilt correction, no DC removal needed. '
        'Raw Z samples can be fed directly into an event detector.',
        'body'),
    P(
        'X is the opposite: 95.8% of its signal is gravity. Using raw X for event detection '
        'means thresholding on gravity with a tiny dynamic signal on top — '
        'requiring a 9.399 m/s² subtraction that is itself sensitive to orientation changes.',
        'body'),
    Tradeoff(
        'The long-term mean approach breaks down for highly asymmetric sessions '
        '(e.g., one-way operation with more acceleration than braking). '
        'The 0.146% error confirms it succeeded here. For one-directional sessions '
        'a gyroscope or AHRS fusion would be needed — unavailable from a 3-axis '
        'accelerometer alone.'),
]

story += [
    SP(10),
    H2('2.4  Acceleration Vector Magnitude'),
    metric_table([
        ('Mean magnitude',       '10.194 m/s²  (+0.388 above g)'),
        ('Median magnitude',     '9.809 m/s²   (within 0.002 of standard g)'),
        ('Std',                  '1.061 m/s²'),
        ('Min / Max',            '3.491 / 29.355 m/s²  (peak = 2.99g)'),
        ('Samples above g+1',    '12,422,336  (23.6% of all samples)'),
        ('Samples below g-1',    '3,273,503   (6.2%)'),
        ('Session peak location', 'Hour 3.430 (the quietest active hour)'),
    ]),
    SP(6),
    P(
        'The mean is pulled above the median by a heavy right tail: a small number of '
        'high-magnitude impact events skew the distribution upward. '
        'The median at 9.809 is essentially g, confirming the most common state '
        'is the system at rest or in smooth operation.',
        'body'),
    P(
        'The peak magnitude of 29.355 m/s² (2.99g) at hour 3.43 is the single most '
        'important observation in this section. Hour 3 is the calmest lowest-activity '
        'hour in the entire session — p95 bin count of only 77 against an expected 180. '
        'A 3g peak buried in the quietest hour is exactly the failure mode that any '
        'window-based intensity detector will miss completely. '
        'This single finding drives the two-scale architecture in Part 3.',
        'body'),
]

story += [
    SP(10),
    H2('2.5  Stationary Period Detection'),

    H3('Two-gate detector'),
    P('Two conditions applied jointly to each 1-second bin:', 'body'),
    P('Gate A:  |bin_mean_magnitude - g| < 0.30 m/s²', 'mono'),
    P('Gate B:  bin_std < 0.10 m/s²', 'mono'),
    P(
        'Gate A alone is not enough: constant-speed lateral motion has mean magnitude near g '
        'but non-zero within-bin oscillation. Gate B alone is not enough: very smooth low-speed '
        'cruise could pass. Together they require both near-gravitational magnitude and '
        'near-zero vibration — only satisfied when the system is genuinely stopped.',
        'body'),
    Tradeoff(
        'Gate A proves nearly redundant in practice: Gate A passes 20,528 bins, Gate B passes '
        '20,445, and the intersection is 20,445 — identical to Gate B alone. '
        'The std threshold does all the work. For a production MCU with a tight compute budget, '
        'a single std gate gives the same result at half the cost. '
        'Gate A stays for fault tolerance on edge cases like parking on a steep hill.'),

    SP(4),
    section_table(
        ['Segment', 'Duration (s)', 'Mean std (m/s²)', 'Engine state'],
        [
            ['1 (long standby)', '17,710', '0.0222', 'Motor off, at sensor noise floor'],
            ['2 (standby)',     '1,985', '0.0259', 'Motor off'],
            ['3-5',          '103-278', '0.046-0.066', 'Likely motor off, still settling'],
            ['6-8 (brief)',    '36-60', '0.060-0.065', 'Motor likely active, brief stop'],
            ['9-15 (micro)',    '4-23', '0.063-0.085', 'Motor active, brief stops'],
        ],
        [3*cm, 3*cm, 3.5*cm, 7*cm]
    ),
    SP(6),
    P(
        'The bin-std gradient across segments is a proxy for motor state. '
        'The 4.92-hour overnight standby sits at 0.022 m/s² — the theoretical sensor noise '
        'floor at 800 Hz. The short traffic stops at 0.063–0.085 m/s² carry enough residual '
        'narrow-band vibration to indicate the motor was never switched off. '
        'The transition threshold is around 0.030 m/s²: motor state inference '
        'from accelerometer data alone, no CAN bus required.',
        'body'),
    H3('Session structure'),
    B('0 to 1.13h: initial 68-minute drive'),
    B('1.13 to 1.25h: brief stop cluster, four micro-segments totalling ~400 seconds'),
    B('1.25 to 8.44h: 7.19-hour uninterrupted drive — dominant feature of the session'),
    B('8.44h: 76-second pause, two back-to-back segments'),
    B('8.46 to 11.79h: 3.33 more hours of active operation'),
    B('11.79 to 13.25h: fragmented wind-down plus a 33-minute park'),
    B('13.37 to 18.28h: terminal 4.92-hour overnight park'),
]

story += [
    SP(10),
    H2('2.6  Trends and Recurring Patterns'),

    H3('Per-hour vibration intensity'),
    section_table(
        ['Hour', 'p95 bins', 'max std (m/s²)', 'What this tells us'],
        [
            ['0-4',  '66-85',  '1.48-1.53', 'Quiet baseline, consistent and unremarkable'],
            ['5',    '208',    '1.48',       'Something changes: p95 count jumps 2.5x'],
            ['6',    '248',    '1.58',       'Progressive climb continuing'],
            ['7',    '335',    '1.55',       'Phase 1 peak, +304% above baseline, hard discrete events'],
            ['8',    '169',    '1.47',       'Brief stop at 8.44h resets the count'],
            ['9',    '181',    '1.49',       'Second phase begins climbing again'],
            ['10',   '228',    '1.49',       'Continued build'],
            ['11',   '381',    '1.46',       'Session peak on sustained count, lower max'],
            ['12-13','falling','falling',    'Wind-down into parking'],
        ],
        [1.5*cm, 2.5*cm, 3*cm, 9.5*cm]
    ),
    SP(6),
    P(
        'Hours 0–4 are calm and consistent — the expected signature of a smooth operational '
        'phase. At hour 5 the p95 count jumps from 85 to 208 (145% increase) and keeps '
        'climbing through hours 6 and 7. The hour 7 peak is driven by max_std (1.550 m/s²): '
        'hard discrete events on an otherwise manageable surface. '
        'The brief stop at 8.44h acts as a phase boundary, after which a second ramp begins. '
        'Hour 11 peaks differently — highest sustained count (381 bins) with a lower max '
        '(1.460 m/s²) — continuous high-vibration operation rather than hard hits. '
        'The double-peak structure with transition at hour 8 points to two distinct '
        'surface or speed regimes.',
        'body'),

    H3('The intensity distribution is strikingly compressed'),
    P(
        'Active bin std: p50 = 1.231 m/s², p95 = 1.330 m/s², p99 = 1.377 m/s². '
        'The entire range from median to 99th percentile is 0.146 m/s² — 11.9% of the '
        'median value. That is unusually tight for 12 hours of varied active operation. '
        'The consequence for threshold-based systems: setting a fixed threshold at 1.0 m/s² '
        'catches everything; at 1.35 m/s² it catches almost nothing. '
        'Session-relative percentiles are not optional — they are required by the data structure.',
        'body'),

    H3('Spectral analysis: 30-minute clip, Z-axis'),
    section_table(
        ['Rank', 'Frequency (Hz)', 'Power (dB)', 'Drift std (Hz)', 'Stability'],
        [
            ['1', '52.35', '-22.49', '>1.0', 'Unstable, moves with speed'],
            ['2', '47.27', '-25.78', '>1.0', 'Unstable'],
            ['3', '23.83', '-27.61', '>1.0', 'Unstable'],
            ['4', '8.20',  '-28.78', '1.04', 'Near-stable, lowest drift in the set'],
            ['5', '31.83', '-29.99', '>1.0', 'Unstable'],
        ],
        [1.5*cm, 3*cm, 2.8*cm, 2.8*cm, 7.5*cm]
    ),
    SP(6),
    P(
        'All five peaks drift with speed: none qualifies as a fixed structural resonance. '
        'That is actually the significant result — a healthy chassis with no fatigue or '
        'bearing issues shows no stable self-excited ringing. Every peak moves as operational '
        'speed changes. The absence of stable peaks is the baseline signature.',
        'body'),
    P(
        'The 8.20 Hz peak has the lowest drift in the set and sits in the rotational component '
        'frequency band. Back-calculating operational speed (assuming a wheeled system with '
        '~0.65 m effective wheel diameter): f = v / (π × d) → v = 16.7 m/s ≈ 60 km/h. '
        'The 23.83 Hz / 47.27 Hz pair is a near-harmonic relationship (47.27 ≈ 2 × 23.83); '
        'the 52.35 Hz peak nearby could represent a chassis mode independently excited '
        'near that harmonic — a testable hypothesis on the next recording.',
        'body'),
    Note('Spectrogram covers one 30-minute window (hours 4.59–5.09). A full-session rolling '
         'spectrogram would reveal how the spectrum evolves with operational speed. '
         'The assumption that this clip represents the dominant regime is reasonable given '
         'its placement in the middle of the extended active phase, but it is still an assumption.'),
    SP(4),
    P(
        '<b>Figures:</b> fig_time_domain.png, fig_frequency_domain.png, '
        'fig_distributions.png, fig_orientation.png, fig_magnitude.png, '
        'fig_stationary.png, fig_trends_activity.png, fig_trends_spectrogram.png.',
        'body'),
    PageBreak(),
]

# =============================================================================
#  PART 3
# =============================================================================
story += [H1('Part 3: Anomaly Detection')]

story += [
    SP(4),
    P(
        'Three detection methods applied to the full 52,660,592-sample dataset. '
        'Every threshold choice, window size, normalisation method, and characterisation '
        'feature is documented with the reasoning behind it.',
        'body'),
    SP(6),
    H2('3.1  Task 1: Local Outlier Detection'),

    H3('Why "local" matters'),
    P(
        'A global threshold — say, flagging any sample where acc_z exceeds 5 m/s² — '
        'treats the same value as equally anomalous at all times. But 5 m/s² on Z '
        'during a lateral manoeuvre is entirely routine; the same value during smooth '
        'steady-state operation is genuinely anomalous. A local Z-score adapts automatically: '
        'the threshold shifts with the local signal level, solving both over-flagging '
        'and under-flagging simultaneously.',
        'body'),

    H3('Two scales because outlier means different things at different timescales'),
    P(
        'A single-scale detector forces a choice: sensitive to fast transients or '
        'sensitive to sustained deviations — not both. The 3g event at hour 3.43 lives '
        'in a single 50 ms window and is invisible at 1-second resolution. '
        'The transition anomalies at hours 1.13 and 1.21 span tens of seconds; '
        'no individual sample there is locally remarkable. '
        'Two different detection problems need two different approaches.',
        'body'),
]

story += [
    SP(6),
    H3('Scale 1: Fine detection within 1-second windows at 5-sigma'),
    P('<b>Formula:</b>', 'body'),
    P('z_fine = |x_i - window_mean| / max(window_std, NOISE_FLOOR)  >  5.0', 'mono'),
    P(
        'One-second windows (800 samples): short enough that the signal is approximately '
        'stationary within it, long enough that the within-window std is a stable variance estimate. '
        'K = 5.0 was chosen with explicit false-positive accounting:',
        'body'),
    B('Under Gaussian noise: P(|z| > 5.0) = 5.7 × 10⁻⁷ per sample'),
    B('Per 1-second window: expected false positives ≈ 0.001'),
    B('Over all 65,825 windows: ~59 expected false positive samples by chance'),
    B('Actual flagged: 2,669 unique samples — roughly 2,610 are real'),
    SP(4),
    Tradeoff(
        'K = 3.0 sigma produces ~25,000 false positives by chance — indistinguishable from '
        'real anomalies. K = 7.0 misses moderate but genuine anomalies. '
        'K = 5.0 gives a false-positive count well below the actual flagged count, '
        'so the output is dominated by real events.'),
    P(
        'The NOISE_FLOOR of 0.005 m/s² as minimum denominator prevents a specific failure: '
        'during the 4.92-hour overnight park the within-window std approaches the sensor '
        'noise floor (~0.022 m/s²). Without a floor, tiny thermal drift would inflate '
        'z-scores and flag the quiet baseline as anomalous.',
        'body'),
    SP(4),
    metric_table([
        ('acc_x fine outliers', '1,863 samples  (0.0035%)  max z = 19.4'),
        ('acc_y fine outliers', '511 samples    (0.0010%)  max z = 17.8'),
        ('acc_z fine outliers', '477 samples    (0.0009%)  max z = 25.2'),
        ('Union across axes',   '2,669 unique samples  (0.0051%)'),
        ('Expected by chance',  '~59 samples  (actual count is 45x higher)'),
    ]),
    SP(6),
    P(
        'The acc_x count being much higher than acc_z reflects X carrying 95.8% gravity '
        'with a small dynamic range. Any transient that shifts the X mean within a window '
        'produces large z-scores because the baseline std is low. '
        'This reinforces why Z is the preferred event detection axis: higher dynamic range '
        'means a higher noise floor and less spurious flagging of borderline events.',
        'body'),
]

story += [
    SP(8),
    H3('Scale 2: Coarse detection over 60-second rolling windows at 4-sigma MAD'),
    P('<b>Formula:</b>', 'body'),
    P('z_coarse = |bin_mean - rolling_median| / (1.4826 x rolling_MAD)  >  4.0', 'mono'),
    SP(4),
    H3('Why MAD and not rolling standard deviation'),
    P(
        'This is the most important single algorithmic decision in Task 1. '
        'The rolling std has a 0% breakdown point with respect to outliers: '
        'one anomalously large bin mean inflates the local std, raises the detection threshold, '
        'and masks every adjacent anomaly in the same window. '
        'You are trying to detect the exact events that break the std estimate — '
        'creating a circular failure where the most anomalous events make themselves harder to detect.',
        'body'),
    P(
        'MAD has a 50% breakdown point: half the bins in the window must be corrupted '
        'before the estimate breaks down. The 1.4826 scaling factor converts MAD to a '
        'consistent-sigma scale under Gaussian data so K = 4.0 has the same probabilistic '
        'meaning as K = 5.0 in Scale 1.',
        'body'),
    Tradeoff(
        'Other robust estimators exist (Huber M-estimator, biweight scale, trimmed std). '
        'MAD was chosen because it is simple, correct, and requires no hyperparameter tuning. '
        'Its 50% breakdown point is more than sufficient for an anomaly rate under 1%.'),
    P(
        'One implementation detail matters for correctness: the first and last 30 bins '
        'are excluded from detection results. scipy.signal.medfilt uses zero-padding '
        'at edges, artificially depressing the rolling median near session boundaries '
        'and producing false spikes there. Excluding those edge bins is a correctness requirement, '
        'not an optimisation.',
        'body'),
    SP(4),
    metric_table([
        ('acc_x coarse outliers', '45 bins   (0.068%)  max z = 6.7'),
        ('acc_y coarse outliers', '20 bins   (0.030%)  max z = 7.2'),
        ('acc_z coarse outliers', '74 bins   (0.112%)  max z = 10.4'),
        ('Union across axes',     '129 unique bins  (0.196%)'),
        ('Top anomaly',           'Hour 1.21  acc_z  z = 10.45'),
        ('Expected by chance',    '~4 bins'),
    ]),
    SP(6),
    P(
        'The top coarse anomalies cluster around hours 1.13 and 1.21 — exactly the brief '
        'stop cluster identified in Part 2. The transition from active operation to stationary '
        'shifts the Z-axis bin mean relative to its 60-second rolling context. '
        'That is a real and expected physical transition — still a genuine anomaly in the '
        'local-deviation sense, as the signal is doing something unusual relative to the '
        'surrounding minute.',
        'body'),
]

story += [
    SP(10),
    H2('3.2  Task 2: Transient Event Detection and Characterisation'),

    H3('Energy timeline: the foundation of event detection'),
    P(
        'The full 52M-sample signal is compressed into a per-window peak energy timeline. '
        'Window: 50 ms non-overlapping (40 samples). Energy metric: peak |mag − g| per window.',
        'body'),
    B('<b>Vector magnitude over any single axis:</b> the sensor orientation is arbitrary. '
      'A vertical impact mostly excites Z; a lateral one mostly excites Y; an oblique one '
      'excites all three. Any single axis misses impacts not aligned with it. '
      'Vector magnitude is orientation-independent.'),
    B('<b>Deviation from g rather than raw magnitude:</b> a stationary system has raw '
      'magnitude near g continuously. Subtracting g makes the metric zero at standby '
      'and non-zero only when something dynamic occurs.'),
    B('<b>Peak within the window rather than RMS:</b> RMS averages energy across the window. '
      'A single-sample 20 m/s² spike in a 40-sample window contributes only 1/40th of its '
      'power to the RMS. Peak preserves the maximum instantaneous amplitude.'),
    B('<b>50 ms window:</b> short enough to resolve a typical mechanical impact (20–100 ms), '
      'long enough that a single-sample glitch is not trivially dominant.'),
    Tradeoff(
        '25 ms windows give finer temporal resolution but double the timeline length and make '
        'gap-merge harder to tune. 100 ms windows would merge adjacent distinct impacts. '
        '50 ms is a standard choice for mechanical impact characterisation.'),

    H3('Session-relative threshold instead of a fixed value'),
    P(
        'The detection threshold is the 99.5th percentile of the energy distribution '
        '(6.920 m/s²). A fixed absolute threshold was explicitly rejected: '
        'the vibration intensity distribution is compressed (p50 to p99 spans 11.9% of the median), '
        'with no natural gap a fixed value could exploit. '
        'In a high-vibration session all percentiles shift upward; the same fixed value that '
        'catches meaningful events in a smooth session would miss most events in a rough one.',
        'body'),
    Tradeoff(
        'Session-relative thresholds are not directly comparable across sessions — p99.5 in '
        'a rough session selects harder events than p99.5 in a smooth one. '
        'For cross-session comparison, a two-stage approach is needed: detect with a '
        'session-relative threshold, then normalise against a deployment-level reference. '
        'Per-session analysis is the scope here; stage two is out of scope.'),

    B('<b>Gap merge at 0.5 seconds:</b> a physical impact produces primary excitation then '
      'ring-down. The ring-down may drop below threshold before the chassis finishes oscillating, '
      'creating two above-threshold runs from one physical event. '
      'Merging runs within 0.5 seconds captures this without merging genuinely distinct events.'),
    B('<b>Minimum duration 25 ms:</b> discards single-bin sensor glitches. '
      'A real physical transient produces excitation lasting at least 25 ms due to mechanical '
      'impedance. In practice this filter had no effect; all detected events were 50 ms or longer.'),
    B('<b>Maximum duration 5 seconds:</b> above-threshold energy persisting beyond 5 seconds '
      'is sustained high-vibration operation, not a transient. '
      'Conflating a 10-second rough patch with a discrete impact muddies the characterisation.'),

    SP(4),
    metric_table([
        ('Raw threshold crossings',  '6,469'),
        ('After 0.5-second gap merge', '6,019'),
        ('After duration filter',    '6,019  (no events removed)'),
        ('Duration range',           '50 ms to 1,050 ms'),
        ('Peak magnitude range',     '6.920 to 19.548 m/s²'),
    ]),
]

story += [
    SP(8),
    H3('Why diversity selection and not just the top 10 by magnitude'),
    P(
        'With 6,019 events, taking the 10 largest would give 10 near-identical high-amplitude '
        'shocks, leaving the full variety of transient types invisible: no sustained bursts, '
        'no oblique multi-axis impacts, no single-axis vertical impacts, no session-boundary '
        'events for stability checking.',
        'body'),
    P(
        'The selection algorithm fills 10 named slots in priority order: top 3 by peak '
        'magnitude, longest duration, broadest axis excitation, most single-axis isolated, '
        'earliest in session, latest in session, highest total impulse, fastest rise time. '
        'No event occupies two slots. This guarantees coverage of the full dynamic range '
        'while preserving the most extreme events.',
        'body'),
]

story += [
    SP(6),
    H3('The 10 Selected Events'),
    section_table(
        ['#', 'Time', 'Dur ms', 'Type', 'Peak m/s²', 'ptpZ', 'Breadth', 'Kurt'],
        [
            ['E01', '00:00:25', '50',   'Shock',   '6.99',  '21.46', '0.737', '12.7'],
            ['E02', '00:28:24', '50',   'Shock',   '7.15',  '12.18', '0.978', '10.2'],
            ['E03', '03:25:50', '250',  'Impulse', '19.55', '43.89', '0.765', '26.0'],
            ['E04', '05:59:09', '50',   'Shock',   '16.52', '37.18', '0.741', '13.9'],
            ['E05', '07:54:03', '50',   'Shock',   '17.13', '40.34', '0.713', '10.1'],
            ['E06', '08:19:33', '1050', 'Impulse', '8.68',  '28.61', '0.769', '12.8'],
            ['E07', '09:04:56', '50',   'Shock',   '12.23', '25.24', '0.860', '14.7'],
            ['E08', '10:06:23', '50',   'Shock',   '19.30', '39.39', '0.725', '19.8'],
            ['E09', '10:53:40', '50',   'Impulse', '8.72',  '31.12', '0.584',  '6.6'],
            ['E10', '13:21:32', '50',   'Impulse', '7.07',  '24.38', '0.690',  '6.8'],
        ],
        [1.2*cm, 2.2*cm, 1.8*cm, 1.8*cm, 2.3*cm, 1.8*cm, 2*cm, 1.5*cm]
    ),
    SP(6),
    P(
        'Nine of ten events are 50 ms; E06 at 1,050 ms is immediately anomalous by inspection. '
        'Peak magnitudes span 6.99 to 19.55 m/s² (2.8x range). Breadth spans 0.584 to 0.978: '
        'E09 is almost entirely single-axis Z; E02 has near-equal energy across all three axes. '
        'Same duration, structurally opposite axis-excitation signatures.',
        'body'),
    SP(8),
    H3('Per-Event Findings'),

    P('<b>E01: The session baseline</b>', 'h3'),
    Finding(
        '25 seconds into the 18-hour recording. Peak 6.99 m/s², 7th population percentile. '
        'Z-dominant, breadth 0.737, kurtosis 12.7. '
        'Establishes the session baseline character — 50 ms, moderate multi-axis spread, '
        'moderate kurtosis — against which all later events are implicitly compared.'),

    SP(4),
    P('<b>E02: The most oblique impact in the set</b>', 'h3'),
    Finding(
        'Breadth 0.978: closest to perfect equipartition across all three axes. '
        'ptpX = 8.85, ptpY = 7.14, ptpZ = 12.18 m/s² — only 1.7x spread between strongest '
        'and weakest axis, versus >3x Z dominance in typical events. '
        'Near-equal multi-axis excitation implies a diagonal or oblique impact direction '
        'rather than a clean vertical surface bounce.'),

    SP(4),
    P('<b>E03: The 3g event — session maximum</b>', 'h3'),
    Finding(
        'Peak 19.55 m/s² at the 100th population percentile. '
        'This is the event identified during magnitude analysis in Part 2: 2.99g at hour 3.43, '
        'the lowest-activity hour in the session. Kurtosis 26.0 — highest in the set: '
        'despite a 250 ms window, virtually all energy concentrates in a sub-instant spike '
        'with trailing ring-down. The sharpest single mechanical event in the recording, '
        'occurring when everything else looked completely unremarkable.'),

    SP(4),
    P('<b>E04 and E05: A recurring shock signature</b>', 'h3'),
    Finding(
        'E04 (peak 16.52 m/s², breadth 0.741, kurtosis 13.9) and E05 '
        '(peak 17.13 m/s², breadth 0.713, kurtosis 10.1) have cosine similarity 0.995 '
        'across all six feature dimensions. They appear 1.92 hours apart during the '
        '7.19-hour continuous drive. Two shocks this structurally similar, 2 hours apart, '
        'are not coincidence — the sensor passed the same physical trigger twice: the same '
        'surface feature, location, or a regular drivetrain cycle hitting the same excitation source.'),

    SP(4),
    P('<b>E06: A sustained vibration burst, not a discrete impact</b>', 'h3'),
    Finding(
        '1,050 ms duration: 21 consecutive 50 ms energy windows above threshold. '
        'Highest total impulse in the full 6,019-event population at 1.1995 m/s²·s. '
        'Peak 8.68 m/s² is moderate; the energy accumulates across 21 detection bins. '
        'This is a surface segment with continuously rough surface — not a discrete impact. '
        'The sustained character makes it the most structurally unusual event in the set '
        'despite having an unremarkable peak.'),

    SP(4),
    P('<b>E07: Zero rise time — already at peak on the first sample</b>', 'h3'),
    Finding(
        'Rise time 0.0 ms: peak magnitude occurs at the very first sample of the event window. '
        'The excitation was already at full intensity when the threshold was first crossed — '
        'no observable build-up phase. Combined with breadth 0.860 and multi-axis response '
        '(ptpX = 7.78, ptpY = 8.78, ptpZ = 25.24), consistent with a direct lateral or '
        'oblique impact rather than a vertical surface event, which typically shows '
        'compression build-up.'),

    SP(4),
    P('<b>E08: Highest instantaneous energy density</b>', 'h3'),
    Finding(
        'Second-highest peak at 19.30 m/s², delivered in a single 50 ms window. '
        'Instantaneous energy density: 386 m/s²/s. Compare to E03 at 19.55 m/s² over 250 ms '
        '= 78 m/s²/s — E08 delivers nearly equal peak intensity in one-fifth the time. '
        'Kurtosis 19.8 confirms an extremely spiky profile still intensifying when '
        'the 50 ms window ends.'),

    SP(4),
    P('<b>E09: The most vertically isolated event</b>', 'h3'),
    Finding(
        'Lowest breadth at 0.584. Z-axis ptpZ = 31.12 m/s²; next highest ptpX = 4.09 m/s² '
        '— a 7.6x ratio. X and Y are essentially quiescent. Contrast with E02 (breadth 0.978): '
        'the same event class (50 ms shock) with the opposite axis-excitation signature. '
        'Tight Z alignment indicates force directed almost exactly along the vertical sensor '
        'axis — a clean normal-surface impact with minimal lateral component.'),

    SP(4),
    P('<b>E10: Sensor stability confirmation</b>', 'h3'),
    Finding(
        'Latest event at hour 13.36 — 13.35 hours after E01. '
        'Peak 7.07 m/s² versus E01 at 6.99 m/s²: a 1.1% difference. '
        'Breadth 0.690 versus E01 at 0.737: delta 0.047. '
        'Statistically indistinguishable from the session opener 13 hours earlier. '
        'No evidence of sensor gain drift, baseline shift, or mounting change — '
        'the sensor is end-to-end stable across the full 18.28-hour recording.'),
]

story += [
    SP(10),
    H2('3.3  Task 3: Cross-Event Comparison and Anomaly Identification'),

    H3('Feature matrix'),
    section_table(
        ['Event', 'peak_mag', 'dur_ms', 'impulse', 'breadth', 'kurtosis', 'rise_ms'],
        [
            ['E01',  '6.989',  '50',    '0.064', '0.737', '12.69', '13.7'],
            ['E02',  '7.146',  '50',    '0.067', '0.978', '10.23', '15.0'],
            ['E03', '19.548', '250',    '0.426', '0.765', '26.04', '38.7'],
            ['E04', '16.515',  '50',    '0.103', '0.741', '13.93', '28.7'],
            ['E05', '17.134',  '50',    '0.136', '0.713', '10.14', '23.7'],
            ['E06',  '8.676', '1050',  '1.199', '0.769', '12.84', '48.7'],
            ['E07', '12.231',  '50',    '0.109', '0.860', '14.68',  '0.0'],
            ['E08', '19.299',  '50',    '0.113', '0.725', '19.83', '38.7'],
            ['E09',  '8.724',  '50',    '0.090', '0.584',  '6.61', '43.7'],
            ['E10',  '7.068',  '50',    '0.078', '0.690',  '6.75', '33.7'],
        ],
        [1.5*cm, 2.5*cm, 2*cm, 2*cm, 2*cm, 2.5*cm, 2*cm]
    ),
    SP(6),
    P(
        'Even before running an algorithm, the table is informative. E06 at 1,050 ms is '
        'the obvious outlier by inspection. The impulse column shows E06 at 1.199 vs E03 '
        'at 0.426 — almost 3x the total mechanical energy dose of the second-ranked event, '
        'despite a far lower peak. E02 and E09 sit at opposite ends of the breadth spectrum: '
        'superficially similar 50 ms shocks, mechanically quite different.',
        'body'),

    H3('Why cosine similarity over Euclidean distance'),
    P(
        'The six features have very different scales: peak_mag ranges 6.99–19.55, '
        'dur_ms ranges 50–1,050, breadth ranges 0.584–0.978. '
        'Euclidean distance would be dominated by whichever feature has the largest absolute '
        'range — peak_mag and dur_ms would drown out breadth and kurtosis. '
        'Cosine similarity normalises each event vector by its magnitude, making features '
        'contribute proportionally to their relative variation: it answers whether two events '
        'have the same shape across all features, regardless of absolute size.',
        'body'),
    metric_table([
        ('Most similar pair',    'E01 vs E02  cosine = 0.9987  (0.47 hours apart)'),
        ('Near-twin pair',       'E04 vs E05  cosine ~= 0.995  (1.92 hours apart)'),
        ('Most dissimilar pair', 'E07 vs E09  cosine = 0.7502'),
    ]),
    SP(6),
    P(
        'The E04–E05 near-twin at cosine 0.995 reinforces the per-event finding: two shocks '
        '1.92 hours apart with nearly identical profiles across six dimensions is not '
        'a statistical coincidence. E07 and E09 being the most dissimilar pair makes sense: '
        'same duration, similar peak magnitude, but opposite axis profiles and very different kurtosis.',
        'body'),

    H3('Within-group anomaly scoring'),
    P('<b>Method:</b>', 'body'),
    P('Z_ij = (T_ij - group_mean_j) / group_std_j', 'mono'),
    P('anomaly_score = sqrt( mean( Z_i squared ) )  [RMS across 6 features]', 'mono'),
    P('<b>Threshold: score above 1.0 sigma RMS = anomalous within the group.</b>', 'body'),
    SP(4),
    P(
        'Composite RMS score rather than maximum per-feature z-score was chosen deliberately. '
        'Max z-score flags any event extreme on even one feature regardless of the other five. '
        'E03 and E08 were selected precisely for their high peak magnitude — flagging them '
        '"anomalous" just because their peak_mag ranks highest would be circular. '
        'The RMS score aggregates across all six dimensions and identifies events '
        'structurally unusual across multiple features simultaneously.',
        'body'),
    SP(4),
    section_table(
        ['Event', 'Anomaly Score', 'Primary dimension', 'z-score', 'Flag'],
        [
            ['E01', '0.607', 'kurtosis',  '+0.22',  ''],
            ['E02', '1.133', 'breadth',   '+2.24',  'ANOMALOUS'],
            ['E03', '1.159', 'kurtosis',  '+2.26',  'ANOMALOUS'],
            ['E04', '0.694', 'peak_mag',  '+0.58',  ''],
            ['E05', '0.671', 'peak_mag',  '+0.64',  ''],
            ['E06', '1.795', 'dur_ms',    '+2.94',  'ANOMALOUS (highest)'],
            ['E07', '0.731', 'rise_ms',   '-1.12',  ''],
            ['E08', '0.856', 'kurtosis',  '+1.19',  ''],
            ['E09', '1.038', 'breadth',   '-1.74',  'ANOMALOUS'],
            ['E10', '0.557', 'rise_ms',   '-0.67',  ''],
        ],
        [1.5*cm, 2.8*cm, 3.5*cm, 2.5*cm, 4*cm]
    ),
    SP(6),
    P(
        'Four events are anomalous within the group. E06 has the highest score by a '
        'significant margin (1.795): duration 1,050 ms is 2.94 standard deviations above '
        'the group mean of 170 ms. Nine of the ten events are 50 ms shocks; E06 is simply '
        'a different kind of event — not bigger, but longer, and that distinction '
        'carries real physical meaning.',
        'body'),
    P(
        'E03 is anomalous on kurtosis at +2.26 sigma. Despite being selected for peak '
        'magnitude, what makes it structurally unusual is the shape of energy distribution: '
        'a single sub-instant spike concentrated in a way none of the other events match. '
        'E02 and E09 are anomalous on breadth from opposite directions — E02 at +2.24 sigma '
        'with near-perfect tri-axial equipartition; E09 at −1.74 sigma with extreme '
        'single-axis Z dominance. Same duration, furthest apart structurally.',
        'body'),

    H3('Population context'),
    section_table(
        ['Event', 'Peak percentile', 'Duration percentile', 'Impulse percentile'],
        [
            ['E01',  '7th',    '0th',  '7th'],
            ['E02', '14th',    '0th', '10th'],
            ['E03', '100th',  '98th', '98th'],
            ['E04',  '96th',   '0th', '57th'],
            ['E05',  '97th',   '0th', '74th'],
            ['E06',  '40th',  '99th', '100th'],
            ['E07',  '77th',   '0th', '60th'],
            ['E08',  '99th',   '0th', '61st'],
            ['E09',  '41st',   '0th', '36th'],
            ['E10',  '12th',   '0th', '21st'],
        ],
        [2*cm, 3.5*cm, 4*cm, 4*cm]
    ),
    SP(6),
    P(
        'The 10 events span the 7th to 100th population percentile on peak magnitude and '
        '0th to 99th on duration — confirming the diversity selection covered the full '
        'dynamic range of the 6,019-event session. E06 sitting at the 100th impulse percentile '
        'despite the 40th peak percentile is the clearest illustration of why impulse matters: '
        'it is a completely independent axis of severity from peak alone.',
        'body'),
    PageBreak(),
]

story += [
    H1('Limitations, Assumptions, and Product Insights'),
    SP(4),
    H2('Limitations'),
    B('<b>44.5% sample clock jitter.</b> Every spectral analysis assumes uniform sampling. '
      'With 44.5% jitter, each FFT window contains phase noise that broadens spectral peaks '
      'and raises the noise floor. The "stable vs unstable" resonance classification is less '
      'reliable as a result. Fix: replace the software polling loop with a hardware timer interrupt.'),
    B('<b>4.5% timestamp anomalies.</b> Sorted and retained without deduplication. '
      'Root cause is the same polling loop. True deduplication requires hardware log correlation '
      'to determine which duplicated rows, if either, represent re-transmitted samples.'),
    B('<b>One 30-minute spectral clip.</b> A full-session rolling spectrogram would show how '
      'the spectrum evolves with speed and surface conditions. The single-clip assumption '
      'is reasonable given its placement in the middle of the extended active phase, '
      'but it is still an assumption.'),
    B('<b>No ground truth.</b> All event characterisation is intrinsic. No GPS, operator '
      'annotations, or external data to confirm the nature of E03, E06, or the E04–E05 '
      'recurring signature.'),
    B('<b>Single session, session-relative thresholds.</b> All detection thresholds adapt '
      'to this session. Broader deployment requires a separate normalisation step against '
      'a deployment-level reference.'),

    SP(8),
    H2('Product Insights'),
    B('<b>Fix the firmware clock first.</b> 44.5% jitter corrupts timestamps at the 4.5% '
      'scale and degrades every spectral result. It is the highest-leverage single change '
      'in the entire system.'),
    B('<b>Use Z-only for event detection.</b> Pure dynamics, no compensation needed, '
      '3.3x the amplitude range of the other axes. A Z-only trigger requires no orientation '
      'model and no tilt correction.'),
    B('<b>Bin-std below 0.030 m/s² reliably indicates motor off.</b> '
      'Motor state is readable from the accelerometer alone — '
      'standby time tracking and emissions inference without an additional sensor.'),
    B('<b>Deploy two parallel detectors.</b> The 3g event at hour 3.43 happened during the '
      'calmest session hour. A windowed intensity detector misses it completely. '
      'A sample-level trigger running simultaneously catches it. '
      'These are structurally independent signals that cannot substitute for each other.'),
    B('<b>Session-relative percentile thresholds are required, not optional.</b> '
      'The 11.9% spread from p50 to p99 means no fixed absolute value cleanly separates '
      'vibration intensity tiers. Normalise per device per session.'),
    B('<b>Track kurtosis as a deployment health metric.</b> Session baseline is 4.38–4.49 '
      'across all axes. If Z-axis kurtosis climbs above 6–8 on a known route without a '
      'corresponding route change, something changed: mounting wear, component condition, '
      'or surface degradation.'),

    SP(12),
    HR(),
    SP(8),

    # ── System Design / Deployment Perspective ────────────────────────────────
    H1('System Design / Deployment Perspective'),
    SP(4),
    P(
        'How this analysis translates to a production IoT system running on the device '
        'or edge server in real time.',
        'body'),
    SP(4),
    B('<b>Real-time Z-axis trigger (hardware interrupt, not polling).</b> '
      'The Z-axis carries pure dynamics — deploy a single-axis threshold comparator running on '
      'hardware timer interrupt at 800 Hz. No floating-point orientation model needed. '
      'Each Z sample is compared against a session-relative threshold computed during '
      'a warm-up window (first N minutes of the session). '
      'Triggering cost: one multiply and one compare per sample.'),
    B('<b>Dual-scale anomaly pipeline running in parallel.</b> '
      'Fine scale (1-second Z-score at 5σ) catches instantaneous spikes like E03. '
      'Coarse scale (60-second rolling MAD at 4σ) catches sustained deviations and '
      'phase transitions like hours 1.13–1.21. '
      'Neither scale can substitute for the other — they detect different physical phenomena. '
      'Both run simultaneously with shared bin-mean computation.'),
    B('<b>Noisy timestamp handling.</b> '
      'With a soft-clock, use row index as the primary sequencing key, not the timestamp. '
      'Timestamps carry inter-sample jitter of 44.5% but the row index is monotonic by construction. '
      'Relative timing (event duration, inter-event gap) should be computed from row counts '
      'multiplied by the nominal sample interval (1.25 ms), not from timestamp deltas. '
      'Wall-clock alignment can use a coarser external sync (GPS tick, NTP) rather than '
      'the firmware soft-clock.'),
    B('<b>Session-relative threshold calibration.</b> '
      'On session start, buffer the first 60 seconds of data to compute a baseline '
      'p99.5 energy estimate. Use this as the event detection threshold for the remainder '
      'of the session. On highly variable routes, recalibrate every 30 minutes using a '
      'rolling history window. Store the per-session threshold alongside the event log '
      'for cross-session normalisation.'),
    B('<b>Motor state inference from bin-std.</b> '
      'Compute bin-std over non-overlapping 1-second windows in real time. '
      'Transition below 0.030 m/s² → motor-off event; above 0.060 m/s² → motor-on. '
      'This state machine feeds standby time counters and emissions inference without '
      'any additional sensor or CAN bus access.'),
    B('<b>Cross-session normalisation layer.</b> '
      'Each device maintains a rolling reference table of per-session p50 and p99 '
      'energy values. When comparing events across sessions or devices, '
      'normalise peak magnitude by (session_p99 − session_p50) to produce a dimensionless '
      'severity score that is comparable regardless of route roughness.'),
    B('<b>Kurtosis health monitor (background process).</b> '
      'Compute per-axis kurtosis over 5-minute rolling windows. '
      'Baseline for this device: 4.38–4.49. '
      'Alert threshold: Z-axis kurtosis sustained above 6.0 for more than two consecutive '
      'windows on a known route. This catches mounting degradation or component wear '
      'before it manifests as catastrophic failure.'),

    SP(12),
    HR(),
    SP(6),
    P('Manu Halapeth  ·  April 2026', 'caption'),
    P('IOV Accelerometer Signal Analysis  ·  Take-Home Exercise', 'caption'),
]

#  BUILD
# =============================================================================
OUT_PATH = '/Users/manuhalapeth/Knaq/ManuHalapeth_Knaq_TakeHome.pdf'

def _on_page(canvas, doc):
    if doc.page == 1:
        return
    canvas.saveState()
    w, h = A4
    canvas.setStrokeColor(RULE_CLR)
    canvas.setLineWidth(0.4)
    canvas.line(L_MAR, h - T_MAR + 8, w - R_MAR, h - T_MAR + 8)
    canvas.setFont('Helvetica', 8)
    canvas.setFillColor(LIGHT)
    canvas.drawString(L_MAR, h - T_MAR + 12, 'IOV Accelerometer Signal Analysis  ·  Manu Halapeth')
    canvas.drawRightString(w - R_MAR, h - T_MAR + 12, 'Take-Home Exercise')
    canvas.line(L_MAR, B_MAR - 8, w - R_MAR, B_MAR - 8)
    canvas.drawCentredString(w / 2, B_MAR - 18, f'Page {doc.page}')
    canvas.restoreState()

doc = SimpleDocTemplate(
    OUT_PATH,
    pagesize=A4,
    leftMargin=L_MAR, rightMargin=R_MAR,
    topMargin=T_MAR,  bottomMargin=B_MAR,
    title='IOV Accelerometer Signal Analysis Take-Home Exercise',
    author='Manu Halapeth',
)

doc.build(story, onFirstPage=_on_page, onLaterPages=_on_page)
print(f'PDF written  →  {OUT_PATH}')
print(f'File size    :  {os.path.getsize(OUT_PATH) / 1024:.0f} KB')
