import pygame
import os.path
import math
import random


pygame.init()
screen_width = 800
screen_height = 600
c = pygame.time.Clock()
background = "white"
gravity_acceleration = 10
maindir = os.path.split(os.path.abspath(__file__))[0]
zh_font_path = os.path.join(maindir, "zh_font", "heiti_GB18030.ttf")
btn_size = (300, 100)
gametime = 1000 * 60


def load_image(img_name, scale=(75, 75)):
    img_path = os.path.join(maindir, "pics", img_name)
    imgsurf = pygame.image.load(img_path)  # .convert()会破坏背景透明。
    return pygame.transform.scale(imgsurf, scale)


screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Bean Shoot")
img_zombie = load_image("zoombie.png", (87, 143))
img_zombie_laydown = pygame.transform.rotate(img_zombie, -90)
img_grass = load_image("grass.png")
img_grass = pygame.transform.scale(img_grass, (screen_width, 50))
img_bullet = load_image("bullet.png")
img_bullet = pygame.transform.scale(img_bullet, (20, 20))
beans_ind_list = [0, 15, 30, 45, 60, 75, 85]
dic_img_bean = dict()
for bean_angle in beans_ind_list:
    dic_img_bean[bean_angle] = load_image(f"beans/bean{bean_angle}.png", (80, 108))


class wall(pygame.sprite.Sprite):
    def __init__(self, bean_rect, rect_zombie, width=50) -> None:
        self.width = width
        self.height = random.randrange(50, screen_height - 100)
        self.x = random.randrange(bean_rect.right + 20, rect_zombie.x - 20)
        self.rect = pygame.Rect(
            self.x, screen_height - self.height, self.width, self.height
        )

    def draw(self):
        screen.fill("black", self.rect)


class gameObject(pygame.sprite.Sprite):
    def __init__(
        self, image_surf, image_rect, boundary_left, boundary_right, *groups
    ) -> None:
        super().__init__(*groups)
        self.image_surf = image_surf
        self.image_rect = image_rect
        self.bdry_left = boundary_left
        self.bdry_right = boundary_right

    def draw(
        self,
    ):
        screen.blit(self.image_surf, self.image_rect)

    def move(self, direct):
        arrive_boundary = False
        if direct == "left":
            self.image_rect.x -= 10
            if self.image_rect.x < self.bdry_left:
                self.image_rect.x = self.bdry_left
                arrive_boundary = True

        elif direct == "right":
            self.image_rect.x += 10
            if self.image_rect.right > self.bdry_right:
                self.image_rect.right = self.bdry_right
                arrive_boundary = True
        return arrive_boundary


class Bullet(gameObject):
    def __init__(
        self, image_surf, image_rect, angle, vo, boundary_left, boundary_right, *groups
    ) -> None:
        super().__init__(image_surf, image_rect, boundary_left, boundary_right, *groups)
        self.t = 0

        self.angle = angle
        start_offset = (0, -10)
        offset_lenght = 20
        self.start_y = (
            self.image_rect.centery
            + start_offset[1]
            - offset_lenght * math.sin(self.angle)
        )
        self.start_x = (
            self.image_rect.centerx
            + start_offset[0]
            + offset_lenght * math.cos(self.angle)
        )
        self.vo = vo

    def updatepos(self, speedadd=10):
        self.draw()
        vox = self.vo * math.cos(self.angle)
        voy = self.vo * math.sin(self.angle)
        if vox != 0:
            self.t += speedadd / vox
            self.image_rect.x = self.start_x + vox * self.t
            self.image_rect.y = int(
                self.start_y
                - (voy * self.t - gravity_acceleration * 1 / 2 * (self.t**2))
            )

    def check_boundary(
        self,
    ):
        if self.image_rect.x > self.bdry_right:
            return False
        if (
            self.image_rect.y > screen_height
        ):  # -img_grass.get_height():#砸到草地上爆炸。考虑草地的高度遮挡，所以减一个值。
            self._explode()
            return False
        return True

    def chk_wall(self, rect_block_wall):
        if self.image_rect.colliderect(rect_block_wall):
            self._explode()
            return True
        return False

    def chk_zombie(self, rect_zombie: pygame.Rect):
        rect_z = rect_zombie.inflate(-20, -10)
        if self.image_rect.colliderect(rect_z):
            self._explode()
            return True
        return False

    def _explode(
        self,
    ):
        ep_range = 50
        ep_color_list = ["blue", "green", "red"]
        ep_count = random.randrange(3, 10)
        for i in range(ep_count):
            ep_x = self.image_rect.x + random.randrange(-ep_range, ep_range)
            ep_y = self.image_rect.y + random.randrange(-ep_range, ep_range)
            if self.image_rect.y > screen_height:
                ep_y = screen_height - 10 + random.randrange(-ep_range, ep_range)
            ep_color = random.choice(ep_color_list)
            ep_radius = random.randrange(3, 6)
            pygame.draw.circle(screen, ep_color, (ep_x, ep_y), ep_radius)


