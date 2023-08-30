
# Setup
import digiCamControlPython as dccp
camera = dccp.Camera()

camera.setIso(100)
# >>> Set the Iso to 100

camera.getShutterspeed()
# >>> Current shutterspeed: 1/125

camera.listCompression()
# >>> List of all possible compressionsettings: ['JPEG (BASIC)', 'JPEG (NORMAL)', 'JPEG (FINE)', 'RAW', 'RAW + JPEG (BASIC)', 'RAW + JPEG (NORMAL)', 'RAW + JPEG (FINE)']

camera.setAutofocus("off")
# >>> Autofocus is off.

camera.setTransfer("Save_to_PC_only")

camera.setFolder(r"C:\Users\Julien\Pictures")
# >>> Set the session.folder to C:\Images\

camera.capture()
# >>> Captured image.
# >>> Current lastcaptured: Image1.jpg
