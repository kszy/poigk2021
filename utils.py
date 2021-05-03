def fix_alpha(slownik):
    slownik['dol'][1][:, -2:, 3] = 0
    slownik['dol'][1][:, :2, 3] = 0
    slownik['lewo'][1][:, :2, 3] = 0
    slownik['lewo'][1][:2, :, 3] = 0
    slownik['prawo'][1][:, -2:, 3] = 0
    slownik['prawo'][1][:2, :, 3] = 0
