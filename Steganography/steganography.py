from stegano import lsb
from stegano import lsbset
from stegano.lsbset import generators
import os;

class Steganographer:
    def __init__(self):
        self.choices = {
            "Fibonacci": generators.fibonacci,
            "Eratosthenes": generators.eratosthenes,
            "Logarithm": generators.log_gen
        }

    def encodePng(self, path, string):
        if ".png" not in path:
            path = path + ".png"
        if "./" not in path:
            path = "./" + path

        newImage = lsb.hide(path, string)
        newImage.save("./steganized/" + path)

    def decodePng(self, path):
        if "./" not in path:
            path = "./" + path
        return lsb.reveal(path)
        #Returns string
    def encodePngWithSet(self, path, string, choice=None):
        if ".png" not in path:
            path = path + ".png"
        if choice is None:
            choice = "Fibonacci"
        if "./" not in path:
            path = "./" + path
        print(self.choices)
        newImage = lsbset.hide(path, string, self.choices[choice]())
        newImage.save("./steganized/" + path)
        print("Called!")

    def decodePngWithSet(self, path, choice):
        if "./" not in path:
            path = "./" + path
        message = lsbset.reveal(path, self.choices[choice]())
        return message
        #Returns string
#for testing
steganographer = Steganographer()
# steganographer.encodePng("wallpaper.png", "hello world")
# print(steganographer.decodePng("./steganized/wallpaper.png"))
steganographer.encodePngWithSet("wallpaper.png", "hindi mo ako kaya", "Eratosthenes")
print(steganographer.decodePngWithSet("./steganized/wallpaper.png", "Eratosthenes"))
