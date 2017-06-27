import os
import shutil

def clean_dir():
    shutil.rmtree("/Users/Nikita/PycharmProjects/TextToImageStego/static/pics/")
    os.mkdir("/Users/Nikita/PycharmProjects/TextToImageStego/static/pics/")