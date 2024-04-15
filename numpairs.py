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
flagcolor = 'red'

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
    return (upnumsurface, downnumsurface, upnum == downnum)


def calscore():
    
    ...

def main():
    pygame.init()
    c = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_w,screen_h))    
    block_h = 90
    topspace = (screen_h - block_h * row)//2
    block_w = fontsize
    leftspace = (screen_w - block_w * col)//2
    l_flag = [] # 上下两块的合起来的块。存入list.
    for i in range(row):
        # l_flag.append([])
        pygame.draw.line(screen, linecolor, (leftspace, topspace + fontsize +fontspace//2+ i * block_h), (screen_w - leftspace, topspace + fontsize +fontspace//2 + i * block_h) )
        for j in range(col):            
            uprect = pygame.Rect((leftspace + j * block_w, topspace + i * block_h), (block_w, fontsize))
            downrect = uprect.move(0, fontsize +fontspace)
            
            upnum, downnum, same = getnumpair()
            
            upnumrect = upnum.get_rect()
            upnumrect.center = uprect.center
            downnumrect = downnum.get_rect()
            downnumrect.center = downrect.center
            
            flag_rect = uprect.union(downrect)
            # print(flag_rect.topleft == uprect.topleft)
            # l_flag[i].append(flag_rect)            
            l_flag.append((flag_rect,same))    
            screen.blit(upnum,upnumrect)
            screen.blit(downnum,downnumrect) 
            # print(l_flag)      
    existarcrect = []
    screencp = screen.copy()
    finalscore = 0
    wronganswerrect = []
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                print('Total score:{0}'.format(finalscore - len(wronganswerrect)))
                sys.exit()
            # if e.type == pygame.MOUSEBUTTONDOWN:                
            #     m_pos = pygame.mouse.get_pos()
            #     if m_pos[0] 
         
        mps = pygame.mouse.get_pressed()
        if mps[0]:
            x,y = pygame.mouse.get_pos()
            for i, same in l_flag:
                # for i in item:
                if i.collidepoint(x,y):
                    # print('mousepressed.')
                    # pygame.draw.ellipse(screen,'red',i)
                    arcrect = pygame.draw.arc(screen,flagcolor,i,0,6.28,2)
                    if arcrect not in existarcrect:
                        existarcrect.append(arcrect)
                        finalscore += 1
                        print('add {0}'.format(finalscore))
                    # 记录上下数字不一致的rect,保存到数组中。
                        if same:
                            wronganswerrect.append(arcrect)
                            
                          
        if mps[2]:# 点右键去掉椭圆标记。
            x,y = pygame.mouse.get_pos()
            for r in existarcrect:
                if r.collidepoint(x,y):
                    screen.blit(screencp,r,r)
                    finalscore -= 1
                    existarcrect.remove(r)
                    if r in wronganswerrect:
                        wronganswerrect.remove(r)
                    print("-{0}".format(finalscore))
                    
            
        # pygame.time.wait(1000)
        pygame.display.update()
        # pygame.time.wait(1000)
        c.tick(60)
    # pygame.quit()
    
 
if __name__ == '__main__':
    main()
    pygame.quit()
