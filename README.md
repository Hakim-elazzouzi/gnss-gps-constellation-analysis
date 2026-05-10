# 🛰️ Project 2 — All GPS Satellites Analysis

> **Full Fleet Pseudorange Arcs & SNR Heatmap | 24-Hour Tracking | Auckland, NZ**

---

## 📌 Overview

This project expands on Project 1 by analysing the **entire GPS satellite fleet** tracked over 24 hours from the **AUCK00NZL** geodetic reference station in Auckland, New Zealand.

Instead of one satellite, we now look at all visible GPS satellites simultaneously — giving a complete picture of the GPS constellation's geometry and signal quality over a full day.

| Plot | What It Shows |
|------|--------------|
| 📡 All GPS Pseudorange Arcs | Every satellite's range evolution overlaid — each curve is one satellite |
| 🌡️ GPS SNR Heatmap | Signal quality matrix: rows = satellites, time flows left to right |
| 📊 Availability Timeline | How many GPS satellites were tracked per epoch |

---

## 🖼️ Output Plots

### Plot 1 — All GPS Pseudorange Arcs

Multi-line plot where each coloured curve is one GPS satellite:
- **U-shaped arc** = satellite rises, passes overhead, then sets
- **Flat curve** = satellite remains high in the sky all day
- **Interrupted line** = signal loss / low elevation

### Plot 2 — GPS SNR Heatmap

Full satellite matrix:
- Each **row** = one GPS satellite (G01 to G32)
- **Columns** = time (UTC, 30-second resolution)
- **Colour** = signal strength in dB-Hz

```
Black/Dark   → satellite below horizon or blocked
Blue/Purple  → weak signal (low elevation)
Green        → good tracking (SNR > 35 dB-Hz)
Yellow/Orange → excellent signal (satellite overhead)
```

### Plot 3 — Satellite Availability Timeline

Line chart showing how many GPS satellites are tracked per epoch, with reference lines for the minimum required for positioning (4 satellites) and the daily mean.

---

## 📂 File Structure

```
project2-all-gps-satellites/
├── Outputs/
│   ├── plot1_all_gps_pseudorange.png
│   ├── plot2_gps_snr_heatmap.png
│   └── plot3_gps_availability.png
├── project2_all_gps_satellites.py      ← Main notebook (run this)
├── requirements.txt                     ← Python dependencies
├── LICENSE                              ← MIT License
└── README.md                            ← This file
```

---

## ⚙️ How to Run

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Add your RINEX file

Update the path in **Step 2** of the notebook:

```python
obs_path = "/path/to/your/file.rnx"   # ← update this
```

### 3. Run all cells

```bash
jupyter notebook project2_all_gps_satellites.ipynb
```

The notebook automatically detects all GPS satellites in your file — no manual configuration needed.

---

## 🛠️ Dependencies

| Package | Purpose |
|---------|---------|
| `georinex` | Parse RINEX 3 observation and navigation files |
| `xarray` | N-dimensional array handling (time × satellite data) |
| `pandas` | Time series manipulation and DataFrame operations |
| `numpy` | Numerical computations and matrix operations |
| `matplotlib` | Publication-quality plotting |

---

## 📡 RINEX File Format

Developed using:

```
File   : AUCK00NZL_R_20260010000_01D_30S_MO.rnx
Station: AUCK00NZL — Auckland, New Zealand (GeoNet / LINZ Network)
Format : RINEX 3.05
Date   : 2026-01-01 (Day-of-Year 001)
Rate   : 30-second sampling
```

Compatible with **any RINEX 3 observation file** from any station.

---

## 🧭 Observables Used

| Code | Description |
|------|-------------|
| `C1C` | Pseudorange on L1 C/A code [metres] |
| `C1X` | Pseudorange on L1 combined [metres] (fallback) |
| `S1C` | Signal-to-Noise Ratio on L1 C/A [dB-Hz] |
| `S1X` | Signal-to-Noise Ratio on L1 combined [dB-Hz] (fallback) |

---

## 💡 Key Concepts

**Why do pseudorange arcs have different shapes?**

Each satellite follows a different orbital track across the sky. The pseudorange reflects the geometric distance between receiver and satellite, which changes continuously as the satellite moves.

**Why is the minimum 4 satellites?**

GNSS positioning solves for 4 unknowns simultaneously: X, Y, Z coordinates + receiver clock offset. Each satellite provides one equation. You need at least as many equations as unknowns — hence a minimum of 4.

---

## 👤 Author

**Hakim El Azzouzi**  
MSc Global Navigation Satellite Systems  
Mohammed First University, Oujda, Morocco  
📧 elazzouzihakim10@gmail.com  
🔗 [linkedin.com/in/Hakim-El-Azzouzi](https://linkedin.com/in/Hakim-El-Azzouzi)  
📍 Luxembourg 🇱🇺

---

## 📜 License

This project is licensed under the **MIT License** — see [LICENSE](LICENSE) for details.

---

## 🔗 Part of the GNSS RINEX Analysis Series

| # | Project |
|---|---------|
| 1 | Single GPS Satellite — Pseudorange & SNR Heatmap |
| **2** | **All GPS Satellites — Fleet Pseudorange & SNR Heatmap** ← You are here |
| 3 | Multi-Constellation GNSS — Single Satellite per System |
| 4 | Pseudorange vs Carrier-Phase Comparison |
| 5 | Constellation Summary — Pie Chart & Histogram |
| 6 | Ionospheric Delay — Geometry-Free Combination |
| 7 | Data Quality Report |
