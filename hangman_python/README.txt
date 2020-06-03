This is a 3 layered design. 

The interface is seperated into a graphical constructor, a graphical handler which uses the constructor and a interface handler which controls all of the mentioned and communicates with the logic layer.

The logic layer is seperated by only a game Instance and the logic itself. The game instance is controlled by the logic class. 
The logic class handles all communications between the game and the server. All methods from logic layer return a python dictionary to the interface with the appropriate data, in a json like fashion.





TO RUN THE GAME:
    1. Click the hangman.exe file located in the main directory


TO USE THE APPLICATION COMMANDS
    1. To enter any text, in any menu, you must first enter a command. After entering the command
    the program will prompt you for an input.
    2. The commands and their explanation are visible in the top part of the interface in any given menu

THE RECOMMENDED SCREEN SIZE IS 100+

IF THE TEXT INTERFACE IS TOO LARE FOR YOUR SCREEN:
    1. Make your terminal bigger or lower the letter size in the terminl settings
    OR
    1. Use the resize command in the main menu


THE SERVER IS ONLINE!

