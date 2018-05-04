#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import os


def nearest_x(df, value):
    """valueに最も近い値下がったところのindexを返す"""
    down = df.max() - value
    absolute_sub = pd.DataFrame(abs(df - down)).sort_values(by=df.columns[0])
    return absolute_sub

class Syncf:
    def __init__(self, df):
       self.df = df
       self.fmax = self.df.idxmax().values[0]
       self.f1, self.f2 = nearest_x(df,3).head(2).index.values  # 3dB down f1 & f2
       self.f3, self.f4 = nearest_x(df,6).head(2).index.values  # 6dB down f3 & f4
       self.fa = abs(self.f1 - self.f2)
       self.fb = abs(self.f3 - self.f4)
       self.f0 = np.mean([self.f1, self.f2, self.f3, self.f4])


    def describe(self):
        dicc = {
        'f1': self.f1,
        'f2': self.f2,
        'f3': self.f3,
        'f4': self.f4,
        'fa': self.fa,
        'fb': self.fb,
        'fmax': self.fmax,
        'f0': self.f0,
        }
        return pd.Series(dicc, index=dicc.keys())

    def plot(self):
        ax = self.df.plot()
        ax.set_ylabel('試験入力利得[dB]')
        ax.plot(self.df.idxmax(), self.df.max(), 'd')
        return ax


