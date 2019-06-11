#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
np.seterr(divide='ignore')  # divideによるエラーを無視する

# import warnings
# warnings.filterwarnings('error')


def binary_c(c_initial: float,
             c_res: float,
             c_num: int,
             lmh: float,
             display_all: bool = False) -> pd.DataFrame:
    """Binary Capacitance table
    インダクタンス容量からコンデンサのバイナリ
    組み合わせテーブルを作成するpythonスクリプト

    usage:
        `binary_c(5, 9, 39)`
        # 5pFのコンデンサから倍倍に9回増えて
        # 最も大きい一つのコンデンサ要領が5*2**9=2560pF
        # 接続するインダクタンスが39mHの場合
    args:
        c_initial: Minimum Capacitance[pf](float)
        c_res: Resolution of capacitance[pf](float)
        c_num: Number of capacitance[uF](int)
        lmh: Indactance[mH](float)
        display_all: default False(bool)
    return:
        df: Binary table (pd.DataFrame)
    """
    # Binary columns
    # 二進数表記に変換
    bin_list = [list(format(_, 'b'))[::-1] for _ in range(2**c_num)]
    c_list = [c_res * 2**_ for _ in range(c_num)]
    df = pd.DataFrame(bin_list, columns=c_list).fillna(0)

    # Capacitance columns
    csum = np.arange(0, sum(c_list) + 1, c_res)
    df.columns += c_initial
    df['CpF'] = csum + c_initial

    # Frequency columns
    fHz = 1 / (2 * np.pi * np.sqrt(df.CpF * 1e-12 * lmh * 1e-3))
    df['fkHz'] = fHz / 1000
    df.drop(0, inplace=True)
    if display_all:
        pd.options.display.max_rows = len(df)
        pd.options.display.width = 0
    return df


def nosyncf(second_trance, first_trance=27, normal_nosyncf=166):
    """ 自己共振点を計算する関数
    usage: nosyncf(second_trance=11, first_trance=27, normal_nosyncf=166)

    second_trance: unit[mH]
    ant_indactance: unit[mH]
    normal_nosyncf: unit[kHz]
    """
    return normal_nosyncf / np.sqrt(second_trance / first_trance)


def main(argv):
    if len(argv) > 1:
        lc_args = []
        lc_args.append(float(argv[1]))
        lc_args.append(int(argv[2]))
        lc_args.append(float(argv[3]))
        lc_table = binary_c(*lc_args, display_all=True)
        return lc_table
    else:
        return binary_c.__doc__


if __name__ == '__main__':
    import sys
    print(main(sys.argv))
