# -*- coding: utf-8 -*-
"""合并第二、三、四篇的新增章内容。"""

from content_part2 import C as C2
from content_part3 import C as C3
from content_part4 import C as C4

CONTENT = {}
CONTENT.update(C2)
CONTENT.update(C3)
CONTENT.update(C4)

__all__ = ["CONTENT"]
