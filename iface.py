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


    def __init__(self):

        GPIO.setmode(GPIO.BOARD);
        GPIO.setup(self.rec_pin, GPIO.IN);

        self.last_poll = time.gmtime(0);

    def poll_iface(self):

        self.last_poll = time.time();

        if GPIO.input(self.rec_pin) and not self.start_rec:
            self.start_rec = True;
        elif not GPIO.input(self.rec_pin) and self.start_rec:
            self.start_rec = False;
