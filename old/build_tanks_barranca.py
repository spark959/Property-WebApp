import pandas as pd 
import csv 
import numpy as np
import matplotlib.pyplot as plt 
import os
import sys

# directory where xlsx of strapping tables are:
directory_path = 'C:\\Users\\christian.abbott\\Desktop\\Off-Sites\\Projects\\EcoPetrol_Barranca2019\\Data\\TIS\\TablaAforo\\ALL_From_Ecopetrol_Formatted'

# picking the xlsx file to open

list_of_files_with_extensions = os.listdir(directory_path)
list_of_files_without_extensions = [x.split('.')[0] for x in list_of_files_with_extensions]
list_of_file_paths = [directory_path+'\\'+str(x) for x in list_of_files_with_extensions]

"""
Defining functions to build the strapping tables
1. CalcStrappingSump
2. CalcStrappingBody
"""

def CalcStrappingSump(heights,volumes,deltas):
    new_volumes = []
    new_heights = []
    strapping_table_list = []

    end_flag = False 
    end_height_full = heights[-1]
    end_height_10cm = int(end_height_full//10//10%10)
    end_height_cm = int(end_height_full//10%10)
    end_height_mm = int(end_height_full%10)

    for i in range(len(heights)-1):
        temp_height_full = heights[i]
        temp_height_10cm = int(temp_height_full//10//10%10)
        temp_height_cm = int(temp_height_full//10%10)
        temp_height_mm = int(temp_height_full%10)

        for j in range(int(heights[i+1])-int(heights[i])):
            temp_height = int(heights[i]+j)
            new_heights.append(temp_height)
            temp_volume = volumes[i]+j*deltas[i]
            new_volumes.append(temp_volume)
            temp_strapping_table_list = (temp_height,temp_volume)
            strapping_table_list.append(temp_strapping_table_list)
                    
    strapping_table = {str(level):volume for level,volume in strapping_table_list}
    return strapping_table, new_heights, new_volumes



def CalcStrappingBody(heights,volumes,fractions_mm,fractions_cm):
    
    new_volumes = []
    new_heights = []
    strapping_table_list = []

    end_flag = False 
    end_height_full = int(round(heights[-1],0))
    end_height_10cm = int(end_height_full//10//10%10)
    end_height_cm = int(end_height_full//10%10)
    end_height_mm = int(end_height_full%10)

    if end_height_full%100 != 0:
        for i in range(len(heights)-1):
            if end_flag == False:
                temp_height_full = int(round(heights[i],0))
                temp_height_10cm = int(temp_height_full//10//10%10)
                temp_height_cm = int(temp_height_full//10%10)
                temp_height_mm = int(temp_height_full%10)

                for j in range(temp_height_cm,10):
                    if end_flag == False:
                        offset_j = 0
                        if temp_height_cm == 0:
                            offset_j = 0
                        else:
                            offset_j = 0-temp_height_cm

                        for k in range(temp_height_mm,10):
                            if end_flag == False:
                                offset_k = 0
                                if temp_height_mm == 0:
                                    offset_k = 0
                                else:
                                    offset_k = 0-temp_height_mm

                                modified_start_volume = volumes[i]-(fractions_cm[abs(offset_j)]+(fractions_mm[abs(offset_k)])) # this is required for any tables whose tank body doesn't start on a multiple of 100

                                if temp_height_full+10*(j+offset_j)+(k+offset_k) == end_height_full: # what to do when the last point on the strapping table is reached
                                    temp_height = int(round(heights[-1],0))
                                    new_heights.append(temp_height)
                                    temp_volume = volumes[-1]
                                    new_volumes.append(temp_volume)
                                    temp_strapping_table_list = (temp_height,temp_volume)
                                    strapping_table_list.append(temp_strapping_table_list)
                                    print(temp_height)
                                    end_flag = True
                                    break
                                else:
                                    temp_height = int(temp_height_full+10*(j+offset_j)+(k+offset_k))
                                    new_heights.append(temp_height)
                                    temp_volume = modified_start_volume+fractions_cm[j]+fractions_mm[k]
                                    new_volumes.append(temp_volume)
                                    temp_strapping_table_list = (temp_height,temp_volume)
                                    strapping_table_list.append(temp_strapping_table_list)
                            else:
                                break
                    else:
                        break
            else:
                break
    else: # special handling for strapping tables that end on a 100....
        for i in range(len(heights)):
            if end_flag == False:
                temp_height_full = int(round(heights[i],0))
                temp_height_10cm = int(temp_height_full//10//10%10)
                temp_height_cm = int(temp_height_full//10%10)
                temp_height_mm = int(temp_height_full%10)

                for j in range(temp_height_cm,10):
                    if end_flag == False:
                        offset_j = 0
                        if temp_height_cm == 0:
                            offset_j = 0
                        else:
                            offset_j = 0-temp_height_cm

                        for k in range(temp_height_mm,10):
                            if end_flag == False:
                                offset_k = 0
                                if temp_height_mm == 0:
                                    offset_k = 0
                                else:
                                    offset_k = 0-temp_height_mm

                                modified_start_volume = volumes[i]-(fractions_cm[abs(offset_j)]+(fractions_mm[abs(offset_k)])) # this is required for any tables whose tank body doesn't start on a multiple of 100

                                if temp_height_full+10*(j+offset_j)+(k+offset_k) == end_height_full: # what to do when the last point on the strapping table is reached
                                    temp_height = int(round(heights[-1],0))
                                    new_heights.append(temp_height)
                                    temp_volume = volumes[-1]
                                    new_volumes.append(temp_volume)
                                    temp_strapping_table_list = (temp_height,temp_volume)
                                    strapping_table_list.append(temp_strapping_table_list)
                                    print(temp_height)
                                    end_flag = True
                                    break
                                else:
                                    temp_height = int(temp_height_full+10*(j+offset_j)+(k+offset_k))
                                    new_heights.append(temp_height)
                                    temp_volume = modified_start_volume+fractions_cm[j]+fractions_mm[k]
                                    new_volumes.append(temp_volume)
                                    temp_strapping_table_list = (temp_height,temp_volume)
                                    strapping_table_list.append(temp_strapping_table_list)
                            else:
                                break
                    else:
                        break
            else:
                break
    strapping_table = {str(level):volume for level,volume in strapping_table_list}
    return strapping_table, new_heights, new_volumes

"""
Iterating through all files in the given directory and pulling out needed information
"""

for i in range(len(list_of_files_with_extensions)):

    file_path = list_of_file_paths[i]
    print('')
    print('Processing {filename}'.format(filename=file_path))
    

    # parsing the data from the 4 different pages in the xlsx file
    # 1. CUERPO_CILINDRO
    # 2. FONDO_CILINDRO
    # 3. FRACCIONES_MM
    # 4. RESUMEN

    # has_sump = True
    # has_body = True


    try:
        tank_sump_df = pd.read_excel(file_path,sheet_name=['FONDO_CILINDRO'],skiprows=5,usecols=[0,1,2])

        tank_sump_height = [x for x in tank_sump_df['FONDO_CILINDRO']['ALTURA']]
        tank_sump_volume = [x for x in tank_sump_df['FONDO_CILINDRO']['VOLUMEN']]
        tank_sump_delta = [x for x in tank_sump_df['FONDO_CILINDRO']['INCREMENTO']]

        sump_answer = CalcStrappingSump(tank_sump_height,tank_sump_volume,tank_sump_delta)
    # except Exception as e:
    #     print('{file} Has no sump...'.format(file=list_of_files_without_extensions[i]))
    #     has_sump = False

    # try:
        tank_body_df = pd.read_excel(file_path,sheet_name=['CUERPO_CILINDRO'],skiprows=7,usecols=[0,1])

        tank_body_height = [x*10 for x in tank_body_df['CUERPO_CILINDRO']['ALTURA']]
        tank_body_volume = [x for x in tank_body_df['CUERPO_CILINDRO']['VOLUMEN']]

        tank_fractions_df = pd.read_excel(file_path,sheet_name=['FRACCIONES_MM'],skiprows=5,usecols=[0,1])

        # tank_fraction_height = [x for x in tank_fractions_df['FRACCIONES_MM']['ALTURA']] # NOT IMPORTANT
        tank_fraction_volume_mm = [round(x,3) for x in tank_fractions_df['FRACCIONES_MM']['VOLUMEN']]
        tank_fraction_volume_cm = [round(x*10,3) for x in tank_fractions_df['FRACCIONES_MM']['VOLUMEN']]
        tank_fraction_volume_mm.insert(0,0)
        tank_fraction_volume_cm.insert(0,0)

        body_answer = CalcStrappingBody(tank_body_height,tank_body_volume,tank_fraction_volume_mm,tank_fraction_volume_cm)

    except Exception as e:
        print('Problem with {file} ...'.format(file=list_of_files_without_extensions[i]))
        # has_body = False


    """
    Graphing results
    """

    # sump_level = [int(x) for x in sump_answer[1]]
    # sump_volume = [round(x,3) for x in sump_answer[2]]
    # body_level = [int(x) for x in body_answer[1]]
    # body_volume = [round(x,2) for x in body_answer[2]]

    # plt.plot(sump_level,sump_volume,label='sump')
    # plt.plot(body_level,body_volume,label='body')
    # plt.legend(loc='best')
    # plt.show()

    # sys.exit()


    """
    Writing results to a csv file
    """
    new_directory_path = 'C:\\Users\\christian.abbott\\Desktop\\Off-Sites\\Projects\\EcoPetrol_Barranca2019\\Data\\TIS\\TablaAforo\\ALL_Recalculated'
    new_file_path = new_directory_path+'\\'+list_of_files_without_extensions[i]+'_new'+'.csv'

    with open(new_file_path,'w') as newfile:
        csv_writer = csv.writer(newfile,delimiter=',',lineterminator='\n')

        # if has_sump == True:
        for i in range(len(sump_answer[1])):
            # info_tuple = (str(int(sump_answer[1][i])),'',str(round(sump_answer[2][i],3)))
            # new_line = ','.join(info_tuple)
            row = (int(sump_answer[1][i]),'',round(sump_answer[2][i],3),'','','')
            csv_writer.writerow(row)

        # if has_body == False:
        for i in range(len(body_answer[1])):
            # info_tuple = (str(int(body_answer[1][i])),'',str(round(body_answer[2][i],2)))
            # new_line = ','.join(info_tuple)
            row = (int(body_answer[1][i]),'',round(body_answer[2][i],2),'','','')
            csv_writer.writerow(row)


    # sys.exit()