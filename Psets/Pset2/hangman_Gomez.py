# Problem Set 2, hangman.py
# Name: Nicolas
# Collaborators: n/a
# Time spent: start 8-9:30

# Hangman Game
# -----------------------------------
# Helper code
# You don't need to understand this helper code,
# but you will have to know how to use the functions
# (so be sure to read the docstrings!)
import random
import string

WORDLIST_FILENAME = "words.txt"


def load_words():
    """
    Returns a list of valid words. Words are strings of lowercase letters.

    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print("Loading word list from file...")
    # inFile: file
    inFile = open(WORDLIST_FILENAME, 'r')
    # line: string
    line = inFile.readline()
    # wordlist: list of strings
    wordlist = line.split()
    print("  ", len(wordlist), "words loaded.")
    return wordlist



def choose_word(wordlist):
    """
    wordlist (list): list of words (strings)

    Returns a word from wordlist at random
    """
    return random.choice(wordlist)

# end of helper code

# -----------------------------------

# Load the list of words into the variable wordlist
# so that it can be accessed from anywhere in the program
wordlist = load_words()


def is_word_guessed(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing; assumes all letters are
      lowercase
    letters_guessed: list (of letters), which letters have been guessed so far;
      assumes that all letters are lowercase
    returns: boolean, True if all the letters of secret_word are in letters_guessed;
      False otherwise
    '''
    for secret_letter in secret_word:
      if secret_letter not in letters_guessed:
        return False
    return True



def get_guessed_word(secret_word, letters_guessed):
    '''
    secret_word: string, the word the user is guessing
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string, comprised of letters, underscores (_), and spaces that represents
      which letters in secret_word have been guessed so far.
    '''
    player_word = []
    for secret_letter in secret_word:
          secret_letter
          if secret_letter in letters_guessed:
            player_word.append(secret_letter)
          else:
            player_word.append('_ ')
    return ''.join(player_word)


def get_available_letters(letters_guessed):
    '''
    letters_guessed: list (of letters), which letters have been guessed so far
    returns: string (of letters), comprised of letters that represents which letters have not
      yet been guessed.
    '''
    alphabet = string.ascii_lowercase
    avaliable_letters = []
    for letter in alphabet:
      if letter not in letters_guessed:
        avaliable_letters.append(letter)
    return ''.join(avaliable_letters)


def hangman(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Remember to make
      sure that the user puts in a letter!

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []

    #calculate base score, number of unique letters
    dict ={}
    for letter in secret_word:
       dict[letter] = ''
    base_score = len(dict)

    print("Welcome to the game Hangman! ")
    print("I am thinking of a word that is ", len(secret_word), "letters long.")
    print("You have ", warnings_remaining, " warnings left" )

    game_state = get_guessed_word(secret_word, letters_guessed)

    while guesses_remaining > 0:
      print("-------------")
      ## check for completed game
      if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won! ")
        total_score = base_score*guesses_remaining
        print("You're total score for this game is: ", total_score)
        break

      print("You have ", guesses_remaining, " guesses left" )
      print("Avaliable letters: ",get_available_letters(letters_guessed))
      guessed_letter = input("Please guess a letter: ")
      # can assume single character input

      ## check if input is a letter and reduce warnings/guesses
      if not guessed_letter.isalpha():
        #reduce warnings if enough avaliable
        if warnings_remaining > 0:
          warnings_remaining += -1
          print ("Oops! That is not a valid letter. You have", warnings_remaining, "warnings left: ", game_state)
        # reduce guess counter if no more warnings
        else:
          guesses_remaining += -1
          print ("Oops! That is not a valid letter. You have no warnings left, so you lose one guess:", game_state)
        #return back to top of while loop for next guess
        continue

      ## check if input has been guessed already and reduce warnings/guesses
      guessed_letter = guessed_letter.lower()
      if guessed_letter in letters_guessed:
        #reduce warnings if enough avaliable
        if warnings_remaining > 0:
          warnings_remaining += -1
          print ("Oops! You've already guessed that letter. You have", warnings_remaining, "warnings left: ", game_state)
        # reduce guess counter if no more warnings
        else:
          guesses_remaining += -1
          print ("Oops! You've already guessed that letter. You have no warnings left, so you lose one guess:", game_state)
        #return back to top of while loop for next guess
        continue

      ## letter is valid, so add to letters guessed
      letters_guessed.append(guessed_letter)

      ## check if letter is in secret_word
      new_gamestate = get_guessed_word(secret_word,letters_guessed)
      ##if no change in gamestate,
      # lose 1 guess if consonant, 2 guesses for vowel
      if (game_state == new_gamestate):
        if guessed_letter in 'aeiou':
          guesses_remaining += -2
        else:
          guesses_remaining += -1
        print("Oops! That letter is not in my word: ", game_state)
        #return back to top of while loop for next guess
        continue
      game_state = new_gamestate
      print("Good guess: ", game_state)

    if guesses_remaining == 0:
      print("-----------")
      print("Sorry, you ran out of guesses. The word was: ", secret_word)


# When you've completed your hangman function, scroll down to the bottom
# of the file and uncomment the first two lines to test
#(hint: you might want to pick your own
# secret_word while you're doing your own testing)


# -----------------------------------



def match_with_gaps(my_word, other_word):
    '''
    my_word: string with _ characters, current guess of secret word
            ex: 't_ _ t'
    other_word: string, regular English word
            ex  'tact
    returns: boolean, True if all the actual letters of my_word match the
        corresponding letters of other_word, or the letter is the special symbol
        _ , and my_word and other_word are of the same length;
        False otherwise:
    '''


    ## get unique letters from my_word
    dict = {}
    for letter in my_word:
      if letter.isalpha:
         dict[letter] = 0
    guessed_letters = list(dict.keys())

    ## get the gaps version of other word.  if they match, its a possible word
    ## this accounts for double letters and length
    other_word_withgaps = get_guessed_word(other_word, guessed_letters)
    if my_word == other_word_withgaps:
      return True
    else:
      return False



def show_possible_matches(my_word):
    '''
    my_word: string with _ characters, current guess of secret word
    returns: nothing, but should print out every word in wordlist that matches my_word
             Keep in mind that in hangman when a letter is guessed, all the positions
             at which that letter occurs in the secret word are revealed.
             Therefore, the hidden letter(_ ) cannot be one of the letters in the word
             that has already been revealed.

    '''
    possible_matches = ''
    for word in wordlist:
        if match_with_gaps(my_word, word):
          possible_matches += word + " "
    if len(possible_matches) == 0:
       print ("No matches found")
    else:
       print(possible_matches)




def hangman_with_hints(secret_word):
    '''
    secret_word: string, the secret word to guess.

    Starts up an interactive game of Hangman.

    * At the start of the game, let the user know how many
      letters the secret_word contains and how many guesses s/he starts with.

    * The user should start with 6 guesses

    * Before each round, you should display to the user how many guesses
      s/he has left and the letters that the user has not yet guessed.

    * Ask the user to supply one guess per round. Make sure to check that the user guesses a letter

    * The user should receive feedback immediately after each guess
      about whether their guess appears in the computer's word.

    * After each guess, you should display to the user the
      partially guessed word so far.

    * If the guess is the symbol *, print out all words in wordlist that
      matches the current guessed word.

    Follows the other limitations detailed in the problem write-up.
    '''
    guesses_remaining = 6
    warnings_remaining = 3
    letters_guessed = []

    #calculate base score, number of unique letters
    dict ={}
    for letter in secret_word:
       dict[letter] = ''
    base_score = len(dict)

    print("Welcome to the game Hangman! ")
    print("I am thinking of a word that is ", len(secret_word), "letters long.")
    print("You have ", warnings_remaining, " warnings left" )

    game_state = get_guessed_word(secret_word, letters_guessed)

    while guesses_remaining > 0:
      print("-------------")
      ## check for completed game
      if is_word_guessed(secret_word, letters_guessed):
        print("Congratulations, you won! ")
        total_score = base_score*guesses_remaining
        print("You're total score for this game is: ", total_score)
        break

      print("You have ", guesses_remaining, " guesses left" )
      print("Avaliable letters: ",get_available_letters(letters_guessed))
      guessed_letter = input("Please guess a letter: ")
      # can assume single character input

      ## HINT MECHANIC: check if input is asterisk, then give hints:
      if guessed_letter == '*':
        print("Possible word matches are:")
        show_possible_matches(game_state)
        continue

      ## check if input is a letter and reduce warnings/guesses
      if not guessed_letter.isalpha():
        #reduce warnings if enough avaliable
        if warnings_remaining > 0:
          warnings_remaining += -1
          print ("Oops! That is not a valid letter. You have", warnings_remaining, "warnings left: ", game_state)
        # reduce guess counter if no more warnings
        else:
          guesses_remaining += -1
          print ("Oops! That is not a valid letter. You have no warnings left, so you lose one guess:", game_state)
        #return back to top of while loop for next guess
        continue

      ## check if input has been guessed already and reduce warnings/guesses
      guessed_letter = guessed_letter.lower()
      if guessed_letter in letters_guessed:
        #reduce warnings if enough avaliable
        if warnings_remaining > 0:
          warnings_remaining += -1
          print ("Oops! You've already guessed that letter. You have", warnings_remaining, "warnings left: ", game_state)
        # reduce guess counter if no more warnings
        else:
          guesses_remaining += -1
          print ("Oops! You've already guessed that letter. You have no warnings left, so you lose one guess:", game_state)
        #return back to top of while loop for next guess
        continue

      ## letter is valid, so add to letters guessed
      letters_guessed.append(guessed_letter)

      ## check if letter is in secret_word
      new_gamestate = get_guessed_word(secret_word,letters_guessed)
      ##if no change in gamestate,
      # lose 1 guess if consonant, 2 guesses for vowel
      if (game_state == new_gamestate):
        if guessed_letter in 'aeiou':
          guesses_remaining += -2
        else:
          guesses_remaining += -1
        print("Oops! That letter is not in my word: ", game_state)
        #return back to top of while loop for next guess
        continue
      game_state = new_gamestate
      print("Good guess: ", game_state)

    if guesses_remaining == 0:
      print("-----------")
      print("Sorry, you ran out of guesses. The word was: ", secret_word)



# When you've completed your hangman_with_hint function, comment the two similar
# lines above that were used to run the hangman function, and then uncomment
# these two lines and run this file to test!
# Hint: You might want to pick your own secret_word while you're testing.


if __name__ == "__main__":
    pass

    # To test part 2, comment out the pass line above and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman(secret_word)

###############

    # To test part 3 re-comment out the above lines and
    # uncomment the following two lines.

    # secret_word = choose_word(wordlist)
    # hangman_with_hints(secret_word)
