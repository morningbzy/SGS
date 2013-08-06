# -*- coding: UTF-8 -*-

import logging
import random

from sgs.misc import smart_lower
from sgs.figures.figures import FigureBase


class SgsFigure(object):
    def __init__(self):
        self.figures = {}
        self.used = []
        for _class in FigureBase.__subclasses__():
            classname = _class.__name__
            objname = smart_lower(classname)
            obj = _class()
            self.figures[obj.pk] = obj
            setattr(self, objname, obj)

    def take_random_figure(self, count=1, from_rest=True):
        ids = set(self.figures.keys())
        used_ids = set(self.used)
        candidates = ids - used_ids if from_rest else ids
        figures = [self.figures[k] for k in random.sample(candidates, count)]
        self.add_used(figures)
        return figures

    def take_zhugong_figures(self):
        zhugongs = [self.cao_cao]
        self.add_used(zhugongs)
        zhugongs += self.take_random_figure()
        return zhugongs

    def add_used(self, figures):
        for figure in figures:
            self.used.append(figure.pk if isinstance(figure, FigureBase)
                             else figure)

    def remove_used(self, figures):
        for figure in figures:
            self.used.remove(figure.pk if isinstance(figure, FigureBase)
                             else figure)


global_figures = SgsFigure()
