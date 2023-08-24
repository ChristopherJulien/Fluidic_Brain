# from DigiCam.Camera import Camera
from DigiCam.DigiCam.Camera import Camera

# Replace the below path with the absolute or relative path to your CameraControlCmd executable.
camera_control_cmd_path = 'C:\\Program Files (x86)\\digiCamControl\\CameraControlCmd.exe'

test_camera = Camera(control_cmd_location=camera_control_cmd_path)

test_camera.capture_single_image(autofocus=True)
