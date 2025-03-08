#! /usr/bin/env python
# -*- coding: utf-8 -*-

import time
import logging
import datetime
import binascii
import platform
import threading
import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk

from UI.MainFrm import MainFrame
from Utils.SerialHelper import SerialHelper

# 根据系统 引用不同的库
if platform.system() == "Windows":
    from serial.tools import list_ports
else:
    import glob
    import os
    import re

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')

# 结束符（16进制）CR 13(\r - 0x0D); NL(LF) 10(\n - 0x0A)
END_HEX = "0D0A"


class MainSerialTool(MainFrame):
    '''
    main func class
    '''

    def __init__(self, master=None):
        super(MainSerialTool, self).__init__(master)
        self.root = master

        self.serial_receive_count = 0
        self.PaperRapair_rev_flag = 0
        self.serial_recieve_data = ""
        self.serial_listbox = list()

        self.find_all_devices()

    def find_all_devices(self):
        '''
        线程检测连接设备的状态
        '''
        self.find_all_serial_devices()
        self.start_thread_timer(self.find_all_devices, 1)

    def find_all_serial_devices(self):
        '''
        检查串口设备
        '''
        try:
            if platform.system() == "Windows":
                self.temp_serial = list()
                for com in list(list_ports.comports()):
                    strCom = com[0] + ": " + com[1][:-7]
                    self.temp_serial.append(strCom)
                for item in self.temp_serial:
                    if item not in self.serial_listbox:
                        self.serial_frm.frm_left_listbox.insert("end", item)
                for item in self.serial_listbox:
                    if item not in self.temp_serial:
                        size = self.serial_frm.frm_left_listbox.size()
                        index = list(self.serial_frm.frm_left_listbox.get(
                            0, size)).index(item)
                        self.serial_frm.frm_left_listbox.delete(index)

                self.serial_listbox = self.temp_serial

            elif platform.system() == "Linux":
                self.temp_serial = list()
                self.temp_serial = self.find_usb_tty()
                for item in self.temp_serial:
                    if item not in self.serial_listbox:
                        self.serial_frm.frm_left_listbox.insert("end", item)
                for item in self.serial_listbox:
                    if item not in self.temp_serial:
                        index = list(self.serial_frm.frm_left_listbox.get(
                            0, self.serial_frm.frm_left_listbox.size())).index(item)
                        self.serial_frm.frm_left_listbox.delete(index)
                self.serial_listbox = self.temp_serial
        except Exception as e:
            logging.error(e)

    def Toggle(self, event=None):
        '''
        打开/关闭 设备
        '''
        self.serial_toggle()

    def Send(self):
        '''
        发送数据
        '''
        self.serial_send()

    def SerialClear(self):
        '''
        clear serial receive text
        '''
        self.serial_receive_count = 0
        self.serial_frm.frm_right_receive.delete("0.0", "end")

    #回零操作
    def MoveToP0(self):
        '''
        Move to Point0
        '''
        send_data = "0300FEFF"#""#
        b_data = bytearray.fromhex(send_data) 
        self.ser.writeBytes(b_data)

        self.serial_frm.frm_status_label["text"] = "layser Move to Point0"

        time.sleep(0.1)

        #回零机械手三个滑台
        send_data = "050300FEFF"#""#
        self.DataSend(send_data)

    def MoveToP1(self):
        '''
        Move to Point1
        '''
        #获取设定速度
        speed = '{:04X}'.format(int(self.serial_frm.frm_cutting_mspeed_ety.get()))
        send_data = "020002151450"+speed+"feff"
        b_data = bytearray.fromhex(send_data) 
        self.ser.writeBytes(b_data)

        self.serial_frm.frm_status_label["text"] = "sprayer Move to Point1"

    def PathMove(self):
        '''
        Move along a Spraying  path
        '''
        self.start_thread_target(self.thread_Spraying,"SprayingThread")

    def PumpToggle(self):
        '''
        turn on/off the pump
        '''
        if(self.serial_frm.frm_debug_pump_btn["text"]=="泵开"):

            self.serial_frm.frm_debug_pump_btn["text"]="泵关"
            send_data = "030201feff"#""#
            b_data = bytearray.fromhex(send_data) 
            self.ser.writeBytes(b_data)

            self.serial_frm.frm_status_label["text"] = "pump turn on！"
        else:
            self.serial_frm.frm_debug_pump_btn["text"]="泵开"
            send_data = "030200feff"#""#
            b_data = bytearray.fromhex(send_data) 
            self.ser.writeBytes(b_data)

            self.serial_frm.frm_status_label["text"] = "pump turn off！"

    def CutMove(self):
        '''
        layser cutting along a path
        '''
        self.start_thread_target(self.thread_Cutting,"CuttingThread")


    def PumpPrePare(self):
        # ...
        # PrePare the bubble Pump 
        # ...

        #打开泡沫泵
        send_data = "0506010100"+"64"+"FEFF"
        b_data = bytearray.fromhex(send_data) 
        self.ser.writeBytes(b_data)

        #0.1s后打开蠕动泵0 50%转速
        send_data = "0506000100"+"32"+"FEFF"
        b_data = bytearray.fromhex(send_data)
        time.sleep(0.1)
        self.ser.writeBytes(b_data)

        #指定时间后，关闭两个泵
        #self.serial_frm.frm_status_label["text"] = "["+ str(datetime.datetime.now()) + " - " + "start timer" + "]"
        send_data = "050604FEFF"
        dur_time = int(self.serial_frm.frm_pump_prepare_ety.get())
        self.start_thread_timer(self.DataSend, dur_time,(send_data,))


    def PumpExtract(self):
        # ...
        # Extract the bubble Pump 
        # ...
        #打开蠕动泵1 50%转速
        send_data = "0506020100"+"64"+"FEFF"
        b_data = bytearray.fromhex(send_data)
        time.sleep(0.1)
        self.ser.writeBytes(b_data)

        #指定时间后，关闭泵
        send_data = "050604FEFF"
        b_data = bytearray.fromhex(send_data)
        dur_time = int(self.serial_frm.frm_pump_extract_ety.get())
        self.start_thread_timer(self.DataSend, dur_time,(send_data,))

    def PumpExe(self):
        # ...
        # PrePare and Extract the bubble Pump 
        # ...

         #打开泡沫泵
        send_data = "0506010100"+"64"+"FEFF"
        b_data = bytearray.fromhex(send_data) 
        self.ser.writeBytes(b_data)

        #0.1s后打开蠕动泵0 50%转速
        send_data = "0506000100"+"32"+"FEFF"
        b_data = bytearray.fromhex(send_data)
        time.sleep(0.1)
        self.ser.writeBytes(b_data)

        #指定时间后，关闭两个泵
        dur_time = int(self.serial_frm.frm_pump_prepare_ety.get())
        self.start_thread_timer(self.DataSend, dur_time,("050604FEFF",))

        #在同一时间打开蠕动泵1（两个线程并行延时）
        send_data = "0506020100"+"64"+"FEFF"
        self.start_thread_timer(self.DataSend, dur_time+0.1,(send_data,))

        #指定时间后，关闭泵（三个延时线程并排）
        send_data = "050604FEFF"
        dur_time = dur_time + int(self.serial_frm.frm_pump_extract_ety.get())
        self.start_thread_timer(self.DataSend, dur_time,(send_data,))

    def CuttingExe(self):
    # ...
    # cutting paper using ultrasound knife
    # ...
        pass

    def SetCutterHeight(self):
        #将超声刀头悬停在指定高度
        height = float(self.serial_frm.frm_cutting_height_ety.get())
        str_height = str(hex(int(height*10))).replace("0x","")
        while len(str_height) < 4:
            str_height = "0" + str_height

        send_data = "0304"+str_height+"14FEFF"
        self.start_thread_timer(self.DataSend, 0.1,(send_data,))


    def thread_Cutting(self):
        # # 打开文件,向下位机发送数据，并返回起始点
        # EndPoint = self.getFilePoints("D:\\CuttingPathFile.txt")

        # #副轴移动到起始点
        # self.threadLock.acquire()
        # self.PaperRapair_rev_flag = 0
        # self.threadLock.release()

        # send_data = "0201"+EndPoint
        # b_data = bytearray.fromhex(send_data) 
        # self.ser.writeBytes(b_data)

        # while True:
        #     self.threadLock.acquire()

        #     if self.PaperRapair_rev_flag ==2:
        #         self.PaperRapair_rev_flag = 0

        #         #激光打开
        #         send_data = "03000102BCFEFF"
        #         b_data = bytearray.fromhex(send_data) 
        #         self.ser.writeBytes(b_data)
        #         time.sleep(0.1)

        #         #副轴按照轨迹移动
        #         send_data = "060301FEFF"
        #         b_data = bytearray.fromhex(send_data) 
        #         self.ser.writeBytes(b_data)

        #     elif self.PaperRapair_rev_flag ==6:
        #         self.PaperRapair_rev_flag = 0

        #          #激光关闭
        #         send_data = "0300000000FEFF"
        #         b_data = bytearray.fromhex(send_data) 
        #         self.ser.writeBytes(b_data)
        #         time.sleep(0.1)

        #         #副轴回到起始点附近
        #         send_data = "0201"+self.mm2HexCor(940,40)+"FEFF"#""#mm：（940，40）
        #         b_data = bytearray.fromhex(send_data) 
        #         self.ser.writeBytes(b_data)
                
        #         break

        #     self.threadLock.release()
        #     time.sleep(0.1)
        #移动到切割起点
        # send_data = "020111ee104400fffeff"#""#mm：（940，40）
        # b_data = bytearray.fromhex(send_data) 
        # self.ser.writeBytes(b_data)

        #获取移动速度
        speed = '{:04X}'.format(int(self.serial_frm.frm_cutting_mspeed_ety.get()))
        #测试切割路径
        send_data = "0306"+speed+"feff"
        b_data = bytearray.fromhex(send_data) 
        self.ser.writeBytes(b_data)
        


    def thread_Spraying(self):
        # # 打开文件,向下位机发送数据，并返回起始点
        # EndPoint = self.getFilePoints("D:\\SprayingPathFile.txt")

        # #主轴移动到起始点
        # self.threadLock.acquire()
        # self.PaperRapair_rev_flag = 0
        # self.threadLock.release()

        # send_data = "0200"+EndPoint
        # b_data = bytearray.fromhex(send_data) 
        # self.ser.writeBytes(b_data)

        # while True:
        #     self.threadLock.acquire()

        #     if self.PaperRapair_rev_flag ==2:
        #         self.PaperRapair_rev_flag = 0

        #         #泵打开
        #         self.serial_frm.frm_debug_pump_btn["text"]="泵关"
        #         send_data = "0701010258FEFF"#""#
        #         b_data = bytearray.fromhex(send_data) 
        #         self.ser.writeBytes(b_data)
        #         self.serial_frm.frm_status_label["text"] = "pump turn on！"
                
        #         time.sleep(0.2)

        #         #主轴按照轨迹移动
        #         send_data = "060300FEFF"
        #         b_data = bytearray.fromhex(send_data) 
        #         self.ser.writeBytes(b_data)

        #     elif self.PaperRapair_rev_flag ==6:
        #         self.PaperRapair_rev_flag = 0

        #          #泵关闭
        #         self.serial_frm.frm_debug_pump_btn["text"]="泵开"
        #         send_data = "0701000258FEFF"#""#
        #         b_data = bytearray.fromhex(send_data) 
        #         self.ser.writeBytes(b_data)
        #         self.serial_frm.frm_status_label["text"] = "pump turn off！"

        #         time.sleep(0.1)

        #         #主轴回到喷胶点附近
        #         send_data = "0200"+self.mm2HexCor(51,556)+"FEFF"#""#mm：
        #         b_data = bytearray.fromhex(send_data) 
        #         self.ser.writeBytes(b_data)
                
        #         break

        #     self.threadLock.release()
        #     time.sleep(0.1)

        # 移动到轨迹起点
        # send_data = "020017940e1400fffeff"#""#mm：(1794,0e14)
        # b_data = bytearray.fromhex(send_data) 
        # self.ser.writeBytes(b_data)

        #获取移动速度
        speed = '{:04X}'.format(int(self.serial_frm.frm_cutting_mspeed_ety.get()))
        # 开始涂胶移动
        send_data = "0307"+ speed +"FEFF"
        b_data = bytearray.fromhex(send_data) 
        self.ser.writeBytes(b_data)


    def getFilePoints(self,filepath):
        # 打开文件
        f = open(filepath,'r') 

        while True:
            # 调用文件的 readline()方法
            line = f.readline()   #每次读取一行内容

            if line == "" or line == "\n" :
                break

            line = line.replace(" ","").replace("\n","")

            cor_data = line[1:-1].split(",")
            if len(cor_data) == 2:

                #发送单个数据
                send_data = "0600" + self.Step2HexCor(cor_data[0],cor_data[1])+ "FEFF"#""#
                b_data = bytearray.fromhex(send_data) 
                self.ser.writeBytes(b_data)
                time.sleep(0.01)
            else:
                break
        
        f.close()

        #记录最后一点的坐标（同时也是第一点）
        EndPoint = send_data[4:]

        #结束发送数据
        send_data = "0601FEFF"#""#
        b_data = bytearray.fromhex(send_data) 
        self.ser.writeBytes(b_data)

        time.sleep(0.1)

        return EndPoint



    def StopMove(self):
        '''
        stop move
        '''
        if(self.serial_frm.frm_debug_stop_btn["text"]=="暂停"):

            self.serial_frm.frm_debug_stop_btn["text"]="继续"
            send_data = "0801FEFF"#""#
            b_data = bytearray.fromhex(send_data) 
            self.ser.writeBytes(b_data)

            self.serial_frm.frm_status_label["text"] = "Stop Move！"
        else:
            self.serial_frm.frm_debug_stop_btn["text"]="暂停"
            send_data = "0800FEFF"#""#
            b_data = bytearray.fromhex(send_data) 
            self.ser.writeBytes(b_data)

            self.serial_frm.frm_status_label["text"] = "Continue Move！"

    def DataSend(self,data):

        b_data = bytearray.fromhex(data) 
        self.ser.writeBytes(b_data)
        self.serial_frm.frm_status_label["text"] = "["+ str(datetime.datetime.now()) + " - " + data + "]"


    def serial_toggle(self):
        '''
        打开/关闭串口设备
        '''
        if self.serial_frm.frm_left_btn["text"] == "Open":
            try:
                serial_index = self.serial_frm.frm_left_listbox.curselection()
                if serial_index:
                    self.current_serial_str = self.serial_frm.frm_left_listbox.get(
                        serial_index)
                else:
                    self.current_serial_str = self.serial_frm.frm_left_listbox.get(
                        self.serial_frm.frm_left_listbox.size() - 1)

                if platform.system() == "Windows":
                    self.port = self.current_serial_str.split(":")[0]
                elif platform.system() == "Linux":
                    self.port = self.current_serial_str
                self.baudrate = self.serial_frm.frm_left_combobox_baudrate.get()
                self.parity = self.serial_frm.frm_left_combobox_parity.get()
                self.databit = self.serial_frm.frm_left_combobox_databit.get()
                self.stopbit = self.serial_frm.frm_left_combobox_stopbit.get()
                self.ser = SerialHelper(Port=self.port,
                                        BaudRate=self.baudrate,
                                        ByteSize=self.databit,
                                        Parity=self.parity,
                                        Stopbits=self.stopbit)
                self.ser.on_connected_changed(self.serial_on_connected_changed)
            except Exception as e:
                logging.error(e)
                try:
                    self.serial_frm.frm_status_label["text"] = "Open [{0}] Failed!".format(
                        self.current_serial_str)
                    self.serial_frm.frm_status_label["fg"] = "#DC143C"
                except Exception as ex:
                    logging.error(ex)

        elif self.serial_frm.frm_left_btn["text"] == "Close":
            self.ser.disconnect()
            self.serial_frm.frm_left_btn["text"] = "Open"
            self.serial_frm.frm_left_btn["bg"] = "#008B8B"
            self.serial_frm.frm_status_label["text"] = "Close Serial Successful!"
            self.serial_frm.frm_status_label["fg"] = "#8DEEEE"

    def get_threshold_value(self, *args):
        '''
        get threshold value
        '''
        try:
            self.ser.threshold_value = int(self.serial_frm.threshold_str.get())
        except:
            pass

    def serial_send(self):
        '''
        串口数据发送 CR 13; NL(LF) 10
        '''
        send_data = self.serial_frm.frm_right_send.get("0.0", "end").strip()
        if self.serial_frm.new_line_cbtn_var.get() == 1:  # 是否添加换行符
            send_data = send_data + "\r\n"

        logging.info(">>>" + str(send_data))
        if self.serial_frm.send_hex_cbtn_var.get() == 1:  # 是否使用16进制发送
            send_data = send_data.replace(" ", "").replace("\n", "0A").replace("\r", "0D")
            self.ser.write(send_data, True)
        else:
            self.ser.write(send_data)

    def serial_on_connected_changed(self, is_connected):
        '''
        串口连接状态改变回调
        '''
        if is_connected:
            self.ser.connect()
            if self.ser._is_connected:
                self.serial_frm.frm_status_label["text"] = "Open [{0}] Successful!".format(
                    self.current_serial_str)
                self.serial_frm.frm_status_label["fg"] = "#66CD00"
                self.serial_frm.frm_left_btn["text"] = "Close"
                self.serial_frm.frm_left_btn["bg"] = "#F08080"
                self.ser.on_data_received(self.serial_on_data_received)
            else:
                self.serial_frm.frm_status_label["text"] = "Open [{0}] Failed!".format(
                    self.current_serial_str)
                self.serial_frm.frm_status_label["fg"] = "#DC143C"
        else:
            self.ser.disconnect()
            self.serial_frm.frm_left_btn["text"] = "Open"
            self.serial_frm.frm_left_btn["bg"] = "#008B8B"
            self.serial_frm.frm_status_label["text"] = "Close Serial Successful!"
            self.serial_frm.frm_status_label["fg"] = "#8DEEEE"

    def serial_on_data_received(self, data):
        '''
        串口接收数据回调函数
        '''
        self.serial_recieve_data += data
        self.serial_recieve_data_hex = binascii.hexlify(
            bytes(self.serial_recieve_data, "utf-8")).decode("utf-8").upper()

        # 当接收到的数据达到阈值或者以结束符结束时
        if self.ser.threshold_value <= len(self.serial_recieve_data) or self.serial_recieve_data_hex.endswith(END_HEX.upper()):
            if self.serial_frm.receive_hex_cbtn_var.get() == 1:
                self.serial_frm.frm_right_receive.insert("end", "[" + str(datetime.datetime.now()) + " - "
                                                         + str(self.serial_receive_count) + "]:\n", "green")
                data_str = " ".join([hex(ord(x))[2:].upper().rjust(
                    2, "0") for x in self.serial_recieve_data])
                logging.info("<<<" + str(data_str))
                self.serial_frm.frm_right_receive.insert(
                    "end", data_str + "\n")
                self.serial_frm.frm_right_receive.see("end")
            else:
                self.serial_frm.frm_right_receive.insert("end", "[" + str(datetime.datetime.now()) + " - "
                                                         + str(self.serial_receive_count) + "]:\n", "green")
                self.serial_frm.frm_right_receive.insert(
                    "end", self.serial_recieve_data + "\n")
                logging.info("<<<" + str(self.serial_recieve_data))
                self.serial_frm.frm_right_receive.see("end")

            #判断古籍修复机器人的返回内容
            self.threadLock.acquire()
            if self.serial_recieve_data.find("06:Complete") != -1:
                self.PaperRapair_rev_flag = 6
            elif self.serial_recieve_data.find("02:TwoMotor") != -1:
                self.PaperRapair_rev_flag = 2
            self.threadLock.release()

            self.serial_receive_count += 1
            self.serial_recieve_data = ""

    def find_usb_tty(self, vendor_id=None, product_id=None):
        '''
        查找Linux下的串口设备
        '''
        tty_devs = list()
        for dn in glob.glob('/sys/bus/usb/devices/*'):
            try:
                vid = int(open(os.path.join(dn, "idVendor")).read().strip(), 16)
                pid = int(open(os.path.join(dn, "idProduct")).read().strip(), 16)
                if ((vendor_id is None) or (vid == vendor_id)) and ((product_id is None) or (pid == product_id)):
                    dns = glob.glob(os.path.join(
                        dn, os.path.basename(dn) + "*"))
                    for sdn in dns:
                        for fn in glob.glob(os.path.join(sdn, "*")):
                            if re.search(r"\/ttyUSB[0-9]+$", fn):
                                tty_devs.append(os.path.join(
                                    "/dev", os.path.basename(fn)))
            except Exception as ex:
                pass
        return tty_devs

    #将mm坐标转换成16进制坐标点位置
    def mm2HexCor(self,x,y):
        roundX = int(round(float(x)/0.1125))
        roundY = int(round(float(y)/0.1125))

        str1 = '{:04X}'.format(roundX)
        str2 = '{:04X}'.format(roundY)
        return str1 + str2

    #将步数转换成16进制坐标点位置
    def Step2HexCor(self,x,y):
        return '{:04X}'.format(int(x)) + '{:04X}'.format(int(y))



if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry()
    root.title("Serial Tool")

    monacofont = tkFont.Font(family="Monaco", size=16)
    root.option_add("*TCombobox*Listbox*background", "#292929")
    root.option_add("*TCombobox*Listbox*foreground", "#FFFFFF")
    root.option_add("*TCombobox*Listbox*font", monacofont)

    root.configure(bg="#292929")
    combostyle = ttk.Style()
    combostyle.theme_use('default')
    combostyle.configure("TCombobox",
                         selectbackground="#292929",
                         fieldbackground="#292929",
                         background="#292929",
                         foreground="#FFFFFF")

    app = MainSerialTool(root)
    root.mainloop()
