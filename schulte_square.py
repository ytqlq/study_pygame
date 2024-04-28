'''
画一张有25个小方格的表格，将1~25的数字顺序打乱，填在表格里面，然后以最快的速度从1数到25，并且边读边指出，一人指读一人帮忙计时。可以多制作几张这样的训练表，每天一练。
1.随机生成表格 ；
2.按顺序点击，错误有提示音；
3.开始有计时功能。
'''
import pygame
import random

from pygame.sprite import _Group

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
    def __init__(self, num, numpos:tuple, *groups: AbstractGroup[_SpriteSupportsGroup]) -> None:
        super().__init__(*groups)
        font = pygame.font.Font(font,numsize)
        self.image = font.render(str(num),1,num_color)
        self.rect = self.image.get_rect(center = numpos) 


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
    pygame.display.flip()
    numlist = create_table()# 5*5二维数组


    running = True
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
        
    
if __name__ == '__main__':
    main()


