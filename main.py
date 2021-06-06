#!/usr/bin/env python
import cv2
import imutils
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

import os
import time


def watch_file(filename, time_limit=3600, check_interval=60):
    '''Return true if filename exists, if not keep checking once every check_interval seconds for time_limit seconds.
    time_limit defaults to 1 hour
    check_interval defaults to 1 minute
    '''

    now = time.time()
    last_time = now + time_limit

    while time.time() <= last_time:
        if os.path.exists(filename):
            return True
        else:
            # Wait for check interval seconds, then check again.
            time.sleep(check_interval)

    return False


def abone_temizleme(resim, bottomx, bottomy):
    resim[0:bottomx, 0:31] = 255
    resim[0:21, 0:bottomy] = 255
    resim[45:bottomx, 0:bottomy] = 255
    resim[0:bottomx, 53:80] = 255
    resim[0:bottomx, 101:128] = 255
    resim[0:bottomx, 150:177] = 255
    resim[0:bottomx, 199:226] = 255
    resim[0:bottomx, 248:bottomy] = 255


def abone_kesinlestir_1(resim, bottomx, bottomy, topx, topy):
    i = 0
    j = 0
    while (i < (bottomx - topx)):
        while (j < (bottomy - topy)):
            if (resim[i, j] >= 30 and resim[i, j] <= 50):
                resim[i, j] -= 20
            j += 1
        i += 1
        j = 0


def abone_kesinlestirme(resim, bottomx, bottomy, topx, topy):
    i = 0
    j = 0
    while (i < (bottomx - topx)):
        while (j < (bottomy - topy)):
            if (resim[i, j] < 55):
                resim[i, j] = 0
            else:
                resim[i, j] = 255
            j += 1
        i += 1
        j = 0


def abone_okuma(img):
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 80, 180)
        image = cv2.GaussianBlur(gray, (5, 5), 0)
        # image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        cv2.imshow('', img)

        (x, y) = 70, 150
        (topx, topy) = (0, 0)
        (bottomx, bottomy) = (np.max(x), np.max(y))
        image = image[topx:bottomx, topy:bottomy]
        abone_kesinlestir_1(image, bottomx, bottomy, topx, topy)
        abone_kesinlestirme(image, bottomx, bottomy, topx, topy)
        # Cropped=cv2.Canny(Cropped,80,150)
        Cropped = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # Cropped = cv2.Canny(Cropped, 10, 60, 65)

        text = pytesseract.image_to_string(Cropped)

        print(text)
        # cv2.imshow('Sayac Endeks', Cropped)
        dosya = open("C:\Php/sayacokumaproje/abone.txt", "w")
        i = 0
        if (len(text) < 5):
            dosya.write('0')
        else:
            while (i < len(text)):
                if (text[i].isdigit()):
                    dosya.write(text[i])
                i += 1
            dosya.close()
            os.remove('bekleme/abone.png')
            file = 'bekleme/sayac.png'
            filename = file
            time_limit = 3600  # one hour from now.
            check_interval = 1  # seconds between checking for the file.

            if watch_file(filename, time_limit, check_interval):
                sayac_img = cv2.imread(filename, cv2.IMREAD_COLOR)
                sayac_img = cv2.resize(sayac_img, (150, 70))
                preproces(sayac_img)


def temizleme(resim, bottomx, bottomy):
    resim[0:bottomx, 0:31] = 255
    resim[0:21, 0:bottomy] = 255
    resim[45:bottomx, 0:bottomy] = 255
    resim[0:bottomx, 53:80] = 255
    resim[0:bottomx, 101:128] = 255
    resim[0:bottomx, 150:177] = 255
    resim[0:bottomx, 199:226] = 255
    resim[0:bottomx, 248:bottomy] = 255


def kesinlestir_1(resim, bottomx, bottomy, topx, topy):
    i = 0
    j = 0
    while (i < (bottomx - topx)):
        while (j < (bottomy - topy)):
            if (resim[i, j] >= 80 and resim[i, j] <= 90):
                resim[i, j] -= 40
            j += 1
        i += 1
        j = 0


def kesinlestirme(resim, bottomx, bottomy, topx, topy):
    i = 0
    j = 0
    while (i < (bottomx - topx)):
        while (j < (bottomy - topy)):
            if (resim[i, j] < 100):
                resim[i, j] = 0
            else:
                resim[i, j] = 255
            j += 1
        i += 1
        j = 0


def preproces(img):
    if img is not None:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        canny = cv2.Canny(gray, 80, 180)
        image = cv2.GaussianBlur(gray, (5, 5), 0)
        # image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        cv2.imshow('', img)

        (x, y) = 70, 150
        (topx, topy) = (0, 0)
        (bottomx, bottomy) = (np.max(x), np.max(y))
        image = image[topx:bottomx, topy:bottomy]
        kesinlestir_1(image, bottomx, bottomy, topx, topy)
        kesinlestirme(image, bottomx, bottomy, topx, topy)
        # Cropped=cv2.Canny(Cropped,80,150)
        Cropped = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # Cropped = cv2.Canny(Cropped, 10, 60, 65)
        cv2.imshow('',Cropped)

        text = pytesseract.image_to_string(Cropped)
        print(text)
        dosya = open("C:\Php\sayacokumaproje/sonuc.txt", "w")
        i = 0
        if (len(text) < 6):
            dosya.write('Endeks Okunamadi')
        else:
            while (i < len(text)):
                if text[i].isdigit():
                    dosya.write(text[i])
                elif (i + 2 == len(text) and text[i].isdigit()==False):
                    dosya.write('0')
                i += 1
                if (i == 6):
                    break
        dosya.close()

        os.remove('bekleme/sayac.png')

i=-1
while i<0:
    if __name__ == '__main__':
        file = 'bekleme/abone.png'

        print('beklemede')
        filename = file
        time_limit = 3600  # one hour from now.
        check_interval = 1  # seconds between checking for the file.

        if watch_file(filename, time_limit, check_interval):

            img = cv2.imread(file, cv2.IMREAD_COLOR)
            img = cv2.resize(img, (150, 70))
            dosya = open("C:\\Php\sayacokumaproje/sonuc.txt", "w")
            dosya.truncate(0)
            dosya.close()
            dosya = open("C:\\Php\sayacokumaproje/abone.txt", "w")
            dosya.truncate(0)
            dosya.close()
            abone_okuma(img)

        else:
            print("File not found after waiting:", time_limit, " seconds!")


cv2.waitKey(0)
cv2.destroyAllWindows()
