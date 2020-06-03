from .hangman_errors import *
class GameInstance:
    def __init__(self):
        self.game_in_progress = False
        self.guessword = None#current word
        self.current_word = [] #currently guessed word
        self.guessed_letters = []
        self.letter_guesses = 0 # guessed letters
        self.word_guesses = 0 #guessed words
        self.remaining_lives = 10 #remaining guesses 
        self.unique_letters = None #unique letters in word
        self.user = None #user playing game

    def start_string(self):
        """Creates the current_word list according to a new word"""
        if self.guessword:
            self.current_word = ["_"]*len(self.guessword)
        return

    def guess_a_letter(self, letter:str)->bool:
        """handles a letter guess"""

        if self.remaining_lives == 0:
            raise GameOverError

        if self.check_win():
            raise GameAlreadyWon

        if letter.upper() in self.guessed_letters:
            raise AlreadyGuessedLetter

        if len(letter)>1 or letter == "":
            raise NotALetterError

        self.validate_letter_input(letter)
        self.letter_guesses+=1
        self.guessed_letters.append(letter.upper())
        was_letter = False
        for i in range(len(self.guessword)):
            if letter.lower() == self.guessword[i]:
                was_letter = True
                self.current_word[i]=letter


        if not was_letter:
            self.remaining_lives-=1

        return was_letter


    def guess_a_word(self, word: str)->bool:
        """Handles a word guess. Returns true if word correct\n
        Otherwise negates 1 from remaining lives and returns false"""
        self.validate_letter_input(word)
        was_word = False

        if self.remaining_lives == 0:
            raise GameOverError

        if self.check_win():
            raise GameAlreadyWon
        
        self.word_guesses+=1
        if word.lower() == self.guessword:
            was_word = True
            for i in range(len(self.guessword)):
                self.current_word[i] = self.guessword[i]
        else:
            self.remaining_lives -=1

        return was_word

    def validate_letter_input(self, inp: str):
        """validate user input"""
        check_spec = inp.split("_")
        check_spec = "".join(check_spec)
        test_spec = check_spec
        for i in range(len(check_spec)):
            if check_spec[i].isnumeric():
                try:
                    index = test_spec.index(check_spec[i])
                    number = test_spec[index]
                    test_spec = test_spec.replace(number, "")
                except:
                    continue

        if inp == "":
            raise InvalidCharactersError
        elif not test_spec.isalpha() and test_spec!="":
            raise InvalidCharactersError
        
        return
    
    def unique(self)->int:
        """counts the amount of unique letters in word"""
        unique_letters = []
        for i in range(len(self.guessword)):
            if self.guessword[i] not in unique_letters:
                unique_letters.append(self.guessword[i])
        
        return len(unique_letters)

    def check_win(self)->bool:
        """Checks if game is won. Method is to be triggered after every guess"""
        if not self.game_in_progress:
            raise NoGameInProgress

        if not "_" in self.current_word:
            return True

    def check_hanged_man(self)->bool:
        """Checks if game has been lost. Method is to be triggered after every guess"""
        if self.remaining_lives == 0:
            self.game_in_progress = False
            return True
        return False

    def get_score(self)->int:
        """returns the game instance's score"""
        guess_score = 150+(self.unique_letters * 100)
        return guess_score

    def new_game(self, newword:str, username:str):
        """Starts new game with argument word"""
        self.game_in_progress = True
        self.guessword = newword.lower()
        self.start_string()
        self.letter_guesses = 0 
        self.word_guesses = 0 
        self.remaining_lives = 10
        self.guessed_letters = []
        self.unique_letters = self.unique()
        self.user = username
        return

    def null(self):
        """Null object"""
        self.guessword = None#current word
        self.current_word = None #currently guessed word 
        self.letter_guesses = 0 
        self.word_guesses = 0 
        self.remaining_lives = 10 #remaining guesses 
        self.unique_letters = None #unique letters in word
        self.user = None #user playing game
        self.guessed_letters = []
        self.game_in_progress = False
        return

    def return_game_data(self)->dict:
        """Returns the game sessions data. Call upon win or loss to retrieve data"""
        game_data = {
            "user": self.user,
            "score": self.get_score(),
            "word": self.guessword,
            "letter_guesses": self.letter_guesses,
            "word_guesses": self.word_guesses
        }
        return game_data
        
