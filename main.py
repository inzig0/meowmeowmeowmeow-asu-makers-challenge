import time

from iface import UserInterface
from keypoll import KeyPoll


CONST_UI_POLL_RATE = 1;      # Interface poll rate.
CONST_REC_POLL_RATE = 0.1;   # Music key poll rate.
CONST_REC_DURATION = 10;     # Music record duration.
CONST_SR = 48000;            # Sample rate. Should match all sound banks.
CONST_POLLING_TOLERANCE = 5; # How many samples may pass before the next keystroke is considered a new chord
                             # Playing the same note again should register as a new chord regardless of tolerance

ui = UserInterface();   # See iface.py
key_poller = KeyPoll(); # See keypoll.py


#def load_bank(name):


def record():
    keylog = [];
    start_time = time.time();

    while (time.time() - start_time) < CONST_REC_DURATION:
        (ts, keys) = key_poller.poll_keys();

        if len(keys) > 0:
            keylog.append((ts, keys));

        time.sleep(CONST_REC_POLL_RATE);

    return keylog

def render(keylog):
    sps = CONST_REC_DURATION/CONST_SR; # Seconds per sample


def main():
    while True:

        ui.poll_iface();

        if ui.start_rec:
            print("Record...");
            keylog = record();

            render(keylog);

        time.sleep(CONST_UI_POLL_RATE);

main()
