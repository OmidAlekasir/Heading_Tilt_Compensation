import numpy as np

### Rotation matrices ###

def Rx(roll):
    roll = np.deg2rad(roll)

    return np.array([[1, 0, 0],
                    [0, np.cos(roll), -np.sin(roll)],
                    [0, np.sin(roll),  np.cos(roll)]])

def Ry(pitch):
    pitch = np.deg2rad(pitch)

    return np.array([[ np.cos(pitch), 0, np.sin(pitch)],
                    [0, 1, 0],
                    [-np.sin(pitch), 0, np.cos(pitch)]])

def Rz(yaw):
    yaw = np.deg2rad(yaw)
    
    return np.array([[np.cos(yaw), -np.sin(yaw), 0],
                    [np.sin(yaw),  np.cos(yaw), 0],
                    [0, 0, 1]])

### Functions ###
def limit_angle(angle, unit='rad'):
    """
    Limits an angle to the range [-pi, pi] for radians or [-180, 180] for degrees.
    Supports both scalar values and NumPy arrays.
    """
    if unit == 'rad':
        return (angle + np.pi) % (2 * np.pi) - np.pi
    elif unit == 'deg':
        return (angle + 180) % 360 - 180
    else:
        raise ValueError("Unit must be 'rad' or 'deg'")