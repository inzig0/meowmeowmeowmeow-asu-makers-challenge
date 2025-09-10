import time

from iface import UserInterface
from keypoll import KeyPoll


CONST_UI_POLL_RATE = 1; # Both in seconds
CONST_REC_POLL_RATE = 0.1;
CONST_REC_DURATION = 10;

ui = UserInterface();   # See iface.py
key_poller = KeyPoll(); # See keypoll.py


def record():
    keylog = [];
    start_time = time.time();

    while (time.time() - start_time) < CONST_REC_DURATION:
        (ts, keys) = key_poller.poll_keys();

        if len(keys) > 0:
            keylog.append((ts, keys));

        time.sleep(CONST_REC_POLL_RATE);

    return keylog

def main():
    while True:

        ui.poll_iface();

        if ui.start_rec:
            print("Record...");
            keylog = record();

            print(str(keylog));

        time.sleep(CONST_UI_POLL_RATE);

main()
