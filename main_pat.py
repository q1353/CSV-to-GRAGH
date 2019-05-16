# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import matplotlib.ticker as ptick
import matplotlib.dates as mdates
#import japanize_matplotlib #macOSでは認識しない...
import seaborn as sns
import glob
import os

from datetime import datetime as dt
from WaterClass import Water
from MoistAirClass import MoistAir
from InstanceAirClass import InstanceAir

#将来暗黙的に登録された日時コンバータをmatplotlibプロット方法に使用する。
#コンバータはインポート時にPandasによって登録されました。
#将来のバージョンのPandasでは明示的にmatplotlibコンバータを登録する必要があります。
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()

#dateディレクトリ内のCSVファイルを表示
FileList = [os.path.basename(r) for r in glob.glob('./data/*.csv')]
for fl in FileList:
    print(fl)

#読み込むCSVファイルの選択と入力
print("上記リストより読み込むcsvファイルをコピペしてください。")
CsvFile = str(input())

#風量AirVolume[m3/hr]の値入力
print("風量[m3/hr]を入力してください。")
AirVolume = int(input())

#補足情報の入力
print("補足情報を入力してください。!!英語入力のみ有効!!　例：Cooling Mode When StartUp EA FAN 20Hz")
ComplementaryInfo = str(input())

#data instance
os.chdir("./data")
df = pd.read_csv(CsvFile)

#NaNの除外 = NaNが含まれると値Float型となってしまうため予め除外しておく
df = df.dropna(how='all')

#df["Date/Time"]を日付型に変換
df["Date/Time"] =  pd.to_datetime(df["Date/Time"])

#int型変換
"""
df['year'] = df['year'] .astype(int)
df['month'] = df['month'] .astype(int)
df['day'] = df['day'] .astype(int)

#int型 ⇒ string型変換
df['year'] = df['year'] .astype(str)
df['month'] = df['month'] .astype(str)
df['day'] = df['day'] .astype(str)

#Date/Time列に年月日時間を結合して日付・時間を代入 & Datetime型に変換
df["Date/Time"] = pd.to_datetime(df['year'] + '-' + df['month'] + '-' + df['day'] + ' ' + df['time'])

#df["Date/Time"]  = pd.to_datetime(df["Date/Time"])
"""

#Date/Time列をインデックスに設定
df = df.set_index("Date/Time")

#year month day time を消去
#df = df.drop(['year','month','day','time'],axis=1)

#最新Pandasデータを確認（頭5行のみ）
#print(df.head())

#PandasデータをNumpyデータに変換
dataframe = df.values
dataframe = dataframe * 0.1

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

#print(state_array)

#dataframeの行数のカウント：時間ごと状態量の数量
y_count = dataframe.shape[0]
#print(y_count)
#dataframeの列数のカウント
x_count = dataframe.shape[1]
#print(x_count)

#state_arrayの要素数カウント
state_array_count = state_array.size
#print(state_array_count)

#時間ごと状態量Arrayの定義 (2次元目)　#初期値=0
t_state_array = np.zeros((y_count,state_array_count))

#print(t_state_array)

i = 0 #カウンタi 初期化 (計算回数)
n = 0 #カウンタt 初期化 (時間ごと状態量Array2次元目配列への連続代入用)
v = 0 #カウンタv 初期化 (_tempデータのカウンタ)
w = 24 #カウンタw 初期化 (_rhumデータのカウンタ)
z = 0 #カウンタz 初期化 (温度、湿度インスタンスごとのカウンタ)

#温度・湿度インスタンスごとの時間毎状態量 Arrayの定義 (3次元目)  #初期値=0
inst_t_state_array = np.zeros((7,y_count,state_array_count))

#各行の温度と相対湿度データを引数として、temporary_array各項目の計算と代入
while z < 7:

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
        instanceair = InstanceAir(_temp , _rhum , AirVolume)

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

    #条件変更
    v += 1
    w += 1
    z += 1

