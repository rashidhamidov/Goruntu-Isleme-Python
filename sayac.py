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
            if (resim[i, j] >= 30 and resim[i, j] <= 70):
                resim[i, j] -= 20
            j += 1
        i += 1
        j = 0


def abone_kesinlestirme(resim, bottomx, bottomy, topx, topy):
    i = 0
    j = 0
    while (i < (bottomx - topx)):
        while (j < (bottomy - topy)):
            if (resim[i, j] < 70):
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
        abone_image = cv2.GaussianBlur(gray, (5, 5), 0)
        # image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        cv2.imshow('', img)

        (x, y) = 70, 150
        (topx, topy) = (0, 0)
        (bottomx, bottomy) = (np.max(x), np.max(y))
        abone_image = abone_image[topx:bottomx, topy:bottomy]
        abone_kesinlestir_1(abone_image, bottomx, bottomy, topx, topy)
        abone_kesinlestirme(abone_image, bottomx, bottomy, topx, topy)
        # Cropped=cv2.Canny(Cropped,80,150)
        Cropped = cv2.threshold(abone_image, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # Cropped = cv2.Canny(Cropped, 10, 60, 65)

        text = pytesseract.image_to_string(Cropped)

        print(text)
        # cv2.imshow('Sayac Endeks', Cropped)
        dosya = open("D:\\xampp\htdocs/sayacokumaproje/abone.txt", "w")
        dosya.write('Abone Numarasi:')
        i = 0
        if (len(text) < 5):
            dosya.write('Abone Numarasi Okunamadi')
        else:
            while (i < len(text)):
                if (text[i].isdigit()):
                    dosya.write(text[i])
                i += 1
        dosya.close()
        os.remove('bekleme/abone.png')


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
            if (resim[i, j] >= 80 and resim[i, j] <= 100):
                resim[i, j] -= 40
            j += 1
        i += 1
        j = 0


def kesinlestirme(resim, bottomx, bottomy, topx, topy):
    i = 0
    j = 0
    while (i < (bottomx - topx)):
        while (j < (bottomy - topy)):
            if (resim[i, j] < 80):
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
        # image=cv2.GaussianBlur(gray,(5,5),0)
        image = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 21, 5)
        # cv2.imshow('', img)

        (x, y) = 400, 600
        (topx, topy) = (0, 0)
        (bottomx, bottomy) = (np.max(x), np.max(y))
        image = gray[topx:bottomx, topy:bottomy]
        kesinlestir_1(image, bottomx, bottomy, topx, topy)
        kesinlestirme(image, bottomx, bottomy, topx, topy)
        # Cropped=cv2.Canny(Cropped,80,150)
        Cropped = cv2.threshold(image, 0, 255,
                                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
        # Cropped = cv2.Canny(Cropped, 10, 60, 65)
        text = pytesseract.image_to_string(Cropped)

        # cv2.imshow('Sayac Endeks', Cropped)
        dosya = open("D:\\xampp\htdocs\sayacokumaproje/sonuc.txt", "w")
        dosya.write('Sayac Endeksi:')
        i = 0
        if (len(text) < 6):
            dosya.write('Endeks Okunamadi')
        else:
            while (i < len(text)):
                if (text[i].isdigit()):
                    dosya.write(text[i])
                if (i + 1 == len(text) or text[i].isalpha()):
                    dosya.write('0')
                i += 1
                if (i == 6):
                    break
        dosya.close()
        os.remove('bekleme/sayac.png')


if __name__ == '__main__':
    file = 'bekleme/sayac.png'
    filename = file
    time_limit = 3600  # one hour from now.
    check_interval = 1  # seconds between checking for the file.

    if watch_file(filename, time_limit, check_interval):

        img = cv2.imread(file, cv2.IMREAD_COLOR)
        img = cv2.resize(img, (600, 400))

        preproces(img)

    else:
        print("File not found after waiting:", time_limit, " seconds!")


cv2.waitKey(0)
cv2.destroyAllWindows()
