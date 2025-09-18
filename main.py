import time

from iface import UserInterface
from keypoll import KeyPoll
from banks import AudioStream, AudioBank


CONST_UI_POLL_RATE = 1;         # Interface poll rate.
CONST_REC_POLL_RATE = 0.1;      # Music key poll rate.
CONST_REC_DURATION = 10;        # Music record duration.
CONST_SR = 48000;               # Sample rate. Should match all sound banks.
CONST_POLLING_TOLERANCE = 5;    # How many samples may pass before the next keystroke is considered a new chord
                                # Playing the same note again should register as a new chord regardless of tolerance
CONST_OCTAVE_COUNT = 1;         # Number of octaves


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

def render(keylog, bank):

    sps = CONST_REC_DURATION/CONST_SR; # Seconds per sample
    curr_i = 0;
    (curr_ts, current_ks) = keylog[0]; # IVs
    render_ts = curr_ts; # First timestamp

    for s in range(0, CONST_SR*CONST_REC_DURATION):
        if render_ts >= curr_ts:
            # Add code here to transcribe audio upon PCM file

            curr_i += 1;
            (curr_ts, curr_ks) = keylog[curr_i];

def main():
    bank = AudioBank("sine", 1);

    while True:

        ui.poll_iface();

        if ui.start_rec:
            print("Record...");
            keylog = record();

            render(keylog, bank);

            print("Done");

        time.sleep(CONST_UI_POLL_RATE);

main()
