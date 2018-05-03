#!/bin/env python3

import pandas as pd
import numpy as np
from scipy import stats
def describe_SN(data, freq):
    """SN比の計算
    * 特定の周波数: atfreq
    * atfreq付近の平均値: sig
    * ノイズフロア=全体の四分位境界値: noise
    * SN比:sn  # snはsigとnoiseの差分
    
    以上をpandas DataFrame形式(表形式)で返す
    """
    atfreq = data.loc[freq]
    sig = data[freq-0.02:freq+0.02].mean()
    noise = data.apply(lambda x: stats.scoreatpercentile(x, 25))
    sn = pd.DataFrame([atfreq, sig]).max() - noise
    dicc = {'{}kHz'.format(freq):atfreq,
            'シグナル平均': sig,
            'ノイズフロア': noise,
            'SN比': sn}
    df = pd.DataFrame(dicc, columns=dicc.keys())
    return df
