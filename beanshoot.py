import pygame
import os.path

pygame.init()
screen_width = 800
screen_height = 600
c = pygame.time.Clock()
background = 'white'

maindir = os.path.split(os.path.abspath(__file__))[0]
# print(maindir)

def load_image(img_name, scale = (75, 75)):
    img_path = os.path.join(maindir,"pics",img_name)
    imgsurf = pygame.image.load(img_path)#.convert()
    return pygame.transform.scale(imgsurf, scale)

def shoot( start_x,start_y,  speedadd = 20):
    pygame.draw.circle(screen,'red',(start_x,start_y),10)
    
    
 
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Bean Shoot")
img_body = load_image('beanbody.png')
img_head = load_image('beanhead.png')
img_zombie = load_image('zoombie.png',(150,150))

def gameloop():    
    fps = 24
    bean_rect = img_head.get_rect(x = 0, y = screen_height-100)
    # start_x, start_y = img_head.get_rect().center
    # start_y = screen_height - 100
    # zoombie_rect = 
    start_x, start_y = bean_rect.center
    speed = 0
    bullets = []
    gamerun = True
    while gamerun:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    speed = 20            
        start_x += speed
        screen.fill(background)
        shoot(start_x,start_y)    
        screen.blit(img_head,bean_rect) 
        screen.blit(img_body,bean_rect)
        screen.blit(img_zombie,(screen_width-150,screen_height-150))
               
        pygame.display.update()
        c.tick(fps)
    pygame.quit()
    quit()
 

gameloop()