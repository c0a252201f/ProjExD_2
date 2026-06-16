import os
import random
import sys
import time
import pygame as pg


WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),  #上矢印キー
    pg.K_DOWN:(0,+5),#下矢印キー
    pg.K_LEFT:(-5,0),#左矢印キー
    pg.K_RIGHT:(+5,0)#右矢印キー

}
os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectか爆弾Rect
    戻り値：タプル（横方向判定結果、縦方向判定結果）
    画面内ならTrue,画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: #横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: #縦方向判定
        tate = False
    return yoko,tate

def gameover(screen: pg.Surface) -> None: #ゲームオーバー画面
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.fill((0, 0, 0)) #黒で塗る
    blackout.set_alpha(200)

    fonto = pg.font.Font(None,80)
    txt = fonto.render("Game Over",True,(255, 255, 255))
    txt_rct = txt.get_rect()
    txt_rct.center = (WIDTH//2), (HEIGHT//2 + 50 )
    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0,1.2)
    cry_rct = cry_img.get_rect()
    cry_left_rct = cry_img.get_rect(center=(WIDTH//2 - 200, HEIGHT//2 + 50))
    cry_right_rct = cry_img.get_rect(center=(WIDTH//2 + 200, HEIGHT//2 + 50))
    blackout.blit(txt, txt_rct)
    blackout.blit(cry_img, cry_left_rct)
    blackout.blit(cry_img, cry_right_rct)
    screen.blit(blackout, (0, 0))
    pg.display.update()
    time.sleep(5)
    

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
        if kk_rct.colliderect(bb_rct):
            print("ゲームオーバー")
            

        screen.blit(bg_img, [0, 0]) 
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return




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
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1]) #動きをなかったことにする
        screen.blit(kk_img, kk_rct)

        bb_rct.move_ip(vx, vy)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bb_img, bb_rct)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
