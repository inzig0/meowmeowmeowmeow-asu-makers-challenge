import time

from iface import UserInterface
from keypoll import KeyPoll
from banks import AudioStream, AudioBank
import sounddevice as sdev
from numpy import array, int16


CONST_UI_POLL_RATE = 1;         # Interface poll rate.
CONST_REC_POLL_RATE = 1;      # Music key poll rate.
CONST_REC_DURATION = 10;        # Music record duration.
CONST_SR = 48000;               # Sample rate. Should match all sound banks.
CONST_POLLING_TOLERANCE = 5;    # How many samples may pass before the next keystroke is considered a new chord
                                # Playing the same note again should register as a new chord regardless of tolerance
CONST_OCTAVE_COUNT = 1;         # Number of octaves
CONST_DEVICE_IDX = 0;


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

def render(keylog, bank):
    sps = CONST_REC_DURATION/CONST_SR; # Seconds per sample
    curr_i = 0;
    (curr_ts, curr_ks) = keylog[0]; # IVs
    render_ts = curr_ts; # First timestamp

    stream_list = [];
    final_pcm = [];

    iterating = True;
    while iterating:
        if render_ts >= curr_ts:
            # Adds streams to a list of transcribing streams
            for k in curr_ks:
                new_stream = bank.spawn_stream(k);
                new_stream.parent_index = len(stream_list);

                stream_list.append(new_stream);

            # Halt rendering at the end of the keylog.
            # Change behavior to halt once all streams have expired AND the end of the keylog has been reached.
            curr_i += 1;
            if curr_i == len(keylog):
                iterating = False
            else:
                (curr_ts, curr_ks) = keylog[curr_i];

        render_ts += sps;

        # Transcribe shorts from all streams into one short
        short = 0;
        for s in stream_list:
            short = short | s.advance();

            if s.finished:
                stream_list.remove(s);

        final_pcm.append(short);

    return array(final_pcm, dtype=int16);

def main():
    bank = AudioBank("sine", 1);

    #for d in range(0, paudio.get_device_count()):
    #    print(str(paudio.get_device_info_by_index(d)));


    while True:

        ui.poll_iface();

        if ui.start_rec:
            print("Record...");
            keylog = record();

            print("Render");
            pcm = render(keylog, bank);

            print("Play");
            sdev.play(pcm, CONST_SR);
            sdev.wait();

            print("Done!");

        time.sleep(CONST_UI_POLL_RATE);

main()