#表示桁数および指数表示の設定
np.set_printoptions(precision=3, suppress=True)
#inst_t_state_arrayの内容確認
#print(inst_t_state_array)

#データ列数のDataFrameカウント初期化
x_count = dataframe.shape[1]

#カウンタの初期化
i = 0
z = 0
s = 0 #各状態量数

#NumpyデータをPandasデータに変換して、Pandas DataFrameへ挿入
while z < 7:

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
        df["Ahum"+str(z)] = np.array(a0)
        df["Enthalpy"+str(z)] = np.array(a1)
        df["DewPoint"+str(z)] = np.array(a2)
        df["SpecificVolume"+str(z)] = np.array(a3)
        df["THCapa"+str(z)] = np.array(a4)
        df["SHCapa"+str(z)] = np.array(a5)
        df["LHCapa"+str(z)] = np.array(a6)
        df["WaterMass"+str(z)] = np.array(a7)

        i += 1

    z += 1


#データ列数の上書き
x_count = df.shape[1]

#交換熱量列の追加
df["PreCoil_TH(kW)"] = abs(df.THCapa1-df.THCapa2)
df["PreCoil_SH(kW)"] = abs(df.SHCapa1-df.SHCapa2)
df["PreCoil_LH(kW)"] = abs(df.LHCapa1-df.LHCapa2)
df["PreCoil_W(L/hr)"] = abs(df.WaterMass1-df.WaterMass2)
df["Coil_TH(kW)"] = abs(df.THCapa2-df.THCapa3)
df["Coil_SH(kW)"] = abs(df.SHCapa2-df.SHCapa3)
df["Coil_LH(kW)"] = abs(df.LHCapa2-df.LHCapa3)
df["Coil_W(kg/h)"] = abs(df.WaterMass2-df.WaterMass3)
df["TCoil_TH(kW)"] = abs(df.THCapa1-df.THCapa3)
df["TCoil_SH(kW)"] = abs(df.SHCapa1-df.SHCapa3)
df["TCoil_LH(kW)"] = abs(df.LHCapa1-df.LHCapa3)
df["TCoil_W(kg/h)"] = abs(df.WaterMass1-df.WaterMass3)

#再熱量列の追加
df["ReHeat_TH(kW)"] = (df.THCapa4-df.THCapa3)
df["ReHeat_SH(kW)"] = (df.SHCapa4-df.SHCapa3)
df["ReHeat_LH(kW)"] = (df.LHCapa4-df.LHCapa3)

#全熱交換器効率
df["SHE(%)"] = (abs(df.SHCapa0-df.SHCapa1) / abs(df.SHCapa0-df.SHCapa5))*100
df["THE(%)"] = (abs(df.THCapa0-df.THCapa1) / abs(df.THCapa0-df.THCapa5))*100

#温度変化
df["oaTemp"] = (df.iloc[:, [0]]) / 10
df["hxTemp"] = (df.iloc[:, [1]]) / 10
df["preTemp"] = (df.iloc[:, [2]]) / 10
df["evaTemp"] = (df.iloc[:, [3]]) / 10
df["condTemp"] = (df.iloc[:, [4]]) / 10
df["tempDiff"] = df.condTemp - df.evaTemp

#最新Pandasデータを確認（頭5行のみ）
#print(df.head())

#最新PndasデータをCSV形式で出力
os.chdir('../result')
df.to_csv('result_' + str(AirVolume) +'m3__' + ComplementaryInfo + '__' + CsvFile)

#グラフ fig インスタンス生成（交換熱量グラフ）
fig_heat = plt.figure(figsize=(14,8))
#グラフ表示数　縦
v_heat = 4
#グラフ表示数　横
h_heat = 1
# グラフ番号（プロット番号）カウント
plotnumber_heat = v_heat * h_heat
#ax_heatオブジェクト保持用list
ax_heat = []

