import time

from iface import UserInterface
from keypoll import KeyPoll
from banks import AudioStream, AudioBank
import sounddevice as sdev
from numpy import array, int16
from math import e


CONST_UI_POLL_RATE = .1;         # Interface poll rate.
CONST_REC_POLL_RATE = .05;      # Music key poll rate.
CONST_REC_DURATION = 10;        # Music record duration.
CONST_SR = 48000;               # Sample rate. Should match all sound banks.
CONST_POLLING_TOLERANCE = 5;    # How many samples may pass before the next keystroke is considered a new chord
                                # Playing the same note again should register as a new chord regardless of tolerance
CONST_OCTAVE_COUNT = 1;         # Number of octaves
CONST_DEVICE_IDX = 0;
CONST_MASTER_VOL = 3;


ui = UserInterface();   # See iface.py
key_poller = KeyPoll(); # See keypoll.py



# Hyperbolic tangent -- for signal mixing
def tanh(x):
    x = x/32767;
    return ( pow(e, x) - pow(e, -x) )/( pow(e, x) + pow(e, -x) ) * 32767

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
    tps = 1/CONST_SR; # Time per sample
    curr_i = 0;
    (curr_ts, curr_ks) = keylog[0]; # IVs
    render_ts = curr_ts; # First timestamp
    master = CONST_MASTER_VOL;

    stream_list = [];
    final_pcm = [];

    iterating = True;
    unfinished = True;
    while unfinished:
        if render_ts >= curr_ts and iterating:
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

        render_ts += tps;

        # Transcribe shorts from all streams into one short
        sigsum = 0;
        for s in stream_list:
            sigsum += (s.advance()/master);

            if s.finished:
                stream_list.remove(s);

        short = tanh(sigsum);

        final_pcm.append(short);

        if not iterating and len(stream_list) == 0:
            unfinished = False;

    print(len(final_pcm));

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
