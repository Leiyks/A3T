import sys
from .expert import Expert

sys.path.append("external/pyCFTrackers")
from cftracker.staple import Staple as Tracker
from cftracker.config import staple_config


class Staple(Expert):
    def __init__(self):
        super(Staple, self).__init__("Staple")
        self.tracker = Tracker(config=staple_config.StapleConfig())

    def initialize(self, image, box):
        self.tracker.init(image, box)

    def track(self, image):
        return self.tracker.update(image)