#グラフ fig インスタンス生成（再熱量グラフ）
fig_reheat = plt.figure(figsize=(14,8))
#グラフ表示数　縦
v_reheat = 3
#グラフ表示数　横
h_reheat = 1
# グラフ番号（プロット番号）カウント
plotnumber_reheat = v_reheat * h_reheat
#ax_heatオブジェクト保持用list
ax_reheat = []

#グラフ fig インスタンス生成（全熱交換器効率グラフ）
fig_hxe = plt.figure(figsize=(14,8))
#グラフ表示数　縦
v_hxe = 2
#グラフ表示数　横
h_hxe = 1
# グラフ番号（プロット番号）カウント
plotnumber_hxe = v_hxe * h_hxe
#ax_heatオブジェクト保持用list
ax_hxe = []

#グラフ fig インスタンス生成（温度変化グラフ）
fig_temp = plt.figure(figsize=(14,12))
#グラフ表示数　縦
v_temp = 2
#グラフ表示数　横
h_temp = 1
# グラフ番号（プロット番号）カウント
plotnumber_temp = v_temp * h_temp

#df.index.values で時間列を取得しTimeに代入
Time = df.index.values
Time = pd.to_datetime(Time)
#X軸用array:経過時間の初期化
TimeSpan = []

#dataframeの行数を取得
y_count = len(df)

#カウンタ初期化
i_ts = 0
#X軸用array:経過時間の初設定
for i_ts in range(0, y_count):
    if i_ts == y_count-1:
        TimeSpan = np.append(TimeSpan, TimeSpan[i_ts-1] + DeltaTime)
        break
    elif i_ts == 0:
        TimeSpan = np.append(TimeSpan, 0)
    elif i_ts > 0:
        DeltaTime = Time[i_ts+1] - Time[i_ts]
        DeltaTime = DeltaTime.seconds
        AddTime = TimeSpan[i_ts-1] + DeltaTime
        TimeSpan = np.append(TimeSpan, AddTime)

#seabornデフォルトスタイルを適用
sns.set()

#使用できる色の設定
color = ['tomato', 'royalblue', 'forestgreen', 'darkorange', 'darkviolet','midnightblue']
color10 = 'lightgrey'
color11 = 'white'

#カウンタ初期化
i_h = 1
i_rh = 1
i_hxe = 1
i_temp = 1

#グラフタイトル名の設定
GraghTitle = CsvFile.replace(".csv", "_")
GraghTitle = GraghTitle.replace("input", "_")
GraghTitle = 'result' + GraghTitle + '_' + str(AirVolume) +'m3/h' + '__' + ComplementaryInfo

#交換熱量グラフの描画と書式設定
for i_h in range(1, plotnumber_heat+1): # 1から始まり、plotnunber_heat+1まで処理する
    ax_heat = np.append(ax_heat,fig_heat.add_subplot(v_heat,h_heat,i_h)) # AXESをfig_heatへ追加(v,h)&順序i ⇒ この配列情報ax_heat list型に追加

    ax_heat[i_h-1].plot(df.iloc[:, [i_h+103]], color = color[0], label=df.columns.values[i_h+103])
    ax_heat[i_h-1].set_ylabel(df.columns.values[i_h+103])
    #ax_heat[i_h-1].grid() #seabornデフォルトスタイルを適用時はOFF
    ax_heat[i_h-1].xaxis.set_major_locator(mdates.HourLocator()) #時系列のX軸の（主）間隔設定
    ax_heat[i_h-1].xaxis.set_minor_locator(mdates.MinuteLocator(30)) #時系列のX軸の（副）間隔設定
    ax_heat[i_h-1].yaxis.set_minor_locator(ptick.MultipleLocator(1)) #Y軸の（主）間隔設定
    ax_heat[i_h-1].tick_params(axis='x', which='major')
    ax_heat[i_h-1].grid(which='minor') #小目盛に対してグリッド表示
    ax_heat[i_h-1].set_ylim(0,4)
    ax_heat[i_h-1].set_facecolor(color10)

    #最後のグラフ以外はX軸表記しない
    if i_h < (plotnumber_heat):
        ax_heat[i_h-1].set_xticklabels([])
    #最初のグラフの上左にタイトル表示
    if i_h == 1:
        #グラフタイトルの表示
        ax_heat[i_h-1].set_title(GraghTitle + '_HeatExchange', loc="left", fontsize=15, fontweight='bold')

