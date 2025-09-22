import time
import RPi.GPIO as GPIO


# Interface for polling all music keys.
#
# This class should interface the GPIO to get all pressed
# music keys.
class KeyPoll:

    set = [];
    __doc__ = "Interface for polling all music keys.";

    key_pins = [29, 31, 32, 33, 35, 36, 37];
    key_map = [2, 3, 4, 5, 6, 0, 1];

    def __init__(self):

        # Any required initialization code will live here

        GPIO.setmode(GPIO.BOARD);
        for kp in self.key_pins:
            GPIO.setup(kp, GPIO.IN);


    def poll_keys(self):

        timestamp = time.time();
        #print(str(timestamp))
        presses = [];

        # Poll all newly-pressed keys in this space.
        #
        # Each key corresponds to a note. The note is
        # encoded as an int. It will count up from
        # A1 = 0, all the way to G2 = 13. The actual octave
        # they correspond to is arbitrary, and
        # determined by either user choice or program's
        # preference.
        #
        # When a key is pressed, check the set list to
        # see if the key has already been pressed. If
        # not, push the key's int code into the set and
        # presses lists. If it is then do nothing. Once
        # that key is depressed, remove it from the set
        # list. This will prevent replaying held keys.

        for ki in range(0, len(self.key_pins)):
            if GPIO.input(self.key_pins[ki]):
                presses.append(self.key_map[ki]);

        for ke in self.set:
            try:
                presses.remove(ke);
            except:
                True;

        self.set = presses;

        return (timestamp, presses)
