#!/usr/bin/env python3
# -*- coding: utf-8 -*-
""" 組み合わせ計算に使用する計算ライブラリ"""
from itertools import combinations_with_replacement
from itertools import chain

# E24系列
CAPLIST_E24 = [
    1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7, 1.8, 1.9, 2.0, 2.1, 2.2, 2.4, 2.7,
    3.0, 3.3, 3.6, 3.9, 4.3, 4.7, 5.1, 5.6, 6.2, 6.8, 7.5, 8.2, 9.1, 10, 11,
    12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56, 62, 68,
    75, 82, 91, 100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270, 300,
    330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910, 1000, 1100,
    1200, 1500, 1800, 2200, 2400, 2700, 3000, 3300, 3900, 4700, 5100
]


def combi_proposer(combo: int, var, caplist: list = CAPLIST_E24) -> tuple:
    """合計してvarになる組み合わせをリストする
    組み合わせパターンをcomboに指定する(2組の合計を出すなら、combo=2)
    caplistから重複ありの組み合わせをc_combinationsに格納
    合計してvarになる組み合わせcaplist要素の組み合わせをtuple in tupleで返す

    usage:
        combi_proposer(combo=2, var=22)  # 22を2個の合計で実現する組み合わせを列挙

    test:
    >>> combi_proposer(2, 100)
    ((18, 82),)

    >>> combi_proposer(2, 102)
    ((11, 91), (20, 82), (27, 75), (51, 51))

    >>> combi_proposer(2, 36)
    ((12, 24), (16, 20), (18, 18))

    # 組み合わせ数を増やすと当然結果が増える
    >>> combi_proposer(3, 36)
    ((10, 10, 16), (10, 11, 15), (10, 13, 13), (11, 12, 13), (12, 12, 12))

    # [::2]で1個置きにすることでE12系列にすると結果が少なくなる。
    >>> combi_proposer(3, 36, CAPLIST_E24[::2])
    ((12, 12, 12),)

    # varにリストかタプルを指定すると、結果をディクショナリで返す
    >>> combi_proposer(2, [22, 24, 26])
    {22: ((10, 12), (11, 11)), 24: ((11, 13), (12, 12)),\
 26: ((10, 16), (11, 15), (13, 13))}
    """
    if not isinstance(var, (list, tuple)):
        # 重複組み合わせ
        c_combinations = list(combinations_with_replacement(caplist, combo))
        # 組み合わせ合計値
        c_patterns = (sum(tpl) for tpl in c_combinations)
        # c_combinationsの合計(=c_patterns)がvarとなるときのインデックス
        ix_list = [i for i, c in enumerate(c_patterns) if c == var]
        # 合計がvarになるときの組み合わせ
        return tuple(c_combinations[i] for i in ix_list)
    return {k: combi_proposer(combo, k, caplist) for k in var}


def has_value(var, combi_proposer_dict):
    """`combi_proposer_all()`の結果から、
    共通で含まれるvarを持つkeyをリストアップする

    >>> cli = combi_proposer(3, [220, 240, 260], CAPLIST_E24[::2])
    >>> cli
    {220: ((18, 22, 180), (18, 82, 120), (56, 82, 82)), \
240: ((10, 10, 220), (22, 68, 150), (27, 33, 180)), \
260: ((10, 100, 150), (12, 68, 180), (18, 22, 220), (33, 47, 180))}

    >>> has_value(100,cli)
    [260]

    >>> has_value(10,cli)
    [240, 260]

    >>> has_value(68,cli)
    [240, 260]
    """
    # `list(chain.from_iterable(v))` <- flatten tuple of tuple
    return [
        k for k, v in combi_proposer_dict.items()
        if var in list(chain.from_iterable(v))
    ]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
