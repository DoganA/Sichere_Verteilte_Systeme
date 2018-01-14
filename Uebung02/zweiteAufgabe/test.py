# -*- coding: cp1252 -*-
import hmac
import hashlib
import os
from xtea import *
from PIL import Image

s = True
while s == True:
    rq=input("password")
    if rq=="1":
        print ("rq=1")
        s = False
    
print("tous est bien")    