class Text:
    def __init__(self, text, color="black", fontsize=50, font=None) -> None:
        self.text = str(text)
        self.fontsize = fontsize
        self.color = color
        self.font = pygame.font.Font(font, fontsize)
        self.updatesurf()

    def updatesurf(
        self,
    ):
        self.fontsurf = self.font.render(self.text, 1, self.color)

    def write(self, ds: pygame.Surface, pos):
        self.pos = pos
        return ds.blit(self.fontsurf, self.pos)

    def updatetext(self, text):
        self.text = text
        self.updatesurf()


class Zombie(gameObject):
    def __init__(
        self, image_surf, image_rect, boundary_left, boundary_right, *groups
    ) -> None:
        super().__init__(image_surf, image_rect, boundary_left, boundary_right, *groups)
        self.laydown = False

    def updateimage(
        self,
    ):
        if self.laydown:
            self._hitdown()
        else:
            self._standup()
        self.draw()

    def move(self, direct):
        if not self.laydown:
            return super().move(direct)

    def _hitdown(
        self,
    ):
        self.image_surf = img_zombie_laydown
        self.image_rect = self.image_surf.get_rect(center=self.image_rect.center)

    def _standup(
        self,
    ):
        self.image_surf = img_zombie
        self.image_rect = self.image_surf.get_rect(center=self.image_rect.center)


class Bean(gameObject):
    def __init__(
        self, image_surf, image_rect, boundary_left, boundary_right, *groups
    ) -> None:
        super().__init__(image_surf, image_rect, boundary_left, boundary_right, *groups)

    def updateimage(self, image):
        self.image_surf = image


class Button(Text):
    def __init__(
        self,
        text,
        btn_size: tuple,
        btn_pos,
        color="black",
        fontsize=50,
        font=os.path.join(maindir, "zh_font", "heiti_GB18030.ttf"),
    ) -> None:
        super().__init__(text, color, fontsize, font)
        self.btn_size = btn_size
        self.btn_pos = btn_pos
        self.active = False
        self.btn_surf = pygame.Surface(
            self.btn_size,
        )
        btn_rect = self.updatecolor()
        self.text_pos = self.fontsurf.get_rect(center=btn_rect.center).topleft
        self.write(self.btn_surf, self.text_pos)
        self.ds_btn_rect = pygame.Rect(self.btn_pos, self.btn_size)

    def updatecolor(self):
        btn_color_list = [(192, 192, 192), (178, 255, 102)]
        self.btn_color = btn_color_list[1] if self.active else btn_color_list[0]
        return self.btn_surf.fill(
            self.btn_color,
        )

    def updateimage(self, ds: pygame.Surface):
        self.updatecolor()
        self.write(self.btn_surf, self.text_pos)
        ds.blit(self.btn_surf, self.ds_btn_rect)

    def chk_collide_mospos(self, mouse_pos):
        return self.ds_btn_rect.collidepoint(mouse_pos)


def update_button(buttons):
    mouse_pos = pygame.mouse.get_pos()
    for b in buttons:
        if b.ds_btn_rect.collidepoint(mouse_pos):
            b.active = True
        else:
            b.active = False
        b.updateimage(screen)


