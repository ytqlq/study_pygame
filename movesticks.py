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

sc_size = (600,800)
block_w = 80
colornum = 7
color_line = 'white'

def drawtable(dessurface:pygame.Surface,startpos:tuple, block_w=block_w, rowcol = colornum, color = color_line):    
    for i in range(rowcol):
        if i %2 != 0:
            rect_grey = pygame.Rect((startpos[0],startpos[1]+i*block_w),(block_w * rowcol,block_w))
            dessurface.fill('grey',rect_grey)
    for i in range(rowcol +1):
        pygame.draw.line(dessurface, color,(startpos[0],startpos[1]+i*block_w),(startpos[0]+rowcol*block_w,startpos[1]+i*block_w))
        pygame.draw.line(dessurface,color,(startpos[0]+i*block_w,startpos[1]),(startpos[0]+i*block_w, startpos[1]+rowcol*block_w))
  

def main():
    pygame.init()
    screen = pygame.display.set_mode(sc_size,pygame.SCALED)
    # 画表格
    startpoint = ((sc_size[0]-colornum*block_w)//2,(sc_size[1] - colornum*block_w)//2)
    drawtable(screen,startpoint)
    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        pygame.display.update()
if __name__ == "__main__":
    main()
 
    





