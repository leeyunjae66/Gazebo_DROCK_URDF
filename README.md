# Gazebo_DROCK_URDF

ROS 2 Humble and Gazebo Classic simulation package for the **DROK_CK tracked robot**.

This repository contains the URDF model, mesh files, Gazebo configuration, and launch files required to spawn and control the DROK_CK robot in a Gazebo simulation environment.

## Overview

The purpose of this package is to simulate a tracked mobile robot in Gazebo and test robot control pipelines before applying them to the real robot platform.

The robot model includes:

* `base_link`
* Front right track wheel: `FR`
* Front left track wheel: `FL`
* Back right track wheel: `BR`
* Back left track wheel: `BL`
* Continuous wheel joints for track-style motion
* Simplified collision geometry for Gazebo simulation
* Gazebo friction parameters for tracked-robot behavior

## Development Environment

This package was developed and tested with:

* Ubuntu 22.04
* ROS 2 Humble
* Gazebo Classic 11
* Colcon build system

## Package Structure

```bash
drok_gazebo/
├── CMakeLists.txt
├── package.xml
├── launch/
│   └── *.launch.py
├── urdf/
│   └── drok_gazebo.urdf
├── meshes/
│   ├── base_link.stl
│   ├── FR.stl
│   ├── FL.stl
│   ├── BR.stl
│   └── BL.stl
├── config/
│   └── *.yaml
└── worlds/
    └── *.world
```

## Installation

Move to your ROS 2 workspace:

```bash
cd ~/yunjae/Gazebo/DROK_CK
```

Build the package:

```bash
colcon build --packages-select drok_gazebo
```

Source the workspace:

```bash
source install/setup.bash
```

If needed, also source ROS 2 Humble:

```bash
source /opt/ros/humble/setup.bash
```

## Run Simulation

Launch Gazebo with the DROK_CK robot:

```bash
ros2 launch drok_gazebo <launch_file_name>.launch.py
```

Replace `<launch_file_name>` with the actual launch file name in the `launch/` directory.

Example:

```bash
ros2 launch drok_gazebo drok_gazebo.launch.py
```

## Robot Model

The main URDF file is located at:

```bash
urdf/drok_gazebo.urdf
```

The robot uses four continuous joints:

```bash
FR_JOINT
FL_JOINT
BR_JOINT
BL_JOINT
```

Each joint is connected to a cylindrical collision model to approximate the contact behavior between the track wheels and the ground.

## Control

The robot can be controlled through ROS 2 control commands or custom velocity command nodes.

Example command topic:

```bash
/track_velocity_controller/commands
```

Example command:

```bash
ros2 topic pub -r 10 /track_velocity_controller/commands std_msgs/msg/Float64MultiArray "{data: [-5.0, 5.0, -5.0, 5.0]}"
```

The command order should match the controller joint order defined in the controller configuration file.

Example joint order:

```yaml
joints:
  - FR_JOINT
  - FL_JOINT
  - BR_JOINT
  - BL_JOINT
```

## Friction Tuning

Gazebo friction parameters are important for tracked robot simulation.

Example Gazebo surface parameters:

```xml
<surface>
  <friction>
    <ode>
      <mu>1.0</mu>
      <mu2>1.0</mu2>
      <fdir1>1 0 0</fdir1>
    </ode>
  </friction>
</surface>
```

Parameter meaning:

* `mu`: friction coefficient in the primary direction
* `mu2`: friction coefficient in the secondary direction
* `fdir1`: primary friction direction in the link frame

For more aggressive turning behavior, tune the friction values and motor effort limits together.

## Useful Commands

Check available topics:

```bash
ros2 topic list
```

Check controller command topic:

```bash
ros2 topic info /track_velocity_controller/commands
```

Check joint states:

```bash
ros2 topic echo /joint_states
```

Build again after modifying URDF or launch files:

```bash
colcon build --packages-select drok_gazebo
source install/setup.bash
```

## Troubleshooting

### Robot is spawned but does not move

Check the following:

1. The controller is loaded correctly.
2. The joint names in the URDF and controller YAML match exactly.
3. The command topic is being published.
4. The command data order matches the controller joint order.
5. The wheel collision geometry touches the ground.
6. The effort and velocity limits are large enough.

### Robot is spawned but not visible

Check the following:

1. Mesh file paths are correct.
2. STL files exist in the `meshes/` directory.
3. The robot is not spawned below the ground.
4. Collision and visual origins are correctly defined.

### Robot slips too much

Increase ground friction or wheel friction:

```xml
<mu>2.0</mu>
<mu2>2.0</mu2>
```

If the robot becomes hard to rotate, reduce lateral friction or tune `fdir1`.

## Author

Developed by **Yunjae Lee**
Kookmin University, Mechanical Engineering

## Repository

```bash
https://github.com/leeyunjae66/Gazebo_DROCK_URDF
```
