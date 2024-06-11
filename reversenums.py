#! /usr/bin/env python3
# This is a game about numbers.
# Read a list of numbers from the game to hope the player to reverse them .
# Critically this is not a game.


from typing import Any


try:
    import pygame
    import random
    from const import *
except ImportError:
    print("Import failed.")


def loadsound(name):
    filepath = os.path.join(maindir, "sound", "{}.wav".format(name))
    sound = pygame.mixer.Sound(filepath)
    return sound


class numMake(pygame.sprite.Sprite):
    def __init__(self, center_pos, fontcolor="white", *groups) -> None:
        super().__init__(*groups)
        self.ds_screen = pygame.display.get_surface()
        self.num = random.randrange(0, 9)
        self.font = pygame.font.Font(None, 75)
        self.centerpos = center_pos
        self.font_color = fontcolor

        self.update()
        self.font_rect = self.font_surf.get_rect(center=center_pos)

    def update(self):
        self.num = random.randrange(0, 9)
        self.font_surf = self.font.render(
            str(self.num),
            1,
            self.font_color,
        )

    def Readnum(self):
        loadsound(self.num).play()

    def draw(
        self,
    ):
        self.ds_screen.blit(self.font_surf, self.font_rect)

    def custom_draw(self, ds_center_pos):
        ds_rect = self.font_rect.copy()
        ds_rect.center = ds_center_pos
        self.ds_screen.blit(self.font_surf, ds_rect)


def get_all_nums_center_pos(
    numcount,
):

    screen_rect = pygame.display.get_surface().get_rect()
    sc_width = screen_rect.w
    sc_height = screen_rect.h
    space = sc_width / numcount

    centerpos_list = []
    for i in range(numcount):
        rect_i = pygame.rect.Rect(i * space, 0, space, sc_height)
        cn_pos = rect_i.center
        centerpos_list.append(cn_pos)
    return centerpos_list


def show_result_to_screen(nums, rect_center_pos):
    res_list = reversed(nums)
    for r, p in zip(res_list, rect_center_pos):
        r.custom_draw(p)


class Button(pygame.sprite.Sprite):
    def __init__(self, text, size, fontcolor=(0, 0, 255), *groups) -> None:
        super().__init__(*groups)
        self.text = text
        self.buttonsurf = pygame.Surface(
            size,
        )
        self.buttonrect = self.buttonsurf.get_rect()
        font = pygame.font.Font(zh_font_path, 50)
        self.font_surf = font.render(text, 1, fontcolor)
        self.font_rect = self.font_surf.get_rect(center=self.buttonrect.center)

    def update(self, cn_pos, screen, button_color):
        self.buttonrect.center = cn_pos
        self.draw_button(screen, button_color)

    def draw_button(self, screen: pygame.Surface, button_color):
        self.buttonsurf.fill(button_color)
        self.buttonsurf.blit(self.font_surf, self.font_rect)
        screen.blit(self.buttonsurf, self.buttonrect)

    def check_click(self, mousepos):
        c1 = self.buttonrect.collidepoint(mousepos)
        c2 = pygame.mouse.get_pressed()[0]
        return c1 and c2


def main():
    pygame.init()
    screensize = (400, 300)
    button_size = (100, 75)
    button_color = (0, 200, 100)
    screen = pygame.display.set_mode(screensize)
    pygame.display.set_caption("reverse nums")
    c = pygame.time.Clock()
    numcount = 3
    bg_color = (200, 200, 200)
    font_color = (0, 0, 255)
    screen.fill(bg_color)

    centerpos_list = get_all_nums_center_pos(numcount)

    i = j = 0
    sc_midbottom = screen.get_rect().midbottom
    button = Button(
        "更新",
        button_size,
    )
    buttoncenter = (sc_midbottom[0], sc_midbottom[1] - button_size[1] / 2 - 10)
    res_btn = Button("答案", button_size)
    res_btn_center = (screensize[0] - button_size[0] / 2, buttoncenter[1])
    # print(buttoncenter)
    button.update(buttoncenter, screen, button_color)
    res_btn.update(res_btn_center, screen, button_color)
    pygame.display.update()
    nums = []
    show_result = False
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                m_pos = pygame.mouse.get_pos()
                if button.check_click(m_pos):
                    i = 0
                    for n in nums:
                        screen.fill(bg_color, n.font_rect)
                elif res_btn.check_click(m_pos):
                    show_result = True
                    reslist = reversed(nums)
                    # reslist2 = reversed(nums)
                    show_result_to_screen(nums, centerpos_list)
        if i < numcount:  # len(centerpos_list):
            if len(nums) < numcount:
                num = numMake(centerpos_list[i], fontcolor=font_color)
                nums.append(num)
            nums[i].update()
            nums[i].Readnum()
            i += 1
            pygame.time.wait(1000)  # wait for speak.
        if show_result:
            try:
                # next(reslist2).custom_draw(next(iter(centerpos_list)))
                next(reslist).Readnum()
                pygame.time.wait(1000)
            except StopIteration:
                show_result = False
        pygame.display.update()
        c.tick(20)


if __name__ == "__main__":
    main()
