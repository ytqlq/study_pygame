"""
这是一个游戏。主要内容：通过鼠标移动打乱的不同颜色的圆点，以满足题目要求。包括将每行都是一样的／每行都不一样等。
红：255,0,0
橙:255,125,0
黄：255,255,0
绿：0,255,0
蓝：0,0,255
靛:0,255,255
紫:255,0,255
"""

import pygame
import random

sc_size = (600, 800)
q_font_size = 30
q_font_color = (155, 48, 255 )
# bg_color = (28, 28, 28)
bg_color = (205, 190, 112)  # 背景颜色
block_w = 80
colornum = 7 # 行列值
color_line = "white" #线色
# color_line = ( 	176, 226, 255 )
line_width = 1 #线宽
color_row_block = (211, 211, 211, 10)  # grey
color_circle = (
    (255, 0, 0),
    (255, 125, 0),
    (255, 255, 0),
    (0, 255, 0),
    (0, 0, 255),
    (0, 255, 255),
    (255, 0, 255),
)
circlescale = 0.8
problems = ["Make all the colors of the circles in any row same.",
            "Make all the colors of the circles in any row different."]
solution = ['judgesame','judgediff']





def get_table_surf(
    block_w=block_w,
    rowcol=colornum,
    color=color_line,
    line_width=line_width,
    color_row_block=color_row_block,
):
    sf_size = (sf_w := block_w * rowcol + line_width, sf_w)
    sf = pygame.Surface(sf_size)
    sf.fill(bg_color)
    
    for i in range(rowcol):
        if i % 2 != 0:
            rect_grey = pygame.Rect((0, i * block_w), (sf_w, block_w))
            sf.fill(color_row_block, rect_grey)
    for i in range(rowcol + 1):
        pygame.draw.line(sf, color, (0, i * block_w), (rowcol * block_w, i * block_w))
        pygame.draw.line(sf, color, (i * block_w, 0), (i * block_w, rowcol * block_w))
    return sf


def drawtable(sf: pygame.Surface, dessurface: pygame.Surface):
    sf_rect = sf.get_rect(center=dessurface.get_rect().center)
    dessurface.blit(sf, sf_rect)
    return sf_rect


class Stick:
    def __init__(self, color, des_rect: pygame.Rect, scale=circlescale) -> None:
        self.color = color
        self.des_rect = des_rect
        self.radius = self.des_rect.w / 2 * scale
        self.circle_rect = pygame.Rect((0, 0), (w := self.radius * 2, w))
        self.circle_rect.center = self.des_rect.center

    def drawcircle(self, dessurface: pygame.Surface):
        if self.color:
            return pygame.draw.circle(
                dessurface, self.color, self.circle_rect.center, self.radius
            )

    def delete(self, dessurface: pygame.Surface, dessfcp: pygame.Surface):
        dessurface.blit(dessfcp, self.circle_rect, self.circle_rect)
        self.color = None

    def upate(self, mousecolor, dessurface: pygame.Surface, dessfccp: pygame.Surface):
        tmpcolor = mousecolor
        mousecolor = self.color
        self.color = tmpcolor
        if self.color:
            self.drawcircle(dessurface)
        else:
            dessurface.blit(dessfccp, self.circle_rect, self.circle_rect)
        return mousecolor


def get_sticks(
    sf_rect: pygame.Rect,
    dessurface: pygame.Surface,
    total=colornum,
    line_width=line_width,
    block_w=block_w,
):
    sticks = []
    d_color = dict.fromkeys(color_circle, 0)
    offset = (sf_rect.x - dessurface.get_rect().x, sf_rect.y - dessurface.get_rect().y)
    for j in range(total):
        for i in range(total):
            pos = (i * block_w + offset[0], j * block_w + offset[1])
            circle_color = random.choice(color_circle)
            while d_color[circle_color] >= 7:
                circle_color = random.choice(color_circle)
            d_color[circle_color] += 1
            size = (block_w + line_width, block_w + line_width)
            r = pygame.Rect(pos, size)
            s = Stick(circle_color, r)
            sticks.append(s)
    return sticks


def draw_all_sticks(sticks: list, dessurface: pygame.Surface):
    for item in sticks:
        item.drawcircle(dessurface)

def showtext(text:str, q_font_size = q_font_size):
    q_font = pygame.font.Font(None,q_font_size)
    q_font_surf = q_font.render(text,1,q_font_color)
    return q_font_surf
    

        
        
        

def judgesame(sticks:list,num = colornum):
    i = 0
    ref = None
    for item in sticks:
        if i % num == 0:
            ref = item.color
            i += 1
            continue
        print(ref,item.color)
        if item.color != ref:
            # print("same wrong.")           
            
            return False               
        i += 1
    # print('All same.')
    return True
            
   
    
    
def judgediff(sticks:list,num = colornum):
    i = 0
    existcolor = []
    for item in sticks:
        if i % num == 0:
            existcolor.clear()
        if item.color in existcolor:            
            return False
        existcolor.append(item.color)
        i += 1    
    return True
    



def main():
    pygame.init()
    fps = 60
    c = pygame.time.Clock()
    screen = pygame.display.set_mode(sc_size, pygame.SCALED)
    screen.fill(bg_color)
    sf = get_table_surf()
    sf_rect = drawtable(sf, screen)
    screencp = screen.copy()
    sticks = get_sticks(sf_rect, screen)
    running = True
    mouse_color = None
    qa_dict = dict()
    for k, v in zip(problems,solution):
        qa_dict[k] = v
    # print(qa_dict)
        
    q_text = random.choice(problems)
    q_font_surf = showtext(q_text)
    
    
    q_font_rect = q_font_surf.get_rect(centerx = screen.get_rect().centerx,y = 40)
    submit_font_surf = showtext("SUBMIT",80)
    sub_font_rect = submit_font_surf.get_rect(centerx = screen.get_rect().centerx, centery = sc_size[1] - 50)
    wrong_font_surf = showtext("Wrong Answer.")
    right_font_surf = showtext('Bravo!')
    wfs_rect = wrong_font_surf.get_rect(centerx = screen.get_rect().centerx,y = 80)
    rfs_rect = right_font_surf.get_rect(centerx = screen.get_rect().centerx,y = 80)
    sub = False
    while running:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False
            if e.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                if sub_font_rect.collidepoint(pos):
                    
                    func = globals()[qa_dict[q_text]]                    
                    worr = func(sticks)
                    sub = True
                       
                    
                    # break
                    
                for s in sticks:
                    if s.circle_rect.collidepoint(pos):
                        mouse_color = s.upate(mouse_color, screen, screencp)
                        break
        screen.fill(bg_color)
        screen.blit(q_font_surf,q_font_rect)
        screen.blit(submit_font_surf,sub_font_rect)
        drawtable(sf, screen)
        draw_all_sticks(sticks, screen)
        if sub:
            if worr:
                screen.blit(right_font_surf,rfs_rect)
            else:
                screen.blit(wrong_font_surf,wfs_rect)
        
        mouse_pos = pygame.mouse.get_pos()
        if mouse_color is not None:
            pygame.draw.circle(screen, mouse_color, mouse_pos, sticks[0].radius)
        pygame.display.update()
        c.tick(fps)


if __name__ == "__main__":
    main()
