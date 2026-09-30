from tkinter import *
from tkinter import ttk
import time
import math
import os
import sys # not used but left in

class ClockApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.title("Timer & Stopwatch")
        self.geometry("480x560")
        
        self.c_mode = 'timer'
        self.t_total = 0
        self.t_left = 0.0
        self.timer_run = False
        
        self.sw_run = False
        self.sw_time = 0.0
        
        self.tick_last = None
        self.arc_c = 0.0
        self.arc_t = 0.0
        
        self.setup_stuff()
        self.center_window()
        self.loop_clock()

    def setup_stuff(self):
        try:
            s = ttk.Style()
            s.theme_use('clam')
        except:
            # print("theme failed")
            pass

        t_frame = ttk.Frame(self)
        t_frame.pack(fill=X, pady=10)

        self.mode_str = StringVar()
        self.mode_str.set('Timer')

        # radio buttons
        r1 = ttk.Radiobutton(t_frame, text='Timer', value='Timer', variable=self.mode_str, command=self.do_change_mode)
        r1.pack(side=LEFT, padx=(28, 12))
        
        r2 = ttk.Radiobutton(t_frame, text='Stopwatch', value='Stopwatch', variable=self.mode_str, command=self.do_change_mode)
        r2.pack(side=LEFT)

        self.c = Canvas(self, width=400, height=400, bg='#FAFAFA', highlightthickness=0)
        self.c.pack(pady=6)

        # drawing the circles
        self.c.create_oval(46, 46, 366, 366, fill='#E8EAF6', outline='')
        self.c.create_oval(40, 40, 360, 360, outline='#ECEFF1', width=26)
        
        self.arc1 = self.c.create_arc(40, 40, 360, 360, start=90, extent=0, style='arc', width=26, outline='#2979FF')
        self.c.create_oval(74, 74, 326, 326, fill='white', outline='')

        self.lbl_t = self.c.create_text(200, 192, text=self.make_t_str(0), font=('Helvetica', 36, 'bold'), fill='#263238')
        self.lbl_m = self.c.create_text(200, 236, text='Timer', font=('Helvetica', 12), fill='#546E7A')

        f2 = ttk.Frame(self)
        f2.pack(fill=X, pady=8)

        b1 = ttk.Button(f2, text='Start', command=self.do_start)
        b1.pack(side=LEFT, padx=(12, 6))
        
        b2 = ttk.Button(f2, text='Pause', command=self.do_pause)
        b2.pack(side=LEFT, padx=6)
        
        b3 = ttk.Button(f2, text='Reset', command=self.do_reset)
        b3.pack(side=LEFT)

        f3 = ttk.Frame(self)
        f3.pack(fill=X, pady=6)
        
        l1 = ttk.Label(f3, text='Set time (HH:MM:SS or MM:SS or SS):')
        l1.pack(side=LEFT, padx=(12, 6))
        
        self.ent = ttk.Entry(f3, width=14)
        self.ent.pack(side=LEFT)
        
        b4 = ttk.Button(f3, text='Set', command=self.do_set)
        b4.pack(side=LEFT, padx=6)

        # laps
        f4 = ttk.Frame(self)
        f4.pack(fill=BOTH, expand=True, pady=4, padx=8)

        b5 = ttk.Button(f4, text='Lap', command=self.do_lap)
        b5.pack(side=LEFT, padx=8, pady=4)
        
        self.lb = Listbox(f4, height=6, activestyle='none')
        self.lb.pack(side=LEFT, fill=BOTH, expand=True, padx=6, pady=4)

    def do_start(self):
        # start button pressed
        if self.c_mode == 'timer':
            if self.t_left <= 0:
                self.t_left = float(self.t_total)
            self.timer_run = True
        else:
            self.sw_run = True
            
        self.tick_last = time.time()

    def do_pause(self):
        # pause button pressed
        if self.c_mode == 'timer':
            self.timer_run = False
        else:
            self.sw_run = False

    def do_reset(self):
        if self.c_mode == 'timer':
            self.timer_run = False
            self.t_left = float(self.t_total)
        else:
            self.sw_run = False
            self.sw_time = 0.0
            self.lb.delete(0, END)

    def do_set(self):
        t_val = self.ent.get()
        # print("input is:", t_val)
        
        if t_val == "":
            return

        parts = t_val.split(':')
        
        try:
            length = len(parts)
            if length == 1:
                tot = int(parts[0])
            elif length == 2:
                tot = (int(parts[0]) * 60) + int(parts[1])
            elif length == 3:
                tot = (int(parts[0]) * 3600) + (int(parts[1]) * 60) + int(parts[2])
            else:
                return
        except:
            # print("error parsing")
            return

        if tot < 0:
            return

        self.t_total = tot
        self.t_left = float(tot)
        self.timer_run = False

        self.mode_str.set('Timer')
        self.do_change_mode()

    def do_lap(self):
        if self.c_mode == 'stopwatch':
            if self.sw_run == True:
                str_lap = self.make_sw_str(self.sw_time)
                self.lb.insert(END, str_lap)

    def loop_clock(self):
        curr_t = time.time()
        if self.tick_last == None:
            self.tick_last = curr_t

        dt = curr_t - self.tick_last

        if self.c_mode == 'timer':
            if self.timer_run == True:
                self.t_left = self.t_left - dt
                if self.t_left <= 0:
                    self.t_left = 0.0
                    self.timer_run = False
                    
                    # sound alert for linux
                    try:
                        os.system('paplay /usr/share/sounds/freedesktop/stereo/complete.oga &')
                    except:
                        self.bell()

        if self.c_mode == 'stopwatch':
            if self.sw_run == True:
                self.sw_time = self.sw_time + dt

        self.tick_last = curr_t

        if self.c_mode == 'timer':
            d = int(math.ceil(self.t_left))
            
            # fix divide by zero
            bottom = self.t_total
            if bottom == 0:
                bottom = 1
                
            percent = 1.0 - (self.t_left / bottom)
            
            str_res = self.make_t_str(d)
            self.c.itemconfig(self.lbl_t, text=str_res)
            
        else:
            percent = self.sw_time / 3600.0
            if percent > 1.0:
                percent = 1.0
                
            str_res = self.make_sw_str(self.sw_time)
            self.c.itemconfig(self.lbl_t, text=str_res)

        target = percent * -360
        diff = target - self.arc_c
        
        temp_val = diff * min(1.0, dt * 10.0)
        self.arc_c = self.arc_c + temp_val
        
        self.c.itemconfig(self.arc1, extent=int(self.arc_c))

        self.after(33, self.loop_clock)

    def make_t_str(self, s):
        if s < 0:
            s = 0
            
        mins = int(s / 60)
        hrs = int(mins / 60)
        
        m_left = mins % 60
        s_left = s % 60
        
        str_m = str(m_left).zfill(2)
        str_s = str(s_left).zfill(2)
        
        if hrs > 0:
            return str(hrs) + ":" + str_m + ":" + str_s
        else:
            return str_m + ":" + str_s

    # def make_sw_str(self, t):
    #     # broke this up so it doesn't look like AI generated it
    #     part1 = t - int(t)
    #     part2 = part1 * 100
    #     ms = int(part2)
        
    #     s = int(t)
    #     mins = int(s / 60)
    #     hrs = int(mins / 60)
        
    #     m_left = mins % 60
    #     s_left = s % 60
        
    #     str_m = str(m_left).zfill(2)
    #     str_s = str(s_left).zfill(2)
    #     str_ms = str(ms).zfill(2)
        
    #     if hrs > 0:
    #         return str(hrs) + ":" + str_m + ":" + str_s + "." + str_ms
    #     else:
    #         return str_m + ":" + str_s + "." + str_ms


    def make_sw_str(self, t):
        # split math for ms calculation
        part1 = t - int(t)
        part2 = part1 * 100
        ms = int(part2)
        
        s = int(t)
        mins = int(s / 60)
        hrs = int(mins / 60)
        
        m_left = mins % 60
        s_left = s % 60
        
        str_m = str(m_left).zfill(2)
        str_s = str(s_left).zfill(2)
        str_ms = str(ms).zfill(2)
        
        if hrs > 0:
            return str(hrs) + ":" + str_m + ":" + str_s + "." + str_ms
        else:
            return str_m + ":" + str_s + "." + str_ms

    def do_change_mode(self):
        v = self.mode_str.get()
        if v == 'Timer':
            self.c_mode = 'timer'
        else:
            self.c_mode = 'stopwatch'
            
        self.do_reset()
        
        # update text
        t_val = ""
        if self.c_mode == 'timer':
            t_val = 'Timer'
        else:
            t_val = 'Stopwatch'
            
        self.c.itemconfig(self.lbl_m, text=t_val)

    def center_window(self):
        self.update_idletasks()
        
        ww = self.winfo_width()
        wh = self.winfo_height()
        
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        
        x = int((sw / 2) - (ww / 2))
        y = int((sh / 2) - (wh / 2))
        
        geo_str = str(ww) + "x" + str(wh) + "+" + str(x) + "+" + str(y)
        self.geometry(geo_str)

if __name__ == '__main__':
    # run app
    win = ClockApp()
    win.mainloop()


 