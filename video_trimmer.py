#This script runs a very simple video editor that only allows trimming but with frame precision and possibly very fast. 
#The window has two image widgets that represent the first and last frame of the video to trim, and 2 slide bars to select the start and end frames.
#There is one text input to put the title (video will be formatted as .mp4) and 1 button to proceed and trim. the path will be fixed for now, later on it will open a browse window to select the folder in which to save the trimmed video.

from cgitb import text
from turtle import end_fill, title
import cv2
import os
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk

#the global variables!
folder_path = ""
total_frames = 100
#Defining functions

def trim_and_save(start_frame, end_frame):
    global folder_path

    if folder_path == "":
        warning_popup= Toplevel(root)
        warning_popup.geometry("620x150")
        warning_popup.title("Warning!")
        Label(warning_popup, text= "Folder not selected! I Don't know where to store the video!", font=('Arial')).place(x=50,y=50)

    #This function intializes the video file and then proceeds to loop through all the frames between the start and end and writes them in the video file.
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video_name = inputtxt.get(1.0, "end-1c")
    out = cv2.VideoWriter(folder_path + "//" + video_name + ".mp4", fourcc, 6.0, (640, 480))
    cap.set(1, start_frame-1)
    for frame_num in range(start_frame, end_frame):
        ret,frame = cap.read()
        out.write(frame)

def skip_frames(video_side, direction, start_frame):
    #This function activates when the user presses one of the 4 '> <' buttons that allow to skip 5 frames. 
    if start_frame > 5:
        cap.set(1, start_frame-5)
    ret, frame = cap.read()
    im = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
    imtk = ImageTk.PhotoImage(image = im)
    if video_side == 0:
        if direction == 0:
            start_frame_slider.set(start_frame_slider.get()-5)
        else:
            start_frame_slider.set(start_frame_slider.get()+5)
    else:
        if direction == 0:
            end_frame_slider.set(end_frame_slider.get()-5)
        else:
            end_frame_slider.set(end_frame_slider.get()+5)

def select_folder():
    global folder_path
    folder_path = filedialog.askdirectory()

def select_video(start_frame_slider, end_frame_slider):
    global total_frames, cap
    filename = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("Videos", ["*.mp4*", ".avi", ".wav", ".mkv"]), ("all files", "*.*"), ("Text files", "*.txt*")))
    if filename != "":

        #Initializing video to trim and getting the total number of frames to set up the sliders.
        cap = cv2.VideoCapture(filename)
        total_frames = cap.get(7)
        start_frame_slider.configure(to = total_frames-1)
        end_frame_slider.configure(to = total_frames-1)

#Main starting!
root = Tk()
root.title("Collection Protocol")

#canvases for the two pictures.
start_frame_canvas = Canvas(root, width = 680, height = 500)      
start_frame_canvas.grid(row = 1, column = 0, pady = 20)

end_frame_canvas = Canvas(root, width = 680, height = 500)
end_frame_canvas.grid(row = 1, column = 1, pady = 20)

#frames for the 4 skip buttons.
skip_frame = LabelFrame(root)
skip_frame.grid(row =3, column = 0)

skip_frame2 = LabelFrame(root)
skip_frame2.grid(row =3, column = 1)

save_frame = LabelFrame(root)
save_frame.grid(row =4, column = 1)

file_dialog_frame = LabelFrame(root)
file_dialog_frame.grid(row = 4, column = 0)

#Setting up the sliders.
start_frame_slider = Scale(root, from_=0, to=total_frames, length = 700, orient=HORIZONTAL)
start_frame_slider.grid(row = 2, column = 0, padx = 20, pady = 20)

end_frame_slider = Scale(root, from_=0, to=total_frames, length = 700, orient=HORIZONTAL)
end_frame_slider.grid(row = 2, column = 1, padx = 20, pady = 20)

#Setting up the trim and skip frames buttons.
trim_button = Button(save_frame, text = "Save", command = lambda: trim_and_save(start_frame, end_frame), width = 15)
trim_button.grid(row = 0, column = 1, padx = 20, pady = 20)

select_video_button = Button(file_dialog_frame, text = "Select Video", command = lambda: select_video(start_frame_slider, end_frame_slider), width = 15)
select_video_button.grid(row = 0, column = 0, padx = 20, pady = 20)

select_folder_button = Button(file_dialog_frame, text = "Select Save Folder", command = lambda: select_folder(), width = 15)
select_folder_button.grid(row = 0, column = 1, padx = 20, pady = 20)

skip_button1 = Button(skip_frame, text = "<", command = lambda: skip_frames(0, 0, start_frame), width = 15)
skip_button1.grid(row = 3, column = 0, padx = 30, pady = 20)

skip_button2 = Button(skip_frame, text = ">", command = lambda: skip_frames(0,1, start_frame), width = 15)
skip_button2.grid(row = 3, column = 1, padx = 30, pady = 20)

skip_button3 = Button(skip_frame2, text = "<", command = lambda: skip_frames(1,0, start_frame), width = 15)
skip_button3.grid(row = 3, column = 2, padx = 30, pady = 20)

skip_button4 = Button(skip_frame2, text = ">", command = lambda: skip_frames(1,1, start_frame), width = 15)
skip_button4.grid(row = 3, column = 3, padx = 30, pady = 20)

#Setting up the text box for the video title.
inputtxt = Text(save_frame, height = 1, width = 20)
inputtxt.grid(row = 0, column = 0, padx = 20,  pady = 20)

#Tkinter loop that updates the pictures based on the position of the sliders.
while True:
    start_frame = start_frame_slider.get()
    end_frame = end_frame_slider.get()

    if 'cap' not in locals():
        pass
    else:
        cap.set(1, start_frame)
        ret, frame1 = cap.read()
        cap.set(1, end_frame)
        ret,frame2 = cap.read()
        
        im1 = Image.fromarray(cv2.cvtColor(frame1, cv2.COLOR_BGR2RGB))
        imtk1 = ImageTk.PhotoImage(image = im1)
        im2 = Image.fromarray(cv2.cvtColor(frame2, cv2.COLOR_BGR2RGB))
        imtk2 = ImageTk.PhotoImage(image = im2)

        start_frame_canvas.create_image(20, 20,  anchor = NW, image=imtk1)
        end_frame_canvas.create_image(20, 20, anchor = NW, image = imtk2)

    root.update_idletasks()
    root.update()

