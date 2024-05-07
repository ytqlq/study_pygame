"""
画一张有25个小方格的表格，将1~25的数字顺序打乱，填在表格里面，然后以最快的速度从1数到25，并且边读边指出，一人指读一人帮忙计时。可以多制作几张这样的训练表，每天一练。
1.随机生成表格 ；
2.按顺序点击，错误有提示音；
3.开始有计时功能。
"""

import pygame
import random
import os.path
import shelve

font = None
numsize = 80
num_color = "black"


def create_table():
    """生成一个5＊5的表格，数字随机生成"""
    l = list(range(1, 26))
    random.shuffle(l)
    l_table = []
    for i in range(0, 21, 5):
        l_table.append(l[i : i + 5])
    return l_table
 
def blitfont(text, font = None,ftsize = 50,color = 'black',bgcolor = None):
    ft = pygame.font.Font(font,ftsize)
    return ft.render(text,1,color,bgcolor)

class BlockNum(pygame.sprite.Sprite):
    def __init__(self, num, numpos: tuple, font=font, *groups) -> None:
        super().__init__(*groups)
        font = pygame.font.Font(font, numsize)
        self.image = font.render(str(num), 1, num_color)
        self.rect = self.image.get_rect(center=numpos)
        self.clicked = False
        self.num = num

    def draw(self, dessurface: pygame.Surface):
        dessurface.blit(self.image, self.rect)

    def update(self, dessurface: pygame.Surface) -> None:
        if self.clicked:
            # print('111111')
            # self.makeflag()
            pygame.draw.arc(dessurface, "red", self.rect, 0, 6.28,width=2)
            self.clicked = False
            return True
        return False
       
    def click(self, rightnum):
        pos = pygame.mouse.get_pos()
        # test_rect = self.rect.inflate(1.8, 1.8)
        test_rect = pygame.Rect((0,0),(85,85)) # 指定大小，格子大小为110＊110（含线宽）,字体大小为80，比字体稍大，不大于格子
        test_rect.center = self.rect.center
        # print("{0}.....{1}".format(self.rect.size,test_rect.size))
        if test_rect.collidepoint(pos):
            if self.num == rightnum:
                self.clicked = True
            return True

    def unclick(self):
        if self.clicked:
            self.clicked = False
def show_history():
    ...



def main():

    maindir = os.path.split(__file__)[0]
    ftpath = os.path.join(maindir,"zh_font/heiti_GB18030.ttf")
    pygame.init()
    c = pygame.time.Clock()
    size = (600, 800)
    screen = pygame.display.set_mode(size, pygame.SCALED)
    fps = 60
    table_wh = 550
    line_w = 3
    pygame.display.set_caption("Schulte Square")

    bg_surf = pygame.Surface(screen.get_size())
    bg_surf.fill("grey")
    table_surf = pygame.Surface((w := table_wh + line_w, w))
    table_rect = table_surf.get_rect(center=bg_surf.get_rect().center)

    
    for i in range(6):
        pygame.draw.line(
            bg_surf,
            "black",
            (table_rect.left, ih := table_rect.top + i * table_wh / 5),
            (table_rect.right - line_w, ih),
            width=line_w,
        )
        pygame.draw.line(
            bg_surf,
            "black",
            (iw := table_rect.left + table_wh / 5 * i, table_rect.top),
            (iw, table_rect.bottom - line_w),
            width=line_w,
        )
    ftsurf = blitfont("按顺序点击数字1-25",font=ftpath)
    ft_rect = ftsurf.get_rect(centerx = bg_surf.get_rect().centerx,y = 30)
    bg_surf.blit(ftsurf,ft_rect)
    screen.blit(bg_surf, (0, 0))

    numlist = create_table()  # 5*5二维数组
    numsp = pygame.sprite.RenderPlain()
    for i in range(5):
        for j in range(5):
            numrect = pygame.Rect(
                table_rect.left + j * table_wh / 5,
                table_rect.top + i * table_wh / 5,
                table_wh / 5 + line_w,
                table_wh / 5 + line_w,
            )
            numpos = numrect.center
            num = numlist[i][j]
            blocknum = BlockNum(num, numpos)
            blocknum.draw(screen)
            numsp.add(blocknum)

    # 历史成绩按钮及保存按钮
    bt_font_size = 50
    history_surf = blitfont("历史成绩",font=ftpath,ftsize=bt_font_size,bgcolor='blue')
    save_surf = blitfont("保存结果",font=ftpath, ftsize=bt_font_size,bgcolor='blue')
    history_rect = history_surf.get_rect(x=30, y =screen.get_height()-100)
    save_rect = history_surf.get_rect(right = screen.get_rect().right -30, y =screen.get_height()-100)
    back_surf = blitfont("Back",font=ftpath,bgcolor='red')
    back_rect = back_surf.get_rect(x = 0,y=0)
    
    
    
    
    
    
    pygame.display.flip()
    history_tag = False
    running = True
    cur_num = 1
    score_file = os.path.join(maindir,'score.db')
    
    while running:
        if cur_num == 0:
            screen.blit(history_surf,history_rect)
            screen.blit(save_surf,save_rect)    
        if cur_num >= 1:
            cur_time = pygame.time.get_ticks()
            timesurf = blitfont("%.1f"%(cur_time/1000),ftsize=80,bgcolor='blue')
            time_rect = timesurf.get_rect(centerx = screen.get_width()//2, y = screen.get_height()-100)            
            screen.blit(timesurf,time_rect)
        
        if cur_num > 25:                   
            cur_num = 0

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                
                with shelve.open(score_file,writeback=True) as f:
                    f_score = f.get('highest_score')                    
                    if cur_num == 0:
                        if f_score:
                            f['highest_score'] = min(f_score,cur_time)
                        else:
                            f['highest_score'] = cur_time                        
                    
                running = False
            if e.type == pygame.MOUSEBUTTONDOWN:
                for item in numsp:
                    if item.click(cur_num):
                        if item.update(screen):
                            cur_num += 1
                        break
                if history_rect.collidepoint(pygame.mouse.get_pos()) and cur_num == 0 and history_tag == False:
                    screencp = screen.copy()
                    screen.fill('blue')
                    with shelve.open(score_file) as f:
                        score = f.get("highest_score")
                    if not score:
                        score = "No data."
                    print(score)
                    score_surf = blitfont(str(score))
                    score_rect = score_surf.get_rect(center = screen.get_rect().center)
                    screen.blit(back_surf,back_rect)
                    screen.blit(score_surf,score_rect)
                    history_tag = True
                if history_tag == True and back_rect.collidepoint(pygame.mouse.get_pos()):
                    screen.blit(screencp,(0,0))
                    
                    
          
        pygame.display.flip()
        c.tick(fps)


if __name__ == "__main__":
    main()
