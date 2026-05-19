def compute_gps_availability(obs, pr_code, gps_sats):
    """
    Computes number of visible GPS satellites per epoch.

    Counts valid pseudorange observations across constellation to estimate
    real-time navigation capability and coverage robustness .
    """
    # Count non-NaN pseudorange values across GPS satellites for each time step
    gps_count = obs[pr_code].sel(sv=gps_sats).count(dim="sv").to_series()
    return gps_count
