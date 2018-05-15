#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
np.seterr(divide='ignore')  # divideによるエラーを無視する

# import warnings
# warnings.filterwarnings('error')


def binary_c(c_initial, c_num, lmh):
    """Binary Capacitance table
    インダクタンス容量からコンデンサのバイナリ
    組み合わせテーブルを作成するpythonスクリプト

    usage:
        `binary_c(5, 9, 39)`
    args:
        c_initial: Minimum Capacitance(float)
        c_num: Number of capacitance[uF](float)
        lmh: Indactance[mH](float)
    return:
        df: Binary table (pd.DataFrame)
    """
    # Binary columns
    bin_list = [list(format(_, 'b'))[::-1] for _ in range(2**c_num)]
    c_list = [c_initial * 2**_ for _ in range(c_num)]
    df = pd.DataFrame(bin_list, columns=c_list).fillna(0)

    # Capacitance columns
    csum = np.arange(0, sum(c_list) + 1, c_initial)
    df['Csum'] = csum

    # Frequency columns
    fHz = 1 / (2 * np.pi * np.sqrt(csum * 1e-12 * lmh * 1e-3))
    df['fkHz'] = fHz / 1000
    df.drop(0, inplace=True)
    return df


def nosyncf(second_trance):
    """
    second_trance: unit[mH]
    ant_indactance: unit[mH]
    normal_nosyncf: unit[kHz]
    """
    first_trance = 27
    normal_nosyncf = 166
    return normal_nosyncf / np.sqrt(second_trance / first_trance)


if __name__ == '__main__':
    print('===binary_c test===')
    print(binary_c(5, 9, 0.39))
