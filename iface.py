#import RPi.GPIO as GPIO
import time


class UserInterface:
    __doc__ = "Interface for controls & statuses.";

    def __init__(self):

        # Any required initialization code will live here

        #GPIO.setmode(GPIO.BOARD)

        self.last_poll = time.gmtime(0)

        print("User interface open!");

    def poll_iface(self):

        self.last_poll = time.time()

