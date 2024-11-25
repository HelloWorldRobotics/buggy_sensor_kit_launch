from launch import LaunchDescription
from launch.actions import GroupAction
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    pkg_prefix = FindPackageShare('buggy_sensor_kit_launch')
    
    # Common configuration for all cameras
    cameras = {
        'back': 'camera_back',
        # 'front': 'camera_front',
        # 'left': 'camera_left',
        # 'right': 'camera_right'
    }
    
    camera_nodes = []
    
    # Create nodes for each camera
    for camera_position, namespace in cameras.items():
        camera_node = Node(
            package='usb_cam',
            executable='usb_cam_node_exe',
            name=f'usb_cam_{camera_position}',
            namespace=namespace,
            output='screen',
            parameters=[{
                PathJoinSubstitution([
                    pkg_prefix,
                    'config',
                    'camera_configuration',
                    f'{camera_position}.yaml'
                ])
            }]
        )
        camera_nodes.append(camera_node)
    
    # Group all camera nodes together
    camera_group = GroupAction(camera_nodes)
    
    ld = LaunchDescription()
    ld.add_action(camera_group)
    return ld
