# ROS2(Humble) 포팅: 기존 description.launch (Clearpath 스톡) 의 동등 변환.
#
# ⚠ 주의: 이 launch는 원본 그대로 외부 husky_description 의 husky.urdf.xacro 를 로드한다
#         (실제 조립체가 아닌 순수 Husky). husky_description(ROS2) 이 설치/워크스페이스에
#         있어야 실행된다 — 없으면 FindPackageShare 에서 실패. 구성 보존을 위해 그대로 변환.
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import (Command, EnvironmentVariable, FindExecutable,
                                   LaunchConfiguration, PathJoinSubstitution)
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    husky_xacro = PathJoinSubstitution(
        [FindPackageShare('husky_description'), 'urdf', 'husky.urdf.xacro'])

    robot_description = {'robot_description': ParameterValue(Command([
        FindExecutable(name='xacro'), ' ', husky_xacro,
        ' robot_namespace:=', LaunchConfiguration('robot_namespace'),
        ' laser_enabled:=', LaunchConfiguration('laser_enabled'),
        ' realsense_enabled:=', LaunchConfiguration('realsense_enabled'),
        ' urdf_extras:=', LaunchConfiguration('urdf_extras'),
    ]), value_type=str)}

    return LaunchDescription([
        DeclareLaunchArgument('robot_namespace', default_value='/'),
        DeclareLaunchArgument('laser_enabled',
                              default_value=EnvironmentVariable('HUSKY_LMS1XX_ENABLED', default_value='false')),
        DeclareLaunchArgument('realsense_enabled',
                              default_value=EnvironmentVariable('HUSKY_REALSENSE_ENABLED', default_value='false')),
        DeclareLaunchArgument('urdf_extras', default_value=''),

        Node(package='robot_state_publisher', executable='robot_state_publisher',
             output='screen', parameters=[robot_description]),
    ])
