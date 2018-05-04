#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os
import cufflinks


def nearest_x(series, value):
    """valueに最も近い値下がったところのindexを返す"""
    down = series.max() - value
    absolute_sub = pd.Series(abs(series - down)).sort_values()
    return absolute_sub

class Syncf:
    """
    args:
        data: Network Analyzerから読んだF特(pandas.Series型)

    return
        f1, f2: 3dB落ちたところの周波数
        f3, f4: 6dB落ちたところの周波数
        fa: 3dB落ちの帯域幅
        fb: 6dB落ちの帯域幅
        f0: 帯域幅から算出する同調周波数(f1~f4の平均値)
        fmax: 最大値から算出する同調周波数
    """

    def __init__(self, data, f1=None, f2=None, f3=None, f4=None):
        self.data = data

        self.down3dB = nearest_x(self.data ,3)
        self.down6dB = nearest_x(self.data ,6)

        self.f1= f1 if f1 else self.down3dB.index[0]
        self.f2= f2 if f2 else self.down3dB.index[1]
        self.f3= f3 if f3 else self.down6dB.index[0]
        self.f4= f4 if f4 else self.down6dB.index[1]

        self.fa = abs(self.f1 - self.f2)
        self.fb = abs(self.f3 - self.f4)
        self.f0 = np.mean([self.f1, self.f2, self.f3, self.f4])
        self.fmax = self.data.idxmax()

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

    def plot(self, ylabel='試験入力利得[dB]', xlim=None, ylim=None, xticks=None, yticks=None):
        ax = self.data.plot(xlim=xlim, ylim=ylim, xticks=xticks, yticks=yticks)
        ax.set_ylabel(ylabel)
        ax.plot([self.f1, self.f2, self.f3, self.f4, self.fmax],
            [self.data[self.f1], self.data[self.f2],
            self.data[self.f3], self.data[self.f4], self.data[self.fmax]], 'd')
        # ax.plot(self.f0, self.data[self.f0], 'd')  # 帯域から導いたf0はインデックスの中にない場合がある
        return ax