#再熱量グラフの描画と書式設定
for i_rh in range(1, plotnumber_reheat+1): # 1から始まり、plotnunber_reheat+1まで処理する
    ax_reheat = np.append(ax_reheat,fig_reheat.add_subplot(v_reheat,h_reheat,i_rh)) # AXESをfig_reheatへ追加(v,h)&順序i ⇒ この配列情報ax_reheat list型に追加

    ax_reheat[i_rh-1].plot(df.iloc[:, [i_rh+107]], color = color[0], label=df.columns.values[i_rh+107])
    ax_reheat[i_rh-1].set_ylabel(df.columns.values[i_rh+107])
    #ax_reheat[i_rh-1].grid() #seabornデフォルトスタイルを適用時はOFF
    ax_reheat[i_rh-1].xaxis.set_major_locator(mdates.HourLocator()) #時系列のX軸の（主）間隔設定
    ax_reheat[i_rh-1].xaxis.set_minor_locator(mdates.MinuteLocator(30)) #時系列のX軸の（副）間隔設定
    ax_reheat[i_rh-1].yaxis.set_minor_locator(ptick.MultipleLocator(1)) #Y軸の（主）間隔設定
    ax_reheat[i_rh-1].tick_params(axis='x', which='major')
    ax_reheat[i_rh-1].grid(which='minor') #小目盛に対してグリッド表示
    ax_reheat[i_rh-1].set_ylim(-2,2)
    ax_reheat[i_rh-1].set_facecolor(color10)

    #最後のグラフ以外はX軸表記しない
    if i_rh < (plotnumber_reheat):
        ax_reheat[i_rh-1].set_xticklabels([])
    #最初のグラフの上左にタイトル表示
    if i_rh == 1:
        #グラフタイトルの表示
        ax_reheat[i_rh-1].set_title(GraghTitle + '_ReHeat', loc="left", fontsize=15, fontweight='bold')

#全熱交換器効率グラフの描画と書式設定
for i_hxe in range(1, plotnumber_hxe+1): # 1から始まり、plotnunber_hxeまで処理する
    ax_hxe = np.append(ax_hxe,fig_hxe.add_subplot(v_hxe,h_hxe,i_hxe)) # AXESをfig_hxeへ追加(v,h)&順序i ⇒ この配列情報ax_hxe list型に追加

    ax_hxe[i_hxe-1].plot(df.iloc[:, [i_hxe+110]], color = color[0], label=df.columns.values[i_hxe+110])
    ax_hxe[i_hxe-1].set_ylabel(df.columns.values[i_hxe+110])
    #ax_hxe[i_hxe-1].grid() #seabornデフォルトスタイルを適用時はOFF
    ax_hxe[i_hxe-1].xaxis.set_major_locator(mdates.HourLocator()) #時系列のX軸の（主）間隔設定
    ax_hxe[i_hxe-1].xaxis.set_minor_locator(mdates.MinuteLocator(30)) #時系列のX軸の（副）間隔設定
    ax_hxe[i_hxe-1].yaxis.set_minor_locator(ptick.MultipleLocator(10)) #Y軸の（主）間隔設定
    ax_hxe[i_hxe-1].tick_params(axis='x', which='major')
    ax_hxe[i_hxe-1].grid(which='minor') #小目盛に対してグリッド表示
    ax_hxe[i_hxe-1].set_ylim(0,100)
    ax_hxe[i_hxe-1].set_facecolor(color10)

    #最後のグラフ以外はX軸表記しない
    if i_hxe < (plotnumber_hxe):
        ax_hxe[i_hxe-1].set_xticklabels([])
    #最初のグラフの上左にタイトル表示
    if i_hxe == 1:
        #グラフタイトルの表示
        ax_hxe[i_hxe-1].set_title(GraghTitle + '_HeatExchangeEfficent', loc="left", fontsize=15, fontweight='bold')

