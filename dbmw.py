#!/usr/bin/env python3
"""デシベルdB <-> ミリワットmW 変換"""

def mw2db(x):
    """mW -> dB
    Usage: `df.mw2db()` or `mw2db(df)`

    ```python:TEST
    mw = pd.Series(np.arange(11))
    df = pd.DataFrame({'watt': mw, 'dBm': mw.mw2db(), 'dB to watt': mw.mw2db().db2mw()})
    print(df)
    #[Out]#     dB to watt        dBm  watt
    #[Out]# 0          0.0       -inf     0
    #[Out]# 1          1.0   0.000000     1
    #[Out]# 2          2.0   3.010300     2
    #[Out]# 3          3.0   4.771213     3
    #[Out]# 4          4.0   6.020600     4
    #[Out]# 5          5.0   6.989700     5
    #[Out]# 6          6.0   7.781513     6
    #[Out]# 7          7.0   8.450980     7
    #[Out]# 8          8.0   9.030900     8
    #[Out]# 9          9.0   9.542425     9
    #[Out]# 10        10.0  10.000000    10
    ```"""
    return 10 * np.log10(x)


def db2mw(x):
    """dB -> mW
    Usage: `df.db2mw()` or `db2mw(df)` """
    return np.power(10, x / 10)


# -----------------------------------------
# メソッドをpd.DataFrame, pd.Seriesに追加
# -----------------------------------------
_cs = 'pd.DataFrame', 'pd.Series'
_flist = 'noisefloor', 'db2mw', 'mw2db'
for _c in _cs:
    for _f in _flist:
        exec('%s.%s=%s' % (_c, _f, _f))

