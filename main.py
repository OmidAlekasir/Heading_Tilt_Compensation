import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from utils import Rx, Ry, limit_angle

if __name__ == "__main__":

    ### PREPARE DATA ###
    address = 'dataset/attitude_log.csv'
    df = pd.read_csv(address)

    # Drop rows with None (NaN) values
    df = df.dropna()

    # Prepare roll, pitch, yaw as numpy arrays
    roll = df['roll'].to_numpy()
    pitch = df['pitch'].to_numpy()
    yaw = df['yaw'].to_numpy()

    # Prepare magnetometer data as Nx3 numpy array
    mag = df[['mag_x', 'mag_y', 'mag_z']].to_numpy()

    ### COMPUTE HEADING (no compensation) ###
    yaw_mag = np.arctan2(-mag[:, 1], mag[:, 0])
    yaw_mag = np.rad2deg(yaw_mag)
    yaw_mag = limit_angle(yaw_mag, 'deg')

    ### COMPUTE HEADING (with compensation) ###
    # Apply compensation for each roll and pitch value
    mag_comp = np.zeros_like(mag)
    for i in range(len(roll)):
        mag_comp[i] = Ry(-pitch[i]) @ Rx(-roll[i]) @ mag[i]

    yaw_mag_comp = np.arctan2(-mag_comp[:, 1], mag_comp[:, 0])
    yaw_mag_comp = np.rad2deg(yaw_mag_comp)
    yaw_mag_comp = limit_angle(yaw_mag_comp, 'deg')

    ### PLOT THE RESULTS ###
    fig, axs = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

    # Subplot 1: True yaw vs. yaw without compensation
    axs[0].plot(yaw, label="Yaw (True)", color="blue")
    axs[0].plot(yaw_mag, '--', label="Yaw (No Compensation)", color="orange")
    axs[0].set_title("Yaw Comparison (No Compensation)")
    axs[0].set_ylabel("Yaw (degrees)")
    axs[0].legend()
    axs[0].grid()

    # Subplot 2: True yaw vs. yaw with compensation
    axs[1].plot(yaw, label="Yaw (True)", color="blue")
    axs[1].plot(yaw_mag_comp, label="Yaw (With Compensation)", color="green")
    axs[1].set_title("Yaw Comparison (With Compensation)")
    axs[1].set_xlabel("Index")
    axs[1].set_ylabel("Yaw (degrees)")
    axs[1].legend()
    axs[1].grid()

    plt.tight_layout()
    plt.show()