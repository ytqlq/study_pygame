import pygame
import os.path
import math
import random


pygame.init()
screen_width = 800
screen_height = 600
c = pygame.time.Clock()
background = "white"
gravity_acceleration = 10
maindir = os.path.split(os.path.abspath(__file__))[0]


def load_image(img_name, scale=(75, 75)):
    img_path = os.path.join(maindir, "pics", img_name)
    imgsurf = pygame.image.load(img_path)  # .convert()
    
    return pygame.transform.scale(imgsurf, scale)


def firebean(start_x, start_y, rect_zombie, vo, angle, block_rect, speedadd=40):
    fire = True
    t = 0
    original_x = start_x
    original_y = start_y
    vox = vo * math.cos(angle)
    voy = vo * math.sin(angle)
    while fire:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
        rect_bullet = pygame.draw.circle(screen, "red", (original_x, original_y), 10)
        if rect_bullet.colliderect(rect_zombie):
            print("Hit the target.")
            return True
            # fire = False
        original_x = int(vox * t + start_x)
        original_y = int(start_y - (voy * t - gravity_acceleration * 1 / 2 * (t**2)))
        if (
            original_x > screen_width
            or original_y > screen_height
            or rect_bullet.colliderect(block_rect)
        ):  
            fire = False
        t += speedadd / vox
        pygame.display.update()
        c.tick(60)
    return False

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bean Shoot")
# img_body = load_image("beanbody.png")
# img_head = load_image("beanhead.png")
img_zombie = load_image("zoombie.png", (150, 150))
img_grass = load_image("grass.png")
img_grass = pygame.transform.scale(img_grass, (screen_width, 50))
img_bullet = load_image("bullet.png")# todo 
img_bullet = pygame.transform.scale(img_bullet,(20,20))
# img_bullet = pygame.Surface((10,10))
beans_ind_list = [0,15,30,45,60,75,85]
dic_img_bean = dict()
for bean_angle in beans_ind_list:
    dic_img_bean[bean_angle] = load_image(f"beans/bean{bean_angle}.png",(80,108))



class wall(pygame.sprite.Sprite):
    def __init__(self, bean_rect, rect_zombie, width=50) -> None:
        self.width = width
        self.height = random.randrange(10, screen_height - 50)
        self.x = random.randrange(bean_rect.right+20, rect_zombie.x-20)
        self.rect = pygame.Rect(
            self.x, screen_height - self.height, self.width, self.height
        )

    def draw(self):
        screen.fill("black", self.rect)


class gameObject(pygame.sprite.Sprite):
    def __init__(
        self, image_surf, image_rect, boundary_left, boundary_right, *groups
    ) -> None:
        super().__init__(*groups)
        self.image_surf = image_surf
        self.image_rect = image_rect
        self.bdry_left = boundary_left
        self.bdry_right = boundary_right

    def draw(
        self,
    ):
        screen.blit(self.image_surf, self.image_rect)

    def move(self, direct):
        arrive_boundary = False
        if direct == "left":
            self.image_rect.x -= 10
            if self.image_rect.x < self.bdry_left:
                self.image_rect.x = self.bdry_left
                arrive_boundary = True

        elif direct == "right":
            self.image_rect.x += 10
            if self.image_rect.right > self.bdry_right:
                self.image_rect.right = self.bdry_right
                arrive_boundary = True
        return arrive_boundary

class Bullet(gameObject):
    def __init__(self, image_surf, image_rect, angle, boundary_left, boundary_right, *groups) -> None:
        super().__init__(image_surf, image_rect, boundary_left, boundary_right, *groups)
        self.t = 0
        self.start_y = self.image_rect.y
        self.start_x = self.image_rect.x
        self.angle = angle
    
    def updatepos(self,vo,speedadd=20):
        # if self.check_boundary():
        self.draw()
        self.vo = vo
        
        # start_y = self.image_rect.y        
        vox = self.vo * math.cos(self.angle)
        voy = self.vo * math.sin(self.angle)
        self.t += speedadd/vox
        self.image_rect.x = self.start_x + vox * self.t        
        self.image_rect.y = int(self.start_y - (voy * self.t - gravity_acceleration* 1 / 2 * (self.t**2)))
        print(self.image_rect.x, self.image_rect.y)
        
        # else:
        #     return False
    
    def check_boundary(self,):
        if (self.image_rect.x > self.bdry_right
            or self.image_rect.y >screen_height
            ):
            return False
        return True

    def chk_wall(self,rect_block_wall):
        if self.image_rect.colliderect(rect_block_wall):
            return True
        return False
     

    def chk_zombie(self,rect_zombie:pygame.Rect):
        # pygame.draw.rect(screen,'red',rect_zombie)
        rect_z = rect_zombie.inflate(-90,-30) 
        # pygame.draw.rect(screen,'green',rect_z)
        if self.image_rect.colliderect(rect_z):
            return True
        return False      

