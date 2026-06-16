import os
import random
import sys
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),  #上矢印キー
    pg.K_DOWN:(0,+5),#下矢印キー
    pg.K_LEFT:(-5,0),#左矢印キー
    pg.K_RIGHT:(+5,0)#右矢印キー

}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg") 
    #工科トンの初期化   
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    #爆弾の初期化
    bb_img = pg.Surface(( 20, 20))
    pg.draw.circle(bb_img, (255 ,0 ,0 ),( 10, 10), 10)
    bb_img.set_colorkey((0,0,0))
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0,WIDTH)#初期座標
    bb_rct.centery = random.randint(0,HEIGHT)
    vx, vy = +5, -5

    clock = pg.time.Clock()
    tmr = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
        screen.blit(bg_img, [0, 0]) 


        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        for key, mv in DELTA.items():
            if key_lst[key]:
                 sum_mv[0] += mv[0] #横方向の移動量
                 sum_mv[1] += mv[1] #縦方向の移動量

        kk_rct.move_ip(sum_mv)
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
