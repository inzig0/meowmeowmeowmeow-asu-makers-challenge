from copy import deepcopy
from numpy import array, int16



class AudioStream:
    __def__ = "Streaming, non-repudiating audio stream.";

    cursor = 0;
    buf = None;
    finished = False;

    def __init__(self, indexable):
        self.buf = indexable;

    def advance(self):
        if self.finished:
            return 0
        else:
            self.cursor += 1;
            if self.cursor == len(self.buf):
                self.finished = True;

            return self.buf[self.cursor - 1]



class AudioBank:
    __def__ = "Auto-loading audio bank.";

    key_lut = [];

    def __init__(self, bank_path, octave_n):

        for o in range(1, octave_n + 1):

            for k in ['A', 'B', 'C', 'D', 'E', 'F', 'G']:
                sample_list = [];
                sample_barr = open("./banks/" + bank_path + "/" + k + str(o) + ".pcm", 'rb').read();

                for b in range(1, int(len(sample_barr)/2)):
                    b = b*2;
                    b_chunk = sample_barr[b-2:b];
                    short = (b_chunk[1] + (b_chunk[0] << 8)) - 32767;
                    sample_list.append(short)

                self.key_lut.append(array(sample_list, dtype=int16));

    def spawn_stream(self, idx):
        return AudioStream(self.key_lut[idx])
