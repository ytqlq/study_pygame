# from pygame.sprite import _Group


from typing import Any


try:
    import pygame
    from pygame.locals import *
    from pygametemplate.tools import *
    import os.path
except ImportError:
    print("Import failed.")


class claw(pygame.sprite.Sprite):
    def __init__(self,init_pos:tuple,*groups) -> None:
        super().__init__(*groups)
        picpath = get_obj_path(__file__,'pics/clawo.png')        
        self.image = load_img(picpath).convert_alpha()
        self.rect = self.image.get_rect(x = init_pos[0],y=init_pos[1])
        self.direction = None
        
    def move(self,speed = 5):
        if self.direction is not None:
            if self.direction == 'left':
                self.rect.x -= speed
            elif self.direction == 'right':
                self.rect.x += speed            
            elif self.direction == 'down':
                self.rect.y += speed
            elif self.direction == 'up':
                self.rect.y -= speed
          
    def draw(self,ds_surf:pygame.Surface):
        ds_surf.blit(self.image,self.rect)
        
        
    def shutclaw(self,):
        picpath = get_obj_path(__file__,'pics/claws.png')        
        self.image = load_img(picpath).convert_alpha()
        self.rect = self.image.get_rect(centerx = self.rect.centerx,y = self.rect.y)
        
    def openclaw(self,):        
        picpath = get_obj_path(__file__,'pics/clawo.png')        
        self.image = load_img(picpath).convert_alpha()
        self.rect = self.image.get_rect(centerx = self.rect.centerx)
        
 
        

class Machine(pygame.sprite.Sprite):
    def __init__(self,):
        pygame.sprite.Sprite.__init__(self)                
        self.image = pygame.Surface((400,600))
        self.image.fill('blue')
        self.window_rect = pygame.Rect([25,25,350,400])
        self.image.fill('yellow',self.window_rect)
        self.claw = claw(self.window_rect.topleft)
        self.claw.draw(self.image)
        self.display_surf = pygame.display.get_surface()
        self.rect = self.image.get_rect(centerx = self.display_surf.get_rect().centerx, )
        self.coin = 0
        
    def draw(self,):        
        self.display_surf.blit(self.image,self.rect,)

    def update(self, ) -> None:
        self.image.fill('yellow',self.window_rect)
        self.claw.draw(self.image)
        self.draw()
        
    def claw_downward(self):        
        # print('down to catch')
        # self.claw.direction = 'down'
        if self.claw.rect.bottom <= self.window_rect.bottom:  
            self.claw.move()
            self.update()
            # return False
        else:            
            self.claw.shutclaw()
            self.update()
            self.claw.direction = 'up'
            # print('up')
            # return True
    
    def claw_upward(self,):        
        if self.claw.rect.top >= self.window_rect.top:
            self.claw.move()
            self.update()
       
    def catch_act(self,):
        if self.claw.direction != 'up':
            self.claw.direction = 'down'
        if self.claw.direction == 'down':
            self.claw_downward()            
        elif self.claw.direction == 'up':
            # print('upup')
            self.claw_upward()
        # if arrive_bottom:
        #     self.claw.direction = 'up'
        
        
    def dropcoin(self,coinnum):
        self.coin += 1
        

        
    
        


def main():
    c = pygame.time.Clock()  
    screen_width = 800
    scree_height = 600
    screensize = (screen_width,scree_height)
    bg_color = (225,225,225)
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption("catchdolls")
    screen.fill(bg_color)
    machine = Machine()
    machine.draw()
    start_catch = False
    gameRun = False
    machine.coin = 2 # 需要额外的统计投币功能。
    if machine.coin >=2 :
        starttime = pygame.time.get_ticks()# start
        gameRun = True
        machine.coin -= 2
    
    while gameRun:
       
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return            
            if e.type == pygame.KEYUP:
                if e.key == pygame.K_SPACE :# 5seconds
                    start_catch = True
                    # machine.claw.direction = 'down'
                # if e.key == pygame.K_c:
                #     machine.coin += 1
        # print(pygame.time.get_ticks() - starttime)
        if not start_catch and  pygame.time.get_ticks() - starttime > 2000:   
            # print('timeout')
            start_catch = True   
            # print(start_catch)      
        if start_catch:            
            machine.catch_act()
        pygame.display.update()
        c.tick(30)
    
    
if __name__ == "__main__":
    main()