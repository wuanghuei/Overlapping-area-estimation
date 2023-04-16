import tkinter as tk
from tkinter import ttk
import TkinterDnD2 as tkd
from TkinterDnD2 import *
import cv2
import numpy as np
from PIL import Image, ImageTk
import overlap
import path 
from main import scene

# create the main window
window = TkinterDnD.Tk()
window.title("Overlapping Area Estimation")

# Initialize the first frame
frame_list = [] # create an empty list to keep track of all frames
frame = tk.Frame(window, width=400, height=300, bg="white")
frame.grid(row=0, column=0, padx=10, pady=10)
frame_list.append(frame) # append the frame to the list of frames

# Label "Drag and drop a video..." at the center of the frame
label = tk.Label(frame, text="Drag and drop a camera...", bg="white")
label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

video_list = []
total = []
first_frame = []
first  = True
# Drag and drop initialization
def drop(event):
    global frame_list
    global first_frame
    if frame in frame_list:
        # Remove the first frame if it is still there
        frame_list[0].destroy()
        frame_list.pop(0)
    else:
        pass
    # Create a new frame for the video
    video_frame = tk.Frame(window, width=400, height=300, bg="white")
    video_frame.grid(row=len(frame_list)//2, column=len(frame_list)%2, padx=10, pady=10)
    video_frame.pack_propagate(0)

    # Create a label for the video and pack it into the new frame
    video_label = tk.Label(video_frame, bg="white")
    video_label.pack(fill=tk.BOTH, expand=True)

    # Label "Camera 1, 2, 3, etc." at the top left of the frame
    label = tk.Label(video_frame, text="Camera {}".format(len(frame_list)+1), bg="white")
    label.place(relx=0, rely=0, anchor=tk.NW)

    # Load the video and display its first frame in the label
    video = event.data

    cap = cv2.VideoCapture(video)
    ret, fram = cap.read()
    
    # Fit the video to the frame size
    
    first_frame.append(fram)
    fram = cv2.resize(fram, (400, 300))
    cv2image = cv2.cvtColor(fram, cv2.COLOR_BGR2RGBA)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    video_label.imgtk = imgtk

    video_label.configure(image=imgtk)

    # Pack the new frame next to the existing frames
    frame_list.append(video_frame) # append the new frame to the list of frames
    video_list.append([cap, video_label]) # append the cap object and the video_label to the list of videos
    #print(video_list)

# Bind the drop event to the frame
window.drop_target_register(tkd.DND_FILES)
window.dnd_bind('<<Drop>>', drop)
k = 0
# Function to remove last frame and play all the videos in the window at once
def play():
    global count
    global total
    global k
    global first
    global scene
    frames = []

    if first == True:
        first = False
        hulls  = overlap.get_hulls(first_frame)
        total.append(hulls)
        prc_frames = overlap.get_lines(hulls,first_frame)
    
        for i in range(len(prc_frames)):

            cv2image = cv2.cvtColor(cv2.resize(prc_frames[i], (400, 300)), cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            
            video_list[i][1].imgtk = imgtk
            video_list[i][1].configure(image=imgtk)

        
    for cap, video_label in video_list:
        
        ret, fram = cap.read()
        if ret:

            frames.append(fram)

    if ret:
        
        hulls  = overlap.get_hulls(frames)
        total.append(hulls)
        prc_frames = overlap.get_lines(hulls,frames)
    
        for i in range(len(prc_frames)):

            cv2image = cv2.cvtColor(cv2.resize(prc_frames[i], (400, 300)), cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            imgtk = ImageTk.PhotoImage(image=img)
            # video_label.imgtk = imgtk
            
            video_list[i][1].imgtk = imgtk
            video_list[i][1].configure(image=imgtk)
            # except:
            #     pass
        window.after(33, play)
    else:
        export(total, scene)
        # schedule the next iteration of the loop at 1/30th of a second
    

# Function to export txt file
def export(total, scenes):
    data = {}
    for i in range(len(total[0])):
        for frame in total:
            if i in data:
                data[i].append(frame[i])
            else:
                data[i] = [frame[i]]
    path.create_txt(data, scenes)
    

    # Export the txt file

    pass       



# Create buttons frame
buttons_frame = tk.Frame(window, bg="white")
buttons_frame.grid(row=0, column=2, padx=10, pady=10, rowspan=2)

# Button "Play" to play all the videos in the window at once
play_button = tk.Button(window, text="Play", command=play)
play_button.grid(row=0, column=2, padx=10, pady=10)


window.mainloop()

