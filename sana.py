#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import csv_reader
import sys


def nearest_x(series, value):
    """valueに最も近い値下がったところのindexを返す"""
    down = series.max() - value
    absolute_sub = pd.Series(abs(series - down)).sort_values()
    return absolute_sub


class Syncf:
    """
    usage:
        # On bash shell
        $ python sana.py hoge.csv

        # In python
        sf = sana.Syncf(df.iloc[:,0])  # Args must be Series type
        sf.describe()  # Show table
        sf.plot()  # Show graph

    args:
        data: Network Analyzerから読んだF特(pandas.Series型)

    return
        f1: 3dB落ちの周波数(低域)
        f2: 3dB落ちの周波数(高域)
        f3: 6dB落ちの周波数(低域)
        f4: 6dB落ちの周波数(高域)
        fa: 3dB落ちの帯域幅(f2-f1)
        fb: 6dB落ちの帯域幅(f4-f3)
        f0: 帯域幅から算出する同調周波数(f1~f4の平均値)
        fmax: 最大値から算出する同調周波数(最大値)
    """

    def __init__(self, data, f1=None, f2=None, f3=None, f4=None):
        self.data = data

        lower = data.loc[data.index <= data.idxmax()]
        upper = data.loc[data.index > data.idxmax()]

        self._lower3dBdown = nearest_x(lower, 3)
        self._upper3dBdown = nearest_x(upper, 3)

        self.f1 = f1 if f1 else self._lower3dBdown.index[0]
        self.f2 = f2 if f2 else self._upper3dBdown.index[0]

        self.f0 = np.mean([self.f1, self.f2])
        self.fmax = self.data.idxmax()

        self.bw = self.f2 - self.f1
        self.q = self.f0 / self.bw

    def score(self):
        """ずれ幅
        1が一番よい値。0が一番悪い値。
        0.95未満だと怪しいので
        sf.plot()でF得を表示して確認するべし
        """
        dicc = {
            'f1': 1 - self._lower3dBdown.values[0],
            'f2': 1 - self._upper3dBdown.values[0],
        }
        print(self.score.__doc__)
        return pd.Series(dicc)

    def describe(self):
        """ 周波数情報を返す
        f1~f4: Frequency
        fa,fb: Bandwidth
        f0, fmax: Sync frequency
        """
        dicc = {
            'f1': self.f1,
            'f2': self.f2,
            'f0': self.f0,
            'fmax': self.fmax,
            'BW': self.bw,
            'Q': self.q,
        }
        return pd.Series(dicc, index=dicc.keys())

    def plot(self, ylabel='試験入力利得[dB]', **kwargs):
        """Return plot and point of f1~f4"""
        ax = self.data.plot(**kwargs)
        ax.set_ylabel(ylabel)
        ax.plot([self.f1, self.f2, self.f3, self.f4, self.fmax],
                [self.data[self.f1], self.data[self.f2],
                self.data[self.f3], self.data[self.f4],
                self.data[self.fmax]], 'd')
        # ax.plot(self.f0, self.data[self.f0], 'd')
        # 帯域から導いたf0はインデックスの中にない場合がある
        return ax


def main(argvs):
    if ('-h' in argvs or '--help' in argvs):
        print(Syncf.__doc__)
    else:
        df = csv_reader.reader_N5071(argvs[1])
        sf = Syncf(df.iloc[:, 0])
        print(sf.score())
        print()
        print(sf.describe())


if __name__ == '__main__':
    main(sys.argv)
