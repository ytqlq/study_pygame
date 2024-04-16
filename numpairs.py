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
rate = 0.33 # 控制出现错误数字对的概率。
fps = 60 #刷新频率
scorecolor = 'white'
score_font_size = 60
commitwidth = 120
commith = 60
commit_bg_color = 'white'
commit_font_color = 'blue'
commit_font_size = 60
commit_w = screen_w/2
commit_h = 90

def getanothernum(num):
    falserate = int(9*rate)
    TFtest = [True] * (9-falserate) + [False] * (falserate)
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

def showfinalscore(score:int, answer:int, dessurface:pygame.Surface, color = scorecolor):
    scorefont = pygame.font.Font(None, score_font_size)
    score_sf = scorefont.render("SCORE:{0}/{1}".format(score, answer),1,color)
    score_rect = score_sf.get_rect(centerx = dessurface.get_rect().centerx, y = 10)
    # print(score_rect.x, score_rect.y)
    dessurface.blit(score_sf,score_rect)
    
    # return score_sf



def main():
    pygame.init()
    c = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_w,screen_h), pygame.SCALED)    
    
    block_h = 90
    topspace = (screen_h - block_h * row)//2
    block_w = fontsize
    leftspace = (screen_w - block_w * col)//2
    l_flag = [] # 上下两块的合起来的块。存入list.
    countwrong = 0 # 统计出题时的不一样对的数量，最后输出成绩时使用，表达正确率。
    for i in range(row):
        # l_flag.append([])
        pygame.draw.line(screen, linecolor, (leftspace, topspace + fontsize +fontspace//2+ i * block_h), (screen_w - leftspace, topspace + fontsize +fontspace//2 + i * block_h) )
        for j in range(col):            
            uprect = pygame.Rect((leftspace + j * block_w, topspace + i * block_h), (block_w, fontsize))
            downrect = uprect.move(0, fontsize +fontspace)
            
            upnum, downnum, same = getnumpair()
            if not same:
                countwrong += 1
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
    
    commitfont = pygame.font.Font(None,commit_font_size)
    commitsf = commitfont.render('COMMIT', 1, commit_font_color, commit_bg_color)        
    commit_font_rect = commitsf.get_rect(centerx = screen.get_rect().centerx, y = screen_h - 80)   
    screen.blit(commitsf, commit_font_rect)
    
    showscore = False
    
    while True:
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                # print('Total score:{0}/{1}'.format((finalscore - len(wronganswerrect)),countwrong))
                sys.exit()
            # if e.type == pygame.MOUSEBUTTONDOWN:                
            #     m_pos = pygame.mouse.get_pos()
            #     if m_pos[0] 
            
        mps = pygame.mouse.get_pressed()
        if mps[0]:
            x,y = pygame.mouse.get_pos()
            if commit_font_rect.collidepoint(x,y) and not showscore:
                showfinalscore(finalscore - len(wronganswerrect), countwrong, screen)
                showscore = True
                # return
                # print('gg')
                
            for i, same in l_flag:
                # for i in item:
                if i.collidepoint(x,y):
                    # print('mousepressed.')
                    # pygame.draw.ellipse(screen,'red',i)
                    if not showscore:
                        arcrect = pygame.draw.arc(screen,flagcolor,i,0,6.28,2)
                        if arcrect not in existarcrect:
                            existarcrect.append(arcrect)
                            finalscore += 1
                            # print('add {0}'.format(finalscore))
                        # 记录上下数字不一致的rect,保存到数组中。
                            if same:
                                wronganswerrect.append(arcrect)
                         
        if mps[2]:# 点右键去掉椭圆标记。
            x,y = pygame.mouse.get_pos()
            for r in existarcrect:
                if r.collidepoint(x,y):
                    if not showscore:
                        screen.blit(screencp,r,r)
                        finalscore -= 1
                        existarcrect.remove(r)
                        if r in wronganswerrect:
                            wronganswerrect.remove(r)
                    
            
        
        pygame.display.update()
        
        c.tick(fps)
    # pygame.quit()
    
 
if __name__ == '__main__':
    main()
    pygame.quit()
