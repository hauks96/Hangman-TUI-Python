from .GameGraphics import GameGraphics
from Logic.hangman_Master import HangmanMaster
from os import system, name 
class InterfaceMaster:
    """I've not commented the methods but they are self explanatory by viewing the function calls to logic master"""
    def __init__(self):
        self.logic = HangmanMaster()
        self.graphics = GameGraphics()
        self.current_graphics = self.graphics.main_menu
    
    def clear(self):
        """Clears screen according to operating system"""
        if name == "nt":
            _ = system("cls")
        else:
            _ = system("clear")
        return

    def main_menu(self):
        self.current_graphics = self.graphics.main_menu
        self.clear()
        print(self.current_graphics)
        commands = ["login", "logout", "play", "cacc", "hist", "top", "lists", 'resize', 'exit']
        while True:
            command_request = input("")
            if command_request in commands:
                if command_request == "login":
                    self.login()
                elif command_request == "logout":
                    self.logout()
                elif command_request == "play":
                    self.play()
                elif command_request == "cacc":
                    self.create_acc()
                elif command_request == "hist":
                    self.history()
                elif command_request == "top":
                    self.leaderboard()
                elif command_request == "lists":
                    self.wordlist()
                elif command_request == "resize":
                    self.resize()
                elif command_request == "exit":
                    quit()

            else:
                feedback_graphic = self.graphics.feedback_graphics("Command not recognized.")
                self.clear()
                print(self.current_graphics+feedback_graphic)

    def resize(self):
        feedback_graphics = self.graphics.feedback_graphics("Enter new size. 100-140 Recommended")
        self.clear()
        print(self.current_graphics+feedback_graphics)
        new_width = input("")
        if not new_width.isnumeric():
            feedback_graphics = self.graphics.feedback_graphics("Invalid number")
            self.clear()
            print(self.current_graphics+feedback_graphics)
            return
        if int(new_width)>220 or int(new_width)<86:
            feedback_graphics = self.graphics.feedback_graphics("Number must be between 85 and 220")            
            self.clear()
            print(self.current_graphics+feedback_graphics)
            return
        self.graphics.set_interface_width(int(new_width))
        self.current_graphics = self.graphics.main_menu
        self.clear()
        print(self.current_graphics)
        return

    def login(self):
        commands = ["usn", "pw", "confirm", "back"]
        username = ""
        password = ""
        self.current_graphics = self.graphics.log_in_interface_graphics()
        self.clear()
        print(self.current_graphics)
        while True:
            command_request = input("")
            if command_request in commands:
                if command_request == "usn":
                    feedback_graphic = self.graphics.feedback_graphics("Enter username")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    username = input()
                    self.current_graphics = self.graphics.log_in_interface_graphics(username, password)
                    self.clear()
                    print(self.current_graphics)

                elif command_request == "pw":
                    feedback_graphic = self.graphics.feedback_graphics("Enter password")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    password = input()
                    self.current_graphics = self.graphics.log_in_interface_graphics(username, password)
                    self.clear()
                    print(self.current_graphics)

                elif command_request == "confirm":
                    logic_data = self.logic.log_in(username, password)
                    if logic_data["Success"]==True:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Message"])
                        self.current_graphics = self.graphics.main_menu
                        self.clear()
                        print(self.current_graphics+feedback_graphic)
                        return
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                        self.clear()
                        print(self.current_graphics+feedback_graphic)

                elif command_request == "back":
                    self.current_graphics = self.graphics.main_menu
                    self.clear()
                    print(self.current_graphics)
                    return
            else:
                feedback_graphic = self.graphics.feedback_graphics("Command not recognized.")
                self.clear()
                print(self.current_graphics+feedback_graphic)

    def logout(self):
        logic_data = self.logic.log_out()
        if logic_data["Success"]==True:
            feedback_graphic = self.graphics.feedback_graphics(logic_data["Message"])
        else:
            feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
        self.clear()
        print(self.current_graphics+feedback_graphic)
        return

    def create_acc(self):
        commands = ["usn", "pw1", "pw2", "confirm", "back"]
        username = ""
        password1= ""
        password2= ""
        self.current_graphics = self.graphics.create_account_graphics()
        self.clear()
        print(self.current_graphics)
        while True:
            command_request = input("")
            if command_request in commands:
                if command_request == "usn":
                    self.current_graphics = self.graphics.create_account_graphics(username, password1, password2)
                    feedback_graphic = self.graphics.feedback_graphics("Enter username")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    username = input("")
                    self.current_graphics = self.graphics.create_account_graphics(username, password1, password2)
                    self.clear()
                    print(self.current_graphics)

                elif command_request == "pw1":
                    self.current_graphics = self.graphics.create_account_graphics(username, password1, password2)
                    feedback_graphic = self.graphics.feedback_graphics("Enter password")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    password1 = input("")
                    self.current_graphics = self.graphics.create_account_graphics(username, password1, password2)
                    self.clear()
                    print(self.current_graphics)

                elif command_request == "pw2":
                    self.current_graphics = self.graphics.create_account_graphics(username, password1, password2)
                    feedback_graphic = self.graphics.feedback_graphics("Re enter password")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    password2 = input("")
                    self.current_graphics = self.graphics.create_account_graphics(username, password1, password2)
                    self.clear()
                    print(self.current_graphics)

                elif command_request == "confirm":
                    logic_data = self.logic.create_user(username, password1, password2)
                    if logic_data["Success"]==True:
                        self.current_graphics = self.graphics.main_menu
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Message"])
                        self.clear()
                        print(self.current_graphics+feedback_graphic)
                        return
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                        self.clear()
                        print(self.current_graphics+feedback_graphic)

                elif command_request == "back":
                    self.current_graphics = self.graphics.main_menu
                    self.clear()
                    print(self.current_graphics)
                    return
            else:
                feedback_graphic = self.graphics.feedback_graphics("Command not recognized.")
                self.clear()
                print(self.current_graphics+feedback_graphic)

    def history(self):
        commands = ["back"]
        logic_data = self.logic.get_user_last10()
        if logic_data["Success"]==False:
            feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
            self.clear()
            print(self.current_graphics+feedback_graphic)
            return

        self.current_graphics = self.graphics.history_graphics(logic_data["Data"])
        self.clear()
        print(self.current_graphics)

        while True:
            command_request = input()
            if command_request in commands:
                if command_request == "back":
                    self.current_graphics = self.graphics.main_menu
                    self.clear()
                    print(self.current_graphics)
                    return
            else:
                feedback_graphic = self.graphics.feedback_graphics("Command not recognized.")
                self.clear()
                print(self.current_graphics+feedback_graphic)

    def leaderboard(self):
        commands = ["back", "me", "all"]
        logic_data = self.logic.get_top10()
        if logic_data["Success"]==False:
            feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
            self.clear()
            print(self.current_graphics+feedback_graphic)
            return

        self.current_graphics = self.graphics.top_10_graphics(logic_data["Data"])
        self.clear()
        print(self.current_graphics)

        while True:
            command_request = input()
            if command_request in commands:
                if command_request == "back":
                    self.current_graphics = self.graphics.main_menu
                    self.clear()
                    print(self.current_graphics)
                    return
                elif command_request == "all":
                    logic_data = self.logic.get_top10()
                    if logic_data["Success"]==False:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                        self.clear()
                        print(self.current_graphics+feedback_graphic)

                    else:
                        self.current_graphics = self.graphics.top_10_graphics(logic_data["Data"])
                        self.clear()
                        print(self.current_graphics)

                elif command_request == "me":
                    logic_data = self.logic.get_users_top10()
                    if logic_data["Success"]==False:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                        self.clear()
                        print(self.current_graphics+feedback_graphic)
                    else:
                        self.current_graphics = self.graphics.top_10_graphics(logic_data["Data"])
                        self.clear()
                        print(self.current_graphics)
            else:
                feedback_graphic = self.graphics.feedback_graphics("Command not recognized.")
                self.clear()
                print(self.current_graphics+feedback_graphic)
    
    def wordlist(self):
        commands = ["create", "select", "add", "remove", "rmtable", "back"]
        logic_data = self.logic.get_tables_and_names() #ADD WORDCOUNT
        if logic_data["Success"]==False:
            feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
            self.clear()
            print(self.current_graphics+feedback_graphic)
            return

        self.current_graphics = self.graphics.word_list_graphics(logic_data["Data"], self.logic.current_table)
        feedb_str = "Current Table: " +self.logic.current_table
        feedback_graphic = self.graphics.feedback_graphics(feedb_str)
        self.clear()
        print(self.current_graphics+feedback_graphic)
        
        while True:
            command_request = input()
            if command_request in commands:
                if command_request == "create":
                    feedback_graphic = self.graphics.feedback_graphics("Enter new table's name")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    tablename = input()
                    logic_data = self.logic.create_table(tablename)
                    if logic_data["Success"]==True:
                        new_logic_data = self.logic.get_tables_and_names()
                        self.current_graphics = self.graphics.word_list_graphics(new_logic_data["Data"], self.logic.current_table)
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Message"])
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                    self.clear()
                    print(self.current_graphics+feedback_graphic)

                elif command_request == "select":
                    feedback_graphic = self.graphics.feedback_graphics("Enter name of table to select")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    tablename = input()
                    logic_data = self.logic.change_current_table(tablename)
                    if logic_data["Success"]==True:
                        new_word_list = self.logic.get_tables_and_names()
                        if new_word_list["Success"]==True:
                            self.current_graphics= self.graphics.word_list_graphics(new_word_list["Data"], self.logic.current_table)
                            feedback_graphic = self.graphics.feedback_graphics(logic_data["Message"])
                            print(self.current_graphics+feedback_graphic)
                        else:
                            feedback_graphic = self.graphics.feedback_graphics(new_word_list["Error"])
                            print(self.current_graphics+feedback_graphic)
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                    self.clear()
                    print(self.current_graphics+feedback_graphic)

                elif command_request == "add":
                    feedback_graphic = self.graphics.feedback_graphics("Enter new word to add to table '"+self.logic.current_table+"'.")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    new_word = input()
                    logic_data = self.logic.insert_word(new_word)
                    if logic_data["Success"]==True:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Message"])
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                    self.clear()
                    print(self.current_graphics+feedback_graphic)

                elif command_request == "remove":
                    feedback_graphic = self.graphics.feedback_graphics("Enter word to remove from table '"+self.logic.current_table+"'.")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    delete_word = input()
                    logic_data = self.logic.delete_word(delete_word)
                    if logic_data["Success"]==True:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Message"])
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                    self.clear()
                    print(self.current_graphics+feedback_graphic)

                elif command_request == "rmtable":
                    feedback_graphic = self.graphics.feedback_graphics("Enter name of table to remove")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    delete_table = input()
                    logic_data = self.logic.remove_table(delete_table)
                    if logic_data["Success"]==True:
                        logic_data = self.logic.get_tables_and_names()
                        if logic_data["Success"]==False:
                            feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                            self.clear()
                            print(self.current_graphics+feedback_graphic)
                        else:
                            self.current_graphics = self.graphics.word_list_graphics(logic_data["Data"], logic_data['current_table'])
                            feedb_str = "Current Table: " +self.logic.current_table
                            feedback_graphic = self.graphics.feedback_graphics(feedb_str)
                            self.clear()
                            print(self.current_graphics+feedback_graphic)
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                    self.clear()
                    print(self.current_graphics+feedback_graphic)

                elif command_request == "back":
                    self.current_graphics = self.graphics.main_menu
                    self.clear()
                    print(self.current_graphics)
                    return
            else:
                feedback_graphic = self.graphics.feedback_graphics("Command not recognized.")
                self.clear()
                print(self.current_graphics+feedback_graphic)

    def play(self):
        commands = ["-l", "-w", "-esc"]
        logic_data = self.logic.play_game()
        if logic_data["Success"]==False:
            feedback_message = self.graphics.feedback_graphics(logic_data["Error"])
            print(self.current_graphics+self.feeback_message)
            return
        
        self.current_graphics = self.graphics.set_ingame_graphics(logic_data["Message"], logic_data["Remaining_lives"],
                                                            logic_data["Current_word"], logic_data["Guessed_letters"], logic_data['Current_score'])
        self.clear()
        print(self.current_graphics)
        
        while True:
            command_request = input("")
            if command_request in commands:
                if command_request == "-l":
                    feedback_graphic = self.graphics.feedback_graphics("Enter letter to guess")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    guess_letter = input()
                    logic_data = self.logic.guess_letter(guess_letter)
                    logic_lose_check = self.logic.check_loss()
                    if logic_lose_check["Game_lost"]==True:
                        logic_data = self.logic.end_game()
                        self.current_graphics = self.graphics.set_ingame_end_graphics(
                            logic_data['Message'], 0, logic_data['Current_word'], logic_data['Word_guesses'],
                            logic_data['Letter_guesses'], logic_data['Score'])
                        self.clear()
                        print(self.current_graphics)
                        self.end_game_input()
                        return
                    elif logic_data["Success"]==True:
                        self.current_graphics = self.graphics.set_ingame_graphics(
                            logic_data["Message"], logic_data["Remaining_lives"],
                            logic_data["Current_word"], logic_data["Guessed_letters"],logic_data['Current_score'])
                        self.clear()
                        print(self.current_graphics)
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                        self.clear()
                        print(self.current_graphics+feedback_graphic)

                elif command_request == "-w":
                    feedback_graphic = self.graphics.feedback_graphics("Enter word to guess")
                    self.clear()
                    print(self.current_graphics+feedback_graphic)
                    guess_word = input()
                    logic_data = self.logic.guess_word(guess_word)
                    logic_lose_check = self.logic.check_loss()
                    if logic_lose_check["Game_lost"]==True:
                        logic_data = self.logic.end_game()
                        self.current_graphics = self.graphics.set_ingame_end_graphics(
                            logic_data['Message'], 0, logic_data['Current_word'], logic_data['Word_guesses'],
                            logic_data['Letter_guesses'], logic_data['Score'])
                        self.clear()
                        print(self.current_graphics)
                        self.end_game_input()
                        return
                    elif logic_data["Success"]==True:
                        self.current_graphics = self.graphics.set_ingame_graphics(
                            logic_data["Message"], logic_data["Remaining_lives"],
                            logic_data["Current_word"], logic_data["Guessed_letters"], logic_data['Current_score'])
                        self.clear()
                        print(self.current_graphics)
                    else:
                        feedback_graphic = self.graphics.feedback_graphics(logic_data["Error"])
                        self.clear()
                        print(self.current_graphics+feedback_graphic)

                elif command_request == "-esc":
                    self.logic.end_game()
                    self.current_graphics = self.graphics.main_menu
                    self.clear()
                    print(self.current_graphics)
                    return

            else:
                feedback_graphic = self.graphics.feedback_graphics("Command not recognized.")
                self.clear()
                print(self.current_graphics+feedback_graphic)

    def end_game_input(self):
        commands = ["back"]
        command_request = input()
        if command_request in commands:
            if command_request == "back":
                self.current_graphics = self.graphics.main_menu
                self.clear()
                print(self.current_graphics)
                return
        else:
            feedback_graphic = self.graphics.feedback_graphics("Command not recognized.")
            self.clear()
            print(self.current_graphics+feedback_graphic)
