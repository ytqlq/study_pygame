'''
画一张有25个小方格的表格，将1~25的数字顺序打乱，填在表格里面，然后以最快的速度从1数到25，并且边读边指出，一人指读一人帮忙计时。可以多制作几张这样的训练表，每天一练。
1.随机生成表格 ；
2.按顺序点击，错误有提示音；
3.开始有计时功能。
'''
import pygame
import random

# from pygame.sprite import _Group

font = None
numsize = 80
num_color = 'black'
def create_table():
    '''生成一个5＊5的表格，数字随机生成'''
    l = list(range(1,26))
    random.shuffle(l)
    l_table = []
    for i in range(0,21,5):
        l_table.append(l[i:i+5])
    return l_table
    # print(l_table)

class BlockNum(pygame.sprite.Sprite):
    def __init__(self, num, numpos:tuple,font = font, *groups) -> None:
        super().__init__(*groups)
        font = pygame.font.Font(font,numsize)
        self.image = font.render(str(num),1,num_color)
        self.rect = self.image.get_rect(center = numpos) 
        self.clicked = False
        self.num = num
        
    
    def draw(self,dessurface:pygame.Surface):
        dessurface.blit(self.image,self.rect)
    
    def update(self,dessurface:pygame.Surface) -> None:
        if self.clicked:
            # print('111111')
            # self.makeflag()
            pygame.draw.arc(dessurface,'red',self.rect,0,6.28)
            self.clicked = False
            return True
        return False
        # return super().update(*args, **kwargs)
    
    def makeflag(self):
        print('111111')
        pygame.draw.arc(self.image,'red',self.image.get_rect(),0,6.28)
        # self.image.fill('red')
        # self.image = pygame.Surface(self.rect.size,masks='red')
        
        

    def click(self,rightnum):
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if self.num == rightnum:
                self.clicked = True
            return True
        

    def unclick(self):
        if self.clicked:
            self.clicked = False
        
        

def main():
    pygame.init()
    size = (600,800)
    screen = pygame.display.set_mode(size,pygame.SCALED)
   
    table_wh = 550
    line_w = 3
    pygame.display.set_caption("Schulte Square")

    bg_surf = pygame.Surface(screen.get_size())
    bg_surf.fill('grey')
    table_surf = pygame.Surface((w := table_wh+line_w,w))
    table_rect = table_surf.get_rect(center = bg_surf.get_rect().center)

    for i in range(6):
        pygame.draw.line(bg_surf,'black',(table_rect.left,ih := table_rect.top + i * table_wh/5),(table_rect.right-line_w,ih),width=line_w)
        pygame.draw.line(bg_surf,"black",(iw := table_rect.left + table_wh/5 *i,table_rect.top),(iw,table_rect.bottom-line_w),width=line_w)
    screen.blit(bg_surf,(0,0))
   
    numlist = create_table()# 5*5二维数组
    numsp = pygame.sprite.RenderPlain()
    for i in range(5):
        for j in range(5):
            numrect = pygame.Rect(table_rect.left + j * table_wh /5, table_rect.top + i * table_wh/5, table_wh /5 + line_w, table_wh/5 + line_w )
            numpos = numrect.center
            num = numlist[i][j]
            blocknum = BlockNum(num, numpos)
            blocknum.draw(screen)
            numsp.add(blocknum)
    
    pygame.display.flip()        
    
    running = True
    cur_num = 1
    while running:
        if cur_num > 25:
            print("complete.")#结束。
            running = False
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                for item in numsp:
                    if item.click(cur_num):
                        if item.update(screen):
                            cur_num += 1
                        break
                        
                
            if e.type == pygame.MOUSEBUTTONUP:
                ...
        # numsp.update(screen)
        pygame.display.flip()
    
if __name__ == '__main__':
    main()


