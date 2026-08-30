# ROS2(Humble) 포팅: 기존 test_2f_85_model.launch 의 동등 변환.
# Robotiq 2f-85 그리퍼 단독 시각화 (self-contained, 로컬 xacro/rviz 사용).
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import (Command, FindExecutable, LaunchConfiguration,
                                   PathJoinSubstitution)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    pkg = FindPackageShare('icir_robotiq_2f_85_description')
    model = PathJoinSubstitution([pkg, 'urdf', 'robotiq_arg2f_85_model.xacro'])
    rviz_cfg = PathJoinSubstitution([pkg, 'visualize.rviz'])

    robot_description = {
        'robot_description': ParameterValue(
            Command([FindExecutable(name='xacro'), ' ', model]), value_type=str)
    }
    gui = LaunchConfiguration('gui')

    return LaunchDescription([
        DeclareLaunchArgument('gui', default_value='true',
                              description='joint_state_publisher GUI 사용 여부'),

        Node(package='robot_state_publisher', executable='robot_state_publisher',
             output='screen', parameters=[robot_description]),

        Node(package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
             condition=IfCondition(gui)),
        Node(package='joint_state_publisher', executable='joint_state_publisher',
             condition=UnlessCondition(gui)),

        Node(package='rviz2', executable='rviz2', name='rviz2',
             arguments=['-d', rviz_cfg]),
    ])
