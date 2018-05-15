#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lcbin.py
インダクタンス容量からコンデンサのバイナリ
組み合わせテーブルを作成するpythonスクリプト
"""
import pandas as pd
import numpy as np

binl = [list(format(_, 'b'))[::-1] for _ in range(512)]
coll = [5 * 2**_ for _ in range(9)]
df = pd.DataFrame(binl, columns=coll).fillna(0)

csum = np.arange(0, 2556, 5)
df['Csum'] = csum

lmh = 0.039
fHz = 1 / (2 * np.pi * np.sqrt(csum * 1e-12 * lmh))

df['fkHz'] = fHz / 1000
df.to_csv('binc.csv')
