import numpy as np

def print_constellation_summary(gps_sats, gps_count):
    """
    Prints overall GPS constellation availability statistics.

    Summarises how many satellites were visible during the observation
    session and evaluates positioning availability over time.
    """

    print()
    print("GPS Satellite Availability Statistics:")
    print("-" * 60)

    print(f"   Total GPS satellites in file  : {len(gps_sats)}")

    print(f"   Mean sats tracked per epoch   : "
          f"{gps_count.mean():.1f}")

    print(f"   Max sats tracked (best epoch) : "
          f"{gps_count.max()}")

    print(f"   Min sats tracked (worst epoch): "
          f"{gps_count.min()}")

    print(
        f"   Epochs with ≥ 4 GPS sats      : "
        f"{(gps_count >= 4).sum()} / {len(gps_count)} "
        f"({(gps_count >= 4).mean()*100:.1f}%)"
    )

    print()
    print("Interpretation:")
    print("   • At least 4 satellites are required for 3D GNSS positioning.")
    print("   • Higher satellite counts improve positioning geometry.")
    print("   • Drops in visibility may indicate masking or low elevation.")
    print("   • Stable visibility throughout the day indicates strong GPS coverage.")


def print_satellite_table(results, total_epochs):
    """
    Prints per-satellite tracking and signal quality statistics.

    Displays observation coverage and mean SNR for each GPS satellite.
    """

    print()
    print(f"Total epochs in file: {total_epochs}")
    print()

    print(f"{'Satellite':<12} {'Valid Epochs':>14} "
          f"{'Coverage %':>12} {'Mean SNR':>12}")

    print("-" * 56)

    for sat, r in results.items():

        if r is None:
            print(f"{sat:<12} {'Error':>14}")
            continue

        snr_mean = r["snr_mean"]

        snr_str = (
            f"{snr_mean:.1f} dB-Hz"
            if not np.isnan(snr_mean)
            else "N/A"
        )

        print(
            f"{sat:<12}"
            f"{r['valid_epochs']:>14}"
            f"{r['coverage']:>11.1f}% "
            f"{snr_str:>14}"
        )


def print_project_summary():
    """
    Prints beginner-friendly explanation of the project purpose.
    """

    print()
    print("Project Interpretation:")
    print("-" * 60)

    print("   • Each GPS satellite rises, passes overhead, then sets.")
    print("   • Pseudorange measures receiver-to-satellite distance.")
    print("   • SNR describes signal quality received by the antenna.")
    print("   • Strong SNR usually occurs when satellites are high in the sky.")
    print("   • Multiple visible satellites are essential for accurate GNSS positioning.")
