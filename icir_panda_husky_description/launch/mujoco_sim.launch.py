# 최소 MuJoCo(ros2_control) 구동 launch — "모델이 MuJoCo에 로딩/구동되는가" 검증용.
#   ros2 launch icir_panda_husky_description mujoco_sim.launch.py
#   ros2 launch icir_panda_husky_description mujoco_sim.launch.py headless:=true   # 창 없이(스모크 테스트)
#
# 구조(당신 Gen3 workout_simulation.launch.py 패턴): URDF에 <ros2_control> 블록을
# 문자열 주입 → mujoco_ros2_control/ros2_control_node(=MuJoCo 내장 controller_manager)
# + robot_state_publisher. 커스텀 컨트롤러(B)는 아직 없음 → 로봇은 그냥 로딩되어 서 있음.
import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node

# MJCF 액추에이터(=ros2_control 조인트) 이름. URDF가 아니라 MJCF(husky_panda_hand.xml) 기준.
MJCF_JOINTS = [
    'f_l_drive_hinge', 'f_r_drive_hinge', 'r_l_drive_hinge', 'r_r_drive_hinge',
    'panda_joint1', 'panda_joint2', 'panda_joint3', 'panda_joint4',
    'panda_joint5', 'panda_joint6', 'panda_joint7',
    'panda_finger_joint1', 'panda_finger_joint2',
]


def _setup(context, *args, **kwargs):
    desc = get_package_share_directory('icir_panda_husky_description')
    urdf_path = os.path.join(desc, 'robots', 'husky_panda_hand.urdf')
    scene_path = os.path.join(desc, 'robots', 'mujoco_simulation_phri.xml')
    headless = LaunchConfiguration('headless').perform(context)

    with open(urdf_path) as f:
        robot_desc = f.read()

    joint_xml = '\n'.join(
        f'''    <joint name="{j}">
      <command_interface name="effort"/>
      <state_interface name="position"/>
      <state_interface name="velocity"/>
      <state_interface name="effort"/>
    </joint>''' for j in MJCF_JOINTS)

    ros2_control_block = f'''
<ros2_control name="MujocoSystem" type="system">
  <hardware>
    <plugin>mujoco_ros2_control/MujocoSystemInterface</plugin>
    <param name="mujoco_model">{scene_path}</param>
    <param name="headless">{headless}</param>
  </hardware>
{joint_xml}
</ros2_control>
'''
    robot_desc = robot_desc.replace('</robot>', ros2_control_block + '</robot>')

    return [
        Node(package='robot_state_publisher', executable='robot_state_publisher',
             output='screen', parameters=[{'robot_description': robot_desc}]),
        Node(package='mujoco_ros2_control', executable='ros2_control_node',
             output='screen',
             parameters=[
                 {'use_sim_time': True},
                 {'robot_description': robot_desc},
                 {'update_rate': 1000},
                 {'mujoco_plugins.mujoco_ros_interface.type':
                  'mujoco_ros2_control_plugins/MujocoRosInterfacePlugin'},
             ],
             remappings=[('~/robot_description', '/robot_description')]),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('headless', default_value='false',
                              description='true면 MuJoCo 창 없이 구동(스모크 테스트)'),
        OpaqueFunction(function=_setup),
    ])
