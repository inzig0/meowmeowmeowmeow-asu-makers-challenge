import RPi.GPIO as GPIO
import time


# Interface for controls & statuses.
#
# This class should interface the GPIO to get and
# set status indicators
class UserInterface:
    __doc__ = "Interface for controls & statuses.";

    rec_pin = 11;

    start_rec = False;
    #ots = True; # For dummy interface. Do not use.

    def __init__(self):

        # Any required initialization code will live here

        GPIO.setmode(GPIO.BOARD)

        GPIO.setup(self.rec_pin, GPIO.IN)

        self.last_poll = time.gmtime(0)

        print("User interface open!");

    def poll_iface(self):

        self.last_poll = time.time();

        if GPIO.input(rec_pin):
            self.start_rec = True;
        else:
            self.start_rec = False;
