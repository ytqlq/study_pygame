import pygame
import sys
import random

screen_w = 600
screen_h = 800
row = 7
col = 15
fontcolor = 'green'
fontsize = 35
typeface = 'arial'
fontspace = 2
linecolor = 'red'

def getanothernum(num):
    TFtest = [True] * 6 + [False] * 3
    l = list(range(10))
    l.remove(num)
    if TFtest[random.randint(0,8)]:
        return num
    else:
        return random.choice(l)
 
     
def getnumpair(typeface = typeface, fontsize = fontsize, fontcolor = fontcolor):
    
    upnum = random.randint(0,9) 
    downnum = getanothernum(upnum)    
    numfont = pygame.font.SysFont(typeface,fontsize)
    upnumsurface = numfont.render(str(upnum), True, fontcolor)
    downnumsurface = numfont.render(str(downnum), True, fontcolor)    
    return (upnumsurface, downnumsurface)


def main():
    pygame.init()
    screen = pygame.display.set_mode((screen_w,screen_h))    
    block_h = 90
    topspace = (screen_h - block_h * row)//2
    block_w = fontsize
    leftspace = (screen_w - block_w * col)//2
    for i in range(row):
        pygame.draw.line(screen, linecolor, (leftspace, topspace + fontsize +fontspace//2+ i * block_h), (screen_w - leftspace, topspace + fontsize +fontspace//2 + i * block_h) )
        for j in range(col):
            upnum, downnum = getnumpair()
            uprect = pygame.Rect((leftspace + j * block_w, topspace + i * block_h), (block_w, block_w))
            downrect = uprect.move(0, fontsize +fontspace)
            screen.blit(upnum,uprect)
            screen.blit(downnum,downrect)
    
    
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()
        pygame.display.update()
    
                
    




if __name__ == '__main__':
    main()
    # pygame.quit()
