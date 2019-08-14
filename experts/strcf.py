import sys
import cv2
from .expert import Expert

sys.path.append("external/pyCFTrackers")
from cftracker.strcf import STRCF as Tracker


class STRCF(Expert):
    def __init__(self):
        super(STRCF, self).__init__("STRCF")
        self.tracker = Tracker()

    def initialize(self, image, box):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        self.tracker.init(image, box)

    def track(self, image):
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        return self.tracker.update(image)
