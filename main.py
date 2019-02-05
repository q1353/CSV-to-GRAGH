# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import math
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
_specificvolume = np.array([]) #比容積Array初期化

#各行の温度と相対湿度データを引数として、絶対湿度＆エンタルピーを計算
while i < count:
    _temp=dataframe[i,0]
    _rhum=dataframe[i,1]

    #MoistAir Classのインスタンス化
    moistair = MoistAir(_temp , _rhum)

    ah = moistair.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity()
    e = moistair.GetEnthalpyFromHumidityRatioAndRelativeHumidity()
    dp = moistair.GetSaturationDryBulbTemperatureFromHumidityRatio()
    sv = moistair.GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio()
    
    #_ahum空Arrayにahデータを後ろから追記
    _ahum = np.append(_ahum, ah)
    _enthalpy = np.append(_enthalpy, e)
    _dewpoint = np.append(_dewpoint, dp)
    _specificvolume = np.append(_specificvolume, sv)

    i += 1

#NumpyデータをPandasデータに変換して、Pandas DataFrameへ挿入
df["A.hum"] = np.array(_ahum)
df["Enthalpy"] = np.array(_enthalpy)
df["DewPoint"] = np.array(_dewpoint)
df["SpecificVolume"] = np.array(_specificvolume)

#最新Pandasデータを確認（頭5行のみ）
print(df.head())

#グラフ表示数　縦
v = 2
#グラフ表示数　横
h = 3

 # グラフ番号（プロット番号）カウント
plotnumber = v * h

#axオブジェクト保持用Numpy array
ax = []

#グラフ fig インスタンス生成
fig = plt.figure(figsize=(15,12))

#seabornデフォルトスタイルを適用
sns.set()

#使用できる色の設定
color1 = 'tab:red'
color2 = 'tab:blue'
color3 = 'tab:Green'

for i in range(1, plotnumber+1): # 1から始まり、plotnunber+1まで処理する
    ax = np.append(ax,fig.add_subplot(v,h,i)) # AXESをfigへ追加(v,h)&順序i ⇒ この配列情報ax arrayに追加
            
    ax[i-1].plot(df.iloc[:, [i-1]], color = color1, label=df.columns.values[i-1])
    ax[i-1].set_xlabel('Date/Time')
    ax[i-1].set_ylabel(df.columns.values[i-1])
    #ax[i-1].grid() #seabornデフォルトスタイルを適用時はOFF
    ax[i-1].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
    #ax[i-1].xaxis.set_major_locator(mdates.DayLocator()) #時系列のX軸の間隔設定
    # y軸の文字サイズ変更
    #plt.tick_params(axis='y', which='major', labelsize=10)
    # x軸の文字サイズ変更
    plt.tick_params(axis='x', which='major', labelsize=10)

#各グラフのylim書式設定
ax[0].set_ylim(0,100)
ax[1].set_ylim(0,100)
ax[2].set_ylim(0,0.01)
ax[3].set_ylim(0,100)
ax[4].set_ylim(0,20)
ax[5].set_ylim(0,1)

# y軸を指数表記する
ax[2].yaxis.set_major_formatter(ptick.ScalarFormatter(useMathText=True))

"""
#凡例表示の設定
handler1, label1 = ax1.get_legend_handles_labels()
handler2, label2 = ax2.get_legend_handles_labels()

ax1.legend(handler1 + handler2, label1 + label2, loc=2, borderaxespad=0.)
"""

#グラフ位置など自動調整
plt.tight_layout()
fig.tight_layout()
#グラフ上の値(x,y)を表示
#plt.style.use('ggplot') 
#グラフ表示
plt.show()


