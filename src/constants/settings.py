import darkdetect


if darkdetect.isDark():
    THEME = 'darkly'
else:
    THEME = 'lumen'

WIDTH = 1200
HEIGHT = int(WIDTH * 9 / 15)
ALPHA = 0.9
ENCOD = 'gbk'
