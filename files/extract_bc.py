#!/usr/bin/python3
"""Extract the Metal bytecode array from RedoX's IAR bc.c
(fw_wpa_wpa2_src: config page with WPA-WPA2 radio, netPmk/netAuth(5))
and regenerate nabgcc's src/bc.c with the same 4-radio bytecode.

Usage: extract_bc.py <fwrepo_bc.c> <nabgcc_bc.c>
"""
import re
import sys

def main():
    src_path, out_path = sys.argv[1], sys.argv[2]
    src = open(src_path, "r", encoding="latin-1").read()
    m = re.search(r"dumpbc\[(\d+)\]=\{(.*?)\};", src, re.S)
    if not m:
        sys.exit("no dumpbc array found")
    declared = int(m.group(1))
    data = bytes(int(x, 16) for x in re.findall(r"0x([0-9a-fA-F]{2})", m.group(2)))
    if len(data) != declared:
        sys.exit("byte count mismatch: declared %d, parsed %d" % (declared, len(data)))
    if len(data) != 36175:
        sys.exit("unexpected bytecode size %d (expected 36175)" % len(data))
    with open(out_path, "w") as f:
        f.write("#include <stdint.h>\n")
        f.write("__attribute__ ((section(\".bytecode\")))\n")
        f.write("const uint8_t dumpbc[%d]={\n" % len(data))
        for i in range(0, len(data), 16):
            f.write(",".join("0x%02x" % b for b in data[i:i+16]) + ",\n")
        f.write("};\n")
    print("replaced bytecode: %d bytes (WPA-WPA2 config page)" % len(data))

if __name__ == "__main__":
    main()
