#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""CSVを読み込んでデータフレーム化
マシン名: 
    ネットワークアナライザ:N5071
    スペクトラムアナライザ:A9010
"""

import pandas as pd
import os
def reader_N5071(*filelist):
    """ネットワークアナライザN5071からデータインポート"""
    skiprows = 3
    tempdata = pd.read_csv(filelist[0], skiprows=skiprows,
                           engine='python', names=['Frequency', 'temp'],
                           usecols=[0,1], index_col=0)
    df = pd.DataFrame(tempdata)
    for file in filelist:
        dff = pd.read_csv(file, skiprows=skiprows-1, engine='python',
                          usecols=[0,1], index_col=0)
        basename = os.path.splitext(os.path.basename(file))[0]
        df[basename] = dff
    del df['temp']
    return df

def reader_A9010(*filelist):
    skiprows = 44
    # 1ファイルだけ読み込んでindex設定用に使う
    tempfile = filelist[0]
    tempdata = pd.read_csv(tempfile, skiprows=skiprows, engine='python',
                           names=['temp'])
    df = pd.DataFrame(tempdata)
    for file in filelist:
        dff = pd.read_csv(file, skiprows=skiprows - 1, engine='python')
        basename = os.path.splitext(os.path.basename(file))[0]
        df[basename] = dff
    del df['temp']
    return df

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


