from PIL import Image
import os
import sys

arguments = sys.argv
# overwrite arguments to test the program without arguments
arguments = ["text.txt", "Bild.bmp"]

# text.txt
INPUT_TEXT = arguments[0]
# bild.bmp
INPUT_IMAGE = arguments[1]
# bild.bmp.ste
OUTPUT = arguments[1] + ".ste.bmp"


def encode_image(img, msg):
    length = len(msg)
    encoded = img.copy()
    width, height = img.size
    index = 0
    for row in range(height):
        for col in range(width):
            r, g, b = img.getpixel((col, row))
            if row == 0 and col == 0 and index < length:
                asc = length
            elif index <= length:
                #c = msg[index -1]
                asc = ord(msg[index -1])
            else:
                asc = r
            encoded.putpixel((col, row), (asc, g , b))
            index += 1
    return encoded

def main():
    #original_image_file = "Bild.bmp"
    img = Image.open(INPUT_IMAGE)
    #verstecktext_Datei = open("Text.txt", "rb")
    msg = INPUT_TEXT.read()
    
    img_encoded = encode_image(img, msg)
    encoded_image_file = Image
    
    thisFile = encoded_image_file
    base = os.path.splitext(thisFile)[0]
    os.rename(thisFile, base + ".bmp.ste")
    img_encoded.save(thisFile)
    
if __name__ == "__main__":
    main()
