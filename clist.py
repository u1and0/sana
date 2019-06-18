#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
組み合わせ計算使用する計算ライブラリ
* def combi_proposer()
"""
from itertools import combinations_with_replacement
from itertools import chain
import json
CAPLIST = [
    10, 11, 12, 13, 15, 16, 18, 20, 22, 24, 27, 30, 33, 36, 39, 43, 47, 51, 56,
    62, 68, 75, 82, 91, 100, 110, 120, 130, 150, 160, 180, 200, 220, 240, 270,
    300, 330, 360, 390, 430, 470, 510, 560, 620, 680, 750, 820, 910, 1000,
    1100, 1200, 1500, 1800, 2200, 2400, 2700
]


def combi_proposer(var: int, combo: int, caplist: list = CAPLIST) -> tuple:
    """合計してvarになる組み合わせをリストする
    組み合わせパターンをcomboに指定する(2組の合計を出すなら、combo=2)
    caplistから重複ありの組み合わせをc_combinationsに格納
    合計してvarになる組み合わせcaplist要素の組み合わせをtupleで返す
    >>> t1 = combi_proposer(100,2)
    >>> t1
    ((18, 82),)
    >>> all(sum(i) for i in t1)
    True

    >>> t2 = combi_proposer(102,2)
    >>> t2
    ((11, 91), (20, 82), (27, 75), (51, 51))
    >>> all(sum(i) for i in t2)
    True

    >>> t3 = combi_proposer(128,2)
    >>> t3
    ((18, 110),)
    >>> all(sum(i) for i in t3)
    True

    >>> t4 = combi_proposer(256,2)
    >>> t4
    ((16, 240), (36, 220), (56, 200))
    >>> all(sum(i) for i in t4)
    True
    """
    # 重複組み合わせ
    c_combinations = list(combinations_with_replacement(caplist, combo))
    # 組み合わせ合計値
    c_patterns = (sum(tpl) for tpl in c_combinations)
    # c_combinationsの合計(=c_patterns)がvarとなるときのインデックス
    ix_list = [i for i, c in enumerate(c_patterns) if c == var]
    # 合計がvarになるときの組み合わせ
    return tuple(c_combinations[i] for i in ix_list)


def combi_propose_all(combo: int, *vars_list) -> dict:
    """call `combi_proposer` giving vars as list_like_object"""
    return {k: combi_proposer(k, combo) for k in vars_list}


def has_value(var, combi_proposer_dict):
    """`combi_proposer_all()`の結果から、
    共通で含まれるvarを持つkeyをリストアップする
    """
    # `list(chain.from_iterable(v))` <- flatten tuple of tuple
    return [
        k for k, v in combi_proposer_dict.items()
        if var in list(chain.from_iterable(v))
    ]


if __name__ == '__main__':
    import doctest
    doctest.testmod()
