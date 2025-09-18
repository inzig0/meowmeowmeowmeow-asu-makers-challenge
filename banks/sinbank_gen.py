import math


bank = "sine"
sr = 48000;


def gen_freq(name, freq):
    fd = open("./" + bank + "/" + name + ".pcm", "wb");

    pcm = bytearray([]);
    i = 0;
    while i < sr:
        pcm += int( 32767*math.sin( (2*math.pi)*( i / sr )*freq ) + 32767 ).to_bytes(2, 'little');
        i += 1;

    fd.write(pcm);


gen_freq("C", 261.63);
gen_freq("D", 293.66);
gen_freq("E", 329.63);
gen_freq("F", 349.23);
gen_freq("G", 392.00);
gen_freq("A", 440.00);
gen_freq("B", 493.88);