def make_all_page_buttons(btn_texts, ds_surf: pygame.Surface):
    tmp_width = screen_width / len(btn_texts)
    boundary_space_width = int((tmp_width - btn_size[0]) / 2)
    buttons = []
    for i, s in enumerate(btn_texts):
        btn_left = i * int(tmp_width) + boundary_space_width
        btn = Button(s, btn_size, (btn_left, screen_height - btn_size[1] - 50))
        buttons.append(btn)
        btn.updateimage(ds_surf)
    return buttons


def click_btns_func(mouse_pos, buttons, fuc_list):
    for b, f in zip(buttons, fuc_list):
        if b.chk_collide_mospos(mouse_pos):
            f()


def myquit():
    pygame.quit()
    quit()


def show_text_onsurf(
    text_list, ds_surf: pygame.Surface, fontsize=30, first_line_y=10, line_space=50
):
    for i, s in enumerate(text_list):
        word = Text(s, fontsize=fontsize, font=zh_font_path)
        word.write(
            ds_surf,
            (
                word.fontsurf.get_rect(centerx=ds_surf.get_rect().centerx).x,
                first_line_y + i * (word.fontsize + line_space),
            ),
        )


def show_control_page():
    control_page = pygame.Surface((screen_width, screen_height))
    control_texts = [
        'press key "SPACE": fire beans',
        'press key "LEFT":moveleft',
        'press key "RIGHT": move right',
        'press key "UP" : add the fire angle',
        'press key "DOWN": reduce the fire angle',
        'press key "A":power down',
        'press key "D":power up',
    ]
    control_page_color = "white"
    control_page.fill(control_page_color)
    show_text_onsurf(control_texts, control_page, line_space=30)
    # for i, s in enumerate(control_texts):
    #     word = Text(s,fontsize=30,font=zh_font_path)
    #     word.write(control_page,(word.fontsurf.get_rect(centerx = control_page.get_rect().centerx).x,10+i*(word.fontsize*2)))
    btn_texts = ["返回"]
    buttons = make_all_page_buttons(btn_texts, control_page)
    screen.blit(control_page, (0, 0))
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    click_btns_func(mouse_pos, buttons, [preface])
        update_button(buttons)
        pygame.display.update()
        c.tick(30)


def preface():
    pre_surf = pygame.Surface((screen_width, screen_height))
    pre_surf.fill("white")
    intro_sentences = [
        "控制豌豆射手发射豌豆越过中间的墙打僵尸",
        "每次计时1分钟,每打倒一次僵尸得1分",
        "重复击打已经击倒的僵尸按一次计",
    ]
    show_text_onsurf(
        intro_sentences,
        pre_surf,
        first_line_y=50,
    )
    btn_texts = [
        "开始游戏",
        "控制说明",
    ]
    buttons = make_all_page_buttons(btn_texts, pre_surf)
    screen.blit(pre_surf, (0, 0))
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    m_click_pos = pygame.mouse.get_pos()
                    click_btns_func(m_click_pos, buttons, [gameloop, show_control_page])

        update_button(buttons)
        pygame.display.update()
        c.tick(30)


def show_left_time(starttime, pos_y):
    endtime = pygame.time.get_ticks()
    left_time = gametime - (endtime - starttime)
    left_time_text = Text("Lefttime:{}".format(int(left_time / 1000)))
    ds_rect = left_time_text.fontsurf.get_rect(centerx=screen_width / 2, y=pos_y)
    left_time_text.write(screen, ds_rect.topleft)
    return endtime


def show_gameover_page(score):
    over_page = pygame.Surface((screen_width, screen_height))
    over_texts = ["GameOver!!!!", "Your Score is {}".format(score)]
    over_page_color = "white"
    over_page.fill(over_page_color)
    show_text_onsurf(
        over_texts, over_page, first_line_y=100, line_space=100, fontsize=60
    )
    btn_texts = ["结束", "再试一次"]
    buttons = make_all_page_buttons(btn_texts, over_page)
    screen.blit(over_page, (0, 0))
    gameover = True
    while gameover:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    mouse_pos = pygame.mouse.get_pos()
                    click_btns_func(mouse_pos, buttons, [myquit, gameloop])                    
        update_button(buttons)
        pygame.display.update()
        c.tick(30)


