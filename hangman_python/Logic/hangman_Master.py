from .game_instance import GameInstance
import requests
from base64 import b64encode
from .hangman_errors import *
class HangmanMaster:
    def __init__(self):
        self.url = 'https://hangmanserver.herokuapp.com/hangman/api/v1/'
        self.current_table = "Hangman"
        self.gameInstance = GameInstance()
        self.game_session = []
        self.current_score = 0
        self.user = None
        self.password = None
        self.logged_in = False
        self.token = None
        self.tables = self.init_tables()

    def invalid_characters(self)->dict:
        """Returns the error format for error InvalidCharactersError
        ["Success": bool]=False -> ["Error": str]"""
        return {
                "Success": False,
                "Error": "Only letters and numbers allowed."
            }

    def init_tables(self):
        """Initializes class variable tables"""
        data = self.get_tables()

        try: 
            tables = data["Data"]
        except KeyError:
            return None

        return tables

    def is_table_creator(self)->bool:
        """Checks wether table that is currently being played is the players creation."""
        data = self.get_tables_and_names()
        if data['Success']==True:
            table_data = data['Data']
            for i in range(len(table_data)):
                if table_data[i][0]==self.current_table and table_data[i][1]==self.user:
                    return True
        return False

    def get_tables(self)->dict:
        """Fetches the name of all word lists. Returns dict
        \n [Success: bool]=True -> ["Message": str], ["Data": list]
        \n[Success: bool]=False -> ["Error": str]"""
        url = 'https://hangmanserver.herokuapp.com/hangman/api/v1/tables/'
        response = requests.get(url)
        data = response.json()
        status = response.status_code
        tables = []
        if status == 200:
            for i in range(len(data)):
                tablename = data[i]['tname']
                tables.append(tablename)

            return {
                "Success": True, 
                "Message": "Successfully fetched word lists", 
                "Data": tables
                }
        else:
            return {
                "Success": False, 
                "Error": "Fatal error retrieving tables"
                }

    def get_tables_and_names(self)->dict:
        """Fetches the complete table tablenames. Returns dict
        \n [Success: bool]=True -> ["Message": str], ["Data": list], ["current_table": str]
        \n[Success: bool]=False -> ["Error": str]"""
        url = 'https://hangmanserver.herokuapp.com/hangman/api/v1/tables/'
        response = requests.get(url)
        data = response.json()
        status = response.status_code
        tables = [("Table Name", "Creator", "Word Count")]
        
        if status == 200:
            for i in range(len(data)):
                tablename = data[i]['tname']
                creator = data[i]['byuser']
                wordcount = data[i]['wordcount']
                entity = (tablename, creator, str(wordcount))
                tables.append(entity)

            return {
                "Success": True, 
                "Message": "Successfully fetched word lists and usernames", 
                "Data": tables,
                "current_table": self.current_table
                }
        else:
            return {
                    "Success": False, 
                    "Error": "Fatal error retrieving tables"
                    }

    def create_table(self, tablename: str)->dict:
        """Creates a new word list table. Returns dict
        \n [Success: bool]=True -> ["Message": str]
        \n[Success: bool]=False -> ["Error": str]"""""
        if not self.logged_in:
            return {
                "Success": False, 
                "Error": "Operation cannot be executed unless logged in."
                }

        req_data = {"token": self.token, "username": self.user, "tablename": tablename}
        url = 'https://hangmanserver.herokuapp.com/hangman/api/v1/tables/'
        response = requests.post(url, json=req_data)
        data = response.json()
        status = response.status_code
        if status == 201:
            msg = data['Message']
            self.tables = self.init_tables()
            if self.tables == None:
                count = 0
                while not self.tables:
                    count+=1
                    self.tables = self.init_tables()
                    if count == 5:
                        break
            return {
                "Success": True, 
                "Message": msg
                }
        else:
            keys = data.keys()
            if "Error" in keys:
                msg = data['Error']
                return {
                "Success": False, 
                "Error": msg
                }
            elif "tname" in keys:
                data['tname']
                return {
                "Success": False, 
                "Error": "Word list with that name already exists."
                }
            else:
                return {
                    "Success": False,
                    "Error": "Something went wrong creating table"
                }
        
    def remove_table(self, table_name: str)->dict:
        """Removes table. Permanently deletes it's content. Returns dict
        \n[Success: bool]=True -> ["Message": str]
        \n[Success: bool]=False -> ["Error": str]"""
        if not self.logged_in:
            return {
                "Success": False, 
                "Error": "Operation cannot be executed unless logged in."
                }
        url = self.url+'tables/'+table_name+'/'
        req_data = {'username': self.user, 'token': self.token}
        response = requests.delete(url, json=req_data)
        data = response.json()
        status = response.status_code
        keys = data.keys()
        if status == 200:
            self.tables = self.init_tables()
            if self.tables == None:
                count = 0
                while not self.tables:
                    count+=1
                    self.tables = self.init_tables()
                    if count == 5:
                        break

            if self.current_table == table_name:
                self.current_table = 'Hangman'
            return {
                "Success": True, 
                "Message": "Successfully removed the table: "+table_name
                }
        elif status==404:
            return {
            "Success": False, 
            "Error": "Table with that name and user doesn't exist"
            }

        elif status==401:
            if "Error" in keys:
                return {
                        "Success": False,
                        "Error": data['Error']
                    }
            else:
                return {
                        "Success": False,
                        "Error": "Permission denied. Must be owner of table to remove from it."
                    }
        else:
            if "Error" in keys:
                return {
                        "Success": False,
                        "Error": data['Error']
                    }
            else:
                return {
                    "Success": False,
                    "Error": "Something unexplainable went wrong"
                }

    def insert_word(self, word: str)->dict:
        """Inserts new word into currently selected word list. Returns dict
        \n [Success: bool]=True -> ["Message": str]
        \n[Success: bool]=False -> ["Error": str]"""
        if not self.logged_in:
            return {
                "Success": False, 
                "Error": "Operation cannot be executed unless logged in."
                }

        if self.current_table.lower() == "hangman":
            return {
                "Success": False,
                "Error": "Cannot add words to the default table"
            }
        url = self.url + 'tables/'+self.current_table+'/words/'
        req_data = {'username':self.user, 'word': word, 'token': self.token}
        response = requests.post(url, json=req_data)
        data = response.json()
        status = response.status_code
        keys = data.keys()
        if status == 201:
            return {
                "Success": True, 
                "Message": "Successfully added word: "+word
                }
        elif status == 401:
            if "Error" in keys:
                return {
                "Success": False,
                "Error": data['Error']
            }
            else:
                return {
                "Success": False,
                "Error": "Permission denied. Must be owner of table to add to it."
            }
        else:
            if "Error" in keys:
                return {
                "Success": False,
                "Error": data['Error']
            }
            else:
                return {
                "Success": False, 
                "Error": "The word ["+word+"] already exists in selected list."
                }

    def fetch_word(self)->dict:
        """Fetches random word from current word list. Returns dict
        \n [Success: bool]=True -> ["Message": str], ["Data": str]
        \n[Success: bool]=False -> ["Error": str]"""
        url = self.url+'tables/'+self.current_table+'/words/'
        response = requests.get(url)
        data = response.json()
        status = response.status_code
        if status == 200:
            return {
                "Success": True, 
                "Message": "Successfully fetched word", 
                "Data": data['word']
            }
        else:
            keys = data.keys()
            if 'Error' in keys:
                return {
                    "Success": False, 
                    "Error": data['Error']
                }
            else:
                return {
                    "Success": False,
                    "Error": "Couldn't fetch word"
                }
           
    def delete_word(self, word: str)->dict:
        """Removes word from current word list. Returns dict
        \n[Success: bool]=True -> ["Message": str]
        \n[Success: bool]=False -> ["Error": str]"""
        if not self.logged_in:
            return {
                "Success": False, 
                "Error": "Operation cannot be executed unless logged in."
                }
        url = self.url+'tables/'+self.current_table+'/words/'
        req_data = {'token':self.token, 'word': word, 'username': self.user}
        response = requests.delete(url, json=req_data)
        data = response.json()
        status = response.status_code
        keys = data.keys()
        if status == 200:
            return {
                "Success": True, 
                "Message": "Successfully removed the word: "+word
                }
        elif status == 404:
            if "Error" in keys:
                return {
                    "Success": False, 
                    "Error": data['Error']
                    }
            else:
                return {
                    "Success": False,
                    "Error": "URL invalid"
                }
        elif status == 401:
            if "Error" in keys:
                return {
                        "Success": False, 
                        "Error": data['Error']
                        }
            else:
                return {
                    "Success": False, 
                    "Error": "Some authorization went wrong"
                }

        return {
                "Success": False, 
                "Error": "Something went wrong"
                }

    def change_current_table(self, new_tablename: str)->dict:
        """Changes currently selected word list to input arg word list. 
        Returns dict
        \n [Success: bool]=True -> ["Message": str]
        \n[Success: bool]=False -> ["Error": str]"""
        if new_tablename in self.tables:
            self.current_table = new_tablename
            return {
                "Success": True, 
                "Message": "Successfully changed table"
                }
        else:
            return {
                "Success": False, 
                "Error": "Table doesn't exists"
                }
    
    def add_to_history(self)->dict:
        """Stores game session to history after game end. Returns dict:
        \n [Success: bool]=True -> ["Game_data": list]
        \n[Success: bool]=False -> ["Error": str]"""
        is_creator = self.is_table_creator()
        if self.user!=None and self.logged_in and not is_creator:
            url = self.url +'history/save/'+self.user+'/'
            req_data = {'user':self.user, 'score':self.current_score, 'token':self.token}
            response = requests.post(url, json=req_data)
            data = response.json()
            status = response.status_code
            if status == 201:
                self.game_session = []
                return {
                    "Success": True, 
                    "Message": "Game stored to history", 
                    "Game_data":self.return_game_summary()
                    }
            else:
                keys = data.keys()
                if "Error" in keys:
                    return {
                        "Success": False,
                        "Error": data['Error']
                    }
                else:
                    return {
                        "Success": False,
                        "Error": "Something went wrong saving to history"
                    }

        return {
            "Success": False, 
            "Message": "Must be logged in with valid user to save to history"
            }

    def get_top10(self)->dict:
        """Fetches top ten highest scores across all users. Returns dict:
        \n [Success: bool]=True -> ["Data": list]
        \n[Success: bool]=False -> ["Error": str]"""
        url = self.url+'history/leaderboard/'
        response = requests.get(url)
        data = response.json()
        status = response.status_code
        if status == 200:   
            ret_data = [('Score', 'User', 'Date')]
            for i in range(len(data)):
                score = data[i]['score']
                user = data[i]['user']
                date = data[i]['date'].split('.')[0]
                entity = (str(score), user, str(date))
                ret_data.append(entity)
            return {
                "Success": True, 
                "Message": "Successfully fetched leaderboard",
                "Data": ret_data
                }
        else:
            keys = data.keys()
            if "Error" in keys:
                return {
                    "Success": False,
                    "Error": data['Error']
                }
            else:
                return {
                    "Success": False,
                    "Error": 'Something went wrong'
                }

    def get_users_top10(self)->dict:
        """Fetches top ten highest scores from current users. Returns dict:
        \n [Success: bool]=True -> ["Message": str], ["Data": list]
        \n[Success: bool]=False -> ["Error": str]"""
        if self.logged_in and self.user:
            url = self.url+'history/leaderboard/'+self.user+'/'
            req_data = {'token':self.token}
            response = requests.get(url, json=req_data)
            data = response.json()
            status = response.status_code
            if status == 200:   
                ret_data = [('Score', 'User', 'Date')]
                for i in range(len(data)):
                    score = data[i]['score']
                    user = data[i]['user']
                    date = data[i]['date'].split('.')[0]
                    entity = (str(score), user, str(date))
                    ret_data.append(entity)
                return {
                    "Success": True, 
                    "Message": "Successfully fetched users last 10 games",
                    "Data": ret_data
                    }
            else:
                keys = data.keys()
                if "Error" in keys:
                    return {
                        "Success": False,
                        "Error": data['Error']
                    }
                else:
                    return {
                        "Success": False,
                        "Error": 'Something went wrong'
                    }
           
        return {
            "Success": False, 
            "Error": "Not logged in"
            }

    def get_user_last10(self)->dict:
        """Fetches top ten highest scores from current users. Returns dict:
        \n [Success: bool]=True -> ["Message": str], ["Data": list]
        \n[Success: bool]=False -> ["Error": str]"""
        if self.logged_in and self.user:
            url = self.url+'history/recent/'+self.user+'/'
            req_data = {'token':self.token}
            response = requests.get(url, json=req_data)
            data = response.json()
            status = response.status_code
            if status == 200:   
                ret_data = [('Score', 'User', 'Date')]
                for i in range(len(data)):
                    score = data[i]['score']
                    user = data[i]['user']
                    date = data[i]['date'].split('.')[0]
                    entity = (str(score), user, str(date))
                    ret_data.append(entity)
                return {
                    "Success": True, 
                    "Message": "Successfully fetched users last 10 games",
                    "Data": ret_data
                    }
            else:
                keys = data.keys()
                if "Error" in keys:
                    return {
                        "Success": False,
                        "Error": data['Error']
                    }
                else:
                    return {
                        "Success": False,
                        "Error": 'Something went wrong'
                    }
           
        return {
            "Success": False, 
            "Error": "Not logged in"
            }

    def log_in(self, user_name: str, password: str)->dict:
        """Checks wether user exists in database. Returns dict:
        \n[Success: bool]=True -> ["Message": str]
        \n[Success: bool]=False -> ["Error": str]"""
        if self.logged_in:
            return {
                "Success": False,
                "Error": "Already logged in"
            }

        url = self.url+'users/login/'
        userAndPass = b64encode(bytes(user_name + ':' + password, "utf-8")).decode("ascii")
        headers = {'Authorization': 'Basic %s'%(userAndPass)}
        response = requests.get(url, headers=headers)
        data = response.json()
        status = response.status_code
        if status == 200:
            self.user = user_name
            self.password = password
            self.logged_in = True
            self.token = data['token']
            self.current_score = 0
            self.current_table = "Hangman"
            self.gameInstance.null()
            self.game_session = []
            return {
                "Success": True, 
                "Message": "Welcome "+user_name+"!"
                    }
        else:
            keys = data.keys()
            if 'Error' in keys:
                return {
                    "Success": False,
                    "Error": data['Error']
                }
            else:
                return {
                    "Success": False,
                    "Error": "Something went wrong, please try again"
                }

    def log_out(self)->dict:
        """Changes session state logged_in to False. 
        \n[Success: bool]=True -> ["Message": str]
        \n[Success: bool]=False -> [Error: str]"""
        if not self.logged_in:
            return {
                "Success": False,
                "Error": "Trying to log out, but not logged in."
            }
        url = self.url+'users/logout/'
        userAndPass = b64encode(bytes(self.user + ':' + self.password, "utf-8")).decode("ascii")
        headers = {'Authorization': 'Basic %s'%(userAndPass)}
        req_data = {'token':self.token}
        response = requests.get(url, json=req_data, headers=headers)
        data = response.json()
        status = response.status_code
        if status == 200:
            self.user = None
            self.password = None
            self.game_session = []
            self.current_score = 0
            self.token = None
            self.current_table = "Hangman"
            self.gameInstance.null()
            self.logged_in = False
            return {
                "Success": True, 
                "Message": "Goodbye!"
                }
        else:
            keys = data.keys()
            if 'Error' in keys:
                return {
                    "Success": False,
                    "Error": data['Error']
                }
            else:
                return {
                    "Success": False,
                    "Error": "Something went wrong in logout proccess. Please try again"
                }
       
    def create_user(self, user_name: str, password1: str, password2: str)->dict:
        """Adds a new user to the database. Returns dict
        \n[Success: bool]=True -> ["Message": str]
        \n[Success: bool]=False -> [Error: str]"""
        if self.logged_in:
            return {
                "Success": False,
                "Error": "You already have an account. Log out to create a new one"
            }
        elif password1!=password2:
            return {
                "Success": False, 
                "Error": "Passwords in fields did not match. Please try again"
                }
        url = self.url+'users/'
        req_data= {'username':user_name, 'password':password1}
        response = requests.post(url, json=req_data)
        data = response.json()
        status = response.status_code
        if status == 201:
            return {
                "Success": True, 
                "Message": "User successfully created"
                }
        else:
            keys = data.keys()
            if "Error" in keys:
                msg = data['Error']
                return {
                    "Success": False, 
                    "Error": msg
                }
            else:
                return {
                    "Success": False,
                    "Error": "User already exists. Log in or try another username."
                }

    def play_game(self)->dict:
        """Starts a new hangman game. Fetches a random word. 
        Game must be ended with end_game() method.
        \n[Success: bool]=True -> ["Message": str], ["Current_word": list], 
        ["Current_score": int], ["Remaining_lives": int], ["Guessed_letters": list]
        \n[Success: bool]=False -> [Error: str]
        """
        if self.gameInstance.game_in_progress:
            return {
                "Success": False, 
                "Error": "Game already in progress. For new word use the new_word() method. Or use end_game() to use play again"""
                }
    
        self.game_session = []
        self.current_score = 0
        self.gameInstance.null()
        data_req = self.fetch_word()
        if data_req["Success"] == True:
            word = data_req["Data"]
            if word and word!="":
                self.gameInstance.new_game(word, self.user)
                return {
                    "Success": True, 
                    "Message": "Game Started. If you play your own word list your score will not be saved", 
                    "Current_word": self.gameInstance.current_word, 
                    "Current_score": self.current_score,
                    "Remaining_lives": self.gameInstance.remaining_lives,
                    "Guessed_letters": []
                    }
            else:
                return {
                    "Success": False, 
                    "Error": "Empty string or Invalid word retrieved"}
        else:
            return data_req

    def new_word(self)->dict:
        """Fetches new word in a running game and updates score and 
           game session data. Returns dict
        \n["Success": bool]=true -> ["Message": str], ["Current_word": list], ["Current_score": int], 
        ["Remaining_lives":int], ["Guessed_letters": list]
        \n[Success: bool]=False -> [Error: str]"""
        if not self.gameInstance.game_in_progress:
            return {
                "Success": False, 
                "Error": "No game in progress for new game use method play_game()"
                    }
        elif not self.gameInstance.check_win():
            return {
                "Success": False, 
                "Error": "A game has already been initialized. Finish guessing before fetching new word"
                }

        data_req = self.fetch_word()
        if data_req["Success"] == True:
            word = data_req["Data"]
            if word and word!="":
                game_data = self.gameInstance.return_game_data()
                self.current_score += self.gameInstance.get_score()
                self.game_session.append(game_data)

                self.gameInstance.new_game(word, self.user)
                return {
                    "Success": True, 
                    "Message": "New word fetched", 
                    "Current_word": self.gameInstance.current_word,
                    "Guessed_letters": [],
                    "Current_score": self.current_score,
                    "Remaining_lives": self.gameInstance.remaining_lives
                    }
            else:
                return {
                    "Success": False, 
                    "Error": "Empty string or invalid word retrieved"
                    }

        else:
            return data_req

    def guess_letter(self, letter: str) -> dict:
        """Makes a guess on letter in current game, Returns dict
        \n[Success: bool]=True -> ["Message": str], ["In_word": bool],
        ["Current_word": list], ["Remaining_lives": int], ["Guessed_letters: list], ["Current_score": int]
        \n[Success: bool]=False -> [Error: str]
        """
        if not self.gameInstance.game_in_progress:
            return {
                "Success": False, 
                "Error": "Word finished or game not started. Start a new game with play_game() or fetch a new word with new_word()"
                }
        try: 
            bool_req = self.gameInstance.guess_a_letter(letter)
            check_if_won = self.check_win()
                 
            if check_if_won["Game_won"]==True:
                game_data = self.gameInstance.return_game_data()
                self.game_session.append(game_data)
                self.new_word()
                return {
                    "Success": True, 
                    "Message": "Word found! The word was '"+self.game_session[-1]["word"]+"'.", 
                    "In_word": True,
                    "Current_word": self.gameInstance.current_word,
                    "Guessed_letters": self.gameInstance.guessed_letters,
                    "Current_score": self.current_score,
                    "Remaining_lives": self.gameInstance.remaining_lives
                    }

            elif bool_req:
                return {
                    "Success": True, 
                    "Message": "Letter is in word!", 
                    "In_word": True, 
                    "Current_word": self.gameInstance.current_word, 
                    "Current_score": self.current_score,
                    "Remaining_lives":self.gameInstance.remaining_lives, 
                    "Guessed_letters": self.gameInstance.guessed_letters
                    }
            else:
                return {
                    "Success": True, 
                    "Message": "Letter is not in word!", 
                    "In_word": False, 
                    "Current_word": self.gameInstance.current_word, 
                    "Remaining_lives":self.gameInstance.remaining_lives, 
                    "Guessed_letters": self.gameInstance.guessed_letters,
                    "Current_score": self.current_score,
                    }
        except NotALetterError:
            return {
                "Success": False, 
                "Error": "Only single characters allowed in letter guesses"
                }
        except InvalidCharactersError or NotALetterError:
            return {
                "Success": False, 
                "Error": "Only alphabetical or numerical characters allowed"
                }
        except AlreadyGuessedLetter:
            return {
                "Success": False, 
                "Error": "Letter has already been guessed"
                }
        except GameAlreadyWon:
            return {
                "Success": False, 
                "Error": "Game has been won, please start another with play_game() method"
                    }
        except GameOverError:
            return {
                "Success": False, 
                "Error": "Game has been lost, please use end_game() method and start another with play_game() method"
                    }

    def guess_word(self, word: str) -> dict:
        """Makes a guess on word in current game, Returns dict
        \n[Success: bool]=True -> ["Message": str], ["In_word": bool],
        ["Current_word": list], ["Remaining_lives": int], ["Guessed_letters: list]
        \n[Success: bool]=False -> [Error: str]"""
        if not self.gameInstance.game_in_progress:
            return {
                "Success": False, 
                "Error": "Word finished or game not started. Start a new game with play_game() or fetch a new word with new_word()"}
        try:
            bool_req = self.gameInstance.guess_a_word(word)
            if bool_req:
                game_data = self.gameInstance.return_game_data()
                self.game_session.append(game_data)
                self.new_word() #initialize new word
                return {
                    "Success": True, 
                    "Message": "Word correctly guessed!",
                    "In_word": True,
                    "Current_word": self.gameInstance.current_word,
                    "Guessed_letters": [],
                    "Current_score": self.current_score,
                    "Remaining_lives": self.gameInstance.remaining_lives
                    }
            else:
                return {
                    "Success": True, 
                    "Message": "Incorrect word guessed!", 
                    "In_word": False,
                    "Current_word": self.gameInstance.current_word,
                    "Guessed_letters": self.gameInstance.guessed_letters,
                    "Current_score": self.current_score,
                    "Remaining_lives": self.gameInstance.remaining_lives
                    }
        except InvalidCharactersError:
                return {
                    "Success": False, 
                    "Error": "Only alphabetical or numerical characters allowed"
                    }
        except AlreadyGuessedLetter:
            return {
                "Success": False, 
                "Error": "Letter has already been guessed"
                }
        except GameAlreadyWon:
            return {
                "Success": False, 
                "Error": "Game has been won, please start another with play_game() method"
                }
        except GameOverError:
            return {
                "Success": False, 
                "Error": "Game has been lost, please use end_game() method and start another with play_game() method"
                    }

    def check_win(self) -> dict:
        """Checks if game has been won. 
        Returns all relevant data if game has been won.
        \n[Success: bool]=True -> ["Message": str], ["Game_won": bool]=
        \n[Success: bool]=False -> [Error: str]"""
        try:
            bool_req = self.gameInstance.check_win()
            if bool_req:
                return {
                "Success": True, 
                "Message": "GAME WON!", 
                "Game_won": True
                }
            else:
                return {
                "Success": True, 
                "Message": "Game still in progress", 
                "Game_won": False
                }
        except NoGameInProgress:
            return {
            "Success": False, 
            "Error": "No game in progress. Start a new one with play_game()"
            }
        
    def get_score(self) ->int:
        return self.current_score

    def check_loss(self)-> dict:
        """Checks if game has been lost
        \n[Success: bool]=True -> ["Message": str], ["Game_lost": bool]
        \n[Success: bool]=False -> [Error: str]"""
        try:
            bool_req = self.gameInstance.check_hanged_man()
            if bool_req:
                return {
                "Success": True, 
                "Message": "GAME LOST!", 
                "Game_lost": True
                }
            else:
                return {
                    "Success": True, 
                    "Message": "Game still in progress", 
                    "Game_lost": False
                    }
        except:
            return {
                "Success": False, 
                "Error": "Critical error in game Instance when checking if game lost"
                }

    def return_game_summary(self)->dict:
        """Returns game summary"""
        total_letter_guesses = self.gameInstance.letter_guesses
        total_word_guesses = self.gameInstance.word_guesses
        words = []
        for i in range(len(self.game_session)):
            total_letter_guesses += self.game_session[i]["letter_guesses"]
            total_word_guesses += self.game_session[i]["word_guesses"]
            words.append(self.game_session[i]["word"])

        return {
            "Success": True,
            "Game_end": True,
            "Message": "Game lost! The word was '"+self.gameInstance.guessword+"'!", 
            "Letter_guesses":total_letter_guesses,
            "Word_guesses": total_word_guesses, 
            "Words": words, 
            "Current_word": self.gameInstance.current_word,
            "Score": self.current_score
            }

    def end_game(self)->dict:
        """End game is to be triggered when a hangman game is lost.
        \n Resets nesseccary variables and saves game. Returns dict
        \n [Success: bool]=True -> ["Success": bool], ["Message":str], ["Letter_guesses": int], ["Game_end": bool]
        ["Word_guesses": int], ["Words": list],["Score": int], ["Current_word":list]
        \n[Success: bool]=False -> ["Error": str]"""
        if self.logged_in and self.current_score!=0:
            self.add_to_history()
 
        ret_data = self.return_game_summary()
        self.game_session = []
        self.current_score = 0
        self.gameInstance.null()

        return ret_data
