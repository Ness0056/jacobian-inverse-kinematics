# Jacobian-Based Inverse Kinematics

A robotics project exploring **forward and inverse kinematics** using
Denavit–Hartenberg parameters, Jacobian matrices, pseudo-inverse methods,
and 3D visualization with POV-Ray.

The project combines Python, C++, and POV-Ray to compute and visualize
the motion of a multi-link robotic manipulator.

## Overview

The robot is modeled using the **Denavit–Hartenberg convention**.

Homogeneous transformation matrices are used to calculate the pose of
each link, while the Jacobian is used to relate joint velocities to the
motion of the robot end-effector.

The project also explores inverse kinematics using the pseudo-inverse of
the Jacobian.

## Features

- Denavit–Hartenberg robot modeling
- Forward kinematics
- Homogeneous transformation matrices
- Jacobian matrix calculation
- Jacobian pseudo-inverse
- Inverse kinematics
- Numerical matrix inversion in C++
- Python-based kinematic calculations
- 3D visualization and animation with POV-Ray

## Technologies

- Python
- C++
- POV-Ray
- Linear Algebra
- Robot Kinematics
- Denavit–Hartenberg Convention
- Jacobian Methods

## Project Structure

```text
.
├── jcb.pov
├── jacobian_ik.py
├── inversion_matrix.cpp
├── inversion_3x3_pseudo_code
├── taula-DH
├── jacobian_checks/
├── homogenous_matrices_checks/
├── animation3.mp4
├── animation41.mp4
├── animation42.mp4
└── README.md
```

## Kinematics

The position and orientation of the robot are obtained by chaining
homogeneous transformation matrices derived from the DH parameters.

The Jacobian describes how changes in joint variables affect the motion
of the robot end-effector.

For inverse kinematics, a pseudo-inverse of the Jacobian is used to
estimate the joint changes required to move the end-effector toward a
desired target.

## Animations

### Animation 3
[▶ Watch animation 3](kinematics/animation3.mp4)

### Animation 41
[▶ Watch animation 41](kinematics/animation41.mp4)

### Animation 42
[▶ Watch animation 42](kinematics/animation42.mp4)

## Concepts Demonstrated

- Forward kinematics
- Inverse kinematics
- Coordinate transformations
- Rotation and translation matrices
- Denavit–Hartenberg parameters
- Jacobian matrices
- Matrix pseudo-inverse
- Numerical linear algebra
- 3D robot visualization

## Academic Context

This project was developed as part of university coursework involving
robotics, geometric transformations, and computational visualization.

Course-provided and third-party material retains its original attribution
where applicable.
