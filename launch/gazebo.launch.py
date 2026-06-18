import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node


def generate_launch_description():

    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    pkg_drok_gazebo = get_package_share_directory('drok_gazebo')

    gazebo_launch = os.path.join(
        pkg_gazebo_ros,
        'launch',
        'gazebo.launch.py'
    )

    urdf_file = os.path.join(
        pkg_drok_gazebo,
        'urdf',
        'drok_gazebo.urdf'
    )

    # URDF 파일 내용을 읽어서 robot_state_publisher에 robot_description으로 전달
    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    # Gazebo empty world 실행
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch)
    )

    # robot_state_publisher 실행
    # gazebo_ros2_control이 여기서 robot_description을 받아감
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[
            {
                'robot_description': robot_description,
                'use_sim_time': True
            }
        ]
    )

    # static TF: base_link -> base_footprint
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_footprint_base',
        arguments=[
            '0', '0', '0',
            '0', '0', '0',
            'base_link',
            'base_footprint'
        ]
    )

    # URDF 모델 Gazebo에 spawn
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_model',
        arguments=[
            '-file', urdf_file,
            '-entity', 'drok_gazebo'
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        static_tf,
        spawn_robot,
    ])
