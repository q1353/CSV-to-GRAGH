import numpy as np

class Water:
    #region 定数宣言

    # <summary>絶対温度と摂氏との変換定数</summary>
    CONVERT_C_TO_K = 273.15

    # <summary>臨界点での比エンタルピー[kJ/kg]</summary>
    TEMPERATURE_AT_CRITICAL_POINT = 647.096

    # <summary>臨界点での比エンタルピー[kJ/kg]</summary>
    ENTHALPY_AT_CRITICAL_POINT = 2099.3

    # <summary>臨界点での比体積[m3/kg]</summary>
    SPECIFIC_VOLUME_AT_CRITICAL_POINT = 0.003155

    # <summary>臨界点での比エントロピー[kJ/kgK]</summary>
    ENTROPY_AT_CRITICAL_POINT = 4.4289

    # <summary>臨界点での飽和水蒸気圧[kPa]</summary>
    PRESSURE_AT_CRITICAL_POINT = 22089

    # <summary>三重点での蒸発潜熱[kJ/kg]</summary>
    VAPORIZATION_HEAT_AT_TRIPLE_POINT = 2500.9

    #endregion

    #region privateメソッド

    # <summary>臨界温度からの離れを求める</summary>
    # <param name="saturationTemperature">飽和温度[C]</param>
    # <returns>臨界温度からの離れ</returns>
    def __TR(saturationTemperature):

        return (Water.TEMPERATURE_AT_CRITICAL_POINT - (saturationTemperature + Water.CONVERT_C_TO_K)) / Water.TEMPERATURE_AT_CRITICAL_POINT
   
    #endregion

    #region 飽和水蒸気圧と飽和温度の計算

    # <summary>飽和温度[℃]から飽和水蒸気圧[kPa]を求める</summary>
    # <param name="saturationTemperature">飽和温度[℃]</param>
    # <returns>飽和水蒸気圧[kPa]</returns>
    def GetSaturationPressure(saturationTemperature):
    
        P_CONVERT = 0.001

        C1 = -5.6745359 * 10 ** 3
        C2 = 6.3925247
        C3 = -9.6778430 * 10 ** -3
        C4 = 6.2215701 * 10 ** -7
        C5 = 2.0747825 * 10 ** -9
        C6 = -9.4840240 * 10 ** -13
        C7 = 4.1635019

        N1 = 0.11670521452767 * 10 ** 4
        N2 = -0.72421316703206 * 10 ** 6
        N3 = -0.17073846940092 * 10 ** 2
        N4 = 0.12020824702470 * 10 ** 5
        N5 = -0.32325550322333 * 10 ** 7
        N6 = 0.14915108613530 * 10 ** 2
        N7 = -0.4823265731591 * 10 ** 4
        N8 = 0.40511340542057 * 10 ** 6
        N9 = -0.23855557567849 * 10 ** 0
        N10 = 0.65017534844798 * 10 ** 3

        ts = saturationTemperature + Water.CONVERT_C_TO_K

        # -100~0.01C#三重点以下はwexler-hylanの式
        if (saturationTemperature < 0.01):
            return np.exp(C1 / ts + C2 + C3 * ts + C4 * np.power(ts, 2) + C5 * np.power(ts, 3) + C6 * np.power(ts, 4) + C7 * np.log(ts)) * P_CONVERT
        # ~647.096K#臨界温度まではIAPWS-IF97実用国際状態式
        else:
            alpha = ts + N9 / (ts - N10)
            a2 = alpha * alpha
            A = a2 + N1 * alpha + N2
            B = N3 * a2 + N4 * alpha + N5
            C = N6 * a2 + N7 * alpha + N8
            return np.power(2 * C / (-B + np.power(B * B - 4 * A * C, 0.5)), 4) / P_CONVERT

    # <summary>飽和水蒸気圧[kPa]から飽和温度[C]を求める</summary>
    # <param name="saturationPressure">飽和水蒸気圧[kPa]</param>
    # <returns>飽和温度[C]</returns>
    def GetSaturationTemperature(saturationPressure):
        P_CONVERT = 0.001

        D1 = -6.0662 * 10 ** 1
        D2 = 7.4624 * 10 ** 0
        D3 = 2.0594 * 10 ** -1
        D4 = 1.6321 * 10 ** -2

        N1 = 0.11670521452767 * 10 ** 4
        N2 = -0.72421316703206 * 10 ** 6
        N3 = -0.17073846940092 * 10 ** 2
        N4 = 0.12020824702470 * 10 ** 5
        N5 = -0.32325550322333 * 10 ** 7
        N6 = 0.14915108613530 * 10 ** 2
        N7 = -0.4823265731591 * 10 ** 4
        N8 = 0.40511340542057 * 10 ** 6
        N9 = -0.23855557567849 * 10 ** 0
        N10 = 0.65017534844798 * 10 ** 3

        # ~0C#wexler-hylanの計算値を近似した式
        if (saturationPressure < 0.611213):
            y = np.log(saturationPressure / P_CONVERT)
            return D1 + y * (D2 + y * (D3 + y * D4))
       
        # 0C~#臨界圧力まではIAPWS-IF97実用国際状態式
        else:
            ps = saturationPressure * P_CONVERT
            beta = np.power(ps, 0.25)
            b2 = beta * beta
            E = b2 + N3 * beta + N6
            F = N1 * b2 + N4 * beta + N7
            G = N2 * b2 + N5 * beta + N8
            D = 2 * G / (-F - np.power(F * F - 4 * E * G, 0.5))
            return (N10 + D - np.power(np.power(N10 + D, 2) - 4 * (N9 + N10 * D), 0.5)) / 2 - Water.CONVERT_C_TO_K

    #endregion

    #region 蒸発潜熱の計算

    # <summary>飽和温度[℃]から蒸発潜熱[kJ/kg]を求める</summary>
    # <param name="saturationTemperature">飽和温度[℃]</param>
    # <returns>蒸発潜熱[kJ/kg]</returns>
    def GetVaporizationLatentHeat(saturationTemperature):

        E1 = -3.87446
        E2 = 2.94553
        E3 = -8.06395
        E4 = 11.5633
        E5 = -6.02884
        B = 0.779221
        C = 4.62668
        D = -1.07931

        # 0度以上とする
        saturationTemperature = np.nax(0, saturationTemperature)

        tr = getTR(saturationTemperature)
        if (tr < 0.0):
            return 0.0

        else:
            y = B * np.power(tr, 1.0 / 3.0) + C * np.power(tr, 5.0 / 6.0) + D * np.power(tr, 0.875)
            y += tr * (E1 + tr * (E2 + tr * (E3 + tr * (E4 + tr * E5))))
            return y * Water.VAPORIZATION_HEAT_AT_TRIPLE_POINT

    #endregion

    #region 飽和水の物性値

    # <summary>飽和温度[℃]から飽和水の比体積[m3/kg]を求める</summary>
    # <param name="saturateTemperature">飽和温度[℃]</param>
    # <returns>飽和水の比体積[m3/kg]</returns>
    def SaturateLiquiSpecificVolume(saturateTemperature):

        A = 1.0
        B = -1.9153882
        C = 12.015186
        D = -7.8464025
        E1 = -3.8886414
        E2 = 2.0582238
        E3 = -2.0829991
        E4 = 0.82180004
        E5 = 0.47549742

        tr = getTR(saturateTemperature)
        y = A + B * np.power(tr, 1.0 / 3.0) + C * np.power(tr, 5.0 / 6.0) + D * np.power(tr, 0.875)
        y += tr * (E1 + tr * (E2 + tr * (E3 + tr * (E4 + tr * E5))))

        return y * SPECIFIC_VOLUME_AT_CRITICAL_POINT

    # <summary>飽和温度[℃]から飽和水のエンタルピー[kJ/kg]を求める</summary>
    # <param name="saturateTemperature">飽和温度[℃]</param>
    # <returns>飽和水のエンタルピー[kJ/kg]</returns>
    def GetSaturateLiquiEnthalpy(saturateTemperature):
 
        # 273.16<Ts<300の係数
        E11 = 624.698837
        E21 = -2343.85369
        E31 = -9508.12101
        E41 = 71628.7928
        E51 = -163535.221
        E61 = 166531.093
        E71 = -64785.4585
        # 300<Ts<600の係数
        A2 = 0.8839230108
        E12 = -2.67172935
        E22 = 6.22640035
        E32 = -13.1789573
        E42 = -1.91322436
        E52 = 68.793763
        E62 = -124.819906
        E72 = 72.1435404
        # 600<Tsの係数
        A3 = 1.0
        B3 = -0.441057805
        C3 = -5.52255517
        D3 = 6.43994847
        E13 = -1.64578795
        E23 = -1.30574143

        tk = saturateTemperature + Water.CONVERT_C_TO_K
        tr = getTR(saturateTemperature)

        if (tk < 300.0):
            y = tr * (E11 + tr * (E21 + tr * (E31 + tr * (E41 + tr * (E51 + tr * (E61 + tr * E71))))))
        elif (tk < 600.0):
            y = tr * (E12 + tr * (E22 + tr * (E32 + tr * (E42 + tr * (E52 + tr * (E62 + tr * E72)))))) + A2
        else:
            y = A3 + B3 * np.power(tr, 1.0 / 3.0) + C3 * np.power(tr, 5.0 / 6.0) + D3 * np.power(tr, 0.875) + tr * (E13 + tr * E23)

        return y * Water.ENTHALPY_AT_CRITICAL_POINT

    # <summary>飽和温度[℃]から飽和水のエントロピー[kJ/kgK]を求める</summary>
    # <param name="saturateTemperature">飽和温度[℃]</param>
    # <returns>飽和水のエントロピー[kJ/kgK]</returns>
    def GetSaturateLiquiEntropy(saturateTemperature):

        #273.16<Ts<300の係数
        E11 = -1836.92956
        E21 = 14706.6352
        E31 = -43146.6046
        E41 = 48606.6733
        E51 = 7997.5096
        E61 = -58333.9887
        E71 = 33140.0718
        #300<Ts<600の係数
        A2 = 0.912762917
        E12 = -1.75702956
        E22 = 1.68754095
        E32 = 5.82215341
        E42 = -63.3354786
        E52 = 188.076546
        E62 = -252.344531
        E72 = 128.058531
        #600<Tsの係数
        A3 = 1.0
        B3 = -0.324817650
        C3 = -2.990556709
        D3 = 3.2341900
        E13 = -0.678067859
        E23 = -1.91910364

        tk = saturateTemperature + Water.CONVERT_C_TO_K
        tr = getTR(saturateTemperature)

        if (tk < 300.0):
            y = tr * (E11 + tr * (E21 + tr * (E31 + tr * (E41 + tr * (E51 + tr * (E61 + tr * E71))))))
        elif (tk < 600.0):
            y = tr * (E12 + tr * (E22 + tr * (E32 + tr * (E42 + tr * (E52 + tr * (E62 + tr * E72)))))) + A2
        else:
            y = A3 + B3 * np.power(tr, 1.0 / 3.0) + C3 * np.power(tr, 5.0 / 6.0) + D3 * np.power(tr, 0.875) + tr * (E13 + tr * E23)

        return y * Water.ENTROPY_AT_CRITICAL_POINT

    #endregion

    #region 飽和蒸気の物性値

    # <summary>飽和温度と飽和圧力から飽和蒸気の比体積を求める</summary>
    # <param name="saturateTemperature">飽和温度[℃]</param>
    # <param name="saturatePressure">飽和圧力[kPa]</param>
    # <returns>飽和蒸気の比体積[m3/kg]</returns>
    
    def GetSaturateVaporSpecificVolume(saturateTemperature,saturatePressure):

        A = 1.0
        B = 1.6351057
        C = 52.584599
        D = -44.694653
        E1 = -8.9751114
        E2 = -0.43845530
        E3 = -19.179576
        E4 = 36.765319
        E5 = -19.462437

        tr = getTR(saturateTemperature)
        y = A + B * np.power(tr, 1.0 / 3.0) + C * np.power(tr, 5.0 / 6.0) + D * np.power(tr, 0.875)
        y += tr * (E1 + tr * (E2 + tr * (E3 + tr * (E4 + tr * E5))))

        return y * Water.PRESSURE_AT_CRITICAL_POINT * SPECIFIC_VOLUME_AT_CRITICAL_POINT / saturatePressure

    # <summary>飽和温度[℃]から飽和蒸気のエンタルピー[kJ/kg]を求める</summary>
    # <param name="saturateTemperature">飽和温度[℃]</param>
    # <returns>飽和蒸気のエンタルピー[kJ/kg]</returns>

    def GetSaturateVaporEnthalpy(saturateTemperature):

        E1 = -4.81351884
        E2 = 2.69411792
        E3 = -7.39064542
        E4 = 10.4961689
        E5 = -5.46840036
        A = 1.0
        B = 0.457874342
        C = 5.08441288
        D = -1.48513244

        tr = getTR(saturateTemperature)
        y = A + B * np.power(tr, 1.0 / 3.0) + C * np.power(tr, 5.0 / 6.0) + D * np.power(tr, 0.875)
        y += tr * (E1 + tr * (E2 + tr * (E3 + tr * (E4 + tr * E5))))

        return y * Water.ENTHALPY_AT_CRITICAL_POINT

    # <summary>飽和温度[℃]から飽和蒸気のエントロピー[kJ/kgK]を求める</summary>
    # <param name="saturateTemperature">飽和温度[℃]</param>
    # <returns>飽和蒸気のエントロピー[kJ/kgK]</returns>
    
    def GetSaturateVaporEntropy(saturateTemperature):
    
        E1 = -4.34839
        E2 = 1.34672
        E3 = 1.75261
        E4 = -6.22295
        E5 = 9.99004
        A = 1.0
        B = 0.377391
        C = -2.78368
        D = 6.93135

        tr = getTR(saturateTemperature)
        y = A + B * np.power(tr, 1.0 / 3.0) + C * np.power(tr, 5.0 / 6.0) + D * np.power(tr, 0.875)
        y += tr * (E1 + tr * (E2 + tr * (E3 + tr * (E4 + tr * E5))))

        return y * Water.ENTROPY_AT_CRITICAL_POINT

    #endregion

    #region 水の物性値

    # <summary>温度[C]から水（液体）の密度[kg/m3]を計算する</summary>
    # <param name="temperature">温度[C]</param>
    # <returns>水（液体）の密度[kg/m3]</returns>
    def GetLiquiensity(temperature):

        a = [9.8811040e2, -1.3273604e3, 4.7162295e3, -4.1245328e3]

        tk = temperature + Water.CONVERT_C_TO_K
        tr = (Water.TEMPERATURE_AT_CRITICAL_POINT - tk) / Water.TEMPERATURE_AT_CRITICAL_POINT

        rho = a[len(a) - 1]
        i = len(a) - 2
              
        while 0 <= i:
            rho = a[i] + rho * tr
            i -= 1

        return rho
    # <summary>温度[C]から水（液体）の定圧比熱[kJ/(kg·K)]を計算する</summary>
    # <param name="temperature">温度[C]</param>
    # <returns>水（液体）の比熱[kJ/(kg·K)]</returns>
    def GetLiquiIsobaricSpecificHeat(temperature):
        a = [1.0570130, 2.1952960e1, -4.9895501e1, 3.6963413e1]

        tk = temperature + Water.CONVERT_C_TO_K
        tr = (Water.TEMPERATURE_AT_CRITICAL_POINT - tk) / Water.TEMPERATURE_AT_CRITICAL_POINT

        cpw = a[len(a) - 1]
        i = len(a) - 2
              
        while 0 <= i:
            cpw = a[i] + cpw * tr
            i -= 1

        return cpw
    # <summary>温度[C]から水（液体）の熱伝導率[W/(m·K)]を計算する</summary>
    # <param name="temperature">温度[C]</param>
    # <returns>水（液体）の熱伝導率[W/(m·K)]</returns>
    def GetLiquiThermalConuctivity(temperature):

        a = [-1.3734399e-1, 4.2128755, -5.9412196, 1.2794890]

        tk = temperature + Water.CONVERT_C_TO_K
        tr = (Water.TEMPERATURE_AT_CRITICAL_POINT - tk) / Water.TEMPERATURE_AT_CRITICAL_POINT

        lamba = a[len(a) - 1]

        while 0 <= i:
            lamba = a[i] + lamba * tr
            i -= 1
        
        return lamba
    # <summary>温度[C]から水（液体）の粘性係数[Pa·s]を計算する</summary>
    # <param name="temperature">温度[C]</param>
    # <returns>水（液体）の粘性係数[Pa·s]</returns>
    def GetLiquiViscosity(temperature):

        a = [5.2136906e1, -4.0910405e2, 1.3270844e3, -1.9089622e3, 1.0489917e3]

        tk = temperature + Water.CONVERT_C_TO_K
        tr = (Water.TEMPERATURE_AT_CRITICAL_POINT - tk) / Water.TEMPERATURE_AT_CRITICAL_POINT

        mu = a[len(a) - 1]

        while 0 <= i:
            mu = a[i] + mu * tr
            i -= 1

        return np.exp(mu) * 0.000001
    # <summary>温度[C]から水（液体）の動粘性係数[m2/s]を計算する</summary>
    # <param name="temperature">温度[C]</param>
    # <returns>水（液体）の動粘性係数[m2/s]</returns>
    def GetLiquiynamicViscosity(temperature):

        mu = GetLiquiViscosity(temperature)
        rho = GetLiquiensity(temperature)

        return mu / rho
    # <summary>温度[C]から水（液体）の熱拡散率[m2/s]を計算する</summary>
    # <param name="temperature">温度[C]</param>
    # <returns>水（液体）の熱拡散率[m2/s]</returns>
    def GetLiquiThermaliffusivity(temperature):

        lamba = GetLiquiThermalConuctivity(temperature)
        cp = GetLiquiIsobaricSpecificHeat(temperature)
        rho = GetLiquiensity(temperature)

        return lamba / (1000 * cp * rho)
    #endregion   




