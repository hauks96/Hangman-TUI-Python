#This class pieces together the interface menu's for the relevant screen, by using the InterfaceMethods class
from .interface_methods import InterfaceMethods
class GameGraphics:
    def __init__(self):
        self.score = 0
        self.IFmethods =InterfaceMethods()
        self.defaultheader = self.IFmethods.head_head()

        self.wordlist_view_default = self.word_list_default()
        self.create_acc_default = self.create_account_interface_default()
        self.login_acc_default = self.log_in_interface_default()
        self.history_view_default = self.default_interface_history()
        self.leaderboard_view_default = self.default_interface_top10()
        self.main_menu = self.main_menu_graphics()

    def set_interface_width(self, new_width:int):
        new_interface_methods = InterfaceMethods(int(new_width))
        self.IFmethods = new_interface_methods
        self.defaultheader = self.IFmethods.head_head()

        self.wordlist_view_default = self.word_list_default()
        self.create_acc_default = self.create_account_interface_default()
        self.login_acc_default = self.log_in_interface_default()
        self.history_view_default = self.default_interface_history()
        self.leaderboard_view_default = self.default_interface_top10()
        self.main_menu = self.main_menu_graphics()
        return
        
    def set_ingame_graphics(self, msg: str, remaining_lives: int, current_word: list, guessed_letters: list, score: int=None):
        """Creates the ingame interface"""
        if score:
            self.score = score
        the_interface = ""
        header = self.header_graphics_ingame(remaining_lives)
        commands = ["-l", "-w", "-esc"]
        comments = ["// Guess a letter", "// Guess a word", "// End game and go to main menu"]
        title = "IN GAME COMMANDS"
        command_if = self.IFmethods.command_interface(commands, comments, title)
        game = self.ingame_graphics(remaining_lives, current_word, guessed_letters)
        feedback = self.feedback_graphics(msg)
        the_interface+=header+command_if+game+feedback
        return the_interface

    def set_ingame_end_graphics(self, msg: str, remaining_lives: int, current_word: list, total_word_guesses: int, total_letter_guesses:int, total_score: int):
        self.IFmethods.hangman_endgame_graphics(remaining_lives, current_word, total_word_guesses, total_letter_guesses, total_score)
        if total_score:
            self.score = total_score
        the_interface = ""
        header = self.header_graphics_ingame(remaining_lives)
        commands = ["back"]
        comments = ["// Back to main menu"]
        title = "GAME ENDED"
        command_if = self.IFmethods.command_interface(commands, comments, title)
        endgame = self.IFmethods.hangman_endgame_graphics(remaining_lives, current_word, total_word_guesses, total_letter_guesses, total_score)
        feedback = self.feedback_graphics(msg)
        the_interface+=header+command_if+endgame+feedback
        return the_interface

    def header_graphics_ingame(self, remaining_lives)->str:
        """Creates the default header for a running hangman game"""
        #DEFAULT HEADER
        self.IFmethods.set_main_commands( self.score, remaining_lives)
        default_game = self.IFmethods.default_interface()
        return default_game

    def feedback_graphics(self, msg):
        """Is to be used for error display or message display"""
        return self.IFmethods.feedback_interface(msg)

    def ingame_graphics(self, remaining_lives:int, current_word: list, guessed_letters: list):
        """Triggered through set_ingame_graphics method"""
        return self.IFmethods.hangman_graphics(remaining_lives, guessed_letters, current_word)

    def main_menu_graphics(self)->str:
        """Triggered on object creation. Not to be used unless screen resizing"""
        commands = ["login", "logout", "play", "cacc", "hist", "top", "lists", 'resize', 'exit']
        comments = ["// Log in to account", "// Log out of account", "// Play hangman", "// Create an account", 
        "// Check your game history", "// Check leaderboard", "// Edit/View available word lists", '// Resize the interface', '// Close game']
        title = "MAIN MENU COMMANDS"
        main_interface = ""
        main = self.IFmethods.command_interface(commands, comments, title)
        main_interface+=self.defaultheader+main
        return main_interface

    def create_account_interface_default(self)->str:
        """Triggered on object creation. Not to be used unless screen resizing"""
        commands = ["usn", "pw1", "pw2", "confirm", "back"]
        comments = ["// Enter username", "// Enter password", "// Enter password again", "// Confirm creation", "// Navigate back to main menu"]
        title = "CREATE ACCOUNT COMMANDS"
        return self.IFmethods.command_interface(commands, comments, title)
    
    def create_account_graphics(self, usn="", pw1="", pw2="")->str:
        """Is to be triggered every time a new input is made in account creation"""
        items = ["Username: ", "Password: ", "Re-Password: "]
        input_list = [usn, "*"*len(pw1), "*"*len(pw2)]
        data_header = "CREATION DATA"
        create = self.IFmethods.creation_interface(items, input_list, data_header)
        return self.defaultheader+self.create_acc_default+create


    def log_in_interface_default(self)->str:
        """Triggered on object creation. Not to be used unless screen resizing"""
        commands = ["usn", "pw", "confirm", "back"]
        comments = ["// Enter username", "// Enter password", "// Log in with input data", "// Navigate back to main menu"]
        title = "LOGIN COMMANDS"
        return self.IFmethods.command_interface(commands, comments, title)

    def log_in_interface_graphics(self, usn ="", pw="")->str:
        """Is to be triggered every time a new input is made inlogin menu"""
        items = ["Username: ", "Password: "]
        input_list = [usn, "*"*len(pw)]
        data_header = "LOGIN DETAILS"
        login = self.IFmethods.creation_interface(items, input_list, data_header)
        return self.defaultheader+self.login_acc_default+login

    def default_interface_history(self)->str:
        """Triggered on object creation. Not to be used unless screen resizing"""
        commands = ["back"]
        comments = ["// Back to main menu"]
        title = "HISTORY VIEW COMMANDS"
        return self.IFmethods.command_interface(commands, comments, title)

    def history_graphics(self, data_list)->str:
        """Is to be triggered every time history menu is requested"""
        title = "USER HISTORY"
        history = self.IFmethods.list_interface(data_list, title)
        return self.defaultheader+self.history_view_default+history

    def default_interface_top10(self)->str:
        """Triggered on object creation. Not to be used unless screen resizing"""
        commands = ["back", "all", "me"]
        comments = ["// Back to main menu", "// Shows overall leaderboard", "// Shows your top 10 scores"]
        title = "LEADERBOARD VIEW COMMANDS"
        return self.IFmethods.command_interface(commands, comments, title)

    def top_10_graphics(self, data_list)->str:
        """Is to be triggered every time leaderboard menu is requested"""
        title = "LEADERBOARD"
        leadboard =self.IFmethods.list_interface(data_list, title, search_date="")
        return self.defaultheader+self.leaderboard_view_default+leadboard

    def word_list_default(self)->str:
        commands = ["create", "select", "add", "remove", "rmtable", "back"]
        comments = ["// Create a new word list", "// Select another word list to play", 
        "// Add a new word to a word list", "// Remove a word from a word list", "// Delete table", "// Back to main menu"]
        title = "WORD LIST COMMANDS"
        word_list_def = self.IFmethods.command_interface(commands, comments, title)
        return word_list_def

    def word_list_graphics(self, data_list: list, current_table: str)->str:
        wordlist = ""
        wordlist+=self.defaultheader+self.wordlist_view_default
        w_list = self.IFmethods.list_interface(data_list, "AVAILABLE WORD LISTS", "CURRENT TABLE: "+str(current_table))
        return wordlist+w_list


        
