from typing import Any


try:
    import pygame
    from pygametemplate.tools import *
    import os.path
    import random
except ImportError:
    print('import failed.')
    
screen_size = (800,600)#todo
caption = 'GameName'# todo
bg_color = (225,225,225)# todo    


class picBlock(pygame.sprite.Sprite):
    def __init__(self, pic_no:tuple, block_size= (100,100),colcount= 4,rowcount = 3, line_w_boundary = 2, table_topleft = (200,10),table_bottomright= (600,310),*groups) -> None:
        super().__init__(*groups)
        self.pic_no = pic_no
        self.surf = pygame.Surface(block_size)
        # screen_surf = pygame.display.get_surface()  
        # scree     
        # self.size = block_size
        x_add = 0
        y_add = 0
        if pic_no[0]>= rowcount -1:
            y_add = line_w_boundary        
        if pic_no[1] >=colcount -1 :
            x_add = line_w_boundary        
        self.size = (block_size[0]+x_add,block_size[1]+y_add)    
        self.right_pos = (table_topleft[0]+pic_no[1]*block_size[0],table_topleft[1]+pic_no[0]*block_size[1])     
        self.img_area_rect = pygame.Rect((0+pic_no[1]*block_size[0],0+pic_no[0]*block_size[1]),self.size)
        pos_x = random.randrange(0,screen_size[0]-self.size[0])
        pos_y = random.randrange(table_bottomright[1],screen_size[1]-self.size[1])
        self.pos = (pos_x,pos_y)
        
        
    def update(self,pos) -> None: 
        self.pos = pos
        
          
    
    def draw(self,image:pygame.Surface,ds_surface:pygame.Surface):        
        self.image = image        
        self.surf.blit(image,(0,0),self.img_area_rect)
        ds_surface.blit(self.surf,self.pos)
    
    def chk_right(self,pic_no):
        if self.pos == self.right_pos:
            return True
    


def main():    
    
    fps = 24
    c = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(caption)
    screen.fill(bg_color)
    table_topleft = (200,10)
    table_bottomright = (600,310)
    
    table_rowcount = 3
    table_colcount = 4
    boundary_line_width = 2
    table_rect = draw_table(screen,table_topleft,table_bottomright,table_rowcount,table_colcount,line_width_boundary = boundary_line_width)    
    picpath = get_obj_path(__file__,'pics/cut01.jpg')
    
    img_surf = load_img(picpath).convert()
    scale_img_surf = pygame.transform.scale(img_surf,table_rect.size)  
    # print(table_rect.size) 
    # screen.blit(scale_img_surf,table_topleft)
    # pygame.display.update()
     
    # pic_no = (0,0)
    block_size = (table_rect.size[0]//table_colcount,table_rect.size[1]//table_rowcount)#(100,100)
   
    pic_block_list = []
    
    for i in range(table_rowcount):
        pic_block_list.append([])
        for j in range(table_colcount):
            tmp_pic_block = picBlock((i,j),block_size=block_size,colcount=table_colcount,rowcount=table_rowcount,line_w_boundary=boundary_line_width,table_topleft=table_topleft,table_bottomright=table_bottomright)
            tmp_pic_block.draw(scale_img_surf,screen)
            # print(tmp_pic_block.pic_no,tmp_pic_block.pos)
            # pygame.display.update()
            # pygame.time.wait(1000)
            pic_block_list[i].append(tmp_pic_block)
            # break
    pygame.display.update()
    
    
    gameRun = True
    
    while gameRun:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
        
        pygame.display.update()
        c.tick(fps)



if __name__ == '__main__':
    main()




    