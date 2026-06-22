import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction
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

    world_file = os.path.join(
        pkg_drok_gazebo,
        'worlds',
        'flipper_test.world'
    )

    # URDF 파일 내용을 robot_state_publisher에 전달
    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    # Gazebo 실행
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(gazebo_launch),
        launch_arguments={
            'world': world_file,
            'verbose': 'true'
        }.items()
    )

    # TF / robot_description 발행
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

    # base_link -> base_footprint static TF
    static_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='tf_footprint_base',
        arguments=[
            '--x', '0',
            '--y', '0',
            '--z', '0',
            '--roll', '0',
            '--pitch', '0',
            '--yaw', '0',
            '--frame-id', 'base_link',
            '--child-frame-id', 'base_footprint'
        ],
        output='screen'
    )

    # Gazebo에 로봇 spawn
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_model',
        arguments=[
            '-file', urdf_file,
            '-entity', 'drok_gazebo',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.25',
            '-Y', '0.0'
        ],
        output='screen'
    )

    # joint_states 발행
    joint_state_broadcaster_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'joint_state_broadcaster',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    # 플리퍼 effort trajectory controller
    flipper_position_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'flipper_position_controller',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    # Gazebo spawn 및 gazebo_ros2_control 초기화 후 controller 실행
    delayed_controller_spawners = TimerAction(
        period=7.0,
        actions=[
            joint_state_broadcaster_spawner,
            flipper_position_controller_spawner,
        ]
    )

    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        static_tf,
        spawn_robot,
        delayed_controller_spawners,
    ])
