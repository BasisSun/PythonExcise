#! /usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter.ttk as ttk
import tkinter.font as tkFont
import tkinter as tk
import datetime
import threading

try:
    from UI import PyTkinter as pytk
    from UI.SerialFrm import SerialFrame
except:
    import PyTkinter as pytk
    from SerialFrm import SerialFrame

g_font = ("Monaco", 16)


class MainFrame(object):
    '''
    main frame
    '''

    def __init__(self, master=None):
        '''
        constructor
        '''
        self.root = master
        self.create_frame()
        self.threadLock = threading.Lock()

        self.state = True
        # self.root.attributes("-fullscreen", self.state)
        self.root.bind("<F11>", self.toggle_fullscreen)

    def create_frame(self):
        self.frm_main = pytk.PyLabelFrame(self.root)
        self.frm_main.pack(fill="both", expand=1)

        self.create_frm_main()

        self.init_serial_frm()

    def create_frm_main(self):
        self.serial_frm = SerialFrame(self.frm_main)
        self.serial_frm.frm.pack(fill="both", expand=1, padx=2, pady=2)

    def show_current_time(self):
        '''
        show computer current date
        '''
        self.frm_status_bottom_label_date["text"] = str(
            datetime.datetime.now())[:-7]
        self.root.after(2**8, self.show_current_time)

    def toggle_fullscreen(self, event=None):
        '''
        toggle fullscreen
        '''
        self.state = not self.state
        self.root.attributes("-fullscreen", self.state)

    def init_serial_frm(self):
        '''
        init serial frm
        '''
        self.serial_frm.frm_left_btn["command"] = self.Toggle
        self.serial_frm.frm_left_listbox.bind("<Double-Button-1>", self.Toggle)
        self.serial_frm.frm_right_send_btn["command"] = self.Send
        self.serial_frm.frm_right_clear_btn["command"] = self.SerialClear
        self.serial_frm.threshold_str.set(1)
        self.serial_frm.threshold_str.trace('w', self.get_threshold_value)

        self.serial_frm.frm_debug_point0_btn["command"] = self.MoveToP0
        self.serial_frm.frm_debug_point1_btn["command"] = self.MoveToP1
        self.serial_frm.frm_debug_move_btn["command"] = self.PathMove
        self.serial_frm.frm_debug_pump_btn["command"] = self.PumpToggle
        self.serial_frm.frm_debug_cut_btn["command"] = self.CutMove
        self.serial_frm.frm_debug_stop_btn["command"] = self.StopMove


    def Toggle(self, event=None):
        '''
        toggle dev
        '''
        pass

    def Send(self):
        '''
        send msg to dev
        '''
        pass

    def SerialClear(self):
        '''
        clear serial recieve text
        '''
        pass

    def UsbClear(self):
        '''
        clear usb recieve text
        '''
        pass

    def get_threshold_value(self, *args):
        '''
        get threshold value
        '''
        pass

    def MoveToP0(self):
        '''
        Move to Point0
        '''
        pass

    def MoveToP1(self):
        '''
        Move to Point1
        '''
        pass

    def PathMove(self):
        '''
        Move along a path
        '''
        pass

    def PumpToggle(self):
        '''
        turn on/off the pump
        '''
        pass

    def CutMove(self):
        '''
        layser cutting along a path
        '''
        pass

    def StopMove(self):
        '''
        stop move
        '''
        pass


    def start_thread_timer(self, callback, timer=1):
        '''
        util: start thread timer
        '''
        temp_thread = threading.Timer(timer, callback)
        temp_thread.setDaemon(True)
        temp_thread.start()

    def start_thread_target(self, callback, name="thread"):
        '''
        util: start thread target
        '''
        temp_thread = threading.Thread(target=callback, name=name)
        temp_thread.setDaemon(True)
        temp_thread.start()


if __name__ == '__main__':
    '''
    main loop
    '''
    root = tk.Tk()
    root.columnconfigure(0, weight=1)
    root.rowconfigure(0, weight=1)
    root.geometry()

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

    app = MainFrame(root)
    root.mainloop()
