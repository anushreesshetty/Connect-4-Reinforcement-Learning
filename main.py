import pygame
from logic import  Game
from pygame.locals import *
import os



pygame_1vs1_image = pygame.image.load('./Asset/onevsone1.png')
pygame_1vscomp_image=pygame.image.load('./Asset/onevscomp.png')
play_image=pygame.image.load('./Asset/Play.png')


screen_width = 800
screen_height = 700
# orange = (255, 165, 0)
# font_path = os.path.join("path_to_your_font_directory", "consolas.ttf")
# consolas_font = pygame.font.Font(font_path, 60) 
# play_game_text = consolas_font.render("Play Game", True, orange)

# play_game_rect.center = (screen_width // 2, screen_height // 2)
class userInterface:

    def __init__(self):
        self.game = Game()  
        pygame.init()
        pygame.font.init()
        self.bigFont= pygame.font.SysFont("Courier New", 60, bold=True)
        self.mediumFont= pygame.font.SysFont(None, 40)
        self.smallFont = pygame.font.SysFont(None, 26)
        self.run = True  
        self.gameDisplay = pygame.display.set_mode((screen_width, screen_height))
        self.yellow = (255, 255, 0)
        self.red = (255, 0, 0)
        self.blue = (0,30,130)#blue
        self.white = (255, 255, 255)
        self.green=(152, 251, 152)
        self.lightblue=(173, 216, 230)
        self.beige= (245, 245, 220)
        self.black=(0,0,0)
        self.orange=(187,111,42)
        self.clock = pygame.time.Clock()
        
        pygame.display.set_caption('Connect-4 Game Reinforcement Learning')
        self.batch_size = 0


    def welcomeScreen (self) :

        skip = False
        self.gameDisplay.fill((255,255,255))
        playgame = self.bigFont.render('Play Now', True, (0,0,0))
        text_rect = playgame.get_rect()
        x = (screen_width - text_rect.width) // 2
        y = (screen_height - text_rect.height) // 2
        # screen.blit(play_game_text, play_game_rect)
        self.gameDisplay.blit(playgame, (x, y))
        while not skip :
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    skip=True
                    self.run=False

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if ((pos[0]>300 and pos[0]<500) and (pos[1]>250 and pos[1]<400)):
                        skip = True
                        self.selectEnemy()
            pygame.display.update()


    def selectEnemy (self):

        skip = False
        self.gameDisplay.fill((255,255,255))
        self.gameDisplay.blit(pygame_1vscomp_image, (50, 250))
        self.gameDisplay.blit(pygame_1vs1_image, (400, 250))
        pos = (0, 0) 
        while not skip:
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    skip = True
                    self.run = False
                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                # Check if the mouse click is within the "One vs One" image area
                if (50 <= pos[0] <= 350) and (250 <= pos[1] <= 450):
                    skip = True
                    self.game.twoPlayer = False
                    self.playgame()
                # Check if the mouse click is within the "One vs Computer" image area
                elif (400 <= pos[0] <= 650) and (250 <= pos[1] <= 450):
                    skip = True
                    self.game.twoPlayer = True
                    self.playgame()    
            pygame.display.update()


    def playgame (self) :

        self.gameDisplay.fill(self.white)
        for row in range(1,7):
            for column in range(1,8):
                pygame.draw.circle(self.gameDisplay, self.beige, [column*100, row* 100 ],30)

        while self.run:
            self.clock.tick(30) #This limits the while loop to a max of 30 times per second.
            player1 = self.mediumFont.render('Player1',1,self.black if self.game.turn==1 else (128,128,128))
            player2 = self.mediumFont.render('Player2' if self.game.twoPlayer==True else 'Computer',1,self.black if self.game.turn==2 else (128,128,128))
            self.gameDisplay.blit(player1,(50,24))
            self.gameDisplay.blit(player2,(650,24))

            if not self.game.game_over:
                if self.game.twoPlayer or (self.game.turn == 1) :
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            self.run = False

                        if  event.type == pygame.MOUSEBUTTONUP:
                            pos = pygame.mouse.get_pos()
                            row,column= self.game.move(pos)
                            if (row == -1 or column == -1 ): continue
                            pygame.draw.circle(self.gameDisplay, self.black if self.game.turn==1 else self.orange, [(column+1)*100, (row+1)* 100 ],30)
                            self.game.isGameFinished()
                else : # computer's move
                    #time.sleep(0.5)
                    pygame.time.wait(300)
                    row,column= self.game.move(self.game.board)
                    pygame.draw.circle(self.gameDisplay, self.orange, [(column + 1) * 100, (row + 1) * 100], 30)
                    self.game.isGameFinished()
            else :
                self.endOfGame()
            pygame.display.update()        

            

    def playAgain (self):

        self.game = Game()
        self.welcomeScreen()


    def endOfGame (self) :

        pygame.draw.rect(self.gameDisplay,(187,111,42) if self.game.turn==1 else (187,111,42),(0,0,800,52))
        pygame.draw.rect(self.gameDisplay, (187,111,42), (0,640 , 800, 30))
        pygame.draw.rect(self.gameDisplay, (187,111,42), (0,670,  800, 30))
        if self.game.winner =='Draw':
            congrats = self.mediumFont.render('Draw!', 1, (0,0,0))
        elif self.game.winner == 'Player1':
            congrats= self.mediumFont.render(self.game.getTurn()+' wins ! Congrats!', 1,(0,0,0))

        else :
            congrats= self.mediumFont.render(self.game.getTurn()+' wins ! Congrats!' if self.game.twoPlayer==True else self.game.getTurn()+' wins !', 1,(0,0,0))
        quit= self.smallFont.render('Quit',1,(0,0,0))
        playAgain= self.smallFont.render('Play again',1,(0,0,0))
        self.gameDisplay.blit(congrats,(280,15))
        self.gameDisplay.blit(quit,(375,680))
        self.gameDisplay.blit(playAgain,(350,650))

        skip = False
        while not skip :
            self.clock.tick(30)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    skip= True
                    self.run = False
                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if pos[1] > 640:
                        if pos[1] < 670:
                            self.playAgain()
                        else :
                            skip = True
                            self.run = False

            pygame.display.update()


if  __name__ == "__main__":
    game = userInterface()
    game.welcomeScreen()