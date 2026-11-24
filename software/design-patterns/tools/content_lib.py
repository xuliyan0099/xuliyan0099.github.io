# -*- coding: utf-8 -*-
"""章节内容的公共零件：四个方框的标准坐标、箭头、章节字典。"""


def bx(i, t, ty, mt, note, x, y, w=190, h=76):
    return dict(id=i, x=x, y=y, w=w, h=h, t=t, ty=ty, mt=mt, note=note)


def ar(x1, y1, x2, y2, label=""):
    return dict(x1=x1, y1=y1, x2=x2, y2=y2, label=label)


def mk(**kw):
    kw.setdefault("fig_tag", "structure")
    return kw


LEFT = (24, 140, 150, 76)
MID = (250, 140, 190, 84)
TOP = (520, 56, 190, 74)
BOT = (520, 212, 190, 74)
