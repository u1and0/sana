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
