import os
import binascii
from Crypto import Random
from Crypto.Cipher import AES
import hashlib
import base64
import numpy as np
from numpy.core.numeric import Infinity
import qrcode
from pyzbar.pyzbar import decode
from PIL import Image
print("\n--------------------Safe Data Transmission Using Stegnography and AES Mechanisms--------------------\n")
print("--------Choose-------\n1.-To convert your text into Qr code,\n2.-To decode Qrcode into text,\n3.-To Encrypt and Decrypt text using Stegnography,\n4.-To perform AES-256 Encryption-Decryption on given data,\n")
choice = int(input("Enter Your choice  :  "))

def qrencode():
    data = input("Enter Text you want to convert into QR code : ")
# Name of the QR code Image file
    QRCodefile = input("Enter name for qrcode File to save : ")
# instantiate QRCode object
    qrObject = qrcode.QRCode(version=1, box_size=12)
# add data to the QR code
    qrObject.add_data(data)
# compile the data into a QR code array
    qrObject.make()
    image = qrObject.make_image()
    image.save(QRCodefile)
# print the image size (version)
    print("Size of the QR image(Version):")
    print(np.array(qrObject.get_matrix()).shape)

def Qrencode(data):
    QRCodefile = input("Enter name for qrcode File to save : ")
    qrObject = qrcode.QRCode(version=1, box_size=12)
    qrObject.add_data(data)
    qrObject.make()
    image = qrObject.make_image()
    image.save(QRCodefile)
    print("Size of the QR image(Version):")
    print(np.array(qrObject.get_matrix()).shape)


def qrdecode():
    file_name = input(
        "Enter the location of image/QRcode which you want to decode : ")
    d = decode(Image.open(file_name))
    x = (d[0].data.decode('ascii'))
    return x

# Python program implementing Image Steganography
def genData(data):
    # list of binary codes
    # of given data
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd
# Pixels are modified according to the
# 8-bit binary data and finally returned


def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        # Extracting 3 pixels at a time
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]
        # Pixel value should be made odd for 1 and even for 0
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j] % 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
                # pix[j] -= 1
        # Eighth pixel of every set tells
        # whether to stop ot read further.
        # 0 means keep reading; 1 means thec
        # message is over.
        if (i == lendata - 1):
            if (pix[-1] % 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1] % 2 != 0):
                pix[-1] -= 1

        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]


def encode_enc(newimg, data):
    w = newimg.size[0]
    (x, y) = (0, 0)
    for pixel in modPix(newimg.getdata(), data):
        # Putting modified pixels in the new image
        newimg.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1

# Encode data into image
def Encode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    data = input("Enter data to be encoded : ")
    if (len(data) == 0):
        raise ValueError('Data is empty')
    newimg = image.copy()
    encode_enc(newimg, data)
    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

def Encode_(data):
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    if (len(data) == 0):
        raise ValueError('Data is empty')
    newimg = image.copy()
    encode_enc(newimg, data)
    new_img_name = input("Enter the name of new image(with extension) : ")
    newimg.save(new_img_name, str(new_img_name.split(".")[1].upper()))

# Dede the data in the image
def Decode():
    img = input("Enter image name(with extension) : ")
    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())
    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]
        # string of binary data
        binstr = ''
        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

# Main Function
def main():
    a = int(input(":: Welcome to Steganography ::\n"
                  "1. Encode\n2. Decode\n"))
    if (a == 1):
        x=Encode()
        print(x)
    elif (a == 2):
        x=Decode()
        print("Decoded Word :  " + x)
    else:
        raise Exception("Enter correct input")


def encrypt_AES_GCM(msg, secretKey):
    aesCipher = AES.new(secretKey, AES.MODE_GCM)
    ciphertext, authTag = aesCipher.encrypt_and_digest(msg)
    return (ciphertext, aesCipher.nonce, authTag)


def decrypt_AES_GCM(encryptedMsg, secretKey):
    (ciphertext, nonce, authTag) = encryptedMsg
    aesCipher = AES.new(secretKey, AES.MODE_GCM, nonce)
    plaintext = aesCipher.decrypt_and_verify(ciphertext, authTag)
    return plaintext

while(True):
    if(choice == 1):
        print("----------QR code Encryption----------")
        qrencode()
        print("Do you want to continue ... (Y/N) :")
        temp = input()
        if(temp == 'Y'):
            choice = int(input("Enter Your choice  :  "))
        else:
            exit()

    if(choice == 2):
        print("----------QR code Decryption----------")
        x = qrdecode()
        print(x)
        print("Do you want to continue ... (Y/N) :")
        temp = input()
        if(temp == 'Y'):
            choice = int(input("Enter Your choice  :  "))
        else:
            exit()

    if(choice == 3):
        if __name__ == '__main__':
            x=main()
            print(x)
        print("Do you want to continue ... (Y/N) :")
        temp = input()
        if(temp == 'Y'):
            choice = int(input("Enter Your choice  :  "))
        else:
            exit()

    if(choice == 4):
        print("\n\n1.Use AES-Encryption with Stegnography..\n2.Use AES-Encryption with QRcode image..\n3.Use AES-Decryption")
        inp = int(input("enter 1 or 2 :"))
        if(inp == 1):
            msg = Decode()
        else:
            msg = qrdecode()
        msg = bytes(msg, 'utf-8')
        secretKey = os.urandom(32)  # 256-bit random encryption key
        print("Encryption key:", binascii.hexlify(secretKey))
        encryptedMsg = encrypt_AES_GCM(msg, secretKey)
        print("encryptedMsg", {
            'ciphertext': binascii.hexlify(encryptedMsg[0])
        })
        print(encryptedMsg)
        if(inp == 1):
            Encode()
        else:
            Qrencode(encryptedMsg)

        print("-------------Decoding and Decrypting our text to check is there any------------- ")
        if(inp==1):
            msg=Decode()
           # msg=msg.encode()
            decryptedMsg = decrypt_AES_GCM(encryptedMsg, secretKey)
            decryptedMsg = decryptedMsg.decode()
            Encode_(decryptedMsg)
        else:
            msg=qrdecode()
           # msg=msg.encode()
            decryptedMsg = decrypt_AES_GCM(encryptedMsg, secretKey)
            decryptedMsg = decryptedMsg.decode()
            Qrencode(decryptedMsg)
        #print(decryptedMsg)
        print("Do you want to continue ... (Y/N) :")
        temp = input()
        if(temp == 'Y'):
            choice = int(input("Enter Your choice  :  "))
        else:
            exit()