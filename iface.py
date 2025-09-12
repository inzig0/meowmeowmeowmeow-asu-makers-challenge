import RPi.GPIO as GPIO
import time


# Interface for controls & statuses.
#
# This class should interface the GPIO to get and
# set status indicators
class UserInterface:
    __doc__ = "Interface for controls & statuses.";

    start_rec = False;
    ots = True; # For dummy interface. Do not use.

    def __init__(self):

        # Any required initialization code will live here

        GPIO.setmode(GPIO.BOARD)

        self.last_poll = time.gmtime(0)

        print("User interface open!");

    def poll_iface(self):

        self.last_poll = time.time();

        if self.ots:
            self.start_rec = True;
        else:
            self.start_rec = False;

        self.ots = False;
