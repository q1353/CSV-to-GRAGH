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

#NaNの除外 = NaNが含まれると値Float型となってしまうため予め除外しておく
df = df.dropna(how='all')

#int型変換
df['year'] = df['year'] .astype(int)
df['month'] = df['month'] .astype(int)
df['day'] = df['day'] .astype(int)

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
#print(df.head())

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

#表示桁数および指数表示の設定
np.set_printoptions(precision=3, suppress=True) 
#inst_t_state_arrayの内容確認
#print(inst_t_state_array)

#カウンタの初期化
i = 0
z = 0
s = 0 #各状態量数

#NumpyデータをPandasデータに変換して、Pandas DataFrameへ挿入
while z < int(x_count/2):
    
    #カウンタの初期化
    i = 0

    while i < int(y_count):

        #3次元データフレームから必要要素の列を抽出し、変数へ代入（各状態量を抽出、格納）
        a0 = inst_t_state_array[z:(z+1),:,0:(0+1)]
        a1 = inst_t_state_array[z:(z+1),:,1:(1+1)]
        a2 = inst_t_state_array[z:(z+1),:,2:(2+1)]
        a3 = inst_t_state_array[z:(z+1),:,3:(3+1)]
        a4 = inst_t_state_array[z:(z+1),:,4:(4+1)]
        a5 = inst_t_state_array[z:(z+1),:,5:(5+1)]
        a6 = inst_t_state_array[z:(z+1),:,6:(6+1)]
        a7 = inst_t_state_array[z:(z+1),:,7:(7+1)]

        #列データを行データに変換
        a0 = a0.transpose((0,2,1))
        a1 = a1.transpose((0,2,1))
        a2 = a2.transpose((0,2,1))
        a3 = a3.transpose((0,2,1))
        a4 = a4.transpose((0,2,1))
        a5 = a5.transpose((0,2,1))
        a6 = a6.transpose((0,2,1))
        a7 = a7.transpose((0,2,1))
        
        #3次元データフレームを1次元データフレームへ変換
        a0 = a0.flatten()
        a1 = a1.flatten()
        a2 = a2.flatten()
        a3 = a3.flatten()
        a4 = a4.flatten()
        a5 = a5.flatten()
        a6 = a6.flatten()
        a7 = a7.flatten()
        
        #pandas DataFlame df にNumpyData inst_t_state_arrayデータ抽出し代入
        df["A.hum"+str(z)] = np.array(a0)
        df["Enthalpy"+str(z)] = np.array(a1)
        df["DewPoint"+str(z)] = np.array(a2)
        df["SpecificVolume"+str(z)] = np.array(a3)
        df["THCapa"+str(z)] = np.array(a4)
        df["SHCapa"+str(z)] = np.array(a5)
        df["LHCapa"+str(z)] = np.array(a6)
        df["WaterMass"+str(z)] = np.array(a7)

        i += 1

    z += 1

#交換熱量列の追加
df["d-TH_0-1"] = df.THCapa0-df.THCapa1
df["d-SH_0-1"] = df.SHCapa0-df.SHCapa1
df["d-LH_0-1"] = df.LHCapa0-df.LHCapa1
df["d-W_0-1"] = df.WaterMass0-df.WaterMass1
df["d-TH_1-2"] = df.THCapa1-df.THCapa2
df["d-SH_1-2"] = df.SHCapa1-df.SHCapa2
df["d-LH_1-2"] = df.LHCapa1-df.LHCapa2
df["d-W_1-2"] = df.WaterMass1-df.WaterMass2


#最新Pandasデータを確認（頭5行のみ）
print(df.head())

#最新PndasデータをCSV形式で出力
#df.to_csv("sample.csv")

#グラフ fig インスタンス生成（状態量グラフ）
fig_state = plt.figure(figsize=(15,12))
#グラフ表示数　縦
v_state = 2
#グラフ表示数　横
h_state = 3
# グラフ番号（プロット番号）カウント
plotnumber_state = v_state * h_state
#ax_heatオブジェクト保持用list
ax_state = []

#グラフ fig インスタンス生成（交換熱量グラフ）
fig_heat = plt.figure(figsize=(15,13))
#グラフ表示数　縦
v_heat = 8
#グラフ表示数　横
h_heat = 1
# グラフ番号（プロット番号）カウント
plotnumber_heat = v_heat * h_heat
#ax_heatオブジェクト保持用list
ax_heat = []

#seabornデフォルトスタイルを適用
sns.set()

#全体共通書式設定
"""
#y軸の文字サイズ変更
plt.tick_params(axis='y', which='major', labelsize=10)
#x軸の文字サイズ変更
plt.tick_params(axis='x', which='major', labelsize=10)
"""

#使用できる色の設定
color1 = 'tab:red'
color2 = 'tab:blue'
color3 = 'tab:Green'

#カウンタ初期化
i_s = 1

#状態量グラフの描画と書式設定
for i_s in range(1, plotnumber_state+1): # 1から始まり、plotnunber_state+1まで処理する
    ax_state = np.append(ax_state,fig_state.add_subplot(v_state,h_state,i_s)) # AXESをfig_stateへ追加(v,h)&順序i ⇒ この配列情報_state list型に追加
            
    ax_state[i_s-1].plot(df.iloc[:, [i_s-1]], color = color1, label=df.columns.values[i_s-1])
    ax_state[i_s-1].set_xlabel('Date/Time')
    ax_state[i_s-1].set_ylabel(df.columns.values[i_s-1])
    #ax_state[i_s-1].grid() #seabornデフォルトスタイルを適用時はOFF
    ax_state[i_s-1].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
    #ax_state[i_s-1].xaxis.set_major_locator(mdates.DayLocator()) #時系列のX軸の間隔設定

    
#カウンタ初期化
i_h = 1

#交換熱量等　状態量差分グラフの描画と書式設定
for i_h in range(1, plotnumber_heat+1): # 1から始まり、plotnunber_heat+1まで処理する
    ax_heat = np.append(ax_heat,fig_heat.add_subplot(v_heat,h_heat,i_h)) # AXESをfig_stateへ追加(v,h)&順序i ⇒ この配列情報ax_heat list型に追加
            
    ax_heat[i_h-1].plot(df.iloc[:, [i_h+29]], color = color1, label=df.columns.values[i_h+29])
    
    ax_heat[i_h-1].set_ylabel(df.columns.values[i_h+29])
    #ax_heat[i_h-1].grid() #seabornデフォルトスタイルを適用時はOFF 
    #ax_heat[i_h-1].xaxis.set_major_locator(mdates.DayLocator()) #時系列のX軸の間隔設定
    ax_heat[i_h-1].tick_params(axis='x', which='major')
    ax_heat[i_h-1].set_xticklabels([]) 


#交換熱量等　状態量差分グラフの描画と書式設定　（特定部分のみ）    
ax_heat[7].xaxis.set_major_formatter(mdates.DateFormatter("%m/%d\n%H:%M"))
ax_heat[7].set_xlabel('Date/Time')


#特定箇所の書式設定
"""
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
"""
#凡例表示の設定
handler1, label1 = ax1.get_legend_handles_labels()
handler2, label2 = ax2.get_legend_handles_labels()

ax1.legend(handler1 + handler2, label1 + label2, loc=2, borderaxespad=0.)
"""

#グラフ位置など自動調整
plt.tight_layout()
fig_state.tight_layout()
fig_heat.tight_layout()
#グラフ上の値(x,y)を表示
#plt.style.use('ggplot') 
#グラフ表示
plt.show()
