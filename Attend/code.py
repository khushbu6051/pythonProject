import tkinter as tk
from tkinter import Message ,Text
import pyttsx3
import cv2,os
import shutil
import csv
import numpy as np
from PIL import Image, ImageTk
import pandas as pd
import datetime
import time
import serial
from time  import sleep
import yagmail
import tkinter.ttk as ttk
import tkinter.font as font
ser = serial.Serial('com3', 9600)
engine= pyttsx3.init('sapi5')
voice = engine.getProperty('voices')

window = tk.Tk()
window.title("Attendance MS")
engine.say('Welcome-to-Face-Recognize-system')
engine.runAndWait()
path = 'logo.jpg'
img = ImageTk.PhotoImage(Image.open(path))
panel = tk.Label(window, image = img)
panel.pack(side = "bottom", fill = "both", expand = "yes")
message = tk.Label(window, text=" Face Attendance System" ,bg="white"  ,fg="black"  ,width=21  ,height=1,font=('times', 24, 'italic bold'))
message.place(x=10, y=10)

message = tk.Label(window, text=" " ,bg="white"  ,fg="black"  ,width=60  ,height=13,font=('times', 10, 'italic bold'))
message.place(x=30, y=130)

message = tk.Label(window, text="New Users" ,bg="white"  ,fg="black"  ,width=25  ,height=2,font=('times', 20, 'italic bold'))
message.place(x=40, y=130)

lbl = tk.Label(window, text="Enter ID:",width=13  ,height=1  ,fg="black"  ,bg="white" ,font=('times', 13, ' bold '))
lbl.place(x=45, y=195)

txt = tk.Entry(window,width=20  ,bg="white" ,fg="black",font=('times', 15, ' bold '))
txt.place(x=183, y=195)

lbl2 = tk.Label(window, text="Enter Name:",width=13  ,fg="black"  ,bg="white"    ,height=2 ,font=('times', 13, ' bold '))
lbl2.place(x=45, y=226)

txt2 = tk.Entry(window,width=20  ,bg="white"  ,fg="black",font=('times', 15, ' bold '))
txt2.place(x=183, y=235)

message = tk.Label(window, text=" " ,bg="white"  ,fg="white"  ,width=60  ,height=7,font=('times', 10, 'italic bold'))
message.place(x=30, y=365)

lbl3 = tk.Label(window, text="Attendance : ",width=10  ,fg="black"  ,bg="white"  ,height=2 ,font=('times', 13, ' bold '))
lbl3.place(x=10, y=395)

message2 = tk.Label(window, text="" ,fg="black"   ,bg="white",activeforeground = "green",width=38 ,height=5  ,font=('times', 13, ' bold '))
message2.place(x=163, y=365)

message = tk.Label(window, text="Designed By:- Khushbu Gupta" ,bg="white"  ,fg="black"  ,width=26  ,height=1,font=('times', 18, 'italic bold'))
message.place(x=20, y=507)

#clear id in entry box
def clear():
    txt.delete(0, 'end')
    res = ""
    message.configure(text= res)

#clear name in entry box
def clear2():
    txt2.delete(0, 'end')
    res = ""
    message.configure(text= res)

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False
def TakeImages():
    Id=(txt.get())
    name=(txt2.get())
    if(is_number(Id) and name.isalpha()):
        cam = cv2.VideoCapture(0)
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector=cv2.CascadeClassifier(harcascadePath)
        sampleNum=0
        while(True):
            ret, img = cam.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = detector.detectMultiScale(gray, 1.3, 5)
            for (x,y,w,h) in faces:
                cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
                #incrementing sample number
                sampleNum=sampleNum+1
                #saving the captured face in the dataset folder TrainingImage
                cv2.imwrite("TrainingImage\ "+name +"."+Id +'.'+ str(sampleNum) + ".jpg", gray[y:y+h,x:x+w])
                #display the frame
                cv2.imshow('Facial Recognition',img)
            if cv2.waitKey(100) & 0xFF == ord('q'):
                break
            elif sampleNum>60:
                break
        engine.say('Dataset-Created')
        engine.runAndWait()
        cam.release()
        cv2.destroyAllWindows()
        res = "Dataset Created"
        row = [Id , name]
        with open('StudentDetails\StudentDetails.csv','a+') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        message.configure(text= res)

    else:
        if(is_number(Id)):
            res = "Enter Alphabetical Name"
            message.configure(text= res)
        if(name.isalpha()):
            res = "Enter Numeric Id"
            message.configure(text= res)

def TrainImages():
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector =cv2.CascadeClassifier(harcascadePath)
    faces,Id = getImagesAndLabels("TrainingImage")
    recognizer.train(faces, np.array(Id))
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Dataset Trained Successfully"
    message.configure(text= res)
    engine.say('Dataset-Trained-Successfully')
    engine.runAndWait()

def getImagesAndLabels(path):
    #get the path of all the files in the folder
    imagePaths=[os.path.join(path,f) for f in os.listdir(path)]
    #print(imagePaths)
    #create empth face list
    faces=[]
    #create empty ID list
    Ids=[]
    #now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        #loading the image and converting it to gray scale
        pilImage=Image.open(imagePath).convert('L')
        #Now we are converting the PIL image into numpy array
        imageNp=np.array(pilImage,'uint8')
        #getting the Id from the image
        Id=int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(Id)
    return faces,Ids

