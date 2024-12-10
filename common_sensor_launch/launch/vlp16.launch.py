import os

from ament_index_python.packages import get_package_share_directory
import launch
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    launch_arguments = []

    def add_launch_arg(name: str, default_value=None, description=None):
        launch_arguments.append(
            DeclareLaunchArgument(name, default_value=default_value, description=description)
        )

    # Get calibration file path
    common_sensor_launch_share_dir = get_package_share_directory("common_sensor_launch")
    sensor_calib_fp = os.path.join(
        common_sensor_launch_share_dir,
        "config",
        "TM16.yaml",
    )

    # Declare launch arguments
    add_launch_arg("sensor_model", "VLP16", description="sensor model name")
    add_launch_arg("sensor_ip", "192.168.1.202", "device ip address")
    add_launch_arg("host_ip", "192.168.1.107", "host ip address")
    add_launch_arg("scan_phase", "300.0")
    add_launch_arg("frame_id", "velodyne_left", "frame id")
    add_launch_arg("cloud_min_angle", "190", "minimum view angle setting on device")
    add_launch_arg("cloud_max_angle", "90", "maximum view angle setting on device")
    add_launch_arg("data_port", "2369", "device data port number")
    add_launch_arg("min_range", "0.3", "minimum view range")
    add_launch_arg("max_range", "250.0", "maximum view range")
    add_launch_arg("return_mode", "Dual", "lidar return mode")
    add_launch_arg("gnss_port", "2370", "gnss port number")
    # Create the Velodyne driver node
    driver_node = Node(
        package="nebula_ros",
        executable="velodyne_hw_ros_wrapper_node",
        name="velodyne_driver_node",
        parameters=[{
            "calibration_file": sensor_calib_fp,
            "sensor_model": LaunchConfiguration("sensor_model"),
            "sensor_ip": LaunchConfiguration("sensor_ip"),
            "host_ip": LaunchConfiguration("host_ip"),
            "data_port": LaunchConfiguration("data_port"),
            "return_mode": LaunchConfiguration("return_mode"),
            "min_range": LaunchConfiguration("min_range"),
            "max_range": LaunchConfiguration("max_range"),
            "frame_id": LaunchConfiguration("frame_id"),
            "scan_phase": LaunchConfiguration("scan_phase"),
            "cloud_min_angle": LaunchConfiguration("cloud_min_angle"),
            "cloud_max_angle": LaunchConfiguration("cloud_max_angle"),
            "gnss_port": LaunchConfiguration("gnss_port"),
        }],
        remappings=[
            ("velodyne_points", "pointcloud_raw"),
        ],
    )

    return launch.LaunchDescription(launch_arguments + [driver_node])