def gameloop():
    fps = 10
    bean_rect = dic_img_bean[0].get_rect(x=0, y=screen_height - 120)
    rect_zombie = img_zombie.get_rect(x=screen_width - 150, y=screen_height - 150)
    rect_grass = img_grass.get_rect(bottom=screen_height)
    firepower = 100
    score = 0
    gamerun = True
    angle = 0
    block_wall = wall(bean_rect, rect_zombie)
    direct = None
    bean_0 = Bean(dic_img_bean[angle], bean_rect, 0, block_wall.x)
    zombie_role = Zombie(img_zombie, rect_zombie, block_wall.rect.right, screen_width)
    zombie_direct = "left"
    zombie_opposite_direct = "right"
    firepowershow = Text(f"firepower:{firepower}", "black")
    score_show = Text(f"score:{score}", "black")
    angle_show = Text(f"angle:{angle}", "black")
    bullets = []
    starttime = pygame.time.get_ticks()
    while gamerun:
        old_angle = angle
        rect_bullet = img_bullet.get_rect(center=bean_0.image_rect.center)
        rect_bullet.move_ip(0, -20)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    angle += 15
                    if angle >= 90:
                        angle = 85
                elif event.key == pygame.K_DOWN:
                    angle -= 15
                    if angle < 0:
                        angle = 0
                    if angle == 70:
                        angle = 75
                elif event.key == pygame.K_LEFT:
                    direct = "left"
                elif event.key == pygame.K_RIGHT:
                    direct = "right"
                elif event.key == pygame.K_a:
                    firepower -= 10
                    if firepower < 0:
                        firepower = 0
                    firepowershow.updatetext("firepower:%d" % firepower)
                elif event.key == pygame.K_d:
                    firepower += 10
                    if firepower > 200:
                        firepower = 200
                    firepowershow.updatetext("firepower:%d" % firepower)
            if event.type == pygame.KEYUP:
                if direct is not None:
                    bean_0.move(direct)
                    direct = None
                if event.key == pygame.K_SPACE:
                    bullets.append(
                        Bullet(
                            img_bullet,
                            rect_bullet.copy(),
                            angle / 180 * math.pi,
                            firepower,
                            0,
                            screen_width,
                        )
                    )
        if angle != old_angle:
            bean_0.updateimage(dic_img_bean[angle])
            angle_show.text = f"angle:{angle}"
            angle_show.updatesurf()

        if zombie_role.move(zombie_direct):
            tmp = zombie_direct
            zombie_direct = zombie_opposite_direct
            zombie_opposite_direct = tmp
        screen.fill(background)
        screen.blit(img_grass, rect_grass)
        for b in bullets:
            if b.check_boundary():
                b.updatepos()
                if b.chk_wall(block_wall.rect):
                    # print("hit the wall")
                    bullets.remove(b)
                elif b.chk_zombie(zombie_role.image_rect):
                    # print("hit the zombie")
                    if not zombie_role.laydown:
                        score += 1
                        score_show.text = f"score:{score}"
                        score_show.updatesurf()
                        zombie_role.laydown = True
                        tag_zombie_laydown = pygame.time.get_ticks()
                    bullets.remove(b)
            else:
                bullets.remove(b)
        block_wall.draw()
        bean_0.draw()
        if zombie_role.laydown:
            if (pygame.time.get_ticks() - tag_zombie_laydown) > 2000:
                zombie_role.laydown = False
        zombie_role.updateimage()
        firepower_rect = firepowershow.write(screen, (10, 10))
        score_show.write(
            screen, (screen_width - score_show.fontsurf.get_width(), firepower_rect.y)
        )
        angle_show.write(
            screen,
            (firepowershow.pos[0], firepower_rect.bottom + 10),
        )

        endtime = show_left_time(starttime, firepower_rect.y)

        # print(endtime - starttime)
        if endtime - starttime >= gametime:
            # print('timeout')
            gamerun = False
        pygame.display.update()
        c.tick(fps)
    show_gameover_page(score)
    pygame.quit()
    quit()


if __name__ == "__main__":
    preface()
