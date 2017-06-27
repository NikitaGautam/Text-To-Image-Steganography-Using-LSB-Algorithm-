from PIL import Image
from glob import glob

def to_bits(v):
    b = []
    for i in range(8):
        b.append(v & 1)
        v >>= 1
    return tuple(reversed(b))


def to_byte(b):
    v = 0
    for bit in b:
        v = (v << 1) | bit
    return v


def bit_sequence(list_of_tuples):
    for t8 in list_of_tuples:
        for b in t8:
            yield b


def byte_sequence(bits):
    byte = []
    for n, b in enumerate(bits):
        if n % 8 == 0 and n != 0:
            yield to_byte(byte)
            byte = []
        byte.append(b)
    yield to_byte(byte)




def messageHide(message):
    img = None
    for test in range(256):
        b = to_bits(test)
        v = to_byte(b)
        assert v == test
    message_bytes = message.encode("UTF-8")
    bits_list = list((to_bits(c) for c in message_bytes))
    len_h, len_l = divmod(len(message_bytes), 256)
    size_list = [to_bits(len_h), to_bits(len_l)]
    final_list = size_list + bits_list
    seq = bit_sequence(final_list)
    seq = list(seq)

    # for image in glob("/Users/Nikita/StegoImage/*"):
    for image in glob("/Users/Nikita/PycharmProjects/TextToImageStego/static/pics/*"):
        # img = Image.open(image)
        img = Image.open(image).convert('RGB')

    w, h = img.size
    for p, m in enumerate(seq):
        y, x = divmod(p, w)
        r, g, b = img.getpixel((x, y))
        r_new = (r & 0xfe) | m
        # print( (r, g, b), m, (r_new, g, b) )
        img.putpixel((x, y), (r_new, g, b))

    # img.save("/Users/Nikita/StegoImage/newImage.png")
    img.save("/Users/Nikita/PycharmProjects/TextToImageStego/static/pics/newImage.png")
    # newImage = Image.open("/Users/Nikita/StegoImage/newImage.png")
    newImage = Image.open("/Users/Nikita/PycharmProjects/TextToImageStego/static/pics/newImage.png")





def get_bits(image, offset=0, size=16):
    w, h = image.size
    for p in range(offset, offset + size):
        y, x = divmod(p, w)
        r, g, b = image.getpixel((x, y))
        yield r & 0x01

def messageRetrieve():
    # image = "/Users/Nikita/StegoImage/newImage.png"
    image = "/Users/Nikita/PycharmProjects/TextToImageStego/static/pics/newImage.png"
    img = Image.open(image)
    size_H, size_L = byte_sequence(get_bits(img, 0, 16))
    size = size_H * 256 + size_L
    message = byte_sequence(get_bits(img, 16, size * 8))
    msg = bytes(message).decode("UTF-8")
    print (msg)
    return msg



