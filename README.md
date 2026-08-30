# icir_panda_husky_description

URDF/mesh descriptions for the Panda + Husky mobile manipulator system used in the iCIR pHRI project.

## Packages

| Package | Description |
|---------|-------------|
| `icir_panda_description` | Franka Emika Panda arm (URDF, meshes, MuJoCo XML) |
| `icir_panda_husky_description` | Panda + Clearpath Husky combined model (URDF, meshes, MuJoCo XML) |
| `icir_robotiq_2f_85_description` | Robotiq 2F-85 gripper (xacro, meshes) |

## Visualize in Rviz

```bash
roslaunch icir_panda_husky_description description.launch
```

## Note

This package provides robot models only. For the full pHRI controller and usage instructions, see [icir_phri_panda_husky](https://github.com/iCIRLab/icir_phri_panda_husky).
