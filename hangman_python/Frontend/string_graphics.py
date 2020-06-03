#These are the hangman graphical's for ingame. The InterfaceMethods class takes it and replaces whitespaces at the appropriate
#locations with the graphics.
class Graphics:
    hangman0 = """
                    
                    
                    
                    
                    
                    
                    
                    
                    
                    """
    hangman1 = """
                    
                    
                    
                    
                    
                    
                    
     \\\\             
      \\\\            
       \\\\           """

    hangman2 = """
                    
                    
                    
                    
                    
                    
                    
  // \\\\             
 //   \\\\            
//     \\\\           """

    hangman3 = """
                    
                    
   |||              
   |||              
   |||              
   |||              
   |||              
  // \\\\             
 //   \\\\            
//     \\\\           """

    hangman4 = """
   _____________    
   -------------    
   |||              
   |||              
   |||              
   |||              
   |||              
  // \\\\             
 //   \\\\            
//     \\\\           """

    hangman5 = """
   _____________    
   -------------|   
   |||          |   
   |||              
   |||              
   |||              
   |||              
  // \\\\             
 //   \\\\            
//     \\\\           """

    hangman6 = """
   _____________    
   -------------|   
   |||          |   
   |||        (o.o) 
   |||              
   |||              
   |||              
  // \\\\             
 //   \\\\            
//     \\\\           """

    hangman7 = """
   _____________    
   -------------|   
   |||          |   
   |||        (o.o) 
   |||         _|_  
   |||        /   \\ 
   |||              
  // \\\\             
 //   \\\\            
//     \\\\           """

    hangman8 = """
   _____________    
   -------------|   
   |||          |   
   |||        (o.o) 
   |||         _|_  
   |||        / | \\ 
   |||          |   
  // \\\\             
 //   \\\\            
//     \\\\           """

    hangman9 = """
   _____________    
   -------------|   
   |||          |   
   |||        (o.o) 
   |||         _|_  
   |||        / | \\ 
   |||          |   
  // \\\\        / \\  
 //   \\\\      -   -  
//     \\\\            """

    hangman10 = """
   _____________    
   -------------|    
   |||          |    
   |||        (~.x) 
   |||         _|_  
   |||        / | \\ 
   |||          |   
  // \\\\        / \\  
 //   \\\\      -   - 
//     \\\\           """
    def get_image(self, remaining_lives: int)->str:
        hangman_nr = 10-remaining_lives
        img_dict = {1: self.hangman1, 2: self.hangman2, 3: self.hangman3, 4:self.hangman4,
                    5: self.hangman5, 6: self.hangman6, 7: self.hangman7, 8: self.hangman8,
                    9: self.hangman9, 10: self.hangman10, 0: self.hangman0}
        return img_dict[hangman_nr]
