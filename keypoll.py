import time


# Interface for polling all music keys.
#
# This class should interface the GPIO to get all pressed
# music keys.
class KeyPoll:

    set = [];
    __doc__ = "Interface for polling all music keys.";

    inc = True;
    note = 0;

    def __init__(self):

        # Any required initialization code will live here

        print("Music key poller open!")



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

        # For the sake of testing, this code will just
        # play an increasing and decreasing scale.

        presses.append(self.note);
        if self.inc:
            self.note += 1;
        if self.inc == False:
            self.note -= 1;

        if self.note == 6:
            self.inc = False;
        if self.note == 0:
            self.inc = True;

        return (timestamp, presses)
