"""S/N Analysis used in Network Analyser or Spectrum Analyser

# sana.py
SA: Spectram Analyzer
NA: Network Analyzer
SAとNAから得たデータの整理用スクリプト


## nearest_x()
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


# csv_reader.py
CSVを読み込んでデータフレーム化
マシン名:
    ネットワークアナライザ:N5071
    スペクトラムアナライザ:N9010A


# describe_SN

SN比の計算
* 特定の周波数: atfreq
* atfreq付近の平均値: sig
* ノイズフロア=全体の四分位境界値: noise
* SN比:sn  # snはsigとnoiseの差分

以上をpandas DataFrame形式(表形式)で返す

# lcbin.py
Binary Capacitance table
インダクタンス容量からコンデンサのバイナリ
組み合わせテーブルを作成するpythonスクリプト

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
        display_all: default False(bool)

    return:
        df: Binary table (pd.DataFrame)
        `x.table`
        ビットテーブルを出力する

    `x.table`
    LCバイナリと合計容量CpF, 同調周波数fkHzを出力する

    `x.to_csv()`
    条件をパースしてcsvファイルを生成する。
    引数directoryを指定することで所定のディレクトリに保存する。
"""

from .csv_reader import reader_N5071
from .csv_reader import reader_N9010A
from .describe_SN import describe_SN
from .sana import Syncf
from .sana import nearest_x
from .dbmw import db2mw
from .dbmw import mw2db
from .lcbin import Lcbin
from .lcbin import binary_c
from .lcbin import combi_proposer
