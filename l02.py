import pygame

pygame.init()
c = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))
bg = pygame.image.load('pics/space.jpeg').convert()

screen.blit(bg,(0,0))
a_rect = pygame.Rect(400,300,100,100)
b_rect = pygame.Rect(500,400,200,200)

# screen.blit()
while True:
    screen.blit(bg,a_rect,b_rect)
    pygame.display.update()
    
    for e in pygame.event.get():
        if e.type == pygame.QUIT:

            pygame.quit()
    c.tick(60)
    