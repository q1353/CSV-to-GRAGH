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
from InstanceAirClass import InstanceAir

#data instance
df = pd.read_csv('test_2.csv')

#int型 ⇒ string型変換
df['year'] = df['year'] .astype(str)
df['month'] = df['month'] .astype(str)
df['day'] = df['day'] .astype(str)

#Date/Time列に年月日時間を結合して日付・時間を代入 & Datetime型に変換
df["Date/Time"] = pd.to_datetime(df['year'] + '-' + df['month'] + '-' + df['day'] + ' ' + df['time'])

#Date/Time列をインデックスに設定
df = df.set_index("Date/Time")

#year month day time を消去
df = df.drop(['year','month','day','time'],axis=1)

#最新Pandasデータを確認（頭5行のみ）
print(df.head())

#PandasデータをNumpyデータに変換
dataframe = df.values

count = dataframe.shape[0] #データ行数のカウント：境界条件設定

#状態量保存用Arrayの定義 (1次元目)
state_array =  np.zeros(8)

#初期値=0
#temporary_array [0]:絶対湿度Array
#temporary_array [1]:エンタルピーArray
#temporary_array [2]:露点温度Array
#temporary_array [3]:比容積Array
#temporary_array [4]:全熱量Array
#temporary_array [5]:顕熱量Array
#temporary_array [6]:潜熱量Array
#temporary_array [7]:水分量Array

print(state_array)

#dataframeの行数のカウント：時間ごと状態量の数量
y_count = dataframe.shape[0]
print(y_count)
#dataframeの列数のカウント
x_count = dataframe.shape[1]
print(x_count)

#state_arrayの要素数カウント
state_array_count = state_array.size
print(state_array_count)

#時間ごと状態量Arrayの定義 (2次元目)　#初期値=0
t_state_array = np.zeros((y_count,state_array_count))

#print(t_state_array)

i = 0 #カウンタi 初期化 (計算回数)
n = 0 #カウンタt 初期化 (時間ごと状態量Array2次元目配列への連続代入用)
v = 0 #カウンタv 初期化 (_tempデータのカウンタ)
w = 1 #カウンタw 初期化 (_rhumデータのカウンタ)
z = 0 #カウンタz 初期化 (温度、湿度インスタンスごとのカウンタ)

#温度・湿度インスタンスごとの時間毎状態量 Arrayの定義 (3次元目)  #初期値=0
inst_t_state_array = np.zeros((int(x_count/2),y_count,state_array_count))

#風量airvolume[m3/hr]の初期化
airvolume = 250

#各行の温度と相対湿度データを引数として、temporary_array各項目の計算と代入
while z < int(x_count/2):

    #カウンタの初期化
    i = 0
    n = 0
       
    while i < y_count:
        _temp = dataframe[i,v]
        _rhum = dataframe[i,w]

        #MoistAir Classのインスタンス化
        moistair = MoistAir(_temp , _rhum)

        #各状態量の計算
        ah = moistair.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity()
        e = moistair.GetEnthalpyFromHumidityRatioAndRelativeHumidity()
        dp = moistair.GetSaturationDryBulbTemperatureFromHumidityRatio()
        sv = moistair.GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio()

        #InstantceAir Classのインスタンス化
        instanceair = InstanceAir(_temp , _rhum , airvolume)

        #各状態量の計算
        TH = instanceair.GetTotalHeatCapacity()
        SH = instanceair.GetSensitiveHeatCapacity()
        LH = instanceair.GetLatentHeatCapacity()
        W = instanceair.GetWaterMass()

        #state_array(1次元)への代入
        state_array[0] = ah
        state_array[1] = e
        state_array[2] = dp
        state_array[3] = sv
        state_array[4] = TH
        state_array[5] = SH
        state_array[6] = LH
        state_array[7] = W
        
        #inst_t_state_arrayの各要素へ状態量代入
        for n in  range(0,int(state_array_count)):

           inst_t_state_array[z,i,n] =  state_array[n]
           
           n += 1

        i += 1

    print(z) 
    #条件変更
    v += 2
    w += 2
    z += 1

np.set_printoptions(precision=3, suppress=True) 
print(inst_t_state_array)

#カウンタの初期化
i = 0
z = 0

#a= inst_t_state_array[z:(z+1),:,0:(i+1)]
#print(a)
#NumpyデータをPandasデータに変換して、Pandas DataFrameへ挿入
while z < int(x_count/2):
    
    #カウンタの初期化
    i = 0

    while i < int(y_count):

        a1 = inst_t_state_array[z:(z+1),:,0:(0+1)]
        a2 = inst_t_state_array[z:(z+1),:,1:(1+1)]
        a3 = inst_t_state_array[z:(z+1),:,2:(2+1)]
        a4 = inst_t_state_array[z:(z+1),:,3:(3+1)]
        a5 = inst_t_state_array[z:(z+1),:,4:(4+1)]
        a6 = inst_t_state_array[z:(z+1),:,5:(5+1)]
        a7 = inst_t_state_array[z:(z+1),:,6:(6+1)]
        a8 = inst_t_state_array[z:(z+1),:,7:(7+1)]

        a1 = a1.transpose((0,2,1))
        a2 = a2.transpose()
        a3 = a3.transpose()
        a4 = a4.transpose()
        a5 = a5.transpose()
        a6 = a6.transpose()
        a7 = a7.transpose()
        a8 = a8.transpose()
 
        print(a1)
        print(a2)
        print(a3)
        
        df["A.hum"] = np.array(a1)
        df["Enthalpy"] = np.array(a2)
        df["DewPoint"] = np.array(a3)
        df["SpecificVolume"] = np.array(a4)
        df["THCap"] = np.array(a5)
        df["SHCapa"] = np.array(a6)
        df["LHCapa"] = np.array(a7)
        df["Water"] = np.array(a8)

        i += 1

    z += 1

#最新Pandasデータを確認（頭5行のみ）
print(df)

#df.to_csv("sample.csv")


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
