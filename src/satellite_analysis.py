def get_gps_satellites(obs):
    """
    Extracts and sorts GPS satellites from multi-GNSS RINEX dataset.

    Filters PRNs starting with 'G' and returns ordered list for analysis.
    """
    all_sv = obs.sv.values          # List all GPS satellites present in the file
    return sorted([s for s in all_sv if s.startswith("G")])

def select_observables(obs):
    """
    Determines available pseudorange and SNR observables.

    Selects standard GPS L1 observables (C1C/S1C) or fallback (C1X/S1X)
    depending on receiver configuration.
    """
    # Determine which pseudorange observable to use
    # C1C is the standard L1 C/A code pseudorange for GPS
    # C1X is an alternative for some receivers
    if "C1C" in obs.data_vars:
        pr_code = "C1C"
    elif "C1X" in obs.data_vars:
        pr_code = "C1X"
    else:
        raise ValueError("No pseudorange observable found")

    if "S1C" in obs.data_vars:
        snr_code = "S1C"
    elif "S1X" in obs.data_vars:
        snr_code = "S1X"
    else:
        raise ValueError("No SNR observable found")

    print(f"✅ Using pseudorange observable : {pr_code}")
    print(f"✅ Using SNR observable         : {snr_code}")
    print()

    return pr_code, snr_code

def compute_satellite_availability(obs, pr_code,snr_code, gps_sats):
    """
    Computes per-satellite tracking quality and signal coverage.

    Calculates number of valid epochs and SNR statistics per GPS satellite
    to evaluate visibility and tracking performance over time.
    """

    total_epochs = obs.dims['time']

    results = {}

    for sat in gps_sats:
        try:
            pr_series = obs[pr_code].sel(sv=sat).to_series()
            snr_series = obs[snr_code].sel(sv=sat).to_series()
          
            valid = pr_series.notna().sum()
            coverage: valid/total_epochs * 100
            snr_mean = snr_series.dropna().mean()

            results[sat] = {
              "valid_epochs": int(valid),
              "coverage": float(coverage),
              "snr_mean": float(snr_mean) if not np.isnan(snr_mean) else np.nan
            }
          
        except Exception:
            results[sat] = None
    return results, total_epochs
