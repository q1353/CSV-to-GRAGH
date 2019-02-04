# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick
import matplotlib.dates as mdates
import datetime
import seaborn as sns

from WaterClass import Water
from MoistAirClass import MoistAir

#data instance
df = pd.read_csv('test.csv')

#int型 ⇒ string型変換
df['year'] = df['year'] .astype(str)
df['month'] = df['month'] .astype(str)
df['day'] = df['day'] .astype(str)

#Date/Time列に年月日時間を結合して日付・時間を代入
df["Date/Time"] = pd.to_datetime(df['year'] + '-' + df['month'] + '-' + df['day'] + ' ' + df['time'])

#Date/Time列をインデックスに設定
df = df.set_index("Date/Time")

#year month day time を消去
df = df.drop(['year','month','day','time'],axis=1)

#PandasデータをNumpyデータに変換
dataframe = df.values

i = 0 #カウンタi 初期化
count = dataframe.shape[0] #データ行数のカウント：境界条件設定

_ahum = np.array([]) #絶対湿度Array初期化
_enthalpy = np.array([]) #エンタルピーArray初期化
_dewpoint = np.array([]) #露点温度Array初期化

#各行の温度と相対湿度データを引数として、絶対湿度＆エンタルピーを計算
while i < count:
    _temp=dataframe[i,0]
    _rhum=dataframe[i,1]

    #MoistAir Classのインスタンス化
    moistair = MoistAir(_temp , _rhum)

    ah = moistair.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity()
    e = moistair.GetEnthalpyFromHumidityRatioAndRelativeHumidity()
    dp = moistair.GetSaturationDryBulbTemperatureFromHumidityRatio()
    
    #_ahum空Arrayにahデータを後ろから追記
    _ahum = np.append(_ahum, ah)
    _enthalpy = np.append(_enthalpy, e)
    _dewpoint = np.append(_dewpoint, dp)

    i += 1

#NumpyデータをPandasデータに変換
df["A.hum"] = np.array(_ahum)
df["Enthalpy"] = np.array(_enthalpy)
df["DewPoint"] = np.array(_dewpoint)

#最新Pandasデータを確認
print(df)

fig, ax1 = plt.subplots()

sns.set(style="darkgrid")

"""
sns.set_style("whitegrid", {'grid.linestyle': '--'})
sns.set_context("paper", 1.5, {"lines.linewidth": 4})
sns.set_palette("winter_r", 8, 1)
sns.set('talk', 'whitegrid', 'dark', font_scale=1.5, rc={"lines.linewidth": 2, 'grid.linestyle': '--'})
"""

color1 = 'tab:red'
color2 = 'tab:blue'
ax1.plot(df.iloc[:, [0]], color = color1, label='Temp')
ax1.plot(df.iloc[:, [1]], color = color2, label='R.Hum')
ax1.set_xlabel('Date/Time')
ax1.set_ylabel('Temp&R.Hum')
ax1.set_ylim(0,100)
ax1.grid()

ax2 =ax1.twinx()

color3 = 'tab:Green'
ax2.plot(df.iloc[:, [2]], color = color3, label='A.Hum')
ax2.set_ylabel('A.Hum')
ax2.set_ylim(0,0.01)
ax2.yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))
ax2.ticklabel_format(style='sci',axis='y',scilimits=(0,0))

fig.tight_layout()

handler1, label1 = ax1.get_legend_handles_labels()
handler2, label2 = ax2.get_legend_handles_labels()

ax1.legend(handler1 + handler2, label1 + label2, loc=2, borderaxespad=0.)

ax1.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))

plt.title('Temp&Humidity')
plt.style.use('ggplot') 
plt.show()


