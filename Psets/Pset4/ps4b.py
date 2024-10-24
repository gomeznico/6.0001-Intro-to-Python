# Problem Set 4B
# Name: Nico Gomez
# Collaborators:
# Time Spent: 3:00

import string

### HELPER CODE ###
def load_words(file_name):
    '''
    file_name (string): the name of the file containing
    the list of words to load

    Returns: a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    '''
    print("Loading word list from file...")
    # inFile: file
    inFile = open(file_name, 'r')
    # wordlist: list of strings
    wordlist = []
    for line in inFile:
        wordlist.extend([word.lower() for word in line.split(' ')])
    print("  ", len(wordlist), "words loaded.")
    return wordlist

def is_word(word_list, word):
    '''
    Determines if word is a valid word, ignoring
    capitalization and punctuation

    word_list (list): list of words in the dictionary.
    word (string): a possible word.

    Returns: True if word is in word_list, False otherwise

    Example:
    >>> is_word(word_list, 'bat') returns
    True
    >>> is_word(word_list, 'asdf') returns
    False
    '''
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\:;'<>?,./\"")
    return word in word_list

def get_story_string():
    """
    Returns: a story in encrypted text.
    """
    f = open("story.txt", "r")
    story = str(f.read())
    f.close()
    return story

### END HELPER CODE ###

WORDLIST_FILENAME = 'words.txt'

class Message(object):
    def __init__(self, text):
        '''
        Initializes a Message object

        text (string): the message's text

        a Message object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        self.message_text = text
        self.valid_words = load_words(WORDLIST_FILENAME)

    def get_message_text(self):
        '''
        Used to safely access self.message_text outside of the class

        Returns: self.message_text
        '''

        return self.message_text

    def get_valid_words(self):
        '''
        Used to safely access a copy of self.valid_words outside of the class.
        This helps you avoid accidentally mutating class attributes.

        Returns: a COPY of self.valid_words
        '''

        return self.valid_words.copy()

    def build_shift_dict(self, shift):
        '''
        Creates a dictionary that can be used to apply a cipher to a letter.
        The dictionary maps every uppercase and lowercase letter to a
        character shifted down the alphabet by the input shift. The dictionary
        should have 52 keys of all the uppercase letters and all the lowercase
        letters only.

        shift (integer): the amount by which to shift every letter of the
        alphabet. 0 <= shift < 26

        Returns: a dictionary mapping a letter (string) to
                 another letter (string).
        '''
        uppercase = string.ascii_uppercase
        lowercase = string.ascii_lowercase

        cipher = {}
        for i in range(26):
            shift_index = (i+shift)%26
            cipher[uppercase[i]] = uppercase[shift_index]
            cipher[lowercase[i]] = lowercase[shift_index]

        return cipher

    def apply_shift(self, shift):
        '''
        Applies the Caesar Cipher to self.message_text with the input shift.
        Creates a new string that is self.message_text shifted down the
        alphabet by some number of characters determined by the input shift

        shift (integer): the shift with which to encrypt the message.
        0 <= shift < 26

        Returns: the message text (string) in which every character is shifted
        down the alphabet by the input shift
        '''

        cipher = self.build_shift_dict(shift)
        message = list(self.get_message_text())

        for i in range(len(message)):
            letter = message[i]
            if letter.isalpha():
                message[i] = cipher[letter]

        message = ''.join(message)
        return message
class PlaintextMessage(Message):
    def __init__(self, text, shift):
        '''
        Initializes a PlaintextMessage object

        text (string): the message's text
        shift (integer): the shift associated with this message

        A PlaintextMessage object inherits from Message and has five attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
            self.shift (integer, determined by input shift)
            self.encryption_dict (dictionary, built using shift)
            self.message_text_encrypted (string, created using shift)

        '''
        Message.__init__(self,text)
        # init instance of Message
        # it will inherit self.message_text and self.valid_words

        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

    def get_shift(self):
        '''
        Used to safely access self.shift outside of the class

        Returns: self.shift
        '''

        return self.shift

    def get_encryption_dict(self):
        '''
        Used to safely access a copy self.encryption_dict outside of the class

        Returns: a COPY of self.encryption_dict
        '''

        return self.encryption_dict.copy()

    def get_message_text_encrypted(self):
        '''
        Used to safely access self.message_text_encrypted outside of the class

        Returns: self.message_text_encrypted
        '''

        return self.message_text_encrypted

    def change_shift(self, shift):
        '''
        Changes self.shift of the PlaintextMessage and updates other
        attributes determined by shift.

        shift (integer): the new shift that should be associated with this message.
        0 <= shift < 26

        Returns: nothing
        '''

        self.shift = shift
        self.encryption_dict = self.build_shift_dict(shift)
        self.message_text_encrypted = self.apply_shift(shift)

class CiphertextMessage(Message):
    def __init__(self, text):
        '''
        Initializes a CiphertextMessage object

        text (string): the message's text

        a CiphertextMessage object has two attributes:
            self.message_text (string, determined by input text)
            self.valid_words (list, determined using helper function load_words)
        '''

        Message.__init__(self,text)
        # init instance of Message
        # it will inherit self.message_text and self.valid_words

    def decrypt_message(self):
        '''
        Decrypt self.message_text by trying every possible shift value
        and find the "best" one. We will define "best" as the shift that
        creates the maximum number of real words when we use apply_shift(shift)
        on the message text. If s is the original shift value used to encrypt
        the message, then we would expect 26 - s to be the best shift value
        for decrypting it.

        Note: if multiple shifts are equally good such that they all create
        the maximum number of valid words, you may choose any of those shifts
        (and their corresponding decrypted messages) to return

        Returns: a tuple of the best shift value used to decrypt the message
        and the decrypted message text using that shift value
        '''

        max_words = 0
        output = (0,self.get_message_text())

        for shift in range(26):
            # create deciphered text and array of 'words'
            deciphered_text = self.apply_shift(shift)
            words = deciphered_text.split()
            real_word_count = 0



            #check each word if is valid and add to count
            for word in words:
                if is_word(self.get_valid_words(), word):
                    real_word_count += 1

            if real_word_count > max_words:
                max_words = real_word_count
                output = (shift, deciphered_text)
        return output



if __name__ == '__main__':


    ##Part 1 Message Object
    print("TESTING MESSAGE OBJECT")
    new_message = Message('hello world!')
    print('Expected Output: hello world!')
    print('  Actual Output: ', new_message.message_text)

    shift = 4

    print("Testing applied shift")
    print('Expected Output: lipps asvph!')
    print('Actual Output:  ', new_message.apply_shift(shift))
    print("----------")

    #Part 2 PlaintextMessage Object
    print("TESTING PLAINTEXTMESSAGE OBJECT")
    plaintext = PlaintextMessage('hello world!', shift)
    print('Expected Output: lipps asvph!')
    print('Actual Output:  ', plaintext.get_message_text_encrypted())


    plaintext.change_shift(shift+4)
    print('Expected Output: pmttw ewztl!')
    print('Actual Output:  ', plaintext.get_message_text_encrypted())

    print('Expected Output: hello world!')
    print('Actual Output:  ', plaintext.get_message_text())
    print("----------")


    #Part 3 CiphertextMessage
    print("TESTING CIPHERTEXTMESSAGE OBJECT")
    ciphertext = CiphertextMessage('pmttw ewztl!')
    print('Expected Output:', (18, 'hello world!'))
    print('Actual Output:  ', ciphertext.decrypt_message())

    encrypted_story = get_story_string()
    ciphertext = CiphertextMessage(encrypted_story)
    print(ciphertext.decrypt_message())
