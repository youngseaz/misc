import os
import numpy as np
from PIL import Image, ImageFont, ImageDraw
import cv2


CHAR_SET = """@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,"^`'. """
CHAR_SET_LEN = len(CHAR_SET)


def pil2cv(image):
    """
    reference:  https://qiita.com/derodero24/items/f22c22b22451609908ee
    transform PIL.Image object to cv2 type

    :param image: PIL.Image instance
    :return:
    """
    new_image = np.array(image, dtype=np.uint8)
    if new_image.ndim == 2:   # 单色
        pass
    elif new_image.shape[2] == 3:   # 彩色
        new_image = cv2.cvtColor(new_image, cv2.COLOR_RGB2BGR)
    elif new_image.shape[2] == 4:
        new_image = cv2.cvtColor(cv2.COLOR_RGBA2BGRA)
    return new_image


def cv2pil(image):
    """
    OpenCV型 -> PIL型
    :param image: array of image
    :return: PIL.Image object
    """
    new_image = image.copy()
    if new_image.ndim == 2:  # モノクロ
        pass
    elif new_image.shape[2] == 3:  # カラー
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGR2RGB)
    elif new_image.shape[2] == 4:  # 透過
        new_image = cv2.cvtColor(new_image, cv2.COLOR_BGRA2RGBA)
    new_image = Image.fromarray(new_image)
    return new_image


def image2text(image):
    """
    When translating a color image to black and white (mode “L”), the library uses the ITU-R 601-2 luma transform:
    L = R * 299/1000 + G * 587/1000 + B * 114/1000

    :param image: array of image
    :return: string
    """
    global CHAR_SET, CHAR_SET_LEN
    percent = (0.299, 0.587, 0.114)
    width = image.shape[0]
    height = image.shape[1]
    string = ""
    for x in range(width):
        for y in range(height):
            gray = int(np.dot(image[x, y], percent))
            index = int(((CHAR_SET_LEN - 1)*gray)/255)
            string = string + CHAR_SET[index-1]
        string = string + "\n"
    return string


def text2image(text, size):
    """
    convert text to image
    :param text: the converting content
    :param size: specific image size
    :return: array of image
    """
    fontPath = os.path.realpath(os.path.join(os.path.dirname(os.path.realpath(__file__)), "simsun.ttc"))
    image = Image.new("RGB", size, (255, 255, 255))  # mode, size(width, height), bg color
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(fontPath, 10)
    # 第一个个参数为距离左上角的坐标， fill参数为填充字体的颜色
    draw.text((0, 0), text, font=font, fill="black", align="left")
    return pil2cv(image)


def main():
    cap = cv2.VideoCapture("badapple.mp4")
    threads = []
    while cap.isOpened():
        ret, frame = cap.read()
        image = cv2pil(frame)
        image = image.resize((int(image.size[0] * 0.35), int(image.size[1] * 0.18)))
        image = pil2cv(image)
        text = image2text(image)
        print(text)
        cv2.imshow("Video to Ascii", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
