# Heading Tilt Compensation

## Abstract
Determining the **heading** (or **yaw**) of a device is commonly done using a **magnetometer**, a 3-axis sensor that detects the direction of the Earth's **magnetic north**. While the concept is simple, interpreting magnetometer data becomes complex when the device is rotated in three dimensions.

To achieve accurate heading measurements, magnetometer readings are combined with data from an **accelerometer**. This process, called **heading tilt compensation**, leverages the **gravity vector** from the accelerometer to correct for tilts and rotations that affect heading accuracy. The gravity vector helps align the magnetometer's output with the true horizontal plane, improving reliability.

This repository offers a step-by-step guide for calculating the correct heading, ultimately yielding the device's **attitude**—comprising **roll**, **pitch**, and **yaw**.

## Description

### Simple heading calculation (sensor is leveled)
A **magnetometer** is a sensor that measures the strength and direction of magnetic fields. It can also detect the Earth's magnetic north, enabling devices to determine their orientation. The output vector of this sensor can be defined as:

$$
M =
\begin{bmatrix}
m_x \\
m_y \\
m_z
\end{bmatrix}
$$

Calculating **heading** (yaw) is straightforward when the sensor is level. The magnetometer output of this situation is defined as follows:

$$
M_\text{level} =
\begin{bmatrix}
m_x' \\
m_y' \\
m_z'
\end{bmatrix}
$$

$$
\gamma = \text{heading} = \arctan2(m_y', m_x')
$$

While the magnetometer is level and facing the magnetic north of the Earth, the output vector is as follows:

$$
M_0 =
\begin{bmatrix}
B\cos\delta \\
0 \\
B\sin\delta
\end{bmatrix}
$$

where $\delta$ is the declination angle of the Earth's magnetic field, and $B$ represents the magnitude of the Earth's magnetic field vector. This means the magnetic force is not only pointing north but also downward due to the Earth's field inclination. However, when the device is tilted, the magnetometer axes no longer align with the Earth's horizontal plane, causing errors in heading calculation. This misalignment occurs because the sensor's coordinate system diverges from the world-frame or **NED** (North-East-Down) coordinate system.

### Tilt calculation
An accelerometer senses acceleration forces, including gravity. The sensor's output is a 3D vector as follows:

$$
G =
\begin{bmatrix}
a_x \\
a_y \\
a_z
\end{bmatrix}
$$

When stationary, its output mainly reflects the gravity vector's direction. While the accelerometer is level, its output vector is as follows:

$$
G_0 =
\begin{bmatrix}
0 \\
0 \\
g
\end{bmatrix}
$$

where $g$ is the acceleration due to gravity (approximately $9.81\,\text{m/s}^2$ on Earth).

By examining the vector of the accelerometer along each axis, roll and pitch angles can be computed.

#### Roll Calculation

The **roll** angle (rotation around the X-axis) is calculated as:

```math
\alpha = \text{roll} = \arctan2(a_y, a_z)
```

- `a_y`: acceleration along the Y-axis
- `a_z`: acceleration along the Z-axis

The `arctan2` function ensures the angle is computed correctly, even if the device is inverted.

#### Pitch Calculation

The **pitch** angle (rotation around the Y-axis) is calculated as:

```math
\beta = \text{pitch} = \arctan2(-a_x, \sqrt{a_y^2 + a_z^2})
```

- `a_x`: acceleration along the X-axis
- The denominator accounts for tilt using Y and Z components

<!-- This method maintains accuracy regardless of device orientation. -->

### Heading tilt Compensation

Accurate orientation in 3D space requires determining the **roll** and **pitch** angles, which describe rotation around the device's X and Y axes. The **gravity vector** measured by an accelerometer serves as a stable reference for these calculations. The result is that by knowing the rotation of the magnetometer sensor in the 3D space, it is possible to "derotate" the magnetometer vector to match the NED coordination system, making it level.

$$
M = RM_0
$$

wehre $R$ is the rotation matrix, describing the rotation of the sensor in the 3D space:

$$
R = R_x(\alpha) R_y(\beta) R_z(\gamma)
$$

where $\alpha$, $\beta$, and $\gamma$ are roll, pitch, and yaw, respectively. By having the roll and pitch values, it is possible to eliminate their effect on the magnetometer output vecotr, $M$.

$$
R_y(-\beta) R_x(-\alpha) M =  R_z(\gamma) M_0 = M_\text{level}
$$