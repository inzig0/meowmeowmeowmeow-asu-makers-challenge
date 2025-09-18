from copy import deepcopy



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
                sample_barr = open("./banks/" + bank_path + "/" + k + str(o) + ".pcm", 'rb');
                sample_base_stream = AudioStream(sample_barr);
                self.key_lut.append(sample_base_stream);

    def spawn_stream(self, idx):
        return deepcopy(self.key_lut[self.idx])
