# -*- coding: utf-8 -*-
"""
Created on Tue Apr 23 16:13:07 2024

@author: kinga
"""

import pygame
import simpleGE
import random


class Guy1(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("guy1.png")
        self.setSize(50, 50)
        self.position = (50, 400)
        self.inAir = True
        
           
    def process(self):
        if self.inAir:
            self.addForce(.2, 270)
        
        if self.y > 450:
            self.inAir = False
            self.y = 450
            self.dy = 0          
        
        if self.scene.isKeyPressed(pygame.K_RIGHT):
            self.x += 5
        if self.scene.isKeyPressed(pygame.K_LEFT):
            self.x -= 5   
        if self.scene.isKeyPressed(pygame.K_SPACE):
            if not self.inAir:
                self.addForce(6, 90)
                self.inAir = True

        self.inAir = True
        for platform in self.scene.platforms:
            if self.collidesWith(platform):                
                if self.dy > 0:
                        self.bottom = platform.top
                        self.dy = 0
                        self.inAir = False
        
class Platform(simpleGE.Sprite):
    def __init__(self, scene, position):
        super().__init__(scene)
        self.position = (position)
        self.setImage("platform.png")
        self.setSize(60, 30)
       
    #def update(self):
        #super().update()
        #if self.mouseDown:
         #   self.position = pygame.mouse.get_pos()
class Ghost(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("enemy.png")
        self.buzzer = simpleGE.Sound("buzzer.mp3")
        self.setSize(30, 25)
        self.timed = False
        self.count = 0
        self.reset()
       
    def reset(self):
        self.y = 10
        self.x = random.randint(0, self.screenWidth)
        #self.dy = random.randint(3, 8)
        self.dy = random.randint(3, 5+(self.scene.level * 2))
        self.dy = random.randint(1, 2)
        
    def checkBounds(self):
        if self.bottom > self.screenHeight:
            self.reset()
    
    def process(self):
        if self.timed:
            self.count += 1
        elif self.collidesWith(self.scene.guy1):
            self.timed = True
            self.buzzer.play()
        if self.count >= 45:
            self.scene.stop()
          

class Exit(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("gate.png")
        self.applause = simpleGE.Sound("applause.WAV")
        self.setSize(60, 60) 
        self.timed = False
        self.count = 0
        # Adjust the size of the exit image as needed
        self.position = (600, 40)  # Adjust the position as needed
        self.trivia = Trivia()  # Initialize trivia questions

    def process(self):
        if self.timed:
            self.count += 1
        elif self.collidesWith(self.scene.guy1):
            self.timed = True
            self.applause.play()
        if self.count >= 45:
            self.scene.stop()
        if self.collidesWith(self.scene.guy1):
            # Present a trivia question to the player
            trivia_question = self.trivia.get_random_question()
            print(trivia_question["question"])
            for choice in trivia_question["choices"]:
                print(choice)
            
            # Get player's answer
            player_answer = input("Choose an option (A, B, C, or D): ")

            # Check if the answer is correct
            if player_answer == trivia_question["answer"]:
                print("Correct answer! Proceeding to the next level...")
                self.scene.level += 1  # Increment the level if the answer is correct
                self.scene.stop()  # Stop the current scene to proceed to the next level
            else:
                print("Incorrect answer! Try again.")
                # Optionally handle incorrect answers (e.g., give another chance or end the game)

        
class StartButton(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("start_btn.png")
        self.setSize(110, 70)
        self.position = (200, 250)

class Trivia:
    def __init__(self):
        # List of trivia questions with their answers
        self.questions = [
            {
                "question": "What is the capital of France?",
                "choices": ["A: Paris", "B: London", "C: Rome", "D: Madrid"],
                "answer": "A"
            },
            {
                "question": "Who was the first president of the United States?",
                "choices": ["A: George Washingthon", "B: Thomas Jefferson", "C: John Adams", "D: James Maddison"],
                "answer": "A"
            },
            {   "question": "What is the largest ocean on Earth?",
                 "choices": ["A: Atlantic Ocean", "B: Indian Ocean", "C: Artic Ocean", "D: Pacific Ocean"],
                 "answer": "A"
            },  
            {   "questions": "What is the capital of Japan?",
                "choices": ["A: Beijing", "B: Seoul", "C: Tokyo", "D: Shanghai"],
                "answer": "C"
            },
            {   "questions": "Which actor played Iron Man in the Marvel Cinematic Universe?",
                "choices": ["A: Chris Hemsworth", "B: Chris Evans", "C: Robert Downey Jr.", "D: Mark Ruffalo"],
                "answer": "C"
            },
        ]
            

    def get_random_question(self):
        # Return a random trivia question from the list
        return random.choice(self.questions)

    
     
class ExitButton(simpleGE.Sprite):
    def __init__(self, scene):
        super().__init__(scene)
        self.setImage("exit_btn.png")
        self.setSize(110, 70)
        self.position = (500, 250)

class IntroPage(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.setImage("plainField.png")
        self.StartButton = StartButton(self)
        self.ExitButton = ExitButton(self)
        self.sprites = [self.StartButton, self.ExitButton]

    def process(self):
        if self.StartButton.clicked:
            self.response = "play"
            self.stop()
            
        elif self.ExitButton.clicked:
             self.response = "quit"
             self.quit()
        
class Game(simpleGE.Scene):
    def __init__(self):
        super().__init__()
        self.level = 0
        self.setImage("sky.png")
        self.guy1 = Guy1(self)
        self.ghosts = [Ghost(self) for _ in range(10)]
        

        self.platforms = [Platform(self, (130, 450)),
                          Platform(self, (200, 400)),
                          Platform(self, (250, 350)),
                          Platform(self, (200, 150)),
                          Platform(self, (350, 180)),
                          Platform(self, (400, 300)),
                          Platform(self, (300, 250)),
                          Platform(self, (550, 350)),
                          Platform(self, (450, 150)),
                          Platform(self, (400, 400)),
]
        self.exit = Exit(self)  # Instantiate the exit sprite      
        self.sprites = [self.platforms, self.guy1, self.exit, self.ghosts] 
        
        pygame.mixer.music.load("soundtrack.WAV")
        pygame.mixer.music.set_volume(0.6)
        pygame.mixer.music.play(-5)
       

class Instruction(simpleGE.Scene):
    def __init__(self, scene):
        super().__init__()
        self.setImage("plainField.png")


def main():
    current_state = "intro"  # Initial state is "intro"
    game_level = 0
    while current_state != "quit":  # Run the loop until the game is set to quit
        if current_state == "intro":
            # Initialize the intro page scene
            intro_scene = IntroPage()
            intro_scene.start()
            
            # Check the user's response after the intro page
            if intro_scene.response == "play":
                current_state = "game"  # Transition to the game state
            elif intro_scene.response == "quit":
                current_state = "quit"  # Transition to the quit state
        
        elif current_state == "game":
            # Initialize the game scene
            print(game_level)
            game_scene = Game()
            game_scene.level = game_level
            game_scene.start()
            game_level = game_scene.level
            
            
            
            
            # Optionally handle game over or game win conditions here
            # Transition back to the intro state or quit state if needed
            # For example, you could set current_state to "intro" for restarting or "quit" to end the game

            # For now, we'll just set it back to "intro" for demonstration
            current_state = "intro"
    
    # When the loop exits, the game ends
    print("Game has exited")

if __name__ == "__main__":
    main()
