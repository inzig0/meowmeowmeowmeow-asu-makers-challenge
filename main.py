import time

from iface import UserInterface
from keypoll import KeyPoll


CONST_POLL_RATE = 0.1;


def main():
    ui = UserInterface();
    key_poller = KeyPoll();

    while(True):

        (timestamp, keys) = key_poller.poll_keys();

        print("Poll results: (" + str(timestamp) + ", " + str(keys) + ")");
        time.sleep(CONST_POLL_RATE);

main()
