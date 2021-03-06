#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" コンデンサ組み合わせバイナリ表を出力する計算ライブラリ"""

import os
from IPython.display import display
import numpy as np
import pandas as pd


class Lcbin(pd.DataFrame):
    """Binary Capacitance table"""

    def __init__(
            self,
            c_res: float,
            c_num: int,
            lmh: float,
            c_initial: float = 0,
            c_para: float = 0,
            c_ser: float = 0,
    ):
        """
        # Quick Start:
        >>> Lcbin(10, 4, 12.5)
            10  20  40  80  CpF        fkHz
        0    0   0   0   0    0         inf
        1    1   0   0   0   10  450.158158
        2    0   1   0   0   20  318.309886
        3    1   1   0   0   30  259.898934
        4    0   0   1   0   40  225.079079
        5    1   0   1   0   50  201.316848
        6    0   1   1   0   60  183.776298
        7    1   1   1   0   70  170.143791
        8    0   0   0   1   80  159.154943
        9    1   0   0   1   90  150.052719
        10   0   1   0   1  100  142.352509
        11   1   1   0   1  110  135.727792
        12   0   0   1   1  120  129.949467
        13   1   0   1   1  130  124.851409
        14   0   1   1   1  140  120.309828
        15   1   1   1   1  150  116.230337

        usage:
            `x = Lcbin(c_initial=0, c_res=10, c_num=4, lmh=12.5)`
            コンデンサを4チャンネル(c_num)用意し、
            それぞれ10, 20, 40, 80pFを割り当てる。
            増加率が10(c_res)から始まり倍々に増えていく(+10, +20, +40, ...)

            CpF列にコンデンサの合計値を出力する
            fkHz列にlmh(=接続するインダクタンス)と計算した同調周波数を出力する

        args:
            c_initial: Minimum Capacitance[pf](float)
            c_res: Resolution of capacitance[pf](float)
            c_num: Number of capacitance[uF](int)
            lmh: Indactance[mH](float)

        self: Binary table (pd.DataFrame)
            ビットテーブルを出力する
            ビットテーブルは行番号1から始まる。
            行番号0はコンデンサなし、つまり非同調なので考える必要がない。
            そのため、あらかじめ削除してあるので、行番号は1から始まる。

        `bc`
        LCバイナリと合計容量CpF, 同調周波数fkHzを出力する
        pandas.DataFrameを継承

        `bc.channels()`
        ONにするビットフラグを

        `bc.to_csv()`
        条件をパースしてcsvファイルを生成する。
        引数directoryを指定することで所定のディレクトリに保存する。

        `bc.dump()`
        pandas 初期設定の省略表示を無視して全行列を標準出力に表示


        # 行数テスト
        # 行の長さは2のn乗
        >>> n=6
        >>> bc = Lcbin(10, n, 100)
        >>> len(bc) == 2**n
        True

        # index のテスト
        # stop=64 = 2 ** 6
        >>> bc.index
        RangeIndex(start=0, stop=64, step=1)


        # columns のテスト
        >>> bc.columns
        Index([10, 20, 40, 80, 160, 320, 'CpF', 'fkHz'], dtype='object')

        # bc.array のテスト
        >>> bc.array[:5]
        array([[0, 0, 0, 0, 0, 0],
               [1, 0, 0, 0, 0, 0],
               [0, 1, 0, 0, 0, 0],
               [1, 1, 0, 0, 0, 0],
               [0, 0, 1, 0, 0, 0]])

        # # 2のn乗数列とかけて合計すると連番になる
        # >>> test_bin = [1, 2, 4, 8, 16, 32]
        # >>> sums = (bc.array * test_bin).sum(1)
        # >>> sums[:12]
        # array([ 0,  1,  2,  3,  4,  5,  6,  7,  8,  9, 10, 11])
        # >>> np.array_equal(sums, np.arange(2**n))
        # True


        # CpF のテスト
        >>> bl = bc.array[8]
        >>> bin2int(reversed(bl))
        8
        >>> ar = np.arange(2**6)
        >>> test = np.array([bin2int(reversed(bl)) for bl in bc.array])
        >>> np.array_equal(test, ar)
        True

        # fkHz のテスト
        # 同調周波数とコンデンサからインダクタンスを逆算
        >>> j = 14
        >>> np.floor(1e3/(( 2*np.pi*bc.fkHz[j]*1e3 )**2 * bc.CpF[j]*1e-12))
        100.0

        # === テストできないメソッド ===
        # >>> bc.dump(): すべての行列をプリント(省略しない)
        # >>> bc.to_csv(): 条件をパースしてファイル名を自動的にアサインしてcsvに保存
        """
        super().__init__(binary_array(c_num))
        # Required
        self._c_res = c_res
        self._c_num = c_num
        self._lmh = lmh
        # Not required
        self._c_initial = c_initial
        self._c_para = c_para
        self._c_ser = c_ser

        # index & columns
        self.index = range(2**c_num)
        self.columns = c_list(c_initial, c_res, c_num)

        # binary array
        # UserWarning: Pandas doesn't allow columns to be created
        # via a new attribute name <- 仕方ないワーニングがでる
        # 「今後array列が作れなくなる副作用がある」という意味のワーニング
        self.array = self.iloc[:, :c_num].values  # Do not use `bc['array']`

        # 合計コンデンサ列CpF & 同調周波数列fkHz
        self['CpF'] = c_para + (self.columns.values * self.array).sum(1)
        if c_ser != 0:  # Evade 0 div warning
            self.CpF = 1 / ((1 / self.CpF) + (1 / c_ser))

        def resonance_freq(l, c):
            """同調周波数を返すクロージャ"""
            return 1 / (2 * np.pi * np.sqrt(l * c))

        self['fkHz'] = resonance_freq(self._lmh * 1e-3,
                                      self.CpF * 1e-12) / 1000

    def to_csv(self, directory=os.getcwd(), sort: str = None, *args, **kwargs):
        """save to csv.
        default current directory
        インスタンス化した際のパラメータをパースして、ファイル名を自動的に決める
        デフォルトではカレントディレクトリ下にファイルを保存する
        """
        init = 'init' + str(self._c_initial)
        res = 'res' + str(self._c_res)
        pat = 'pat' + str(self._c_num)
        lmh = 'l' + str(self._lmh)

        # ドットをp(pointの意味)に変換(ファイルネームに.は紛らわしい)
        name = [s.replace('.', 'p') for s in (init, res, pat, lmh)]
        name.append('.csv')
        name.insert(0, '/')
        name.insert(0, directory)
        filename = ''.join(name)
        if sort:
            self.table.sort_values(sort).to_csv(filename, *args, **kwargs)
        else:
            self.table.to_csv(filename, *args, **kwargs)

    def channels(self, ix):
        """self.tableの行数を引数に、ONにするビットフラグをリストで返す

        channles 1  2  3  4  5  6
               |  |  |  |  |  |
        array([0, 1, 1, 0, 0, 0])

        >>> c_res, c_num , lmh, c_initial = 100, 6, 10, 0
        >>> bc = Lcbin(c_res, c_num, lmh, c_initial)
        >>> bc.channels(0)
        []

        >>> bc.channels(1)
        [1]

        >>> bc.channels(-1)
        [1, 2, 3, 4, 5, 6]

        >>> bc.channels(len(bc))
        Traceback (most recent call last):
        ...
        IndexError: index 64 is out of bounds for axis 0 with size 64

        >>> bc.channels(len(bc)-1)
        [1, 2, 3, 4, 5, 6]

        >>> bc.array[6]
        array([0, 1, 1, 0, 0, 0])
        >>> bc.channels(6)
        [2, 3]

        2チャンネルと3チャンネルをONにしろ、という意味
        """
        return [i for i, b in enumerate(self.array[ix], start=1) if b]


