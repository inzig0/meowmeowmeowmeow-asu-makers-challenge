import time

from iface import UserInterface
from keypoll import KeyPoll
from banks import AudioStream, AudioBank
from pyaudio import PyAudio, paInt16


CONST_UI_POLL_RATE = 1;         # Interface poll rate.
CONST_REC_POLL_RATE = 0.5;      # Music key poll rate.
CONST_REC_DURATION = 10;        # Music record duration.
CONST_SR = 48000;               # Sample rate. Should match all sound banks.
CONST_POLLING_TOLERANCE = 5;    # How many samples may pass before the next keystroke is considered a new chord
                                # Playing the same note again should register as a new chord regardless of tolerance
CONST_OCTAVE_COUNT = 1;         # Number of octaves


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
    final_pcm = bytearray();

    iterating = True;
    while iterating:
        if render_ts >= curr_ts:
            # Add code here to transcribe audio upon PCM file
            for k in curr_ks:
                new_stream = bank.spawn_stream(k);
                new_stream.parent_index = len(stream_list);

                stream_list.append(new_stream);

            curr_i += 1;
            if curr_i == len(keylog):
                iterating = False
            else:
                (curr_ts, curr_ks) = keylog[curr_i];

        byte = 0;
        for stream in stream_list:
            byte = byte | stream.advance();

            if stream.finished:
                stream_list.remove(stream.parent_index);

        final_pcm += byte.to_bytes(1, 'big'); # Endianess doesn't matter since it's only one byte
        render_ts += sps;

    return bytes(final_pcm)

def main():
    bank = AudioBank("sine", 1);
    paudio = PyAudio();
    astream = paudio.open(rate=CONST_SR, channels=1, output=True, format=paInt16);

    while True:

        ui.poll_iface();

        if ui.start_rec:
            print("Record...");
            keylog = record();

            pcm = render(keylog, bank);
            print(str(astream.get_read_available()));
            astream.write(pcm);

            print(str(pcm));

        time.sleep(CONST_UI_POLL_RATE);

main()
