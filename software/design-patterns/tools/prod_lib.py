# -*- coding: utf-8 -*-
import re

def PD(title, lead, cons, puml):
    lead = re.sub(r"<b>([^<]*)</li></b>", r"<b>\1</b>", lead)
    lead = lead.replace("</p>\n<li>", "</li>\n<li>")
    return dict(title=title, lead=lead, cons=cons, puml=puml)