def dump(self):
    """print all rows & columns""" ""
    with pd.option_context('display.max_rows', len(self), 'display.width', 0):
        display(self)


setattr(pd.DataFrame, 'dump', dump)
# === わざわざsetattrしている理由 ===
# sort_values()メソッド使った後にもdumpしたいので、
# Lcbinだけでなく、pandas.DataFrameにメソッドを割り当てたい


def c_list(c_initial, c_res, c_num):
    """Capacitance list
    >>> c_list(0, 10, 3)
    [10, 20, 40]
    >>> c_list(2,1,4)
    [3, 4, 6, 10]
    """
    return [c_initial + c_res * 2**_c for _c in range(c_num)]


def int2bin(int_i: int, zero_pad: int) -> str:
    """
    >>> int2bin(3, 4)
    '0011'
    >>> int2bin(5, 5)
    '00101'
    """
    return '{:0{}b}'.format(int_i, zero_pad)


def bin2int(bc_array):
    """テスト用関数(int2bin()の逆関数)
    >>> bin2int([0, 1, 1])
    3
    >>> bin2int([0, 0, 1, 1])
    3
    >>> bin2int([1, 1, 1, 1, 1])
    31
    """
    mp_str = map(str, bc_array)
    joined_str = ','.join(mp_str).replace(',', '')
    return int(joined_str, 2)  # 2進数の2


def binary_array(c_num) -> np.ndarray:
    """Binary Capacitance table
    インダクタンス容量からコンデンサのバイナリ
    組み合わせテーブルを作成するpythonスクリプト

    usage:
        `Lcbin.array(c_res=5, c_num=9, lmh=39, c_initial=120)`
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

    >>> binary_array(2)
    array([[0, 0],
           [1, 0],
           [0, 1],
           [1, 1]])

    >>> binary_array(3)
    array([[0, 0, 0],
           [1, 0, 0],
           [0, 1, 0],
           [1, 1, 0],
           [0, 0, 1],
           [1, 0, 1],
           [0, 1, 1],
           [1, 1, 1]])

    >>> binary_array(6)[0]
    array([0, 0, 0, 0, 0, 0])

    >>> binary_array(6)[-1]
    array([1, 1, 1, 1, 1, 1])

    >>> n = 10
    >>> binary_array(n).shape == (2**n, n)
    True
    """
    # ':0{}b'.format(_i, c_num) <- c_numの数だけ0-paddingし、_iを二進数に変換する
    b_list = np.array([reversed(int2bin(_i, c_num)) for _i in range(2**c_num)])
    # b_list like...
    # array(['000000000000', '100000000000', '010000000000', ...,
    # '101111111111', '011111111111', '111111111111'], dtype='<U12')

    b_array = np.array([list(b) for b in b_list]).astype(int)
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
            float(argv[1]),  # c_res
            int(argv[2]),  # c_num
            float(argv[3]),  # lmh
            float(argv[4]),  # c_initial
            float(argv[5]),  # c_para
            float(argv[6]),  # c_ser
        ]
        Lcbin(*lc_args).dump()
        return ''  # for chomp last 'None' word
    return Lcbin.__init__.__doc__


if __name__ == '__main__':
    import sys
    if 'debug' in sys.argv:
        import doctest
        doctest.testmod()
    else:
        print(main(sys.argv))
