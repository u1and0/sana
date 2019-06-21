#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" コンデンサ組み合わせバイナリ表を出力する計算ライブラリ"""
import os
import numpy as np
import pandas as pd


class Lcbin(pd.DataFrame):
    """Binary Capacitance table
    インダクタンス容量からコンデンサのバイナリ
    組み合わせテーブルを作成するpythonスクリプト
    """

    def __init__(self, c_initial: float, c_res: float, c_num: int, lmh: float):
        """
        usage:
            `x = Lcbin(c_initial=120, c_res=5, c_num=9, lmh=39)`
            コンデンサを9チャンネル用意し、
            120pFのコンデンサから倍倍に9-1回増えて
            最も大きい一つのコンデンサ容量が120 + 5*2**8=1400pF
            接続するインダクタンスが39mHの場合
            同調周波数が最高72kHz, 最低15kHz

        args:
            c_initial: Minimum Capacitance[pf](float)
            c_res: Resolution of capacitance[pf](float)
            c_num: Number of capacitance[uF](int)
            lmh: Indactance[mH](float)

        return:
            df: Binary table (pd.DataFrame)
            `x.table`
            ビットテーブルを出力する

        `x.table`
        LCバイナリと合計容量CpF, 同調周波数fkHzを出力する

        `x.to_csv()`
        条件をパースしてcsvファイルを生成する。
        引数directoryを指定することで所定のディレクトリに保存する。

        >>> x = Lcbin(160, 2, 12, 13.5)
        >>> len(x.table) == x.len
        True
        """
        super().__init__(data=binary_array(c_num),
                         columns=c_list(c_initial, c_res, c_num))
        self._c_initial = c_initial
        self._c_res = c_res
        self._c_num = c_num
        self._lmh = lmh
        self.array = binary_array(self._c_num)
        # self.table = self._table()

    def csum(self):
        """binary tableに応じてCapacitanceの合計値を列加える"""
        # c_df = self.copy()
        self['CpF'] = (self.columns * self).sum(1)
        return self

    def fsync(self):
        """Frequency column"""

        def _sync(l_, c_):
            """同調周波数を返す"""
            return 1 / (2 * np.pi * np.sqrt(l_ * c_))

        self['fkHz'] = _sync(self.lmh * 1e-3, self.CpF * 1e-12) / 1000
        return self

    def to_csv(self, directory=os.getcwd(), sort: str = None):
        """save to csv.
        default current directory
        """
        init = 'init' + str(self.c_initial)
        res = 'res' + str(self.c_res)
        pat = 'pat' + str(self.c_num)
        lmh = 'l' + str(self.lmh)
        name = [s.replace('.', 'p') for s in (init, res, pat, lmh)]
        name.append('.csv')
        name.insert(0, '/')
        name.insert(0, directory)
        filename = ''.join(name)
        if sort:
            self.table.sort_values(sort).to_csv(filename)
        else:
            self.table.to_csv(filename)


def dump(self):
    """print all rows & columns""" ""
    with pd.option_context('display.max_rows', len(self), 0):
        print(self)


setattr(pd.DataFrame, 'dump', dump)

# def _table(self) -> pd.DataFrame:
#     """arrayをpandas DataFrame化し、
#     合計キャパシタンス列(CpF) と 同調周波数列(fkHz) を追加するメソッド
#     """
#     c_list = [
#         self.c_initial + self.c_res * 2**_c for _c in range(self.c_num)
#     ]
#     blc_df = pd.DataFrame(self.array, columns=c_list)
#
#     # Capacitance column
#     blc_df['CpF'] = (blc_df.columns * blc_df).sum(1)
#
#     # Frequency column
#     blc_df['fkHz'] = syncf(self.lmh * 1e-3, blc_df.CpF * 1e-12) / 1000
#     return blc_df


def channels(self, ix):
    """self.tableの行数を引数に、ONにするビットフラグをリストで返す"""
    return [i for i, b in enumerate(self.array[ix], start=1) if b]


def c_list(c_initial, c_res, c_num):
    """Capacitance list"""
    return [c_initial + c_res * 2**_c for _c in range(c_num)]


def binary_array(c_num) -> np.ndarray:
    """Binary Capacitance table
    インダクタンス容量からコンデンサのバイナリ
    組み合わせテーブルを作成するpythonスクリプト

    usage:
        `Lcbin.array(c_initial=120, c_res=5, c_num=9, lmh=39)`
        コンデンサを9チャンネル用意し、
        120pFのコンデンサから倍倍に9-1回増えて
        最も大きい一つのコンデンサ容量が120 + 5*2**8=1400pF
        接続するインダクタンスが39mHの場合
        同調周波数が最高72kHz, 最低15kHz
    args:
        c_initial: Minimum Capacitance[pf](float)
        c_res: Resolution of capacitance[pf](float)
        c_num: Number of capacitance[uF](int)
        lmh: Indactance[mH](float)
    return:
        df: Binary table (pd.DataFrame)
    """
    # ':0{}b'.format(_i, c_num) <- c_numの数だけ0-paddingし、_iを二進数に変換する
    b_list = np.array(
        ['{:0{}b}'.format(_i, c_num)[::-1] for _i in range(2**c_num)])
    # b_list like...
    # array(['000000000000', '100000000000', '010000000000', ...,
    # '101111111111', '011111111111', '111111111111'], dtype='<U12')

    b_array = np.array([list(b) for b in b_list[1:]]).astype(int)
    # [1:] は0のみの行排除のため
    # b_array like...
    # [[0,0,1,...],
    # [1,0,1,...],
    # [1,1,1,...]]
    return b_array


def main(argv):
    """call from shell function"""
    if len(argv) > 1:
        lc_args = [
            float(argv[1]),  # c_initial
            float(argv[2]),  # c_res
            int(argv[3]),  # c_num
            float(argv[4])  # lmh
        ]
        Lcbin(*lc_args).pprint()
        return ''  # for chomp last 'None' word
    return Lcbin.__init__.__doc__


if __name__ == '__main__':
    import sys
    if 'debug' in sys.argv:
        import doctest
        doctest.testmod()
    else:
        print(main(sys.argv))
