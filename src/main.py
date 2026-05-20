import matplotlib.pyplot as plt

from config import OBS_PATH, PLOT_STYLE
from rinex_loader import load_rinex
from satellite_analysis import (
    get_gps_satellites,
    select_observables,
    compute_satellite_availability
)
from snr_matrix import build_snr_matrix
from availability import compute_gps_availability
from visualization import (
    plot_all_pseudorange,
    plot_snr_heatmap,
    plot_availability
)
from reporting import (
    print_satellite_table,
    print_constellation_summary,
    print_project_summary
)

plt.rcParams.update(PLOT_STYLE)

obs, header = load_rinex(OBS_PATH)

gps_sats = get_gps_satellites(obs)

pr_code, snr_code = select_observables(obs)

# Availability stats
availability, total_epochs = compute_satellite_availability(obs, pr_code, snr_code, gps_sats)

for sat, val in availability.items():
    if val:
        print(sat, val)

# Plot 1
plot_all_pseudorange(obs, pr_code, gps_sats)

# SNR matrix
snr_matrix, snr_df = build_snr_matrix(obs, snr_code, gps_sats)

# Plot 2
plot_snr_heatmap(snr_df, snr_matrix, gps_sats)

# Availability curve
gps_count = compute_gps_availability(obs, pr_code, gps_sats)

plot_availability(gps_count, len(gps_sats))

# Statistics reporting
print_satellite_table(availability, total_epochs)

print_constellation_summary(gps_sats, gps_count)

print_project_summary()

print("✅ Project 2 completed")