def TrackImages():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("C:/Users/CG-DTE/PycharmProjects/pythonProject1/Attend/TrainingImageLabel" + os.sep + "Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("C:/Users/CG-DTE/PycharmProjects/pythonProject1/Attend/StudentDetails" + os.sep + "StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time', 'Temp','Status']
    attendance = pd.DataFrame(columns=col_names)

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        print('wait...')
        for x in range(100):
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5, minSize=(int(minW), int(minH)),
                                                 flags=cv2.CASCADE_SCALE_IMAGE)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (10, 159, 255), 2)
                Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if conf<75:
                    aa = df.loc[df['Id'] == Id]['Name'].values
                    confstr = "  {0}%".format(round(100 - conf))
                    tt = str(Id) + "-" + aa
                    facecheck = 0
                    print(tt)


                else:
                    facecheck=1
                    aa= '  Unknown  '
                    Id = '  Unknown  '
                    tt = str(Id)+ "-" + aa
                    confstr = "  {0}%".format(round(100 - conf))

                if (100 - conf) > 50:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = str(aa)[2:-2]

                tt = str(tt)[2:-2]
                if (100 - conf) > 67:
                    tt = tt + " [Pass]"
                    cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

                if (100 - conf) > 67:
                    cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 0), 1)
                elif (100 - conf) > 50:
                    cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
                else:
                    cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)

            cv2.imshow('Attendance', im)
            time.sleep(0.01)
            if (cv2.waitKey(1) == ord('q')):
                break
        ini = 'A'
        ser.write(str.encode(ini))
        sleep(0.1)
        ser_bytes = ser.readline()
        string_n = ser_bytes.decode()  # decode byte string into Unicode
        string = string_n.rstrip()
        print(string)
        temp= float(string)
        if temp > 95:
            status='Absent'
        else:
            status = 'Present'
        temp1 =float ((temp-32)*(5/9))
        temp1="{:.2f}".format(temp1)
        if facecheck == 0:
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            attendance.loc[len(attendance)] = [Id, aa, date, timeStamp,temp1,status]
            attendance = attendance.drop_duplicates(subset=['Id'], keep='first')

            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            Hour, Minute, Second = timeStamp.split(":")
            fileName = "Attendance" + os.sep + "Attendance_" + date + ".csv"
            attendance.to_csv(fileName, index=False, mode='a')
            print("Attendance Successful")
            engine.say(f'Thank-you-{aa}-Your-attendance-updated and   Your tempereture is {temp1}')
            engine.runAndWait()
            res = attendance
            message2.configure(text=res)
            if (cv2.waitKey(1) == ord('q')):
                break
        else:
            engine.say(f'Sorry-unknow-Your-attendance-will not updated ')
            engine.runAndWait()

        engine.say('Next please')
        engine.runAndWait()
        time.sleep(4)
    cam.release()
    cv2.destroyAllWindows()
    #print(attendance)
def email():

    date = datetime.date.today().strftime("%B %d, %Y")
    path = 'C:/Users/CG-DTE/PycharmProjects/pythonProject1/Attend/Attendance'
    os.chdir(path)
    files = sorted(os.listdir(os.getcwd()), key=os.path.getmtime)
    newest = files[-1]
    filename = newest
    sub = "Attendance Report for " + str(date)
    # mail information
    yag = yagmail.SMTP(user="khush150669@gmail.com", password='Khu$h@6051')
    body = "kindly Find Attachment"
    # sent the mail
    yag.send(
        to="khush150669@gmail.com",
        subject=sub,  # email subject
        contents=body,  # email body
        attachments=filename  # file attached
    )
    engine.say('Email Sent Successfully')
    engine.runAndWait()
    print("Email Sent!")

clearButton = tk.Button(window, text="-", command=clear  ,fg="white"  ,bg="red"  ,width=3  ,height=1 ,activebackground = "Red" ,font=('times', 10, ' bold '))
clearButton.place(x=400, y=195)

clearButton2 = tk.Button(window, text="-", command=clear2  ,fg="white"  ,bg="red"  ,width=3  ,height=1, activebackground = "Red" ,font=('times', 10, ' bold '))
clearButton2.place(x=400, y=235)

takeImg = tk.Button(window, text="Register", command=TakeImages  ,fg="white"  ,bg="grey"  ,width=10  ,height=1, activebackground = "aqua" ,font=('times', 15, ' bold '))
takeImg.place(x=100, y=280)

trainImg = tk.Button(window, text="Trained", command=TrainImages  ,fg="white"  ,bg="blue"  ,width=10  ,height=1, activebackground = "gold" ,font=('times', 15, ' bold '))
trainImg.place(x=260, y=280)

trackImg = tk.Button(window, text="Mark Attendance", command=TrackImages  ,fg="white"  ,bg="green"  ,width=14  ,height=1, activebackground = "lime" ,font=('times', 15, ' bold '))
trackImg.place(x=20, y=70)

trackImg = tk.Button(window, text="Mail Attendence", command=email  ,fg="white"  ,bg="red"  ,width=14  ,height=1, activebackground = "lime" ,font=('times', 15, ' bold '))
trackImg.place(x=250, y=70)

window.mainloop()
