import math
import os
import random
import sys
import time

import pygame as pg


WIDTH, HEIGHT = 1100, 650

# 押下キーと移動量の対応
DELTA = {
    pg.K_UP:    (0, -5),   # 上矢印キー
    pg.K_DOWN:  (0, +5),   # 下矢印キー
    pg.K_LEFT:  (-5, 0),   # 左矢印キー
    pg.K_RIGHT: (+5, 0),   # 右矢印キー
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    オブジェクトRectが画面内かどうかを判定する関数

    引数:
        rct: こうかとんRectか爆弾Rect
    戻り値:
        (横方向判定結果, 縦方向判定結果)
        画面内ならTrue, 画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    ゲームオーバー画面を表示して数秒待つ関数

    引数:
        screen: スクリーンSurface
    戻り値:
        なし
    """
    blackout = pg.Surface((WIDTH, HEIGHT))
    blackout.fill((0, 0, 0))
    blackout.set_alpha(200)

    fonto = pg.font.Font(None, 80)
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))

    cry_img = pg.transform.rotozoom(pg.image.load("fig/8.png"), 0, 1.2)
    cry_left_rct = cry_img.get_rect(center=(WIDTH // 2 - 200, HEIGHT // 2 + 50))
    cry_right_rct = cry_img.get_rect(center=(WIDTH // 2 + 200, HEIGHT // 2 + 50))

    blackout.blit(txt, txt_rct)
    blackout.blit(cry_img, cry_left_rct)
    blackout.blit(cry_img, cry_right_rct)
    screen.blit(blackout, (0, 0))
    pg.display.update()
    time.sleep(5)


def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    爆弾の大きさ10段階のSurfaceリストと
    加速度リスト(1〜10)を返す関数

    戻り値:
        (爆弾Surfaceリスト, 加速度リスト)
    """
    bb_imgs: list[pg.Surface] = []
    bb_accs: list[int] = [a for a in range(1, 11)]

    for r in range(1, 11):
        bb_img = pg.Surface((20 * r, 20 * r))
        bb_img.set_colorkey((0, 0, 0))
        pg.draw.circle(bb_img, (255, 0, 0), (10 * r, 10 * r), 10 * r)
        bb_imgs.append(bb_img)

    return bb_imgs, bb_accs


def get_kk_imgs() -> dict[tuple[int, int], pg.Surface]:
    """
    移動量タプルに対応するこうかとん画像Surfaceの辞書を返す関数

    戻り値:
        キー: (dx, dy)
        値: 向きに応じて回転・反転したこうかとんSurface
    """
    base_img = pg.image.load("fig/3.png")
    base_flipped_img = pg.transform.flip(base_img, True, False)

    kk_imgs: dict[tuple[int, int], pg.Surface] = {
        (0, 0):   pg.transform.rotozoom(base_img,          0,   0.9),  # 停止
        (+5, 0):  pg.transform.rotozoom(base_flipped_img,  0,   0.9),  # 右
        (+5, -5): pg.transform.rotozoom(base_flipped_img,  45,  0.9),  # 右上
        (0, -5):  pg.transform.rotozoom(base_img,         -90,  0.9),  # 上
        (-5, -5): pg.transform.rotozoom(base_img,         -45,  0.9),  # 左上
        (-5, 0):  pg.transform.rotozoom(base_img,          0,   0.9),  # 左
        (-5, +5): pg.transform.rotozoom(base_img,          45,  0.9),  # 左下
        (0, +5):  pg.transform.rotozoom(base_img,          90,  0.9),  # 下
        (+5, +5): pg.transform.rotozoom(base_flipped_img, -45,  0.9),  # 右下
    }

    return kk_imgs


def calc_orientation(org: pg.Rect,
                     dst: pg.Rect,
                     current_xy: tuple[float, float]) -> tuple[float, float]:
    """
    追従型爆弾の移動方向ベクトル(vx, vy)を計算する関数

    引数:
        org: 爆弾のRect
        dst: こうかとんのRect
        current_xy: 前フレームの(vx, vy)

    戻り値:
        新しい(vx, vy)タプル
        ・距離が300以上: 差ベクトルをノルム√50に正規化した方向
        ・距離が300未満: current_xy(慣性)
    """
    dx = dst.centerx - org.centerx
    dy = dst.centery - org.centery
    dist = math.sqrt(dx * dx + dy * dy)

    # 慣性: 近づきすぎたら急旋回せず、前の方向を維持
    if dist < 300:
        return current_xy

    if dist != 0:
        speed_norm = math.sqrt(50)  # 課題指定: ノルム√50
        scale = speed_norm / dist
        vx = dx * scale
        vy = dy * scale
    else:
        vx, vy = 0.0, 0.0

    return vx, vy


def main() -> None:
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")

    # こうかとんの初期化
    kk_imgs = get_kk_imgs()
    kk_img = kk_imgs[(0, 0)]
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200

    # 爆弾の初期化
    bb_imgs, bb_accs = init_bb_imgs()
    bb_img = bb_imgs[0]
    bb_rct = bb_img.get_rect()
    bb_rct.centerx = random.randint(0, WIDTH)
    bb_rct.centery = random.randint(0, HEIGHT)
    vx, vy = +5.0, -5.0  # 初期方向ベクトル

    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                return

        # 衝突判定
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return

        screen.blit(bg_img, (0, 0))

        # こうかとんの移動
        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for key, mv in DELTA.items():
            if key_lst[key]:
                sum_mv[0] += mv[0]
                sum_mv[1] += mv[1]

        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        # こうかとん画像の向き切り替え
        kk_img = kk_imgs.get(tuple(sum_mv), kk_imgs[(0, 0)])
        screen.blit(kk_img, kk_rct)

        # 爆弾の拡大・加速段階
        idx = min(tmr // 500, 9)
        bb_img = bb_imgs[idx]
        acc = bb_accs[idx]

        # 追従方向ベクトルを計算
        vx, vy = calc_orientation(bb_rct, kk_rct, (vx, vy))

        # 加速をかけて移動
        avx = vx * acc
        avy = vy * acc
        bb_rct.move_ip(avx, avy)

        # 画面外に出ないようにする（反射ではなく「戻す」だけ）
        if check_bound(bb_rct) != (True, True):
            bb_rct.move_ip(-avx, -avy)

        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
