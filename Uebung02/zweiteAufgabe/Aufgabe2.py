# -*- coding: cp1252 -*-
import hmac

import os
from xtea import *
import hashlib
from PIL import Image
from pip._vendor.distlib.compat import raw_input


# verschlüsselung 

def encrypt(en_msg,p):
    
    key = p
    text = en_msg*8
    x = new(key, mode=MODE_CFB, IV="12345678")
    l=x.encrypt(text)
    return l

#entschlüsselung

def decrypt(dec_msg,p):
 
    key = p
    x = new(key, mode= MODE_CFB, IV="12345678",)
    y =x.decrypt(dec_msg)
    return y

# Dateien versteckung
def encode_image(img, msg,length):
   
    
   
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                c = msg[index -1]
                asc = ord(c)
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1
    return encoded

#Dateien Wiedergabe

def decode_image(img,length):
    
    width, height = img.size
    msg = ""
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if index <= length-1:
                msg += chr(r)
                index += 1
    return msg

 

# datei laden
nachricht_Datei = open('Text.txt', 'r')
nachricht = nachricht_Datei.read()
# mac password nehmen
macpassword=raw_input('Geben Sie den Macpassword:')
# password nehmen + password überprüfung ( 128 Bit!)

q=True
while q==True:
    
    password=raw_input('Geben Sie das Password:')
    password_lenght=len(password)
    if (password_lenght> 16) or (password_lenght == 0):
        print("das Password ist ungültig")
    if (password_lenght > 0) and (password_lenght <= 16):

        while password_lenght < 16:
            password += '?'
            password_lenght += 1
        q=False
#--------------------------------------------------------------------------
#Verschlüsselung + Authentifizierung 
#--------------------------------------------------------------------------



#password und mac password hashen
hash
hash_password=hashlib.sha256(password).hexdigest()
hash_password=chr(len(hash_password)) + hash_password


hash_mac=hashlib.sha256(macpassword).hexdigest()
hash_mac=chr(len(hash_mac)) + hash_mac


nachricht = nachricht + chr(len(nachricht))

#Dateien verschlüsseln  
hash_datei= hash_mac+ hash_password + nachricht
hash_datei_encrypt= encrypt(hash_datei,password)

#Dateien verstecken
original_image_file = "Bild.bmp"
img = Image.open(original_image_file)


img_encoded = encode_image(img, hash_datei_encrypt, len(hash_datei_encrypt))
encoded_image_file = original_image_file

thisFile = encoded_image_file
base = os.path.splitext(thisFile)[0]

if os.path.exists("Bild.bmp.sae")== True:
    os.remove("Bild.bmp.sae")

os.rename(thisFile, base + ".bmp.sae")    
img_encoded.save(thisFile)
    


print("Verschlüsselung ist fertig!, die Datein sind im Bild verteckt")  



#--------------------------------------------------------------------------
#enstschlüsslung + MAC Überprüfung
#--------------------------------------------------------------------------

request=raw_input("wollen Sie die Dateien entschlüsseln? ( 0 = NEIN ; 1 = JA )")

if request=='1':
# verschlüsselte Dateien wierdergeben
    encoded_image_file = "Bild.bmp.sae"
    img2 = Image.open(encoded_image_file)
    datei_encrypt = decode_image(img2,len(hash_datei_encrypt))
    

    s= True
    while s== True:
        # Password überprüfen    
        password_try=raw_input("Geben Sie das Password:")
        password_try_lenght=len(password_try)
        if (password_try_lenght> 16) or (password_try_lenght == 0):
             print("das Password ist ungültig")
             password_try=raw_input("Geben Sie das Password erneut:")
             password_try_lenght=len(password_try)
        if (password_try_lenght > 0) and (password_try_lenght < 16):
             while password_try_lenght < 16:
                 password_try += '?'
                 password_try_lenght += 1

       # Dateien entschlüsseln     
        if password_try == password:
            hash_datei_decrypt = decrypt(hash_datei_encrypt,password_try)
            datei_decrypt_lenght= len(hash_datei_decrypt)/8
            i=0
            decrypt_datei=''
            while i< datei_decrypt_lenght:
                decrypt_datei += hash_datei_decrypt[i]
                i+=1
                s= False
        else:
            print("Das Password ist falsch")
            
        
            
# Nachricht wiedergeben    
    lauf=len(decrypt_datei)-1
    nachricht_decrypt=''

    nachricht_length = ord(decrypt_datei[lauf])
    nachricht_length = len(decrypt_datei) - (nachricht_length+1)
    lauf -=1
    while nachricht_length<= lauf:
        nachricht_decrypt += decrypt_datei[nachricht_length]
        nachricht_length+=1
    print("entschlüsselung fertig!")
    print("mac Überprüfung:")

    while s==False:
        # Mac überprüfen/ Nachricht zeigen
        macpassword_try=raw_input("Geben Sie den Macpassword:")
        hash_macpassword_try =hashlib.sha256(macpassword_try).hexdigest()

        lauf=ord(decrypt_datei[0])
        mac_decrypt=''
        i=1
        while i<=lauf:
            mac_decrypt+=decrypt_datei[i]
            i+=1

        if mac_decrypt==hash_macpassword_try :
            print ("die Nachricht ist:")
            print("nachricht_decrypt")
            s=True
        else:
            print("Macpassword ist falsh")
        
