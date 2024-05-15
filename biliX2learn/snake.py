import pygame
import random

pygame.init()
black = (0,0,0)
white = (255,255,255)
red = (255,0,0)
font = pygame.font.SysFont(None,25)
screen_width = 800
screen_height = 600


def message_to_show(dessurf:pygame.Surface, text):
    fontsurf = font.render(text,1,red)
    dessurf.fill(white)
    dessurf.blit(fontsurf,(screen_width/2, screen_height/2))
    
    
    

def gameloop():
    
    c = pygame.time.Clock()
    
    
    screen = pygame.display.set_mode((screen_width,screen_height))
    pygame.display.set_caption("Snake")
    # pygame.display.update()
    block_size = 10
    start_x = screen_width/2
    start_y = screen_height/2
    start_x_change = 0
    start_y_change = 0
    fps = 30
    randAppleX = round(random.randrange(0,screen_width)/block_size)*block_size
    randAppleY = round(random.randrange(0,screen_height)/block_size)*block_size
    
    gameExit = False  
    gameOver = False  
    while not gameExit:
        
        for event in pygame.event.get():  
            if gameOver:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_c:
                        gameloop()
                    elif event.key == pygame.K_q:
                        gameExit = True
            
            if event.type == pygame.QUIT:
                gameExit = True
            if event.type == pygame.KEYDOWN:  
                # print(help(event.key))             
                if event.key == pygame.K_UP:                  
                    start_y_change = -block_size
                    start_x_change = 0
                elif event.key == pygame.K_DOWN:
                    start_y_change = block_size
                    start_x_change = 0
                elif event.key == pygame.K_LEFT:
                    start_x_change = -block_size
                    start_y_change = 0
                elif event.key == pygame.K_RIGHT:
                    start_x_change = block_size
                    start_y_change = 0
            
        start_x += start_x_change
        start_y += start_y_change
        screen.fill(white)
        
        pygame.draw.rect(screen,black,[start_x,start_y,block_size,block_size])
        pygame.draw.rect(screen,red,[randAppleX,randAppleY,block_size,block_size])
        pygame.display.update()
        if start_x == randAppleX and start_y == randAppleY:
            randAppleX = round(random.randrange(0,screen_width)/block_size)*block_size
            randAppleY = round(random.randrange(0,screen_height)/block_size)*block_size
            
            
        if start_x <0 or start_x >= screen_width or start_y <0 or start_y >= screen_height:
            message_to_show(screen, "Press C to replay, or Q to quit.")
            pygame.display.update()
            pygame.time.wait(2000)
            gameOver = True
        c.tick(fps)
    
    
    
    
    
if __name__ == "__main__":
    gameloop()