# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from WaterClass import Water
from MoistAirClass import MoistAir

a = 10
b = 55

#MoistAirClass インスンタンス化 
"""
MoistAir = MoistAir(a,b)

#絶対湿度の計算[kg/kg]
humidityratio = MoistAir.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity()
print(humidityratio)
#比エンタルピーの計算[kJ/kg]
enthalpy = MoistAir.GetEnthalpyFromHumidityRatioAndRelativeHumidity()
print(enthalpy)
#比容積の計算[m3/kg]
specificvolume = MoistAir.GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio()
print(specificvolume)
#露点温度の計算[℃DP]
dewpoint = MoistAir.GetSaturationDryBulbTemperatureFromHumidityRatio()
print(dewpoint)
#大気圧[kPa]の計算/引数altitude[m]
altitude = 100
atompressure = MoistAir.GetAtmosphericPressure(altitude)
print(atompressure)
#比熱の計算 引数altitude[m]
specificheat = MoistAir.GetSpecificHeat()
print(specificheat)
#粘性係数[Pa s]を計算
viscoucity = MoistAir.GetViscosity()
print(viscoucity)
#動粘性係数[m2/s]を計算する
dynamicviscosity = MoistAir.GetDynamicViscosity()
print(dynamicviscosity)
#熱伝導率[W/(mK)]を計算する
conductivity = MoistAir.GetThermalConductivity()
print(conductivity)
#膨張率[1/K]を計算する
expansioncoefficient = MoistAir.GetExpansionCoefficient()
print(expansioncoefficient)
#熱拡散率[m2/s]を計算する
thermaldiffusivity = MoistAir.GetThermalDiffusivity()
print(thermaldiffusivity)
#以上デバック完了　2019/2/1
"""