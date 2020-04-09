from pandapipes.properties.carbondioxid import CarbonDioxide as CO2
from pandapipes.properties.carbondioxid import Library_Variables as LV

lib_path = LV.STR_FILEPATH2USE
lib_tables = LV.STRL_SHEETS2USE
lib_columns = LV.STR_COL2USE

database = CO2.load_property_library(path=lib_path, tables=lib_tables, columns=lib_columns)

Pressure = 180
'bar'
Temperature = 300
'Kelvin'

Interpolated_Values = CO2.interpolate_property(p=Pressure, t=Temperature, property_library=database)

Interpolated_Pressure = Interpolated_Values["Pressure (bar)"]
Interpolated_Temperature = Interpolated_Values["Temperature (K)"]
Interpolated_Density = Interpolated_Values["Density (kg/m3)"]
Interpolated_Cp = Interpolated_Values["Cp (J/g*K)"]
Interpolated_Viscosity = Interpolated_Values["Viscosity (Pa*s)"]
Interpolated_ThermCond = Interpolated_Values["Therm. Cond. (W/m*K)"]
