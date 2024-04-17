import pygame
import sys
import random


screen_w = 600
screen_h = 800
row = 7
col = 15
fontcolor = "green"
fontsize = 35
typeface = "arial"
fontspace = 2
linecolor = "red"
flagcolor = "blue"
rate = 0.33  # 控制出现错误数字对的概率。
fps = 60  # 刷新频率
scorecolor = "white"
score_font_size = 60
commitwidth = 120
commith = 60
commit_bg_color = "white"
commit_font_color = "blue"
commit_font_size = 60
commit_w = screen_w / 2
commit_h = 90

# trsf.w =
wronganscolor = "red"
nongetanscolor = "purple"
showfontcolor = "white"


def getanothernum(num):
    falserate = int(9 * rate)
    TFtest = [True] * (9 - falserate) + [False] * (falserate)
    l = list(range(10))
    l.remove(num)
    if TFtest[random.randint(0, 8)]:
        return num
    else:
        return random.choice(l)


def getnumpair(typeface=typeface, fontsize=fontsize, fontcolor=fontcolor):
    upnum = random.randint(0, 9)
    downnum = getanothernum(upnum)
    numfont = pygame.font.SysFont(typeface, fontsize)
    upnumsurface = numfont.render(str(upnum), True, fontcolor)
    downnumsurface = numfont.render(str(downnum), True, fontcolor)
    return (upnumsurface, downnumsurface, upnum == downnum)


def showfinalscore(
    score: int, answer: int, dessurface: pygame.Surface, color=scorecolor
):
    scorefont = pygame.font.Font(None, score_font_size)
    score_sf = scorefont.render("SCORE:{0}/{1}".format(score, answer), 1, color)
    score_rect = score_sf.get_rect(centerx=dessurface.get_rect().centerx, y=20)

    dessurface.blit(score_sf, score_rect)

    return score_rect


def showans(
    list_rect: list[pygame.Rect],
    currentsurface: pygame.Surface,
    copysuface: pygame.Surface,
    color=wronganscolor,
):
    """
    圈示错误答案
    """
    for i in list_rect:
        currentsurface.blit(copysuface, i, i)  # 屏幕还原
        pygame.draw.arc(currentsurface, color, i, 0, 6.28, 2)


def analyse_answer(right_answers, answers):
    not_get = right_answers[:]
    wrong_ans = []
    for item in answers:
        if item in right_answers:
            not_get.remove(item)
        else:
            wrong_ans.append(item)
    return not_get, wrong_ans


def colorflag(dessurface: pygame.Surface, position: pygame.Rect, color=showfontcolor):

    size = position.size
    sf_flag = pygame.Surface(size)
    font = pygame.font.Font(None, 20)

    rect_list = []
    for i in range(3):
        rect_list.append(pygame.Rect(0, 0 + size[1] // 3 * i, size[0], size[1] // 3))
    color_list = [nongetanscolor, flagcolor, wronganscolor]

    str_lsit = [
        "Answers not gotten",
        "Right answers submitted",
        "Wrong answers submitted",
    ]
    for c, r, s in zip(color_list, rect_list, str_lsit):
        sf_flag.fill(c, r)
        fontsf = font.render(s, 1, color)
        fontr = fontsf.get_rect(centery=r.centery)
        sf_flag.blit(fontsf, fontr)

    dessurface.blit(sf_flag, position)


def main():
    pygame.init()
    c = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_w, screen_h), pygame.SCALED)

    block_h = 90
    topspace = (screen_h - block_h * row) // 2
    block_w = fontsize
    leftspace = (screen_w - block_w * col) // 2
    l_flag = []

    right_answer = []
    for i in range(row):

        pygame.draw.line(
            screen,
            linecolor,
            (leftspace, topspace + fontsize + fontspace // 2 + i * block_h),
            (screen_w - leftspace, topspace + fontsize + fontspace // 2 + i * block_h),
        )
        for j in range(col):
            uprect = pygame.Rect(
                (leftspace + j * block_w, topspace + i * block_h), (block_w, fontsize)
            )
            downrect = uprect.move(0, fontsize + fontspace)

            upnum, downnum, same = getnumpair()

            upnumrect = upnum.get_rect()
            upnumrect.center = uprect.center
            downnumrect = downnum.get_rect()
            downnumrect.center = downrect.center

            flag_rect = uprect.union(downrect)

            l_flag.append((flag_rect, same))
            screen.blit(upnum, upnumrect)
            screen.blit(downnum, downnumrect)

    existarcrect = []
    screencp = screen.copy()
    finalscore = 0

    commitfont = pygame.font.Font(None, commit_font_size)
    commitsf = commitfont.render("SUBMIT", 1, commit_font_color, commit_bg_color)
    commit_font_rect = commitsf.get_rect(
        centerx=screen.get_rect().centerx, y=screen_h - 80
    )
    screen.blit(commitsf, commit_font_rect)

    showscore = False

    while True:

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                sys.exit()

        mps = pygame.mouse.get_pressed()
        if mps[0]:
            x, y = pygame.mouse.get_pos()
            if commit_font_rect.collidepoint(x, y) and not showscore:# 点击提交按钮后的显示。
                no_get_ans, wronganswerrect = analyse_answer(right_answer, existarcrect)
                fs_rect = showfinalscore(
                    finalscore - len(wronganswerrect), len(right_answer), screen
                )
                showans(wronganswerrect, screen, screencp)
                showans(no_get_ans, screen, screencp, color=nongetanscolor)

                colorflag(
                    screen,
                    pygame.Rect(
                        fs_rect.right + 10,
                        0,
                        (screen_w - fs_rect.size[0]) // 2 - 10,
                        topspace,
                    ),
                )
                showscore = True

            for i, same in l_flag:

                if not same and i not in right_answer:
                    right_answer.append(i)

                if i.collidepoint(x, y):

                    if not showscore:
                        arcrect = pygame.draw.arc(screen, flagcolor, i, 0, 6.28, 2)
                        if arcrect not in existarcrect:
                            existarcrect.append(arcrect)
                            finalscore += 1

        if mps[2]:  # 点右键去掉椭圆标记。
            x, y = pygame.mouse.get_pos()
            for r in existarcrect:
                if r.collidepoint(x, y):
                    if not showscore:
                        screen.blit(screencp, r, r)
                        finalscore -= 1
                        existarcrect.remove(r)

        pygame.display.update()

        c.tick(fps)


if __name__ == "__main__":
    main()
    pygame.quit()
