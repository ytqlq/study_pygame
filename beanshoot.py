import pygame
import os.path
import math
import random



pygame.init()
screen_width = 800
screen_height = 600
c = pygame.time.Clock()
background = 'white'

maindir = os.path.split(os.path.abspath(__file__))[0]

def load_image(img_name, scale = (75, 75)):
    img_path = os.path.join(maindir,"pics",img_name)
    imgsurf = pygame.image.load(img_path)#.convert()
    return pygame.transform.scale(imgsurf, scale)

def firebean( start_x,start_y, rect_zombie,vo,angle,block_rect, speedadd = 20):
    fire = True
    t = 0
    original_x = start_x
    original_y = start_y
    vox = vo*math.cos(angle)    
    voy = vo*math.sin(angle)
    while fire:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()     
        rect_bullet = pygame.draw.circle(screen,'red',(original_x,original_y),10)        
        if rect_bullet.colliderect(rect_zombie) :      
            print('Hit the target.')      
            fire = False
        original_x = int(vox * t + start_x)
        original_y = int(start_y - (voy * t - 10 * 1/2*(t**2)))
        if original_x >screen_width or original_y > screen_height or rect_bullet.colliderect(block_rect):# todo
            fire = False
        t += speedadd/vox
        pygame.display.update()
        c.tick(30)   
screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Bean Shoot")
img_body = load_image('beanbody.png')
img_head = load_image('beanhead.png')
img_zombie = load_image('zoombie.png',(150,150))



class wall(pygame.sprite.Sprite):
    def __init__(self,bean_rect,rect_zombie) -> None:
        self.width = 20
        self.height = random.randrange(10,screen_height-50)
        self.x = random.randrange(bean_rect.right,rect_zombie.x)
        self.rect = pygame.Rect(self.x,screen_height-self.height,self.width,self.height)    
    def draw(self):
        screen.fill('black',self.rect)
        
class gameObject(pygame.sprite.Sprite):
    def __init__(self,image_surf,image_rect,boundary_left,boundary_right, *groups) -> None:
        super().__init__(*groups)
        self.image_surf = image_surf
        self.image_rect = image_rect
        self.bdry_left = boundary_left
        self.bdry_right = boundary_right
    
    def draw(self,):
        screen.blit(self.image_surf,self.image_rect)
        
    def move(self,direct):
        arrive_boundary = False
        if direct == 'left':
            self.image_rect.x -= 10  
            if self.image_rect.x < self.bdry_left:
                self.image_rect.x = self.bdry_left
                arrive_boundary = True
                
        elif direct == 'right':
            self.image_rect.x += 10
            if self.image_rect.right > self.bdry_right:
                self.image_rect.right = self.bdry_right
                arrive_boundary = True
        return arrive_boundary
        

class zombie(gameObject):
    def __init__(self,image_surf,image_rect,boundary_left,boundary_right, *groups) -> None:
        super().__init__(self,image_surf,image_rect,boundary_left,boundary_right, *groups)
    
    def automove(self,):
        automove = True
        direct = 'left'
        opposite = 'right'
        while automove:
            if super().move(direct):
                tmp = direct
                direct = opposite
                opposite = tmp
        
        


def gameloop():    
    fps = 24
    bean_rect = img_head.get_rect(x = 0, y = screen_height-100)    
    # start_x, start_y = bean_rect.center    
    rect_zombie = img_zombie.get_rect(x= screen_width-150,y = screen_height-150)
    rect_zombie_shrink = rect_zombie.inflate(-80,-10)
    firepower = 100
    gamerun = True
    angle = 0
    block_wall = wall(bean_rect,rect_zombie)
    direct = None
    bean_body = gameObject(img_body,bean_rect,0,block_wall.x)
    bean_head = gameObject(img_head,bean_rect,0,block_wall.x)
    zombie_role = gameObject(img_zombie,rect_zombie,block_wall.rect.right,screen_width)
    zombie_direct = 'left'
    zombie_opposite_direct = 'right'
    while gamerun:
        start_x, start_y = bean_head.image_rect.center 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:                    
                    angle += 15
                    if angle > 90:
                        angle = 90
                elif event.key == pygame.K_DOWN:
                    angle -= 15
                    if angle <0:
                        angle = 0    
                elif event.key == pygame.K_LEFT:
                    direct = 'left'
                    # bean_head.move(direct)
                    # bean_body.move(direct)
                elif event.key == pygame.K_RIGHT:
                    direct = 'right'
                    # bean_head.move(direct)
                    # bean_body.move(direct)
            if event.type == pygame.KEYUP:
                if direct is not None:
                    bean_head.move(direct)
                    bean_body.move(direct) 
                    direct = None
                if event.key == pygame.K_SPACE: 
                    firebean(start_x,start_y,rect_zombie_shrink,firepower,angle/180*math.pi,block_wall.rect)
                    print(f'{angle}: fire') 
        if zombie_role.move(zombie_direct):
            tmp = zombie_direct
            zombie_direct = zombie_opposite_direct
            zombie_opposite_direct = tmp
        screen.fill(background)
        block_wall.draw()
        bean_body.draw()
        bean_head.draw()
        # screen.blit(img_zombie,rect_zombie)   
        zombie_role.draw()            
        pygame.display.update()
        c.tick(fps)
    pygame.quit()
    quit()
 

gameloop()