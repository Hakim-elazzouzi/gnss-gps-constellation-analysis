import numpy as np

def build_snr_matrix(obs, snr_code, gps_sats):
    """
    Constructs SNR matrix for full constellation heatmap visualization.

    Converts GNSS SNR dataset into satellite × time matrix and replaces
    missing values with sentinel values for visualization.
    """
    # Build SNR matrix: rows = satellites, columns = time epochs
    snr_gps = obs[snr_code].sel(sv=gps_sats)  # Select GPS satellites and load their SNR
    snr_df = snr_gps.to_pandas()       # Convert to pandas DataFrame: rows = time, columns = satellites

    sn_matrix = snr_df[gps_sats].T.values  # Transpose: rows = satellites, columns = time (for heatmap)

    # Replace NaN (satellite not visible) with a sentinel value
    # We use 10 dB-Hz so it shows as dark on the colormap
    snr_matrix_display = np.where(np.isnan(matrix), 10, matrix) 

    return matrix_display, snr_df
