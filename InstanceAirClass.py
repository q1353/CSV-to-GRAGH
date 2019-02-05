from MoistAirClass import MoistAir

# MoistAirClassを継承したInstanceAirClassの作成 
class InstanceAir(MoistAir):

    # 乾球温度 = dryBulbTemperature[C]
    # 相対湿度 = relativeHumidity[%]
    # 風量 = airVolume[m3/hr]
   
    def __init__(self, dryBulbTemperature = 25, relativeHumidity = 55, airVolume = 100):
        super().__init__(dryBulbTemperature, relativeHumidity)
        self.AirVolume = airVolume
        # 風量 = AirMass [kg/hr]
        self.AirMass = self.AirVolume / super().GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio()

    # 全熱[kW = kJ/sec]の取得メソッド
    def GetTotalHeatCapacity(self):
        en = super().GetEnthalpyFromHumidityRatioAndRelativeHumidity()
        sv = super().GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio()
        return self.AirMass * en / 3600
    
    # 顕熱[kW = kJ/sec]の取得メソッド    
    def GetSensitiveHeatCapacity(self):
        sh = super().GetSpecificHeat()
        sv = super().GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio()
        return self.AirMass * sh * self.DryBulbTemperature / 3600
    
    # 潜熱[kW = kJ/sec]の取得メソッド
    def GetLatentHeatCapacity(self):
        return InstanceAir.GetTotalHeatCapacity(self) - InstanceAir.GetSensitiveHeatCapacity(self)

    # 空気中の水分量[kg/hr]の取得メソッド
    def GetWaterMass(self):
        hrt = super().GetHumidityRatioFromDryBulbTemperatureAndRelativeHumidity()
        sv = super().GetSpecificVolumeFromDryBulbTemperatureAndHumidityRatio()
        return hrt * self.AirMass





