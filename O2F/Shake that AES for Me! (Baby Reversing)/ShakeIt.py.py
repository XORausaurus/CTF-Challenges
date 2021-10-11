from Crypto.Cipher import AES
import bitstring

def Slim_Shady():
    try:
        AES_key = b'H@ck3rMan__kN0ws'
        flag1_input = input("Enter the first part of the flag!\n (The flag is 16 characters)\n").encode("utf-8")
        flag1_cipher = AES.new(AES_key, AES.MODE_ECB)
        AES_flag1_cipher = flag1_cipher.encrypt(flag1_input)
        if AES_flag1_cipher == b'\x19\xe3\xc9\xa8\xf2\x05\xdaX\x90aP~\xe2L\xbeY':
            print("That is correct!\nLet's move to the next part!")
            Eminem()
        else:
            print("Incorrect")
    except:
        print("Incorrect input format.\n Flag is 16 characters.")


def Marshall(i, msg):
    msg.rol(1)
    return msg

def Mathers(i, msg):
    msg.ror(1)
    return msg

def Eminem():
    msg_input = input("\n\nEnter the second half of the flag (in hex):\n")
    msg = bitstring.BitArray(hex='0x'+msg_input)
    for i in range(812345,812355):
        msg = Marshall(i,msg)
    for i in range(98647,98650):
        msg = Mathers(i,msg)
    if msg.hex == "b92faa3419b6afa0363619":
        print("That's the correct flag!\n\nEnter as O2F{flag1+flag2}")
    else:
        print("Incorrect! Try again")

Slim_Shady()
