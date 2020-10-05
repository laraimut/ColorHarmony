from tkinter import filedialog
from tkinter import *
import PIL as PIL
from PIL import Image
from PIL import ImageTk
import cv2
from Solver import Solver
from tkinter import messagebox


def main():
    global panelA, panelB,panelC,textscore,textvalue,lamarunning,btnnew,LastScore,scoreawallabel,lamarunninginfo
    text = Label(root, text="Loading.....", fg="black")
    text.pack(side="left", padx=10, pady=10)
    global path
    path = filedialog.askopenfilename()
    textscore = Label(root, text="", fg="black")
    if len(path) > 0:
        images=cv2.imread(path)
        if (images.shape[0] > 1000 or images.shape[1] > 1000):
            text.destroy()
            messagebox.showerror("Error", "Ukuran lebar atau tinggi Poster melebihi batas")
        else:
            filename,score,time,scoreawal = Solver.Skripsi(images,0)
            LastScore = score
            if score > 2:
                scorevalue = "Sangat Baik"
            elif score > 1.5 and score < 2:
                scorevalue = "Baik"
            else:
                scorevalue = "Kurang Baik"
            ######################################
            image2 = cv2.imread(filename)
            image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
            image2 = PIL.Image.fromarray(image2)
            image2 = PIL.ImageTk.PhotoImage(image2)
            ######################################
            images = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
            images = PIL.Image.fromarray(images)
            images = PIL.ImageTk.PhotoImage(images)
            # the first panel will store our original image
            if panelA is None:
                panelA = Label(image=images)
                panelA.image = images
                panelA.pack(side="left", padx=10, pady=10)
                # while the second panel will store the edge map
                panelB = Label(image=image2)
                panelB.image = image2
                panelB.pack(side="right", padx=10, pady=10)
                score = round(score, 2)
                textscore.configure(text="Skor Harmoni " + "  " + str(score))
                textscore.pack()
                textvalue = Label(root, text=scorevalue, fg="black")
                textvalue.pack()
                time = round(time, 2)
                lamarunninginfo = Label(root, text="Waktu yang diperlukan : ", fg="black")
                lamarunninginfo.pack()
                lamarunning = Label(root, text=str(time) + " " + "second", fg="black")
                lamarunning.pack()
                # scoreawallabel = Label(root, text="Score Awal+" +"  "+str(scoreawal), fg="black")
                # scoreawallabel.pack()
                btnnew = Button(root, text="Generate new color", command=reselect)
                btnnew.pack(side="top", fill="both", expand="no", padx="10", pady="10")
            ###############################################
            else:
                panelA.configure(image=images)
                panelB.configure(image=image2)
                # panelC.configure(image=image2)
                panelA.image = images
                panelB.image = image2
                score = round(score, 2)
                textscore.configure(text="Skor Harmoni " + "  " + str(score))
                textvalue.configure(text=scorevalue)
                time = round(time, 2)
                lamarunninginfo.configure(text="Waktu yang diperlukan :")
                lamarunning.configure(text=str(time) + " " + " second")
                btnnew.configure(text="Generate new color")
            text.destroy()


        # else:
        #     panelA.configure(image=images)
        #     panelB.configure(image=image2)
        #     panelA.image = images
        #     panelB.image = image2

def reselect():
    text = Label(root, text="Loading.....", fg="black")
    text.pack(side="left", padx=10, pady=10)
    images = cv2.imread(path)
    filename,score,time,scoreawal = Solver.Skripsi(images,LastScore)
    if score > 2:
        scorevalue = "Sangat Baik"
    elif score > 1.5 and score < 2:
        scorevalue = "Baik"
    else:
        scorevalue = "Kurang Baik"
    ######################################
    if(len(filename)) > 0 :
        image2 = cv2.imread(filename )
        image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)
        image2 = PIL.Image.fromarray(image2)
        image2 = PIL.ImageTk.PhotoImage(image2)
        ######################################
        images = cv2.cvtColor(images, cv2.COLOR_BGR2RGB)
        images = PIL.Image.fromarray(images)
        images = PIL.ImageTk.PhotoImage(images)
        panelA.configure(image=images)
        panelB.configure(image=image2)
        panelA.image = images
        panelB.image = image2
        # scoreawallabel.configure(text=str(scoreawal))
        score = round(score, 2)
        textscore.configure(text="Skor Harmoni "+"  " +str(score))
        textvalue.configure(text = scorevalue)
        time = round(time, 2)
        lamarunninginfo.configure(text="Waktu yang diperlukan :" )
        lamarunning.configure(text=str(time)+" " + " second")
        btnnew.configure(text="Generate new color")
        text.destroy()

class quitButton(Button):
    def __init__(self, parent):
        Button.__init__(self, parent)
        self['text'] = 'Close'
        # Command to close the window (the destory method)
        self['command'] = parent.destroy
        self.pack(side=BOTTOM)

root = Tk()

panelA = None
panelB = None
panelC = None

root.title("Color Harmony Pallete Generator")
w = Label(root, text="Insert your poster here!", fg="black")
w.pack()
btn = Button(root, text="Select an image", command=main)
btn.pack(side="bottom", fill="both", expand="no", padx="10", pady="10")
quitButton(root)
root.minsize(400, 200)


root.mainloop()
