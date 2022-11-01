#!/usr/bin/env python

import launch
from launch_ros.actions import Node
from launch_ros.actions import ComposableNodeContainer
from launch_ros.descriptions import ComposableNode
from ament_index_python.packages import get_package_share_directory
import os
import sys


def generate_launch_description():

    ld = launch.LaunchDescription()

    pkg_name = "octomap_server2"
    pkg_share_path = get_package_share_directory(package_name=pkg_name)

    DRONE_DEVICE_ID=os.getenv('DRONE_DEVICE_ID')

    # RPLIDAR_TOPIC = <raw | filtered>
    rplidar_topic_name = "raw"
    RPLIDAR_TOPIC = os.getenv('RPLIDAR_TOPIC')
    if not RPLIDAR_TOPIC or RPLIDAR_TOPIC == "raw":
        rplidar_topic_name = "/" + DRONE_DEVICE_ID + "/rplidar/scan"
        print('RPLIDAR: using raw scan.')
    elif RPLIDAR_TOPIC  == "filtered":
        rplidar_topic_name = "/" + DRONE_DEVICE_ID + "/rplidar/scan_filtered"
        print('RPLIDAR: using filtered scan.')
    else:
        print('ERROR: not valid RPLIDAR_TOPIC.')
        sys.exit(1)

    ld.add_action(launch.actions.DeclareLaunchArgument("debug", default_value="false"))
    ld.add_action(launch.actions.DeclareLaunchArgument("use_sim_time", default_value="false"))
    ld.add_action(launch.actions.DeclareLaunchArgument("world_frame_id", default_value="world"))
    ld.add_action(launch.actions.DeclareLaunchArgument("robot_frame_id", default_value=str(DRONE_DEVICE_ID) + "/fcu"))
    
    dbg_sub = None
    if sys.stdout.isatty():
        dbg_sub = launch.substitutions.PythonExpression(['"" if "false" == "', launch.substitutions.LaunchConfiguration("debug"), '" else "debug_ros2launch ' + os.ttyname(sys.stdout.fileno()) + '"'])

    namespace=DRONE_DEVICE_ID

    ld.add_action(ComposableNodeContainer(
        namespace='',
        name=namespace+'_octomap_server',
        package='rclcpp_components',
        executable='component_container_mt',
        composable_node_descriptions=[
            ComposableNode(
                namespace=namespace,
                name='octomap_server',
                package=pkg_name,
                plugin='octomap_server::OctomapServer',
                remappings=[
                    # subscribers
                    ('laser_scan_in', rplidar_topic_name),
                    
                    # publishers
                    ('octomap_global_binary_out', '~/octomap/global/binary'),
                    ('octomap_global_full_out', '~/octomap/global/full'),
                    ('octomap_local_binary_out', '~/octomap_binary'),
                    ('octomap_local_full_out', '~/octomap_full'),
                    
                    # service servers
                    ('reset_map_in', '~/reset'),
                ],
                parameters=[
                    pkg_share_path + '/config/params.yaml',
                    {"world_frame_id": launch.substitutions.LaunchConfiguration("world_frame_id")},
                    {"robot_frame_id": launch.substitutions.LaunchConfiguration("robot_frame_id")},
                    {"use_sim_time": launch.substitutions.LaunchConfiguration("use_sim_time")},
                ],
            ),
        ],
        output='screen',
        prefix=dbg_sub,
        parameters=[{"use_sim_time": launch.substitutions.LaunchConfiguration("use_sim_time")},],
    ))
    return ld
