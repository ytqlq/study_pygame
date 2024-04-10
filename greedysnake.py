"""
这是一个模拟贪吃蛇的游戏
"""



import pygame
import random
import sys

screen_w = 800
screen_h = 600

part_w = 40
part_h = part_w
speed = part_w
fps = 10
class SnakePart():
    def __init__(self,left,top,width=part_w, height = part_h,speed = speed) -> None:
        self.rect = pygame.Rect(left,top,width,height)
        self.speed = speed
        # self.direct = direct
        
    def move(self,Up=False,Down=False,Left = False,Right = False):
        if Up:
            self.rect.top -= self.speed
        if Down:
            self.rect.top += self.speed
        if Left:
            self.rect.left -= self.speed
        if Right:
            self.rect.left += self.speed
        

        if self.rect.left<0:
            self.rect.left = screen_w
        elif self.rect.left >= screen_w:
            self.rect.left = 0
        elif self.rect.top >= screen_h:
            self.rect.top = 0
        elif self.rect.top <0:
            self.rect.top = screen_h

        
    
pygame.init()
c = pygame.time.Clock()
screen = pygame.display.set_mode((screen_w,screen_h))
# screen.fill('blue')
pygame.display.set_caption('greedysnake')
gg = pygame.image.load('pics/gameover.png').convert()

hdx = random.randint(0,19)*part_w
hdy = random.randint(0,15)*part_h

head = SnakePart(hdx,hdy)
head_rect = head.rect

# head2 = SnakePart(screen.get_rect().centerx,screen.get_rect().centery)
# head_rect2 = head2.rect

# print(head_rect == head_rect2)
screen.fill('blue')

def snakemove(snakelist,head_rect,eaten=False):
    snakelist.insert(1,head_rect)
    if not eaten:
        snakelist.pop()
    return snakelist


direct = 'right'
running = True
snake = [head_rect]
foodexist = False
while running:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False
               
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if len(snake) == 1:
            direct = 'up'
        elif direct != 'down' :
            direct = 'up'
        # head.move(Up=True)
    if keys[pygame.K_s]:
        # head.move(Down=True)
        if len(snake) == 1:
            direct = 'down'
        elif direct != 'up':
            direct = 'down'
    if keys[pygame.K_a]:
        if len(snake) == 1:
            direct = 'left'
        elif direct != 'right':
            direct = 'left'
        # head.move(Left=True)
    if keys[pygame.K_d]:
        if len(snake) == 1:
            direct = 'right'
        elif direct != 'left':
            direct = 'right'
        # head.move(Right=True)
    for p in snake:
        pygame.draw.rect(screen,'blue',p)
    
    # tail_rect = snake[-1]
    last_head_rect = snake[0].copy()
    # # 判断是否吃到食物
    # if foodexist:
    #     if food.rect.colliderect(snake[0]):
    #         snake.append(tail_rect)
    #         foodexist = False

    
    if direct == 'up':
        head.move(Up=True)
        
    elif direct == 'down':
        head.move(Down=True)
    elif direct == 'left':
        head.move(Left=True)
    elif direct == 'right':
        head.move(Right=True)
    
    if foodexist:
        if food.rect.colliderect(snake[0]):
            snakemove(snake,last_head_rect,eaten=True)
            foodexist = False
        else:
            snakemove(snake,last_head_rect)
    
    # if head_rect != head.rect:
    #     print('oops')
    # screen.fill('blue')
    # print(keys)
    # 更新蛇身
    # if head_last_rect == food.rect:
        # snake.append(food.rect)

    if not foodexist:
        while True:
            rdx = random.randint(0,19)*part_w
            rdy = random.randint(0,14)*part_h
            food = SnakePart(rdx,rdy)
            if food.rect not in snake:
                foodexist = True
                # print(rdx,rdy)
                pygame.draw.rect(screen,'green',food.rect)
                break

    for part in snake:
        pygame.draw.rect(screen,'red',part)
    
    pygame.display.update()
    # pygame.time.delay(5000)
    # 结束条件 
    # print(snake[0].collidelist(snake[2:]))
    if snake[0].collidelist(snake[1:])!=-1:
        print("游戏结束，得分为{0}".format(len(snake)-1))  
        gg_w, gg_h = gg.get_size()  
        ggx = (screen_w - gg_w) //2
        ggy = (screen_h - gg_h) //2 
        screen.fill('black')        
        screen.blit(gg,(ggx,ggy)) 
        scorefont = pygame.font.SysFont('arial', 20)
        scoretext = scorefont.render('Score: {0}'.format(len(snake)-1),True,'green')        
        screen.blit(scoretext,(350,500))
        pygame.display.flip()
        # pygame.time.delay(5000)       
        break
    c.tick(fps)
    # pygame.quit()
while True:
    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            sys.exit()

