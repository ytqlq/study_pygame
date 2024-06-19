from typing import Any


try:
    import pygame
    from pygametemplate.tools import *
    import os.path
    import random
except ImportError:
    print("import failed.")

screen_size = (800, 600)  # todo
caption = "GameName"  # todo
bg_color = (225, 225, 225)  # todo


class picBlock(pygame.sprite.Sprite):
    def __init__(
        self,
        pic_no: tuple,
        image,
        table_rect: pygame.Rect,
        /,
        block_size=(100, 100),
        colcount=4,
        rowcount=3,
        line_w_boundary=2,
        *groups,
    ) -> None:
        super().__init__(*groups)
        self.pic_no = pic_no
        self.image = image
        self.surf = pygame.Surface(block_size)
        x_add = 0
        y_add = 0
        if pic_no[0] >= rowcount - 1:
            y_add = line_w_boundary
        if pic_no[1] >= colcount - 1:
            x_add = line_w_boundary
        self.size = (block_size[0] + x_add, block_size[1] + y_add)
        self.right_pos = (
            table_rect.topleft[0] + pic_no[1] * block_size[0],
            table_rect.topleft[1] + pic_no[0] * block_size[1],
        )
        self.img_area_rect = pygame.Rect(
            (0 + pic_no[1] * block_size[0], 0 + pic_no[0] * block_size[1]), self.size
        )
        pos_x = random.randrange(0, screen_size[0] - self.size[0])
        pos_y = random.randrange(
            table_rect.bottomright[1], screen_size[1] - self.size[1]
        )
        self.pos = (pos_x, pos_y)
        self.rect_on_screen = pygame.Rect(self.pos, self.size)
        self.clicked = False
        self.rect_right_on_screen = pygame.Rect(self.right_pos, self.size)

    def update(self, pos) -> None:
        self.pos = pos        
        self.rect_on_screen.topleft = self.pos

    def draw(self, ds_surface: pygame.Surface):
        # self.image = image
        self.surf.blit(self.image, (0, 0), self.img_area_rect)
        return ds_surface.blit(self.surf, self.pos)

    def chk_right(self):
        if self.pos == self.right_pos:
            return True
        return False

    def move(self, offset, new_mouse_pos):  # offset define toplet- mouseposition
        if self.clicked:            
            pos = tuple((of + mp) for of, mp in zip(offset, new_mouse_pos))
            self.update(pos)

    

def chk_click_pos(mouse_pos, sprite_group):
    for obj in sprite_group:
        if obj.rect_right_on_screen.collidepoint(mouse_pos):
            return obj.rect_right_on_screen.topleft

def chk_exist_pos(group,last_sprite):
    for obj in reversed(group.sprites()):
        if obj!= last_sprite and obj.pos == last_sprite.pos:
            obj.clicked = True
            group.remove(obj)
            group.add(obj)
            return obj
    return None
    
    

def main():
    fps = 24
    c = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption(caption)
    # print(screen is pygame.display.get_surface())
    bg_surf  = pygame.Surface(screen_size)
    bg_surf.fill(bg_color)
    # table_topleft = (200, 10)
    # table_bottomright = (600, 310)
    table_size = (400, 300)
    table_rowcount = 3
    table_colcount = 4
    boundary_line_width = 2
    table_surf_size = tuple(x + boundary_line_width for x in table_size)
    # print(table_surf_size)
    table_surf = draw_table(
        table_surf_size,
        table_rowcount,
        table_colcount,
        background_color=bg_color,
        line_width_boundary=boundary_line_width,
    )
    table_rect = table_surf.get_rect(centerx=screen_size[0] // 2, y=10)
    bg_surf.blit(table_surf, table_rect)
    
    # table_topleft = table_rect.topleft
    # print(table_rect.topleft,table_rect.size)
    picpath = get_obj_path(__file__, "pics/cut01.jpg")

    img_surf = load_img(picpath).convert()
    scale_img_surf = pygame.transform.scale(img_surf, table_surf_size)
    block_size = (
        table_surf_size[0] // table_colcount,
        table_surf_size[1] // table_rowcount,
    )

    block_group = pygame.sprite.Group()
    # pic_block_list = []
    for i in range(table_rowcount):
        # pic_block_list.append([])
        for j in range(table_colcount):
            tmp_pic_block = picBlock(
                (i, j),
                scale_img_surf,
                table_rect,
                block_size=block_size,
                colcount=table_colcount,
                rowcount=table_rowcount,
                line_w_boundary=boundary_line_width,
            )
            print((i,j),tmp_pic_block.size)
            # tmp_pic_block.draw(scale_img_surf, screen)
            block_group.add(tmp_pic_block)
    pygame.display.update()
    clicked_pic = False
    gameRun = True
    while gameRun:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return
            if e.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed()[0]:
                    # print('left button')
                    for obj in reversed(block_group.sprites()):# reverserd当与两块都有交集时，先拿最后绘制上，即最上面的（与break配合）。
                        clicked_mouse_pos = pygame.mouse.get_pos()
                        if obj.rect_on_screen.collidepoint(clicked_mouse_pos):
                            if not clicked_pic:
                                if  not obj.clicked:
                                    offset = tuple(
                                        (tl - m_pos)
                                        for tl, m_pos in zip(obj.pos, clicked_mouse_pos)
                                    )
                                    obj.clicked = True
                                    clicked_pic = True
                                    target_block = obj
                                    print(target_block.pic_no)
                                    block_group.remove(obj)
                                    block_group.add(obj)# remove + add,使移动的块最后绘制，即保证在最上面。
                            elif clicked_pic:
                                target_block.clicked = False 
                                clicked_pic = False
                                if table_rect.collidepoint(clicked_mouse_pos):
                                    click_table_block_topleft = chk_click_pos(clicked_mouse_pos,block_group)
                                    target_block.update(click_table_block_topleft)
                                    target_block = chk_exist_pos( block_group,target_block)
                                    if target_block is not None:
                                        clicked_pic = True
                                    
                            break
               

        mouse_pos = pygame.mouse.get_pos()
        if clicked_pic:        
            target_block.move(offset, mouse_pos)        
        screen.blit(bg_surf,(0,0))        
        for obj in block_group: 
            obj.draw(screen)
        pygame.display.update()
        c.tick(fps)


if __name__ == "__main__":
    main()
