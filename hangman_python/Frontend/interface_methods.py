#This class is the graphical constructor, which creates pieces of the interface. It is puzzled together by the InterfaceMethods class
from datetime import datetime
from .string_graphics import Graphics
class InterfaceMethods:
    """Contains creation methods for interface display"""
    #Default attributes of interface (for interface building)
    MAIN_COMMANDS = [["CURRENT SCORE: ", "REMAINING LIVES: "]]
    COMMANDS_POSITION = 5
    COMMENTS_POSITION = 22
    ITEMS_POSITION = 5
    INPUT_POSITION = 22
    SEARCH_DATE_POSITION = 4
    NEWLINE = "\n"
    


    MAIN_TITLE = "| HANGMAN V1.1 |"
    MAIN_TOP = (len(MAIN_TITLE)-2)*"-"

    def __init__(self, interface_width=100):
        #Varying attributes according to screen size
        self.INTERFACE_WIDTH = interface_width
        self.FRAME_END = " "+((self.INTERFACE_WIDTH-2)*"-")+" "
        self.FRAME_COMMANDS = "|"+((self.INTERFACE_WIDTH-2)*" ")+"|"
        self.FRAME_START = " "+((self.INTERFACE_WIDTH-2)*"-")+" "
        self.MAIN_HEADER = self.INTERFACE_WIDTH*" "
        self.GRAPHICS = Graphics()

    def command_interface(self, current_commands, current_comments, current_menu_title):
        """Returns command menu(display/create/menu) interface as string"""
        command_interface = self.center_align_string(current_menu_title, self.FRAME_COMMANDS, True)
        for i in range(len(current_commands)):
            temp_frame_string = self.FRAME_COMMANDS
            temp_frame_string = self.replace_whitespace(self.COMMANDS_POSITION, current_commands[i], temp_frame_string)
            frame_command = self.replace_whitespace(self.COMMENTS_POSITION, current_comments[i], temp_frame_string)

            command_interface += self.NEWLINE+frame_command
        
        command_interface+=self.NEWLINE+self.FRAME_END
        return command_interface

    def set_main_commands(self, score: int, lives: int):
        change = ["CURRENT SCORE: ", "REMAINING LIVES: "]
        change[0]+=str(score)
        change[1]+=str(lives)
        self.MAIN_COMMANDS[0] = change

    def list_interface(self, datalist, list_title, search_date=None):
        """list_interface(current_object) Returns an interface string for any given list"""        
        current_date = datetime.now()
        dt_string = current_date.strftime("%d.%m.%Y   %H:%M:%S")
        date_time_list = dt_string.split(" ")
        search_date = str(search_date)           

        refresh_date_time = "LAST REFRESH: " + str(dt_string)
        REFRESH_TIME_POSITION = self.INTERFACE_WIDTH-(len(refresh_date_time)+5)

        #list header
        list_header_string = self.FRAME_COMMANDS
        list_header_string = self.center_align_string(list_title, list_header_string)
        list_header_string+="|"+self.NEWLINE

        #date & time header 
        temp_list_string = self.FRAME_COMMANDS
        if search_date:
            temp_list_string = self.replace_whitespace(self.SEARCH_DATE_POSITION, search_date, temp_list_string)
        list_header_string+= self.replace_whitespace(REFRESH_TIME_POSITION, refresh_date_time, temp_list_string)

        #data list
        list_interface = ""
        if len(datalist)!=0:
            list_data_space = int(self.INTERFACE_WIDTH/len(datalist[0]))
            for i in range(len(datalist)):
                new_str = ""
                for q in range(len(datalist[i])-1):
                    initial_temp = str("|" + (list_data_space-1)*" ")
                    if len(str(datalist[i][q]))>list_data_space-2:
                        datalist[i][q] = str(datalist[i][q])[:(list_data_space-4)]
                    temp_current_data = self.center_align_string(str(datalist[i][q]), initial_temp)
                    new_str +=temp_current_data

                remaining_space = self.INTERFACE_WIDTH - len(new_str)
                remaining_string = "|"+ (remaining_space-1)*" "
                remaining_string = self.center_align_string(datalist[i][-1][:remaining_space-2], remaining_string)

                new_str += remaining_string + "|"
                list_interface+=self.NEWLINE + new_str

        return self.NEWLINE+list_header_string+list_interface+self.NEWLINE+self.FRAME_END


    def creation_interface(self, items, input_list, data_header):
        """Returns string of creation or edit sub menu interface"""
        create_interface = ""
        append_create_interface = self.FRAME_COMMANDS
        append_create_interface = self.center_align_string(data_header, append_create_interface)
        create_interface += self.NEWLINE + append_create_interface + "|"

        for i in range(len(items)):
            temp_frame_command = self.FRAME_COMMANDS
            temp_frame_command = self.replace_whitespace(self.ITEMS_POSITION, items[i], temp_frame_command)
            frame_command = self.replace_whitespace(self.INPUT_POSITION, input_list[i], temp_frame_command)

            create_interface += self.NEWLINE+frame_command
        
        create_interface+=self.NEWLINE+self.FRAME_END
        return create_interface

    def head_head(self):
        DEFAULT = self.center_align_string(self.MAIN_TOP, self.MAIN_HEADER)
        DEFAULT +=self.NEWLINE + self.center_align_string(self.MAIN_TITLE, self.MAIN_HEADER)
        DEFAULT += self.NEWLINE + self.FRAME_START+self.NEWLINE
        return DEFAULT

    def default_interface(self):
        """The default header of all screens"""
        DEFAULT = self.center_align_string(self.MAIN_TOP, self.MAIN_HEADER)
        DEFAULT +=self.NEWLINE + self.center_align_string(self.MAIN_TITLE, self.MAIN_HEADER)
        DEFAULT += self.NEWLINE + self.FRAME_START
        datalist = self.MAIN_COMMANDS
        list_interface = ""
        if len(datalist)!=0:
            list_data_space = int(self.INTERFACE_WIDTH/len(datalist[0]))
            for i in range(len(datalist)):
                new_str = ""
                for q in range(len(datalist[i])-1):
                    initial_temp = str("|" + (list_data_space-1)*" ")
                    temp_current_data = self.center_align_string(datalist[i][q], initial_temp)
                    new_str +=temp_current_data

                remaining_space = self.INTERFACE_WIDTH - len(new_str)
                remaining_string = "|"+ (remaining_space-1)*" "
                remaining_string = self.center_align_string(datalist[i][-1], remaining_string)

            new_str += remaining_string + "|"
            list_interface+=self.NEWLINE + new_str

        DEFAULT +=list_interface+self.NEWLINE+self.FRAME_END+self.NEWLINE
        return DEFAULT


    def feedback_interface(self, msg):
        """Creates an addon feedback string for interface when called"""
        temp_string = self.FRAME_COMMANDS
        message_header = self.center_align_string(msg, temp_string, True)
        
        message_header+=self.NEWLINE+self.FRAME_END
        return self.NEWLINE + message_header

    def instruction_window(self, user_command_input, instruction_dict):
        """Creates an instruction window for interface when a prompt command is entered"""
        instruction = instruction_dict[user_command_input]
        if instruction == None:
            return None
        temp_interface_string = self.FRAME_COMMANDS
        interface_instruction = self.center_align_string(instruction, temp_interface_string, True)
        interface_instruction +=self.NEWLINE+self.FRAME_END
        return self.NEWLINE + interface_instruction

    def replace_whitespace(self, position, replacement_string, initial_string):
        """Method replaces whitespace on a given input location - replace_whitespace(position, replacement_string, initial_string)"""
        total_length = len(initial_string)
        temp_start = initial_string[:position]
        temp_start +=replacement_string
        temp_end = initial_string[len(temp_start):]

        final_string = temp_start+temp_end
        return final_string

    def center_align_string(self, replacement_string, initial_string, header=False):
        """Method center aligns an input string in the second argument string -center_align_string(replacement_string, initial_string, header=False)"""
        start_position_replacement = int(len(initial_string)/2)-int(len(replacement_string)/2)
        temp_new_datastring = initial_string[:start_position_replacement]
        temp_new_datastring +=replacement_string
        max_length = len(initial_string)
        remaining_space = max_length-len(temp_new_datastring)
        if header:
            final_string = temp_new_datastring + (remaining_space-1)*" "+"|"
        else:
            final_string = temp_new_datastring + (remaining_space-1)*" "
        return final_string

    def hangman_graphics(self, remaining_lives, guessed_letters, current_word):
        hangman_figure = self.GRAPHICS.get_image(remaining_lives)
        list_figure = hangman_figure.split("\n")
        interface_piece = self.NEWLINE
        initial_string = "|"+" "*(int(self.INTERFACE_WIDTH/2)-1)
        initial2_string = " "*(int(self.INTERFACE_WIDTH/2))+"|"

        string_word, string_guessd = self.hangman_letters(guessed_letters, current_word)
        word_height_pos = len(list_figure)-2
        guessed_height_pos = len(list_figure)-8
        for i in range(len(list_figure)):
            interface_piece += self.center_align_string(list_figure[i], initial_string)
            if i==word_height_pos-1:
                remaining_piece = self.center_align_string("YOUR WORD:", initial2_string, True)
            elif i==word_height_pos:
                remaining_piece = self.center_align_string(string_word, initial2_string, True)
            elif i==guessed_height_pos-1:
                remaining_piece = self.center_align_string("GUESSED LETTERS:", initial2_string, True)
            elif i==guessed_height_pos:
                remaining_piece = self.center_align_string(string_guessd, initial2_string, True)
            else:
                remaining_piece = initial2_string

            interface_piece+=remaining_piece
            interface_piece += self.NEWLINE
        
        interface_piece+=self.FRAME_END
        return interface_piece

    def hangman_endgame_graphics(self, remaining_lives, current_word: list, total_word_guesses: int, total_letter_guesses: int, total_score: int):
        hangman_figure = self.GRAPHICS.get_image(remaining_lives)
        list_figure = hangman_figure.split("\n")
        interface_piece = self.NEWLINE
        initial_string = "|"+" "*(int(self.INTERFACE_WIDTH/2)-1)
        initial2_string = " "*(int(self.INTERFACE_WIDTH/2))+"|"
        string_word, string_guessed = self.hangman_letters([], current_word)
        word_height_pos = len(list_figure)-2
        guessed_height_pos = len(list_figure)-8
        for i in range(len(list_figure)):
            interface_piece += self.center_align_string(list_figure[i], initial_string)
            if i==word_height_pos-1:
                remaining_piece = self.center_align_string("YOUR WORD:", initial2_string, True)
            elif i==word_height_pos:
                remaining_piece = self.center_align_string(string_word, initial2_string, True)
            elif i==guessed_height_pos-1:
                remaining_piece = self.center_align_string("GAME OVER! SUMMARY: ", initial2_string, True)
            elif i==guessed_height_pos:
                remaining_piece = self.center_align_string("Total word guesses: "+str(total_word_guesses), initial2_string, True)
            elif i==guessed_height_pos+1:
                remaining_piece = self.center_align_string("Total letter guesses: "+str(total_letter_guesses), initial2_string, True)
            elif i==guessed_height_pos+2:
                remaining_piece = self.center_align_string("Total score: "+str(total_score), initial2_string, True)
            else:
                remaining_piece = initial2_string

            interface_piece+=remaining_piece
            interface_piece += self.NEWLINE
        
        interface_piece+=self.FRAME_END
        return interface_piece

    def hangman_letters(self, guessed_letters: list, current_word: list)->str:
        string_word = ""
        for i in range(len(current_word)):
            string_word+=current_word[i].upper()+" "
        
        string_guessed = ""
        for i in range(len(guessed_letters)):
            string_guessed+=guessed_letters[i]+", "

        return string_word, string_guessed
            