#温度変化グラフの描画と書式設定

#第1軸設定
ax_temp = fig_temp.add_subplot(2,1,2)
for i_temp in range (1, 6):
    ax_temp.plot(TimeSpan, df.iloc[:, [i_temp+112]], color = color[i_temp-1], label=df.columns.values[i_temp+112])

ax_diff = fig_temp.add_subplot(2,1,1)
ax_diff.plot(TimeSpan, df.iloc[:,118], color = color[5], label=df.columns.values[118], ls="--")

#ax_tempの書式設定
ax_temp.grid(which='major')
#ax_temp.xaxis.set_major_locator(mdates.HourLocator()) #時系列のX軸の（主）間隔設定
#ax_temp.xaxis.set_minor_locator(mdates.MinuteLocator(30)) #時系列のX軸の（副）間隔設定
ax_temp.yaxis.set_minor_locator(ptick.MultipleLocator(5)) #Y軸の（主）間隔設定
ax_temp.tick_params(axis='x', which='major')
ax_temp.grid(which='minor', ls=":") #小目盛に対してグリッド表示
ax_temp.set_ylim(0,50)
ax_temp.set_ylabel('Temp(C)')
ax_temp.set_facecolor(color10)


#ax_diffの書式設定
ax_diff.grid(which='major')
ax_diff.yaxis.set_minor_locator(ptick.MultipleLocator(5)) #Y軸の（主）間隔設定
ax_diff.tick_params(axis='x', which='major')
ax_diff.grid(which='minor', ls=":") #小目盛に対してグリッド表示
ax_diff.set_ylim(0,50)
ax_diff.set_ylabel('DiffTemp Cond & Eva (C)')
ax_diff.set_facecolor(color10)
ax_diff.set_xticklabels([])
ax_diff.set_title(GraghTitle + '_Temprature', loc="left", fontsize=15, fontweight='bold')

#グラフの背景を透明に。
#ax_temp.patch.set_alpha(0)
#ax_diff.patch.set_alpha(0)

#凡例を表示（グラフ左上、ax2をax1のやや下に持っていく）
ax_temp.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0.5, fontsize=10)
ax_diff.legend(bbox_to_anchor=(0, 1), loc='upper left', borderaxespad=0.5, fontsize=10)

#グラフ下段のみX軸書式設定
ax_heat[i_h-1].set_xlabel('Date/Time')
ax_heat[i_h-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax_reheat[i_rh-1].set_xlabel('Date/Time')
ax_reheat[i_rh-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax_hxe[i_hxe-1].set_xlabel('Date/Time')
ax_hxe[i_hxe-1].xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))

ax_temp.set_xlabel('TimeSpan(Sec)')
#ax_temp.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))


#グラフ位置など自動調整
plt.tight_layout()

#グラフ上の値(x,y)を表示
plt.style.use('ggplot')

#グラフをpng形式で保存 保存先resultディレクトリ
os.chdir('../result')
PngFile = CsvFile.replace(".csv", ".png")
fig_heat.savefig('result_' + str(AirVolume) +'m3__' + ComplementaryInfo + '__heat_' + PngFile, transparent=False, bbox_inches='tight', dpi=400)
fig_reheat.savefig('result_' + str(AirVolume) +'m3__' + ComplementaryInfo + '__reheat_' + PngFile, transparent=False, bbox_inches='tight', dpi=400)
fig_hxe.savefig('result_' + str(AirVolume) +'m3__' + ComplementaryInfo + '__hxe_' + PngFile, transparent=False, bbox_inches='tight', dpi=400)
fig_temp.savefig('result_' + str(AirVolume) +'m3__' + ComplementaryInfo + '__temp_' + PngFile, transparent=False, bbox_inches='tight', dpi=400)

#グラフ表示
plt.show()
