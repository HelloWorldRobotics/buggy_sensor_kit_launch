# sample_sensor_kit_launch

## Camera (camera_left)

Forward-facing ELP USB camera, 1920x1080 via `usb_cam`, publishing under
`/sensing/camera/camera_left/`. Started automatically by `sensing.launch.xml`.

| File | |
|---|---|
| `launch/cameras.launch.xml` | Driver + throttled compressed stream for recording |
| `config/camera_configuration/camera_left.yaml` | Driver parameters |
| `config/camera_configuration/camera_left_info.yaml` | Placeholder intrinsics — not calibrated |

Needs the udev rule `99-buggy-camera.rules` (installed outside this repo) to
provide `/dev/buggy_cam0`.

Several parameters here fail silently if written the obvious way. The launch
file and YAML carry comments explaining each — read them before editing.
