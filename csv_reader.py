#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CSVを読み込んでデータフレーム化
マシン名:
    ネットワークアナライザ:N5071
    スペクトラムアナライザ:N9010A
"""

from pathlib import Path
import pandas as pd


def read_network_analyzer(*files):
    """ネットワークアナライザN5071からデータインポート
    USAGE:
        read_network_analyzer(test1.CSV, test2.CSV, test3.CSV)
            or
        import glob
        testdata = glob.iglob('*.CSV')
        read_network_analyzer(*testdata)
            then
        return pandas DataFrame
    """
    skiprows = 2
    return pd.DataFrame({
        Path(i).stem: pd.read_table(i,
                                    sep=',',
                                    skiprows=skiprows,
                                    engine='python',
                                    index_col=0,
                                    usecols=[0, 1]).squeeze()
        for i in files
    })


def read_spectrum_analyzer(*files):
    """ネットワークアナライザN9010Aからデータインポート
    USAGE:
        read_spectrum_analyzer(test1.CSV, test2.CSV, test3.CSV)
            or
        import glob
        testdata = glob.iglob('*.CSV')
        read_spectrum_analyzer(*testdata)
            then
        return pandas DataFrame
    """
    skiprows = 43
    return pd.DataFrame({
        Path(i).stem: pd.read_table(i,
                                    sep=',',
                                    skiprows=skiprows,
                                    engine='python',
                                    index_col=0,
                                    usecols=[0, 1]).squeeze()
        for i in files
    })


def nearest_x(df, value):
    """valueに最も近い値下がったところのindexを返す"""
    down = df.max() - value
    absolute_sub = pd.DataFrame(abs(df - down)).sort_values(by=df.columns[0])
    return absolute_sub


# 残骸
# class DataReader:
#     machine=(A_9010, N_5071)
#     __init__(file, machine)
#         if not machine
#         machine=self.machine

# class Reader:
#     machines = {'N5071': 2, 'N9010A': 43}
#     def __init__(self):
#
#
#     def read_spectrum_analyzer(skiprows=Reader.machines['N5071'], *data):
