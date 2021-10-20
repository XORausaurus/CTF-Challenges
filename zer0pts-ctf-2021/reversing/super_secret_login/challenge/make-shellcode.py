# make shellcode

import os
import pefile
import subprocess

print("[+] Building Shellcode... ", end='')
subprocess.call(["fasm", "fuck.asm"])
print("Done!")

pe = pefile.PE("fuck.exe")
dp = pe.sections[0].get_data()

print("[+] Dumping shellcode to 'shellcode.bin'... ", end='')
with open("shellcode.bin", "wb") as fuck:
    fuck.write(dp)
print("Done!")

print("[+] Packing shellcode+script ... ", end='')
subprocess.call(["clang", "-o", "change.exe", "-O3", "update.c"])
subprocess.call(["change.exe"])
print("Done!")

# data = bytearray(open("SolveMe-Temp.exe", "rb").read())
# offset = 0x87931
# target = b'\xe8\xa0\xd2\x08\x00\x90'
# open("SolveMe-Final.exe", "wb").write(data)
# fp = open("SolveMe-Final.exe", "rb+")
# fp.seek(offset)
# for i in target:
#     fp.write(bytes([i]))
# fp.close()

# data = bytearray(open("SolveMe-Final.exe", "rb").read())
# assert data[offset:offset+6] == target

print("[+] Patching call ... ")
subprocess.call(["clang", "-o", "target.exe", "-O3", "target.c"])
subprocess.call(["target.exe"])

# os.remove("SolveMe-Temp.exe")

print("\nDone!")
# print("[+] Saved to 'SolveMe-Final.exe'")