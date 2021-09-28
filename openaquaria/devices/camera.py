from picamera import PiCamera


class Camera:
    def __init__(self, resolution=(1024, 768)):
        self.camera = PiCamera()
        self.camera.resolution = resolution
        self.camera.start_preview()

    def photo(self, savePath: str):
        self.camera.capture(savePath)
