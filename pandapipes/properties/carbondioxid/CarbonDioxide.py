import pandas as pd
import numpy as np
import math

try:
    import pplog as logging
except ImportError:
    import logging
logger = logging.getLogger(__name__)


def load_property_library(path, tables, columns):
    '''
    loads a library with Fluid_Properties. Each Table inherits the properties from Pressure A to Pressure B at a
    constant Temperature (Isothermal curves)

    :param path: Path as String, where to find the Table, e.g. path = r".../Path.xlsx"
    :param tables: List of Strings, which Tables should be used, e.g. tables = ["Table1", "Table2", "Table3"]
    :param columns: String of comma seperated Letters of Columns which should be loaded, e.g. columns = "A,C,D,J,M,N"
    :return: Returns the needed Tables within the .xlsx-file as list and the available Temperatures as list
    '''

    # pandas and xlrd needed
    lib_as_OrderedDictionary = pd.read_excel(path, sheet_name=tables, usecols=columns)
    lib_as_list = list(lib_as_OrderedDictionary.items())

    temp_DataFrame = pd.DataFrame()

    for idx, t in lib_as_list:
        temp_DataFrame = temp_DataFrame.append(t, ignore_index=True)

    indexes = {}
    for idx, t in lib_as_list:
        indexes[t["Temperature (K)"].iloc[0]] = t

    available_temperatures = list(indexes.keys())
    available_temperatures.sort()
    return indexes, available_temperatures, lib_as_list


def get_closest_values(array, value):
    '''
    finding the closest 2 Temperatures within the Temperature-Tables (isothermal curves)

    :param array: array with float values, e.g. available_temperatures in "load_property_library"
    :param value: float value in between array values, e.g. 300
    :return: returns the closest 2 values to the searched value
    '''
    if value <= min(array):
        logging.warning(
            "def find nearest_lower_upper: Value is smaller than or equal to the smallest value in array! Return lower, lower")
        lower = min(array)
        return lower, lower

    if value >= max(array):
        logging.warning(
            "def find nearest_lower_upper: Value is bigger than or equal to the biggest value in array! Return upper, upper")
        upper = max(array)
        return upper, upper

    lower = max([x for x in array if x <= value])
    upper = min([x for x in array if x >= value])

    return lower, upper


def get_nearest_indexes(table, indexes_column, value):
    '''

    :param table:
    :param indexes_array:
    :param value:
    :return:
    '''
    table.index = table[indexes_column]
    index_lower, index_upper = get_closest_values(table.index, value)
    sel = table.loc[[index_lower, index_upper]]
    return sel


def find_nearest_right(llist, list_index, value):
    array = llist[list_index][1].values[:, 1]
    idx = np.searchsorted(array, value, side="left")
    if idx > 0 and (
            idx == len(array) or math.fabs(value - array[idx]) < math.fabs(value - array[idx])):
        return llist[list_index][1].values[idx,]
    else:
        return llist[list_index][1].values[idx,]
        # due to the complexity of the span-wagner-equation, this is a work-around to "calculate" the fluid properties of carbon dioxide by searching the closest values first and calculate weighted mean value

        # Prepared .xlsx-File with several sheets of different isothermal properties of Carbondioxide which can be found in the Properties-Folder of Carbondioxide


def interpolate_property(p, t, property_library):
    """

    :param p:
    :type p:
    :param t:
    :type t:
    :return:
    :rtype:
    """
    # Two function to find the rows we are intrested in the Function is taken from the following weblink and slightly altered to return the rows we need https://stackoverflow.com/questions/2566412/find-nearest-value-in-numpy-array' finds P_min @ Temp'EXAMPLE VALUES, to check if the concept is working or not
    # T_is = 319

    temps = property_library[1]
    T_is = t
    # P_is = 200
    P_is = p
    # definitely needs to be done, otherwise the Variables Temp_Index0 and Temp_Index1 have to be set manual based on the Temperature (T_is) we choose the proper Tables. T_lower <= T_is <= T_upper
    'todo: Temperature to Index of List, which is why the values for both variables are fixed'
    Temp_Lower, Temp_Upper = get_closest_values(temps, T_is)
    t_weight = (Temp_Upper - T_is) / (Temp_Upper - Temp_Lower)

    Properties_at_Temp_Lower = get_nearest_indexes(property_library[0][Temp_Lower], "Pressure (bar)", P_is)
    Properties_at_Temp_Upper = get_nearest_indexes(property_library[0][Temp_Upper], "Pressure (bar)", P_is)

    pLow_tLow, pUp_tLow = min(Properties_at_Temp_Lower.index), max(Properties_at_Temp_Lower.index)
    pweight_tlow = (pUp_tLow - P_is) / (pUp_tLow - pLow_tLow)
    corr1 = Properties_at_Temp_Lower.iloc[0] * (1 - pweight_tlow) + Properties_at_Temp_Lower.iloc[1] * pweight_tlow

    pLow_tUp, pUp_tUp = min(Properties_at_Temp_Upper.index), max(Properties_at_Temp_Upper.index)
    pweight_tup = (pUp_tUp - P_is) / (pUp_tUp - pLow_tUp)
    corr2 = Properties_at_Temp_Upper.iloc[0] * (1 - pweight_tup) + Properties_at_Temp_Upper.iloc[1] * pweight_tup

    Values_PTcorr = corr1 * (1 - t_weight) + corr2 * t_weight

    return Values_PTcorr
