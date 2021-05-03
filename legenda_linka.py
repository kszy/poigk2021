import cv2
import imageio
import numpy as np
from utils import fix_alpha
from scipy.ndimage import rotate

# tlo = cv2.imread('background.png')
# print(np.shape(tlo))
# cv2.imshow('tlo', tlo)
# cv2.waitKey(0)
# link = imageio.mimread('link_front.gif')
# print(len(link))
# print(np.shape(link[0]))
# link1 = cv2.cvtColor(link[0][:, :, :3], cv2.COLOR_BGR2RGB)
# cv2.imshow('link', link1)
# cv2.waitKey(0)

# nowe_tlo = np.load('new_background.npy')
# cv2.imshow('nowe tlo', nowe_tlo[:, :, 3])
# cv2.waitKey()

class Wyswietlacz:
    def __init__(self):
        self.przygotuj_tlo()
        self.przygotuj_sprity()
        self.shift = [125, 170]
        self.shift_oponenta = [288, 170]
        self.sprite_size = self.slownik_sprity['dol'][0].shape
        self.krok = 2
        self.pokonane = 0
        self.zmiana_animacja = 3
        self.poprzednia_animacja = 'dol'
    def przygotuj_tlo(self):
        self.tlo = np.load('new_background.npy')
    def przygotuj_sprity(self):
        etykiety = ['dol', 'gora', 'lewo', 'prawo']
        sciezki = ['link_front.gif', 'link_back.gif', 'link_left.gif', 'link_left.gif']
        self.slownik_sprity = dict()
        for etykieta, sciezka in zip(etykiety, sciezki):
            gif = imageio.mimread(sciezka)
            for img in gif:
                img[:, :, :3] = cv2.cvtColor(img[:, :, :3], cv2.COLOR_BGR2RGB)
                if etykieta == 'prawo':
                    img[:, ::-1, :] = img
                self.slownik_sprity[etykieta] = gif
        fix_alpha(self.slownik_sprity)
        sprite_oponenta = np.load('oponent.npy')
        etykiety = ['o_dol', 'o_gora', 'o_lewo', 'o_prawo']
        katy = [0, 180, 270, 90]
        for etykieta, kat in zip(etykiety, katy):
            self.slownik_sprity[etykieta] = rotate(sprite_oponenta, kat)
    def no_collision(self, shift, frame=None):
        if frame is None:
            frame = self.tlo
        y1, y2 = shift[0], shift[0] + self.sprite_size[0]
        x1, x2 = shift[1], shift[1] + self.sprite_size[1]
        return np.sum(frame[y1:y2, x1:x2, 3]) == 0
    def wyswietl_oponenta(self, frame):
        if self.shift_oponenta[0] == 288 and self.shift_oponenta[1] > 51:
            self.shift_oponenta[1] -= self.krok
            animacja = 'o_lewo'
        elif self.shift_oponenta[1] == 50 and self.shift_oponenta[0] > 188:
            self.shift_oponenta[0] -= self.krok
            animacja = 'o_gora'
        elif self.shift_oponenta[0] == 188 and self.shift_oponenta[1] < 174:
            self.shift_oponenta[1] += self.krok
            animacja = 'o_prawo'
        else:
            self.shift_oponenta[0] += self.krok
            animacja = 'o_dol'
        y1, y2 = self.shift_oponenta[0], self.shift_oponenta[0] + np.size(self.slownik_sprity[animacja], 0)
        x1, x2 = self.shift_oponenta[1], self.shift_oponenta[1] + np.size(self.slownik_sprity[animacja], 1)
        frame[y1:y2, x1:x2, :] = self.slownik_sprity[animacja]
    def wyswietl(self, ruch=None):
        if ruch is None:
            sprite = self.slownik_sprity[self.poprzednia_animacja]
        else:
            nowy_shift = self.shift.copy()
            if ruch == 'dol':
                nowy_shift[0] += self.krok
            elif ruch == 'gora':
                nowy_shift[0] -= self.krok
            elif ruch == 'lewo':
                nowy_shift[1] -= self.krok
            else:
                nowy_shift[1] += self.krok
            self.pokonane += 1
            sprite = self.slownik_sprity[ruch]
            self.poprzednia_animacja = ruch
            if self.no_collision(nowy_shift):
                self.shift = nowy_shift
        frame = self.tlo.copy()
        self.wyswietl_oponenta(frame)
        no_death = self.no_collision(self.shift, frame)
        animacja = (self.pokonane // self.zmiana_animacja) % 2
        y1, y2 = self.shift[0], self.shift[0] + np.size(sprite[animacja], 0)
        x1, x2 = self.shift[1], self.shift[1] + np.size(sprite[animacja], 1)
        alpha_s = sprite[animacja][:, :, 3:] / 255
        alpha_b = 1 - alpha_s
        frame[y1:y2, x1:x2, :3] = alpha_s * sprite[animacja][:, :, :3] + \
                                alpha_b * frame[y1:y2, x1:x2, :3]
        if no_death:
            cv2.imshow('Legenda Linka', frame)
        else:
            game_over_frame = cv2.imread('game_over.jpeg')
            cv2.imshow('Game Over', game_over_frame)

gra = Wyswietlacz()

# ruchy = ['dol', 'lewo', 'gora', 'prawo']
# liczba_krokow = [48, 60, 48, 60]
# for _ in range(5):
#     for ruch, liczba in zip(ruchy, liczba_krokow):
#         for i in range(liczba):
#             gra.wyswietl(ruch)
#             cv2.waitKey(50)
# cv2.waitKey()


gra.wyswietl()
while True:
    k = cv2.waitKey(200)
    if k == -1:
        gra.wyswietl()
    elif k == 0:
        gra.wyswietl('gora')
    elif k == 1:
        gra.wyswietl('dol')
    elif k == 2:
        gra.wyswietl('lewo')
    elif k == 3:
        gra.wyswietl('prawo')
    elif k == 27:
        cv2.destroyAllWindows()
        break

