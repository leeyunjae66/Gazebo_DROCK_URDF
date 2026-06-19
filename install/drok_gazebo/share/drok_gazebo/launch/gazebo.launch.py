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
    # 플리퍼 초기각도는 따로 지정하지 않음
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

    # joint_state_broadcaster 자동 활성화
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

    # 궤도 바퀴 velocity controller 자동 활성화
    track_velocity_controller_spawner = Node(
        package='controller_manager',
        executable='spawner',
        arguments=[
            'track_velocity_controller',
            '--controller-manager',
            '/controller_manager'
        ],
        output='screen'
    )

    # 플리퍼 position controller 자동 활성화
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

    # Gazebo에 로봇이 spawn되고 gazebo_ros2_control/controller_manager가 뜬 뒤 controller들을 켬
    delayed_controller_spawners = TimerAction(
        period=7.0,
        actions=[
            joint_state_broadcaster_spawner,
            track_velocity_controller_spawner,
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
