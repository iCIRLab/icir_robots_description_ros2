# 조립된 모바일 매니퓰레이터(Husky + Panda + 그리퍼) RViz 뷰어.
#   ros2 launch icir_panda_husky_description view_robot.launch.py            # 기본: 2f_85(실기)
#   ros2 launch icir_panda_husky_description view_robot.launch.py gripper:=hand
# 그리퍼: 2f_85 (Robotiq, 실기) | hand (Panda hand, 시뮬)
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import (Command, FindExecutable, LaunchConfiguration,
                                   PathJoinSubstitution, TextSubstitution)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('icir_panda_husky_description')
    gripper = LaunchConfiguration('gripper')
    gui = LaunchConfiguration('gui')
    rviz_cfg = PathJoinSubstitution([pkg, 'rviz', 'view_robot.rviz'])

    # RViz 표시 모델 = <share>/robots/husky_panda_<gripper>_rviz_ns1.urdf
    #   (ROS1 launch가 robot_description으로 로드하던 그 파일. 4바퀴 포함.
    #    제어 모델 husky_panda_<gripper>.urdf 는 단순화되어 앞 2바퀴만 있음)
    robot_description = {'robot_description': ParameterValue(Command([
        FindExecutable(name='xacro'), ' ',
        pkg, TextSubstitution(text='/robots/husky_panda_'),
        gripper, TextSubstitution(text='_rviz_ns1.urdf'),
    ]), value_type=str)}

    return LaunchDescription([
        DeclareLaunchArgument('gripper', default_value='2f_85',
                              description='2f_85 (Robotiq, 실기) | hand (Panda hand, 시뮬)'),
        DeclareLaunchArgument('gui', default_value='true',
                              description='joint_state_publisher GUI 슬라이더 사용 여부'),

        Node(package='robot_state_publisher', executable='robot_state_publisher',
             output='screen', parameters=[robot_description]),

        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             condition=IfCondition(gui)),
        Node(package='joint_state_publisher', executable='joint_state_publisher',
             condition=UnlessCondition(gui)),

        Node(package='rviz2', executable='rviz2', name='rviz2',
             arguments=['-d', rviz_cfg]),
    ])
