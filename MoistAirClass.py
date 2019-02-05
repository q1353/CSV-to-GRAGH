import numpy as np
from WaterClass import Water

class MoistAir():
    # 絶対温度と摂氏との変換定数
    CONVERT_C_TO_K = 273.15

    # 乾き空気の定圧比熱[kJ/kg-K]
    DRYAIR_ISOBARIC_SPECIFIC_HEAT = 1.006

    # 水蒸気の定圧比熱[kJ/kg-K]
    VAPOR_ISOBARIC_SPECIFIC_HEAT = 1.805

    # 0℃の水の定圧比熱[kJ/kg-K]
    WATER_ISOBARIC_SPECIFIC_HEAT = 4.186

    # 0℃の水の蒸発潜熱[kJ/kg]
    VAPORIZATION_LATENT_HEAT = 2501

    # 海抜0mでの大気圧=101.325[kPa]
    ATMOSPHERIC_PRESSURE_AT_SEALEVEL = 101.325

    # 乾き空気のガス定数[kJ/(kg K)]
    DRYAIR_GAS_CONSTANT = 0.287055

    #<summary>コンストラクタ</summa
    #<param name="dryBulbTemperature">乾球温度[℃]</param>
    #<param name="wetBulbTemperature">湿球温度[℃]</param>
    #<param name="atmosphericPressure">大気圧[kPa]：1気圧は101.325[kPa]</param>
    #<returns>絶対湿度[kg/kg]</returns>
    #乾球温度と湿球温度から絶対湿度求める。


    def __init__(self, dryBulbTemperature = 24, relativeHumidity = 45):
        #self.AtmosphericPressure = atmosphericPressure
        self.DryBulbTemperature = dryBulbTemperature
        self.RelativeHumidity = relativeHumidity
        #self.HumidityRatio = MoistAir.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity(dryBulbTemperature, relativeHumidity, MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL)
        #self.RelativeHumidity = MoistAir.GetRelativeHumidityFromDryBulbTemperatureAndHumidityRatio(dryBulbTemperature, humidityRatio, MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL)
        #self.Enthalpy = MoistAir.GetEnthalpyFromDryBulbTemperatureAndHumidityRatio(drybulbTemperature, humidityRatio)
        #self.WetbulbTemperature = MoistAir.GetWetBulbTemperatureFromDryBulbTemperatureAndHumidityRatio(dryBulbTemperature, humidityRatio, MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL)
        #self.SpecificVolume = MoistAir.GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio(dryBulbTemperature, humidityRatio, MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL) 
    
    #デストラクタ 
    def __del__(self):
        pass

    #<summary>乾球温度[℃]と湿球温度[℃]から絶対湿度[kg/kg]を求める</summa
    #<param name="dryBulbTemperature">乾球温度[℃]</param>
    #<param name="wetBulbTemperature">湿球温度[℃]</param>
    #<param name="atmosphericPressure">大気圧[kPa]：1気圧は101.325[kPa]</param>
    #<returns>絶対湿度[kg/kg]</returns>
    #乾球温度と湿球温度から絶対湿度求める。

    #def GetHumidityRatioFromDryBulbTemperatureAndWetBulbTemperature(DryBulbTemperature, WetBulbTemperature, AtmosphericPressure):
        #ps = Water.GetSaturationPressure(WetBulbTemperature)
        #ws = GetHumidityRatioFromWaterVaporPartialPressure(ps, AtmosphericPressure)
        #a = ws * (MoistAir.VAPORIZATION_LATENT_HEAT + (MoistAir.VAPOR_ISOBARIC_SPECIFIC_HEAT - MoitAir.WATER_ISOBARIC_SPECIFIC_HEAT)* WetBulbTemperature)
        #+ MoistAir.DRYAIR_ISOBARIC_SPECIFIC_HEAT * (WetBulbTemperature - DryBulbTemperature)

        #b = MoistAir.VAPORIZATION_LATENT_HEAT + MoistAir.VAPOR_ISOBARIC_SPECIFIC_HEAT * DryBulbTemperature - MoistAir.WATER_ISOBARIC_SPECIFIC_HEAT * WetBulbTemperature
        #return a / b

    #<summary>水蒸気分圧[kPa]と大気圧[kPa]から絶対湿度[kg/kg]を求める</summary>
    #<param name="waterVaporPartialPressure">水蒸気分圧[kPa]</param>
    #<param name="atmosphericPressure">大気圧[kPa]：1気圧は101.325[kPa]</param>
    #<returns>絶対湿度[kg/kg]</returns>

    def GetHumidityRatioFromWaterVaporPartialPressure(WaterVaporPartialPressure):
        AtmosphericPressure = MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL 
        return 0.62198 * WaterVaporPartialPressure / (AtmosphericPressure - WaterVaporPartialPressure)
        
    #<summary>絶対湿度[kg/kg]と大気圧[kPa]から水蒸気分圧[kPa]を求める</summary>
    #<param name="humidityRatio">絶対湿度[kg/kg]</param>
    #<param name="atmosphericPressure">大気圧[kPa]：1気圧は101.325[kPa]</param>
    #<returns>水蒸気分圧[kPa]</returns>

    def GetWaterVaporPartialPressureFromHumidityRatio(HumidityRatio):
        AtmosphericPressure = MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL
        return AtmosphericPressure * HumidityRatio / (0.62198 + HumidityRatio)

    #<summary>乾球温度[C]と相対湿度[%]から絶対湿度[kg/kg]を求める</summary>
    #<param name="dryBulbTemperature">乾球温度[C]</param>
    #<param name="relativeHumidity">相対湿度[%]</param>
    #<param name="atmosphericPressure">大気圧[kPa]</param>
    #<returns>絶対湿度[kg/kg]</returns>

    def GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity(self):
        AtmosphericPressure = MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL
        #飽和水蒸気分圧[kPa]の計算
        ps = Water.GetSaturationPressure(self.DryBulbTemperature)
        #水蒸気分圧[kPa]の計算
        pw = 0.01 * self.RelativeHumidity * ps
        return MoistAir.GetHumidityRatioFromWaterVaporPartialPressure(pw)
 
    # <summary>絶対湿度[kg/kg]と相対湿度[%]からエンタルピー[kJ/kg]を求める</summary>
    # <param name="humidityRatio">絶対湿度[kg/kg]</param>
    # <param name="relativeHumidity">相対湿度[%]</param>
    # <param name="atmosphericPressure">大気圧[kPa]</param>

    def GetEnthalpyFromHumidityRatioAndRelativeHumidity(self):
        AtmosphericPressure = MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL
        #乾球温度[℃]と相対湿度[%]から絶対湿度[kg/kg]を求める
        hrt = MoistAir.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity(self)
        #水蒸気分圧[kPa]の計算
        return MoistAir.GetEnthalpyFromDryBulbTemperatureAndHumidityRatio(self, hrt)

    # <summary>乾球温度[℃]と絶対湿度[kg/kg]からエンタルピー[kJ/kg]を求める</summary>
    # <param name="dryBulbTemperature">乾球温度[℃]</param>
    # <param name="humidityRatio">絶対湿度[kg/kg]</param>
    # <returns>エンタルピー[kJ/kg]</returns>
    def GetEnthalpyFromDryBulbTemperatureAndHumidityRatio(self, HumidityRatio):
        return MoistAir.DRYAIR_ISOBARIC_SPECIFIC_HEAT * self.DryBulbTemperature + HumidityRatio * (MoistAir.VAPOR_ISOBARIC_SPECIFIC_HEAT * self.DryBulbTemperature + MoistAir.VAPORIZATION_LATENT_HEAT)
 
    # <summary>乾球温度[C]および相対湿度[kg/kg]から比体積[m3/kg]を求める</summary>
    # <param name="dryBulbTemperature">乾球温度[C]</param>
    # <param name="relativeHumidity">相対湿度[%]</param>
    # <param name="humidityRatio">絶対湿度[kg/kg]</param>
    # <param name="atmosphericPressure">大気圧[kPa]</param>
    # <returns>比体積[m3/kg]</returns>
    def GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio(self):
        AtmosphericPressure = MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL
        hrt = MoistAir.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity(self)
        return ((self.DryBulbTemperature + MoistAir.CONVERT_C_TO_K) * MoistAir.DRYAIR_GAS_CONSTANT) / AtmosphericPressure * (1.0 + 1.6078 * hrt)
    
    # <summary>乾球温度[C]および相対湿度[kg/kg]から飽和乾球温度（露点温度）[℃]を求める</summary>
    # <param name="humidityRatio">絶対湿度[kg/kg]</param>
    # <param name="atmosphericPressure">大気圧[kPa]</param>
    # <returns>飽和乾球温度（露点温度）[℃]</returns>
    def GetSaturationDryBulbTemperatureFromHumidityRatio(self):
        AtmosphericPressure = MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL
        hrt = MoistAir.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity(self)
        ps = MoistAir.GetWaterVaporPartialPressureFromHumidityRatio(hrt)
        return Water.GetSaturationTemperature(ps)
    
    # <summary>標高[m]に応じた大気圧[kPa]を取得する</summary>
    # <param name="altitude">標高[m]</param>
    # <returns>大気圧[kPa]</returns>
    def GetAtmosphericPressure(self, altitude):
        return MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL * np.power(1.0 - 2.25577*10**-5 * altitude, 5.2559)

    # <summary>湿り空気比熱[kJ/kg-K]を計算する</summary>
    # <param name="humidityRatio">絶対湿度[kg/kg(DA)]</param>
    # <returns>湿り空気比熱[kJ/kg-K]</returns>
    def GetSpecificHeat (self):
        hrt = MoistAir.GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity(self)
        return MoistAir.DRYAIR_ISOBARIC_SPECIFIC_HEAT + MoistAir.VAPOR_ISOBARIC_SPECIFIC_HEAT * hrt

    # <summary>粘性係数[Pa s]を計算する</summary>
    # <param name="drybulbTemperature">乾球温度[C]</param>
    # <returns>粘性係数[Pa s]</returns>
    def GetViscosity(self):
        return (0.0074237 / (self.DryBulbTemperature + 390.15))* np.power((self.DryBulbTemperature + MoistAir.CONVERT_C_TO_K) / 293.15, 1.5)

    # <summary>動粘性係数[m2/s]を計算する</summary>
    # <param name="drybulbTemperature">乾球温度[C]</param>
    # <param name="humidityRatio">絶対湿度[kg/kg]</param>
    # <param name="atmosphericPressure">大気圧[kPa]</param>
    # <returns>動粘性係数[m2/s]</returns>
    def GetDynamicViscosity(self):
        AtmosphericPressure = MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL
        return MoistAir.GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio(self) * MoistAir.GetViscosity(self)


    # <summary>熱伝導率[W/(mK)]を計算する</summary>
    # <param name="drybulbTemperature">乾球温度[C]</param>
    # <returns>熱伝導率[W/(mK)]</returns>
    def GetThermalConductivity(self):
        return 0.0241 + 0.000077 * self.DryBulbTemperature

    # <summary>膨張率[1/K]を計算する</summary>
    # <param name="drybulbTemperature">乾球温度[C]</param>
    # <returns>膨張率[1/K]</returns>
    def GetExpansionCoefficient(self):
        return 1 / (self.DryBulbTemperature + MoistAir.CONVERT_C_TO_K)

    # <summary>熱拡散率[m2/s]を計算する</summary>
    # <param name="drybulbTemperature">乾球温度[C]</param>
    # <param name="humidityRatio">絶対湿度[kg/kg]</param>
    # <param name="atmosphericPressure">大気圧[kPa]</param>
    # <returns>熱拡散率[m2/s]</returns>
    def GetThermalDiffusivity (self):
        AtmosphericPressure = MoistAir.ATMOSPHERIC_PRESSURE_AT_SEALEVEL
        lam = MoistAir.GetThermalConductivity(self)
        cp = MoistAir.GetSpecificHeat(self)
        sv = MoistAir.GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio(self)
        return (lam * sv ) / (1000 * cp )
