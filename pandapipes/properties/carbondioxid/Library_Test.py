import pandapipes.properties.carbondioxid.CarbonDioxide as CO2
import pandapipes.properties.carbondioxid.Library_Variables as LV

path = LV.lib_path
tables = LV.lib_tables
columns = LV.lib_columns

database = CO2.load_property_library(path=path, tables=tables, columns=columns)

Pressure = 180
'bar'
Temperature = 300
'Kelvin'

Interpolated_Values = CO2.interpolate_property(p=Pressure, t=Temperature, property_library=database)