class Text:
    def __init__(self, text, color, fontsize=50) -> None:
        self.text = text
        self.fontsize = fontsize
        self.color = color
        self.font = pygame.font.Font(None, fontsize)
        self.updatesurf()

    def updatesurf(
        self,
    ):
        self.fontsurf = self.font.render(self.text, 1, self.color)

    def write(self, ds: pygame.Surface, pos):
        self.pos = pos
        ds.blit(self.fontsurf, self.pos)

    def updatetext(self, text):
        self.text = text
        self.updatesurf()

class Bean(gameObject):
    def __init__(self, image_surf, image_rect, boundary_left, boundary_right, *groups) -> None:
        super().__init__(image_surf, image_rect, boundary_left, boundary_right, *groups)
        
    def updateimage(self, image):
        self.image_surf = image
        

def gameloop():
    fps = 10
    bean_rect = dic_img_bean[0].get_rect(x=0, y=screen_height - 120)  
      
    rect_zombie = img_zombie.get_rect(x=screen_width - 150, y=screen_height - 150)
    rect_zombie_shrink = rect_zombie.inflate(-80, -10)
    rect_grass = img_grass.get_rect(bottom=screen_height)
    
    firepower = 100
    score = 0
    gamerun = True
    angle = 0
    block_wall = wall(bean_rect, rect_zombie)
    direct = None
    bean_0 = Bean(dic_img_bean[angle], bean_rect, 0, block_wall.x)
    # bean_head = gameObject(img_head, bean_rect, 0, block_wall.x)
    
    # rect_bullet = pygame.draw.circle(img_bullet,"green",img_bullet.get_rect().center,5)
    zombie_role = gameObject(
        img_zombie, rect_zombie, block_wall.rect.right, screen_width
    )
    zombie_direct = "left"
    zombie_opposite_direct = "right"
    firepowershow = Text(f"firepower:{firepower}", "black")
    score_show = Text(f"score:{score}",'black')
    # fire = False
    # count = 0
    bullets = []
    while gamerun:
        # start_x, start_y = bean_head.image_rect.center
        old_angle = angle
        rect_bullet = img_bullet.get_rect(center = bean_0.image_rect.center)
        rect_bullet.move_ip(0,-20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerun = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle += 15
                    if angle >= 90:
                        angle = 85
                elif event.key == pygame.K_DOWN:
                    angle -= 15
                    if angle < 0:
                        angle = 0
                    if angle == 70:
                        angle = 75
                elif event.key == pygame.K_LEFT:
                    direct = "left"                    
                elif event.key == pygame.K_RIGHT:
                    direct = "right"                    
                elif event.key == pygame.K_a:
                    firepower -= 10
                    firepowershow.updatetext("firepower:%d" % firepower) 
                elif event.key == pygame.K_d:
                    firepower += 10
                    firepowershow.updatetext("firepower:%d" % firepower)
            if event.type == pygame.KEYUP:
                if direct is not None:
                    bean_0.move(direct)
                    # bean_body.move(direct)
                    direct = None
                if event.key == pygame.K_SPACE:                
                    # b = Bullet(img_bullet,rect_bullet.copy(),0,screen_width)
                    bullets.append(Bullet(img_bullet,rect_bullet.copy(),angle/180 * math.pi,0,screen_width))
                    # fire = True
        if angle != old_angle:
            bean_0.updateimage(dic_img_bean[angle])
        if zombie_role.move(zombie_direct):
            tmp = zombie_direct
            zombie_direct = zombie_opposite_direct
            zombie_opposite_direct = tmp
        screen.fill(background)
        # if fire:
        for b in bullets:
            # print(f"{count}:angle:{angle}")
            if b.check_boundary():
                b.updatepos(firepower,)
                if b.chk_wall(block_wall.rect):
                    print('hit the wall')
                    bullets.remove(b)
                elif b.chk_zombie(zombie_role.image_rect):
                    print(zombie_role.image_rect.x)
                    print('hit the zombie')
                    bullets.remove(b)

            else:
                bullets.remove(b)
     
            # count += 1
        
        screen.blit(img_grass, rect_grass)
        block_wall.draw()
        bean_0.draw()
        # bean_head.draw()
        zombie_role.draw()
        firepowershow.write(screen, (10, 10))
        score_show.write(screen,(screen_width-score_show.fontsurf.get_width(),10))
        # pygame.draw.circle(screen,'red',rect_bullet.center,10)

        pygame.display.update()
        c.tick(fps)
       
    pygame.quit()
    quit()


gameloop()
