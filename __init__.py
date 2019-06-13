"""S/N Analysis used in Network Analyser or Spectrum Analyser

* reader_N5071
* reader_A9010
    CSVを読み込んでデータフレーム化
    マシン名:
        ネットワークアナライザ:N5071
        スペクトラムアナライザ:A9010


* describe_SN
    SN比の計算

    * 特定の周波数: atfreq
    * atfreq付近の平均値: sig
    * ノイズフロア=全体の四分位境界値: noise
    * SN比:sn  # snはsigとnoiseの差分

    以上をpandas DataFrame形式(表形式)で返す


* nearest_x
    valueに最も近い値下がったところのindexを返す
* Syncf
    3dB, 6dBゲイン落ちの周波数を返す
    任意のdB落ちゲインを返すときは`sana.nearest_x`を参照
"""

from .csv_reader import reader_N5071
from .csv_reader import reader_A9010
from .describe_SN import describe_SN
from .sana import Syncf
from .sana import nearest_x
from dbmw import db2mw
from dbmw import mw2db
