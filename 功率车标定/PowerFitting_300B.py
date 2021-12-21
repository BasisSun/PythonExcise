# -*-coding:gb2312-*-
import numpy as np
import os
import openpyxl

str_path = "��ſع��ʳ��궨"
path_file = ""

duty_num = [0.45*x for x in range(0, 17)]
speed_num = range(3, 8)
fst_row_num = 5

# ����������λ��
List_Col_num = [5, 10, 15, 20, 25]


def get_files():
    global path_file

    for each_file in os.listdir(os.curdir):
        if str_path in each_file:
            path_file = each_file


if __name__ == '__main__':

    f = open("a.txt", 'a')

    # ����excel���
    get_files()

    print("��ʼ����"+path_file+"�Ĵ���")

    f.write("\n"+path_file+"\n")

    f.write("\nfloat PWM_Power[5][5] = {")
    f.flush()

    wb_path = openpyxl.load_workbook(str(path_file), data_only=True)
    path_sheet = wb_path.worksheets[0]

    list_Pwr = []

    # ��ȡ��������30��40��50��60��70���ֱ������ϸ��ٶ��¡�PWM��Power֮��Ĺ�ϵ
    for speed_id in range(5):
        list_Pwr0 = []
        for y in range(fst_row_num, fst_row_num+17):
            list_Pwr0.append(path_sheet.cell(
                row=y, column=List_Col_num[speed_id]).value)

        list_Pwr.append(list_Pwr0)

        # �Ĵζ���ʽ���
        z1 = np.polyfit(duty_num, list_Pwr0, 4)

        z1_list = np.round(z1, 4).tolist()
        str_z1 = str(z1_list)[1:-1]

        str_z1 = "\n{" + str_z1 + "}"

        if speed_id != 4:
            str_z1 += ","

        f.write(str_z1)
        f.flush()

    f.write("};\n\n")
    f.flush()

    # ��ȡ�������ݷֱ������ϸ���λ�£��ٶ���Power֮��Ĺ�ϵ
    f.write("\nfloat Speed_Power[17][4] = {")
    f.flush()

    for duty_id in range(0, 17):
        List_spd_pwr = []
        for list_Pwr0 in list_Pwr:
            List_spd_pwr.append(list_Pwr0[duty_id])

        # ���ζ���ʽ���
        z2 = np.polyfit(speed_num, List_spd_pwr, 3)
        z2_list = np.round(z2, 4).tolist()
        str_z2 = str(z2_list)[1:-1]

        str_z2 = "\n{" + str_z2 + "}"

        if duty_id != 16:
            str_z2 += ","

        f.write(str_z2)
        f.flush()

    f.write("};\n\n")
    f.flush()

    input("�����������򿪱���a.txt�ļ��鿴��")
