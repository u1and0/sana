#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os


def nearest_x(series, value):
    """valueに最も近い値下がったところのindexを返す"""
    down = series.max() - value
    absolute_sub = pd.Series(abs(series - down)).sort_values()
    return absolute_sub

class Syncf:
    """
    args:
        se: Network Analyzerから読んだF特(pandas.Series型)

    return
        f1, f2: 3dB落ちたところの周波数
        f3, f4: 6dB落ちたところの周波数
        fa: 3dB落ちの帯域幅
        fb: 6dB落ちの帯域幅
        f0: 帯域幅から算出する同調周波数(f1~f4の平均値)
        fmax: 最大値から算出する同調周波数
    """

    def __init__(self, se):
       self.se = se
       self.f1, self.f2 = nearest_x(se,3).head(2).index.values  # 3dB down f1 & f2
       self.f3, self.f4 = nearest_x(se,6).head(2).index.values  # 6dB down f3 & f4
       self.fa = abs(self.f1 - self.f2)
       self.fb = abs(self.f3 - self.f4)
       self.f0 = np.mean([self.f1, self.f2, self.f3, self.f4])
       self.fmax = self.se.idxmax()

    def describe(self):
        dicc = {
        'f1': self.f1,
        'f2': self.f2,
        'f3': self.f3,
        'f4': self.f4,
        'fa': self.fa,
        'fb': self.fb,
        'f0': self.f0,
        'fmax': self.fmax,
        }
        return pd.Series(dicc, index=dicc.keys())

    def plot(self):
        ax = self.se.plot()
        ax.set_ylabel('試験入力利得[dB]')
        ax.plot(self.se.idxmax(), self.se.max(), 'd')
        return ax


