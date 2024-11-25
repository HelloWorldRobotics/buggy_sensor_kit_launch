from launch import LaunchDescription
from launch.actions import GroupAction
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import PathJoinSubstitution

def generate_launch_description():
    pkg_prefix = FindPackageShare('buggy_sensor_kit_launch')
    
    # Common configuration for all cameras
    cameras = {
        'back': {
            'namespace': '/sensing/camera/camera0',
            'device_id': '0',
            'flip': True,
            'flip_angle': 180
        },
        # 'front': {
        #     'namespace': '/sensing/camera/camera1',
        #     'device_id': '1',
        #     'flip': False
        # },
        # 'left': {
        #     'namespace': '/sensing/camera/camera2',
        #     'device_id': '2',
        #     'flip': False
        # },
        # 'right': {
        #     'namespace': '/sensing/camera/camera3',
        #     'device_id': '3',
        #     'flip': False
        # }
    }
    
    nodes = []
    
    # Create nodes for each camera
    for camera_position, config in cameras.items():
        namespace = config['namespace']
        camera_num = config['device_id']
        
        # Base topics for the camera
        base_image_topic = 'image_rect_color'
        base_camera_info_topic = 'camera_info'
        
        # Create the camera node
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
            }],
            remappings=[
                ('image_raw', 'preflipped/image_raw' if config.get('flip', False) else base_image_topic),
                ('image_raw/compressed', 'preflipped/compressed' if config.get('flip', False) else f'{base_image_topic}/compressed'),
                ('camera_info', base_camera_info_topic),
            ]
        )
        nodes.append(camera_node)
        
        # If camera needs to be flipped, add rotation node
        if config.get('flip', False):
            rotate_node = Node(
                package='camera_publisher',
                executable='image_rotate',
                name=f'image_rotate_{camera_position}',
                namespace=namespace,
                parameters=[{
                    'input_image_topic': f'{namespace}/preflipped/image_raw',
                    'output_image_topic': f'{namespace}/{base_image_topic}',
                    # 'input_camera_info_topic': f'{namespace}/preflipped/camera_info',
                    # 'output_camera_info_topic': f'{namespace}/{base_camera_info_topic}',
                    'rotation_angle': config.get('flip_angle', 180),
                    'use_compressed': True
                }]
            )
            nodes.append(rotate_node)
    
    # Group all nodes together
    group = GroupAction(nodes)
    
    ld = LaunchDescription()
    ld.add_action(group)
    return ld
