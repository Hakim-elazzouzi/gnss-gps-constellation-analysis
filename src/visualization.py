# ─────────────────────────────────────────────
# Plot 1: All GPS Pseudorange Arcs
# ─────────────────────────────────────────────
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np

def plot_all_pseudorange(obs, pr_code, gps_sats):
    """
    Visualizes pseudorange evolution for all GPS satellites.

    Each curve represents one satellite's range evolution over 24 hours,
    showing rise, zenith passage, and setting geometry.
    """
    # Build a colour palette for all GPS satellites
    # Using a qualitative colormap so satellites are easily distinguishable

    n_sats = len(gps_sats)
    palette = plt.cm.tab20(np.linspace(0, 1, n_sats))
    sat_colors = {sat: palette[i] for i, sat in enumerate(gps_sats)}
    
    # Figure
    fig, ax = plt.subplots(figsize=(16, 7), facecolor="#0d1117")
    ax.set_facecolor("#111827")
    ax.set_title(
        f'All GPS Satellites — Pseudorange ({pr_code}) | AUCK00NZL | 2026-01-01\n'
        f'Each curve is one satellite | {n_sats} satellites tracked over 24 hours',
        fontsize=13, fontweight='bold', color="#ffffff"
    )
    # Plot one arc per GPS satellite

    plotted = []
    
    for sat in gps_sats:
        try:
            pr = obs[pr_code].sel(sv=sat).to_series().dropna()
    
            if len(pr) < 5:   # skip satellites with almost no data
                continue
            ax.plot(pr.index, pr.values / 1e6, lw=1.4, alpha=0.85, color=sat_colors[sat], label=sat)
            plotted.append(sat)

        except Exception as e:
        print(f"   Skipped {sat}: {e}")

    # Axes formatting

    ax.set_ylabel('Pseudorange [Mm = million metres]', fontsize=11, color="#aaaaaa")
    ax.set_xlabel('UTC Time (HH:MM)', fontsize=11, color="#aaaaaa")
      
    ax.tick_params(colors="#aaaaaa")
    ax.grid(True, color="#222222", linewidth=0.5)
      
    for spine in ax.spines.values():
      spine.set_edgecolor("#333333")
      
    # Time axis
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=30, color="#aaaaaa")
      
    # Legend (compact, 4 columns)
    legend = ax.legend(ncol=4, fontsize=8,loc='upper right',framealpha=0.3,facecolor="#1a1a2e",edgecolor="#444444")
      for text in legend.get_texts():
          text.set_color("white")
      
    plt.tight_layout()
    plt.savefig('plot1_all_gps_pseudorange.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.show()
# ──────────────────────────────────────────────────────────────
# Plot 2: Full GPS SNR Heatmap (Satellite Availability)
# ──────────────────────────────────────────────────────────────
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LinearSegmentedColormap
import numpy as np

def plot_snr_heatmap(snr_df, snr_matrix, gps_sats):
    """
    Displays full GPS constellation SNR heatmap.

    Each row represents one satellite, showing signal strength variations
    over time and visibility gaps due to geometry or obstruction.
    """
    gnss_cmap = LinearSegmentedColormap.from_list(
        "gnss_snr",
        [
            "#0d1117",  # background / no data
            "#1a0533",  # deep purple (very weak signal)
            "#2c3e8c",  # blue (low signal)
            "#0099cc",  # cyan (moderate signal)
            "#00e676",  # green (good signal)
            "#ffeb3b",  # yellow (strong signal)
            "#ff6f00",  # orange (excellent / saturation)
        ],
        N=256
    )
    # Figure

    fig, ax = plt.subplots(figsize=(16, 8), facecolor="#0d1117")
    ax.set_facecolor("#0d1117")
    
    im = ax.pcolormesh(
        snr_df.index,         # x-axis: time
        range(len(gps_sats)), # y-axis: satellite index
        snr_matrix_display,   # colour data
        cmap=gnss_cmap,
        vmin=15,
        vmax=55,
        shading='auto'
    )
    # Colorbar

    cbar = plt.colorbar(im, ax=ax, pad=0.01)
    cbar.set_label('SNR [dB-Hz]', color="#e0e0e0", fontsize=11)
    cbar.ax.yaxis.set_tick_params(color="#aaaaaa")
    plt.setp(cbar.ax.get_yticklabels(), color="#aaaaaa")
    
    # Add quality reference labels to colorbar
    cbar.ax.axhline(25, color='#F44336', lw=1.5, linestyle='--')
    cbar.ax.axhline(35, color='#4CAF50', lw=1.5, linestyle='--')
    
    # Y axis — satellite PRN labels
    
    ax.set_yticks(range(len(gps_sats)))
    ax.set_yticklabels(gps_sats, fontsize=9, color="#e0e0e0")
    
    # Titles and labels
    
    ax.set_title(
        f'GPS Signal-to-Noise Ratio Heatmap — All {len(gps_sats)} Satellites\n'
        'AUCK00NZL | Auckland, New Zealand | 2026-01-01 | 30-sec sampling',
        fontsize=13, fontweight='bold', color="#ffffff"
    )
    
    ax.set_xlabel('UTC Time (HH:MM)', fontsize=11, color="#e0e0e0")
    ax.set_ylabel('GPS Satellite (PRN)', fontsize=11, color="#e0e0e0")
    
    # Time axis formatting
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=30, color="#aaaaaa")
    ax.tick_params(axis='y', colors="#aaaaaa")
    
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")
    
    plt.tight_layout()
    plt.savefig('plot2_gps_snr_heatmap.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.show()

# ──────────────────────────────────────────────────────────────
# Plot 3: Satellite Availability
# ──────────────────────────────────────────────────────────────
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_availability(gps_count, n_sats):
    """
    Visualizes number of GPS satellites visible over time.

    Shows system-level GNSS availability and redundancy, including
    minimum positioning threshold (4 satellites).
    """
    fig, ax = plt.subplots(figsize=(14, 4), facecolor="#0d1117")
    ax.set_facecolor("#111827")
    
    ax.plot(gps_count.index, gps_count.values, color="#2196F3", lw=1.5, label='GPS satellites tracked')
    ax.fill_between(gps_count.index, gps_count.values, color="#2196F3", alpha=0.2)
    
    # Minimum needed for positioning
    ax.axhline(4, color="#F44336", ls='--', lw=1.2, label='Min for positioning (4 sats)')
    ax.axhline(gps_count.mean(), color="#FFEB3B", ls='--', lw=1.2, label=f'Mean: {gps_count.mean():.1f} sats')
    
    ax.set_ylabel('GPS Satellites Tracked', color="#aaaaaa", fontsize=11)
    ax.set_xlabel('UTC Time (HH:MM)', color="#aaaaaa", fontsize=11)
    ax.set_title(
        'GPS Satellite Availability Over 24 Hours | AUCK00NZL | 2026-01-01',
        fontsize=12, fontweight='bold', color="#ffffff"
    )
    
    ax.set_ylim(0, n_sats + 2)
    ax.tick_params(colors="#aaaaaa")
    ax.grid(True, color="#222222", linewidth=0.5)
    
    for spine in ax.spines.values():
        spine.set_edgecolor("#333333")
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    ax.xaxis.set_major_locator(mdates.HourLocator(interval=2))
    plt.xticks(rotation=30, color="#aaaaaa")
    
    legend = ax.legend(fontsize=9, framealpha=0.3, facecolor="#1a1a2e", edgecolor="#444444")
    for text in legend.get_texts():
        text.set_color("white")
    
    plt.tight_layout()
    plt.savefig('plot3_gps_availability.png', dpi=150, bbox_inches='tight', facecolor=fig.get_facecolor())
    plt.show()
