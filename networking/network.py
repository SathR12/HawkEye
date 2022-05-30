import tkinter
import tkinter.messagebox
import customtkinter
import cv2 as cv
import PIL
import sys
import numpy as np
import time
import os
import json

from tkinter import *
from PIL import Image, ImageTk
from camera_init import *

sys.path.append(os.getcwd() + "\\shapes")

from circle import *

customtkinter.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"

class Network(customtkinter.CTk):

    WIDTH = 1500
    HEIGHT = 1000
    
    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)
        self.title("Network")
        self.geometry(f"{Network.WIDTH}x{Network.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(1, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        
        #configure sidebar for different frame buttons  
        self.sidebar = customtkinter.CTkFrame(master = self, width = 400, corner_radius = 0)
        self.sidebar.grid(row = 0, column = 0, sticky = "nswe")
        
        #right side frame
        self.frame_right = customtkinter.CTkFrame(master = self)
        self.frame_right.grid(row = 0, column = 1, sticky = "nswe", padx = 20, pady = 20)
        
        #configure rows for button maps 
        self.sidebar.grid_rowconfigure(0, minsize = 10)  
        self.sidebar.grid_rowconfigure(5, weight = 1)  
        self.sidebar.grid_rowconfigure(8, minsize = 20)    
        self.sidebar.grid_rowconfigure(11, minsize = 10)
        
        #sidebar title: Networking; subject to change 
        self.sidebar_title = customtkinter.CTkLabel(master = self.sidebar, text = "Networking", text_font = ("Roboto Medium", -20))  
        self.sidebar_title.grid(row = 1, column = 0, pady = 50, padx = 50)
        
        self.mask_button = customtkinter.CTkButton(master = self.sidebar, text = "Mask", fg_color = ("gray75", "gray30"), command = self.mask_frame)
        self.mask_button.grid(row = 2, column = 0, pady = 10, padx = 20)

        self.canny_button = customtkinter.CTkButton(master = self.sidebar, text = "Canny", fg_color = ("gray75", "gray30"), command = self.canny_frame)
        self.canny_button.grid(row = 3, column = 0, pady = 10, padx = 20)

        self.stream_button = customtkinter.CTkButton(master = self.sidebar, text = "Stream", fg_color = ("gray75", "gray30"), command = self.stream)
        self.stream_button.grid(row = 4, column = 0, pady = 10, padx = 20)        
        
        #trackbars for hsv
        self.low_hue = customtkinter.CTkSlider(master = self.frame_right, to = 255)
        self.low_hue.grid(row = 4, column = 0, columnspan = 2, pady = 10, padx = 30, sticky = "we")
       
        self.low_sat = customtkinter.CTkSlider(master = self.frame_right, to = 255)
        self.low_sat.grid(row = 5, column = 0, columnspan = 2, pady = 10, padx = 30, sticky = "we")
       
        self.low_val = customtkinter.CTkSlider(master = self.frame_right, to = 255)
        self.low_val.grid(row = 6, column = 0, columnspan = 2, pady = 10, padx = 30, sticky = "we")
        
        self.high_hue = customtkinter.CTkSlider(master = self.frame_right, to = 255)
        self.high_hue.grid(row = 8, column = 0, columnspan = 2, pady = 10, padx = 30, sticky = "we")
       
        self.high_sat = customtkinter.CTkSlider(master = self.frame_right, to = 255)
        self.high_sat.grid(row = 9, column = 0, columnspan = 2, pady = 10, padx = 30, sticky = "we")
       
        self.high_val = customtkinter.CTkSlider(master = self.frame_right, to = 255)
        self.high_val.grid(row = 10, column = 0, columnspan = 2, pady = 10, padx = 30, sticky = "we")
        
        #frame to display
        self.frame_right.rowconfigure((0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16), weight = 1)
        self.frame_right.rowconfigure(20, weight = 10)
        self.frame_right.columnconfigure((0, 1), weight = 1)
        self.frame_right.columnconfigure(2, weight = 0)
        
        
        #display to stream feed
        self.frame_info = customtkinter.CTkFrame(master = self.frame_right)
        self.frame_info.grid(row = 0, column = 0, columnspan = 2, rowspan = 4, pady = 20, padx = 20, sticky = "nsew")
        self.frame_info.rowconfigure(0, weight = 1)
        self.frame_info.columnconfigure(0, weight = 1)
        
        self.canvas = tkinter.Canvas(master = self.frame_info)
        self.canvas.grid(column = 0, row = 0, sticky = "nwse", padx = 15, pady = 15)
        
        self.switch = customtkinter.CTkSwitch(master = self.sidebar, text = "Dark Mode", command = self.change_mode)
        self.switch.grid(row = 10, column = 0, pady = 10, padx = 20, sticky = "w")
        
        self.switch_debug = customtkinter.CTkSwitch(master = self.sidebar, text = "Troubleshoot")
        self.switch_debug.grid(row = 9, column = 0, pady = 10, padx = 20, sticky = "w")
        
        #Path for exporting code and screenshot dump
        self.entry = customtkinter.CTkEntry(master = self.frame_right, width = 120, placeholder_text = "Use this as a place to jot down data")
        self.entry.grid(row = 16, column = 0, columnspan = 2, pady = 20, padx = 20, sticky = "we")
        
        self.snapshot = customtkinter.CTkButton(master = self.frame_right, text = "Screenshot", command = self.take_screenshot)
        self.snapshot.grid(row = 16, column = 2, columnspan = 1, pady = 20, padx = 20, sticky = "we")
        
        self.profile = customtkinter.CTkButton(master = self.frame_right, text = "Save Profile", command = self.save_profile)
        self.profile.grid(row = 15, column = 2, columnspan = 1, pady = 20, padx = 20, sticky = "we")
        
        self.load_profile = customtkinter.CTkButton(master = self.frame_right, text = "Load Profile", command = self.load_profile_cmd)
        self.load_profile.grid(row = 14, column = 2, columnspan = 1, pady = 20, padx = 20, sticky = "we")
        
        
        #Constraints
        self.aspect_ratio = customtkinter.CTkLabel(master = self.frame_right, text = "Min Aspect Ratio",  text_font = ("Roboto Medium", -15))  
        self.aspect_ratio.grid(row = 0, column = 2, pady = 10, padx = 50)
        
        self.aspect_slider = customtkinter.CTkSlider(master = self.frame_right, to = 3.0)
        self.aspect_slider.grid(row = 1, column = 2, columnspan = 1, pady = 10, padx = 10, sticky = "we")
        
        self.edges = customtkinter.CTkLabel(master = self.frame_right, text = "Min Edges", text_font = ("Roboto Medium", -15))  
        self.edges.grid(row = 2, column = 2, pady = 10, padx = 50)
        
        self.edges_slider = customtkinter.CTkSlider(master = self.frame_right, to = 20)
        self.edges_slider.grid(row = 3, column = 2, columnspan = 1, pady = 10, padx = 10, sticky = "we")
        
        self.area = customtkinter.CTkLabel(master = self.frame_right, text = "Min Contour Area", text_font = ("Roboto Medium", -15))  
        self.area.grid(row = 5, column = 2, pady = 10, padx = 50)
        
        self.area_slider = customtkinter.CTkSlider(master = self.frame_right, to = 400)
        self.area_slider.grid(row = 7, column = 2, columnspan = 1, pady = 10, padx = 10, sticky = "we")
        
        self.single_target = customtkinter.CTkCheckBox(master = self.frame_right, text = "Single Target")
        self.single_target.grid(row = 0, column = 4, columnspan = 1, pady = 10, padx = 20, sticky = "we")
        
        self.circle_detect = customtkinter.CTkCheckBox(master = self.frame_right, text = "Detect Circles")
        self.circle_detect.grid(row = 1, column = 4, columnspan = 1, pady = 10, padx = 20, sticky = "we")
        

        self.cam = Camera()
        self.delay = 15
                
        #system defaults
        self.low_hue.set(0)
        self.low_val.set(0)
        self.low_sat.set(0)
        
        self.high_hue.set(255)
        self.high_sat.set(255)
        self.high_val.set(255)
        
        #dark mode 
        self.switch.select()
        
      
    def stream(self):    
        self.canvas.destroy()
        
        self.canvas = tkinter.Canvas(master = self.frame_info)
        self.canvas.grid(column = 0, row = 0, sticky = "nwse", padx = 15, pady = 15)
        
        ret, frame = self.cam.get_feed()

        if ret:
            frame = cv.resize(frame, (1000, 500))
            if self.switch_debug.get() == 1:
                grayscale = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
                rt, thresh = cv.threshold(grayscale, 127, 255, 0)
                contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
                cv.drawContours(frame, contours, -1, (0, 255, 255), 3)
                cv.putText(frame, "debug mode", (10, 20), cv.FONT_HERSHEY_COMPLEX, .5, (0, 255, 255), 2)
            
            hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            lower = np.array([int(self.low_hue.get()), int(self.low_val.get()), int(self.low_sat.get())])
            upper = np.array([int(self.high_hue.get()), int(self.high_val.get()), int(self.high_sat.get())])
            mask = cv.inRange(hsv, lower, upper)
            contours = Network.get_contours(mask)
            for contour in contours:         
                approx = cv.approxPolyDP(contour, 0.01 * cv.arcLength(contour, True), True)
                x, y, w, h = cv.boundingRect(contour)
                if self.circle_detect.get() == 1:
                    if isCircle(contour):
                        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                        
                elif self.single_target.get() == 1:
                    quick_sort = sorted(contours, key = cv.contourArea, reverse = True)
                    biggest_contour = cv.contourArea(quick_sort[0])
                    if cv.contourArea(contour) == biggest_contour:
                        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    
                    
                else:
                    if self.aspect_slider.get() + .3 >= w / h >= self.aspect_slider.get() and len(approx) >= self.edges_slider.get() and cv.contourArea(contour) > self.area_slider.get():
                        cv.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            
           
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)
            
        
        self.canvas.after(self.delay, self.stream)
        
    def canny_frame(self):
        self.canvas.destroy()
        
        self.canvas = tkinter.Canvas(master = self.frame_info)
        self.canvas.grid(column = 0, row = 0, sticky = "nwse", padx = 15, pady = 15)
        
        ret, frame = self.cam.get_feed()

        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            frame = cv.resize(frame, (1000, 500))
            frame = cv.Canny(frame, 100, 200)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.canvas.after(self.delay, self.canny_frame)
        
    
    def mask_frame(self):
        self.canvas.destroy()
        self.canvas = tkinter.Canvas(master = self.frame_info)
        self.canvas.grid(column = 0, row = 0, sticky = "nwse", padx = 15, pady = 15)
        
        ret, frame = self.cam.get_feed()

        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
            frame = cv.resize(frame, (1000, 500))
            lower = np.array([int(self.low_hue.get()), int(self.low_val.get()), int(self.low_sat.get())])
            upper = np.array([int(self.high_hue.get()), int(self.high_val.get()), int(self.high_sat.get())])
            frame = cv.inRange(frame, lower, upper)
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = tkinter.NW)

        self.canvas.after(self.delay, self.mask_frame)
    
    def get_contours(mask):
        contours = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
        if len(contours) == 2:
            contours = contours[0]
            
        else:
            contours = contours[1]
        
        return contours
    
    def save_profile(self):
        data = {
            "low sat" : int(self.low_hue.get()),
            "low val" : int(self.low_sat.get()),
            "low hue" : int(self.low_val.get()),
            "high sat" : int(self.high_hue.get()),
            "high val" : int(self.high_sat.get()),
            "high hue" : int(self.high_val.get()),
            "min aspect ratio" : self.aspect_slider.get(),
            "min edges" : int(self.edges_slider.get()),
            "min contour area" : int(self.area_slider.get())
        }
        
        with open(os.path.join(os.getcwd() + "\\profiles", "profile-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".json"), "w") as f:
            json.dump(data, f)
            
    def load_profile_cmd(self):
        filename = filedialog.askopenfilename()
        #system defaults
        with open(filename, "r") as f:
            data = json.load(f)
            
        self.low_hue.set(data["low hue"])
        self.low_val.set(data["low sat"])
        self.low_sat.set(data["low val"])
        
        self.high_hue.set(data["high hue"])
        self.high_sat.set(data["high sat"])
        self.high_val.set(data["high val"])
        
        self.aspect_slider.set(data["min aspect ratio"])
        self.edges_slider.set(data["min edges"])
        self.area_slider.set(data["min contour area"])
        
        
    def take_screenshot(self):
        ret, frame = self.cam.get_feed()
        if ret:
            cv.imwrite(os.path.join(os.getcwd() + "\\screenshots", ("stream-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".png")), frame)
    
    def change_mode(self):
        if self.switch.get() == 1:
            customtkinter.set_appearance_mode("dark")
            
        else:
            customtkinter.set_appearance_mode("light")
    
    def get_slider_value(value):
        print(value)

    def ping(self):
        print("Functional!")
    
    def on_closing(self, event = 0):
        self.destroy()
        sys.exit()
    
    def start(self):
        self.mainloop()
    
    
if __name__ == "__main__":
    hawk = Network()
    hawk.start()

     