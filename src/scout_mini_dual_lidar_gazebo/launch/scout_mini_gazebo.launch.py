#!/usr/bin/env python3

import os
from pathlib import Path

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    """Launch Scout Mini in Gazebo simulator."""
    
    # Get package directories
    scout_description_dir = get_package_share_directory('scout_description')
    gazebo_ros_dir = get_package_share_directory('gazebo_ros')
    this_package_dir = get_package_share_directory('scout_mini_dual_lidar_gazebo')
    
    # Declare launch arguments
    use_sim_time_arg = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='Use simulation (Gazebo) clock'
    )
    
    # Get workspace root - world file is in project root's worlds directory
    world_file = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(this_package_dir))),
        'worlds',
        'simple_test_world.world'
    )
    
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=world_file,
        description='SDF world file'
    )
    
    x_pose_arg = DeclareLaunchArgument(
        'x_pose',
        default_value='0.0',
        description='Initial X position of robot'
    )
    
    y_pose_arg = DeclareLaunchArgument(
        'y_pose',
        default_value='0.0',
        description='Initial Y position of robot'
    )
    
    z_pose_arg = DeclareLaunchArgument(
        'z_pose',
        default_value='0.1',
        description='Initial Z position of robot (above ground)'
    )
    
    # Robot state publisher
    scout_description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(scout_description_dir, 'launch', 'scout_base_description.launch.py')
        ),
        launch_arguments={
            'use_sim_time': LaunchConfiguration('use_sim_time'),
        }.items()
    )
    
    # Start Gazebo server using gazebo_ros pkg (handles ROS plugin setup)
    start_gazebo_server_cmd = ExecuteProcess(
        cmd=['gzserver', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so',
             LaunchConfiguration('world')],
        output='screen'
    )
    
    # Start Gazebo client (GUI) - optional, may fail without X11
    start_gazebo_client_cmd = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )
    
    # Spawn Scout Mini robot in Gazebo using gazebo_ros spawn_entity service
    spawn_entity_cmd = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-entity', 'scout_mini',
            '-topic', '/robot_description',
            '-x', LaunchConfiguration('x_pose'),
            '-y', LaunchConfiguration('y_pose'),
            '-z', LaunchConfiguration('z_pose'),
        ],
        output='screen',
    )
    
    return LaunchDescription([
        use_sim_time_arg,
        world_arg,
        x_pose_arg,
        y_pose_arg,
        z_pose_arg,
        scout_description_launch,
        start_gazebo_server_cmd,
        start_gazebo_client_cmd,
        spawn_entity_cmd,
    ])
