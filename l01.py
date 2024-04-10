import pygame as pg
import os


pwdpath = os.path.split(os.path.abspath(__file__))[0]
# print(filename)
screen_w = 800
screen_h = 600

alien_w = 80
alien_h = 45

class GameObject():
    def __init__(self, image,height, speed) -> None:

        self.image = image
        self.speed = speed
        self.pos = self.image.get_rect().move(0,height)

    
        
        

    def move(self, up = False, down= False, left = False, right = False):
        if up:
            self.pos.top -=self.speed
        if down:
            self.pos.top += self.speed
        if left:
            self.pos.left -= self.speed
        if right:
            self.pos.left += self.speed
        
        if self.pos.right <0:
            self.pos.left = screen_w
        elif self.pos.left > screen_w:
            self.pos.right = 0
        
        if self.pos.bottom < 0:
            self.pos.top = screen_h
        elif self.pos.top > screen_h:
            self.pos.bottom = 0




def load_image(fn):
    fn_abspath = os.path.join(pwdpath,'pics',fn)
    return pg.image.load(fn_abspath).convert()
  

def main():
    pg.init()
    c = pg.time.Clock()
    screen = pg.display.set_mode((screen_w,screen_h))
    pg.display.set_caption('space+alien')
    bg_image = load_image('space.jpeg')
    UFO_image = load_image('UFO.jpg')
    UFO_image = pg.transform.scale(UFO_image,(alien_w,alien_h))    
    ufo = GameObject(UFO_image,100,10)
    

    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                return
        keys = pg.key.get_pressed()
        if keys[pg.K_w]:
            ufo.move(up=True)
        if keys[pg.K_s]:
            ufo.move(down=True)
        if keys[pg.K_a]:
            ufo.move(left=True)
        if keys[pg.K_d]:
            ufo.move(right=True)
        # print(ufo.pos.left)
        screen.blit(bg_image,(0,0))
        screen.blit(ufo.image,ufo.pos)
        pg.display.update()
        c.tick(60)


if __name__ == '__main__':
    main()
    pg.quit()