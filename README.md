# sana.py
SA: Spectram Analyzer
NA: Network Analyzer
SAとNAから得たデータの整理用スクリプト


## nearest\_x()
valueに最も近い値下がったところのindexを返す


## class Syncf:
usage:
    # On bash shell
    $ python sana.py hoge.csv

    # In python
    sf = sana.Syncf(df.iloc[:,0])  # Args must be Series type
    sf.describe()  # Show table
    sf.plot()  # Show graph

args:
    data: Network Analyzerから読んだF特(pandas.Series型)

return
    f1: 3dB落ちの周波数(低域)
    f2: 3dB落ちの周波数(高域)
    f0: 帯域幅から算出する同調周波数(f1, f2の平均値)
    fmax: 最大値から算出する同調周波数(最大値)
    BW: 3dB落ちの帯域幅 (f2-f1)
    Q: Q値 (f0 / BW)
    a: 1Hzあたりの減衰[dB]


### score()
ずれ幅
1が一番よい値。0が一番悪い値です。
0.95未満だとデータ数が足りないか、
データの端が切れています。
sf.plot()でF得を表示して確認してください。


### describe()
周波数情報を返す

* f1,f2: Frequency
* f0, fmax: Sync frequency
* BW; f2-f1
* Q: f0 / BW
* a: -a[dB] / Hz


### plot
Return plot and point of f1~f2


### main()
from shell session
$ python sana.py test.csv


# csv\_reader.py
CSVを読み込んでデータフレーム化
マシン名:
    ネットワークアナライザ:N5071
    スペクトラムアナライザ:A9010


# describe\_SN

SN比の計算
* 特定の周波数: atfreq
* atfreq付近の平均値: sig
* ノイズフロア=全体の四分位境界値: noise
* SN比:sn  # snはsigとnoiseの差分

以上をpandas DataFrame形式(表形式)で返す

# lcbin.py
""" コンデンサ組み合わせバイナリ表を出力する計算ライブラリ

## Quick Start:
>>> Lcbin(0, 10, 4, 12.5)
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


## usage:
    `x = Lcbin(c_initial=0, c_res=10, c_num=4, lmh=12.5)`
    コンデンサを4チャンネル(c_num)用意し、
    それぞれ10, 20, 40, 80pFを割り当てる。
    増加率が10(c_res)から始まり倍々に増えていく(+10, +20, +40, ...)

    CpF列にコンデンサの合計値を出力する
    fkHz列にlmh(=接続するインダクタンス)と計算した同調周波数を出力する

## args:
    c_initial: Minimum Capacitance[pf](float)
    c_res: Resolution of capacitance[pf](float)
    c_num: Number of capacitance[uF](int)
    lmh: Indactance[mH](float)

## self: Binary table (pd.DataFrame)
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


```python
# 行数テスト
# 行の長さは2のn乗
>>> n=6
>>> bc = Lcbin(0, 10, n, 100)
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
```
