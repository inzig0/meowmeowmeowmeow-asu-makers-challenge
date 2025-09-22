import math


bank = "sine"
sr = 48000;


def attack(v, x):
    atk = 0;
    x = x/(sr/10);

    if x <= 1:
        atk = pow(x, 2);
    else:
        atk = pow(2/3, x);

    return v*atk

def gen_freq(name, freq):
    fd = open("./" + bank + "/" + name + "1.pcm", "wb");

    pcm = bytearray([]);
    i = 0;
    while i < sr:
        smpl = int(attack(( 32767*math.sin( (2*math.pi)*( i / sr )*freq ) + 32767 ), i));
        #print(str(smpl));
        pcm += smpl.to_bytes(2, 'little');
        i += 1;

    fd.write(pcm);


gen_freq("C", 261.63);
gen_freq("D", 293.66);
gen_freq("E", 329.63);
gen_freq("F", 349.23);
gen_freq("G", 392.00);
gen_freq("A", 440.00);
gen_freq("B", 493.88);
