# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from WaterClass import Water
from MoistAirClass import MoistAir
from InstanceAirClass import InstanceAir


a = 26
b = 50
c = 100

#InstanceAirClass インスンタンス化 
instanceair = InstanceAir(a,b,c)

#絶対湿度の計算[kg/kg]

TH = instanceair.GetTotalHeatCapacity()
print (TH)

SH = instanceair.GetSensitiveHeatCapacity()
print (SH)

LH = instanceair.GetLatentHeatCapacity()
print (LH)

W = instanceair.GetWaterMass()
print(W)

#以上デバック完了　2019/2/5
