#!/usr/bin/env python3
"""Package a raw firmware binary into Nabaztag:tag flash formats.

Usage: pack_sim.py <template.sim> <input.bin> <output.sim> <output.sim.txt>
"""
import sys, struct

invb = [1, 171,205,183,57, 163,197,239,241,27,
61, 167,41, 19, 53, 223,225,139,173,151,
25, 131,165,207,209,251,29, 135,9, 243,
21, 191,193,107,141,119,249,99, 133,175,
177,219,253,103,233,211,245,159,161,75,
109,87, 217,67, 101,143,145,187,221,71,
201,179,213,127,129,43, 77, 55, 185,35,
69, 111,113,155,189,39, 169,147,181,95,
97, 11, 45, 23, 153,3,  37, 79, 81, 123,
157,7,  137,115,149,63, 65, 235,13, 247,
121,227,5,  47, 49, 91, 125,231,105,83,
117,31, 33, 203,237,215,89, 195,229,15,
17, 59, 93, 199,73, 51, 85, 255]

def main():
    template, inbin, outsim, outtxt = sys.argv[1:5]
    t = open(template, 'rb').read()
    b = open(inbin, 'rb').read()
    assert len(t) >= 26, "template too short"
    hdr = bytearray(t[:26])
    struct.pack_into('>I', hdr, 8, len(b))
    struct.pack_into('>I', hdr, 22, len(b))
    sim = bytes(hdr) + b
    with open(outsim, 'wb') as f:
        f.write(sim)
    lenx = len(b)
    l = lenx * 2
    out = bytearray()
    out += b'-violet-'
    out += ('%08x' % l).encode()
    alpha = 47
    key = 0x47
    limit = lenx + 26
    for z in range(len(sim)):
        if 25 < z < limit:
            v = sim[z]
            o = (alpha + v * invb[key >> 1]) & 0xff
            key = (v + v + 1) & 0xff
            out += ('%02x' % o).encode()
    out += b'-violet-'
    with open(outtxt, 'wb') as f:
        f.write(bytes(out))
    print("packed: %d bytes binary -> %s (%d bytes), %s (%d bytes)"
          % (len(b), outsim, len(sim), outtxt, len(out)))

if __name__ == '__main__':
    main()
