from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction, DeclareLaunchArgument, RegisterEventHandler
from launch.launch_description_sources import AnyLaunchDescriptionSource
from launch_ros.actions import PushRosNamespace
from launch.substitutions import PathJoinSubstitution, LaunchConfiguration
from launch.actions import GroupAction
from launch.event_handlers import OnProcessStart
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    common_sensor_launch = get_package_share_directory('common_sensor_launch')
    velodyne_launch = PathJoinSubstitution([common_sensor_launch, 'launch', 'velodyne_VLP16.launch.xml'])

    # Declare the launch arguments
    launch_driver_arg = DeclareLaunchArgument(
        'launch_driver',
        default_value='true',
        description='Whether to launch the driver'
    )
    
    vehicle_mirror_param_file_arg = DeclareLaunchArgument(
        'vehicle_mirror_param_file',
        description='Path to vehicle mirror parameter file'
    )
    
    pointcloud_container_name_arg = DeclareLaunchArgument(
        'pointcloud_container_name',
        description='Name of the pointcloud container'
    )

    # Update base_args to use LaunchConfiguration
    base_args = {
        'max_range': '250.0',
        'scan_phase': '300.0',
        'launch_driver': LaunchConfiguration('launch_driver'),
        'vehicle_mirror_param_file': LaunchConfiguration('vehicle_mirror_param_file'),
        'container_name': LaunchConfiguration('pointcloud_container_name'),
    }

    # Top LiDAR
    top_lidar = GroupAction([
        PushRosNamespace('lidar'),
        PushRosNamespace('top'),
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(velodyne_launch),
            launch_arguments={
                **base_args,
                'sensor_frame': 'velodyne_top',
                'sensor_ip': '192.168.1.201',
                'host_ip': '192.168.1.106',
                'data_port': '2367',
                'cloud_min_angle': '0',
                'cloud_max_angle': '360',
            }.items()
        )
    ])

    # Left LiDAR with 2-second delay
    left_lidar = GroupAction([
        PushRosNamespace('lidar'),
        PushRosNamespace('left'),
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(velodyne_launch),
            launch_arguments={
                **base_args,
                'sensor_frame': 'velodyne_left',
                'sensor_ip': '192.168.1.201',
                'host_ip': '192.168.1.107',
                'data_port': '2369',
                'cloud_min_angle': '190',
                'cloud_max_angle': '90',
            }.items()
        )
    ])

    # Right LiDAR with 2-second delay
    right_lidar = GroupAction([
        PushRosNamespace('lidar'),
        PushRosNamespace('right'),
        IncludeLaunchDescription(
            AnyLaunchDescriptionSource(velodyne_launch),
            launch_arguments={
                **base_args,
                'sensor_frame': 'velodyne_right',
                'sensor_ip': '192.168.1.201',
                'host_ip': '192.168.1.105',
                'data_port': '2368',
                'cloud_min_angle': '270',
                'cloud_max_angle': '170',
            }.items()
        )
    ])

    return LaunchDescription([
        launch_driver_arg,
        vehicle_mirror_param_file_arg,
        pointcloud_container_name_arg,
        top_lidar,
        RegisterEventHandler(
            OnProcessStart(
                target_action=top_lidar,
                on_start=[left_lidar],
            )
        ),
        RegisterEventHandler(
            OnProcessStart(
                target_action=left_lidar,
                on_start=[right_lidar],
            )
        ),

        # left_lidar,
        # right_lidar,
    ])
