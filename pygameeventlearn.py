import pygame
import random

pygame.init()
size = (800, 600)

screen = pygame.display.set_mode(size)
c = pygame.time.Clock()
i = 0
startdraw = False
while True:
    i += 1
    print(i)
    # event = pygame.event.wait()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
            
        elif event.type == pygame.MOUSEMOTION:
            print(event.pos)
            # print(event.buttons)
            if startdraw:
                color= (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))
                
                pygame.draw.circle(screen,color,event.pos,50)
                print('circle{0}'.format(i))
            
            
        elif event.type == pygame.MOUSEBUTTONUP:
            # print(event.button,event.pos)
            # pygame.event.pump()
            if event.button == 1:
                startdraw = True
            
    pygame.display.update()
    # pygame.event.pump()
    c.tick(20)
        



