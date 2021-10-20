import pefile

pe = pefile.PE("shell.exe")

print(pe.sections[0].get_data().hex())