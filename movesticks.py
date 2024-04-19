'''
这是一个游戏。主要内容：通过鼠标移动打乱的不同颜色的圆点，以满足题目要求。包括将每行都是一样的／每行都不一样等。
红：255,0,0
橙:255,125,0
黄：255,255,0
绿：0,255,0
蓝：0,0,255
靛:0,255,255
紫:255,0,255
'''
import pygame
import random

sc_size = (600,800)
# bg_color = (255,235, 205)
block_w = 80
colornum = 7
color_line = 'white'
line_width = 1
color_row_block = (211,211,211,10)# grey
color_circle = ((255,0,0),(255,125,0),(255,255,0),(0,255,0),(0,0,255),(0,255,255),(255,0,255))
circlescale = 0.8


def drawtable( block_w=block_w, rowcol = colornum, color = color_line, line_width = line_width, color_row_block = color_row_block):   
      
    sf_size = (sf_w :=block_w * rowcol + line_width,sf_w)
    sf = pygame.Surface(sf_size)
    # sf.fill(bg_color)
    for i in range(rowcol):
        if i %2 != 0:
            rect_grey = pygame.Rect((0,i*block_w),(sf_w,block_w))
            sf.fill(color_row_block,rect_grey)
    for i in range(rowcol +1):
        pygame.draw.line(sf, color,(0,i*block_w),(rowcol*block_w,i*block_w))
        pygame.draw.line(sf,color,(i*block_w,0),(i*block_w, rowcol*block_w))
    draw_all_sticks(sf)
    return sf

class Stick:
    def __init__(self, color, des_rect:pygame.Rect, scale = circlescale ) -> None:        
        self.color = color
        self.des_rect = des_rect        
        self.radius = self.des_rect.w /2 *scale
        
    def drawcircle(self,dessurface:pygame.Surface):
        return pygame.draw.circle(dessurface, self.color, self.des_rect.center,self.radius)
        
        
def draw_all_sticks(dessurface:pygame.Surface, total = colornum, line_width = line_width,block_w = block_w):
    d_color = dict.fromkeys(color_circle,0)
    
    for i in range(total):
        for j in range(total):
            pos = (i*block_w+line_width, j*block_w+line_width)
            
            circle_color = random.choice(color_circle)
            while d_color[circle_color] >= 7:
                circle_color = random.choice(color_circle)
            d_color[circle_color] += 1             
            
            size = (block_w-line_width,block_w-line_width)
            r = pygame.Rect(pos, size)
            s = Stick(circle_color,r)
            s.drawcircle(dessurface)
            
            
            
            
    
    
    
        
    

def main():
    pygame.init()
    screen = pygame.display.set_mode(sc_size,pygame.SCALED)
    # 画表格
    # screen.fill(bg_color)
    
    sf = drawtable()
    sf_rect = sf.get_rect(center = screen.get_rect().center)
    screen.blit(sf,sf_rect)    
    
    
    # pygame.draw.circle()
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        pygame.display.update()
if __name__ == "__main__":
    main()
 
    





