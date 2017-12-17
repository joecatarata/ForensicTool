import hashlib

class Cipher:
    def __init__(self):
        self.upper = [chr(65+i) for i in range(0,26)]
        self.lower = [chr(97+i) for i in range(0,26)]
        
        
        #Emoji
        emoji_dictionary = [':)', ':D', ':(', 'XD', '>_<', '-_-', ';(', 'o_O', 'xC', ';D','xP', 'xb', 'B-)', 'B-(', 'X)', 'X(', ':3', ':*', ';)', '>:(','>:)', ":'(", 'XO', 'D:', '(:', ':/']

        #NATO Alphabet
        NATO_dictionary = ["Alpha", "Beta", "Charlie", "Delta", "Echo", "Foxtrot","Golf", "Hotel", "India", "Juliett", "Kilo","Lima", "Mike", "November", "Oscar", "Papa","Quebec", "Romeo", "Sierra", "Tango", "Uniform", "Victor", "Whiskey", "Xray", "Yankee", "Zulu"]

        #Super Heroes! jk
        super_dictionary = ["Aquaman", "Batman", "CondimentKing", "Deadpool", "Elektra", "Falcon", "Gamora", "Hero", "Ironman", "JonasBrothers", "KatyPerry", "Lockjaw", "Magneto", "Neosporin", "Ovaltine", "PerrythePlatypus", "Crossaint", "RedTide", "SuperDuper", "Tango", "Umbrella" , "Volkswagen", "Nani", "Ex-men", "Yournext", "soom"]

        #Sha1 Dictionary
        upper = [chr(65+i) for i in range(0,26)]
        sha1_dictionary = [hashlib.sha1(i.encode('utf-8')).hexdigest() for i in upper]
        
        #Reverse
        reverse_dictionary = [chr(97+i) for i in range(25,-1,-1)]

        self.dictionaries = {"Emoji":emoji_dictionary, "NATO":NATO_dictionary, "Super":super_dictionary, "SHA1":sha1_dictionary, "Reverse":reverse_dictionary}
        self.set_dictionary()
    
    def set_dictionary(self, dictionary_type="Reverse"):
        self.dictionary = self.dictionaries[dictionary_type]
        
    def cut_dictionary(self, num=4):
        self.dictionary = [i[:num]  for i in dictionary]
    
    def def_shift_num(self, num=0, isUI=False):
        if isUI:
            self.main_cipher = num
        
        self.cipher = num#IMPORTANT
        
    def start_cipher(self, plaintext="My name is Jeff"):
        self.ciphertext = '' #Container of the ciphered Text
        isCaps = False
        sub = 0
        nCtr = 0
        print("Plain: ", plaintext)
        while nCtr < len(plaintext):
            value = ord(plaintext[nCtr])
            if value != 32:
                if value < 95:
                    isCaps = True
                    sub = 65
                    temp = (value - sub + self.cipher) % len(self.dictionary)
                    self.ciphertext = self.ciphertext + self.dictionary[temp]
                else:
                    isCaps = False
                    sub = 97
                    temp = (value - sub + self.cipher) % len(self.dictionary)
                    self.ciphertext = self.ciphertext + self.dictionary[temp]
            else:
                self.ciphertext = self.ciphertext + ' '
            nCtr+=1

        print("Cipher: ", self.ciphertext)
        return self.ciphertext
    
    def start_decipher(self, ciphertext):
        if ciphertext:
            plaintext = ""
            charString =""
            newWord = True
            nCtr = 0
            while nCtr < len(ciphertext):
                value = ord(ciphertext[nCtr])
                #If the character is not  a ' '
                if value != 32:
                    charString += ciphertext[nCtr]  
                    for index,i in enumerate(self.dictionary):
                        if charString == i:
                            charString = ""


                            if index < self.cipher:
                                n = len(self.dictionary) + index - self.cipher 
                            else:    
                                n = index - self.cipher

                            if(not newWord):
                                plaintext += self.lower[n%26]
                            else:
                                plaintext += self.upper[n%26]
                            newWord = False
                            break   
                #If the character is a ' '
                else:
                    plaintext += " "
                    newWord = True

                nCtr+=1

            print("DeCipher: ", plaintext)
            return plaintext
    
    def start_dynamic_cipher(self, plaintext="My name is Jeff"):
        self.ciphertext = '' #Container of the ciphered Text
        isCaps = False
        sub = 0
        nCtr = 0
        print("Plain: ", plaintext)
        while nCtr < len(plaintext):
            value = ord(plaintext[nCtr])
            if value != 32:
                if value < 95:
                    isCaps = True
                    sub = 65
                    temp = (value - sub + self.cipher) % len(self.dictionary)
                    self.ciphertext = self.ciphertext + self.dictionary[temp]
                else:
                    isCaps = False
                    sub = 97
                    temp = (value - sub + self.cipher) % len(self.dictionary)
                    self.ciphertext = self.ciphertext + self.dictionary[temp]
                
                print("the cipher ", self.cipher)
                self.def_shift_num((self.cipher+5)%26)
            else:
                self.ciphertext = self.ciphertext + ' '
            nCtr+=1

        print("Cipher: ", self.ciphertext)
        return self.ciphertext
    
    def start_dynamic_decipher(self, ciphertext):
        if ciphertext:
            plaintext = ""
            charString =""
            newWord = True
            nCtr = 0
            while nCtr < len(ciphertext):
                value = ord(ciphertext[nCtr])
                #If the character is not  a ' '
                if value != 32:
                    charString += ciphertext[nCtr]  
                    for index,i in enumerate(self.dictionary):
                        if charString == i:
                            charString = ""

                            index_cipher = self.cipher % 26
                            if index < index_cipher:
                                n = index - index_cipher + len(self.dictionary)
                            else:    
                                n = index - index_cipher
                            
                            print("the n ", n)
                            if(not newWord):
                                plaintext += self.lower[n%26]
                            else:
                                plaintext += self.upper[n%26]
                            newWord = False
                            break
                    self.def_shift_num(self.cipher+5)
                #If the character is a ' '
                else:
                    plaintext += " "
                    newWord = True

                nCtr+=1

            print("DeCipher: ", plaintext)
            return plaintext