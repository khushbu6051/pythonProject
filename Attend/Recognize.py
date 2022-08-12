import datetime
import os
import time
from time import sleep
import cv2
import pandas as pd
import serial
ser = serial.Serial('com8', 9600)

#-------------------------
def recognize_attendence():
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    recognizer.read("TrainingImageLabel"+os.sep+"Trainner.yml")
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath)
    df = pd.read_csv("StudentDetails"+os.sep+"StudentDetails.csv")
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time','Temp']
    attendance = pd.DataFrame(columns=col_names)

    # Initialize and start realtime video capture
    cam = cv2.VideoCapture(1, cv2.CAP_DSHOW)
    cam.set(3, 640)  # set video width
    cam.set(4, 480)  # set video height
    # Define min window size to be recognized as a face
    minW = 0.1 * cam.get(3)
    minH = 0.1 * cam.get(4)

    while True:
        print('wait...')
        for x in range(200):
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5,minSize = (int(minW), int(minH)),flags = cv2.CASCADE_SCALE_IMAGE)
            for(x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x+w, y+h), (10, 159, 255), 2)
                Id, conf = recognizer.predict(gray[y:y+h, x:x+w])

                if conf < 100:

                    aa = df.loc[df['Id'] == Id]['Name'].values
                    confstr = "  {0}%".format(round(100 - conf))
                    tt = str(Id)+"-"+aa


                else:
                    Id = '  Unknown  '
                    tt = str(Id)
                    confstr = "  {0}%".format(round(100 - conf))

                if (100-conf) > 50:
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = str(aa)[2:-2]


                tt = str(tt)[2:-2]
                if(100-conf) > 67:
                    tt = tt + " [Pass]"
                    cv2.putText(im, str(tt), (x+5,y-5), font, 1, (255, 255, 255), 2)
                else:
                    cv2.putText(im, str(tt), (x + 5, y - 5), font, 1, (255, 255, 255), 2)

                if (100-conf) > 67:
                    cv2.putText(im, str(confstr), (x + 5, y + h - 5), font,1, (0, 255, 0),1 )
                elif (100-conf) > 50:
                    cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 255, 255), 1)
                else:
                    cv2.putText(im, str(confstr), (x + 5, y + h - 5), font, 1, (0, 0, 255), 1)


            cv2.imshow('Attendance', im)
            time.sleep(0.01)
            if (cv2.waitKey(1) == ord('q')):
                break
        ini ='A'
        ser.write(str.encode(ini))
        sleep(0.1)
        ser_bytes = ser.readline()
        string_n = ser_bytes.decode()  # decode byte string into Unicode
        string = string_n.rstrip()
        print(string)
        attendance.loc[len(attendance)] = [Id, aa, date, timeStamp,string]
        attendance = attendance.drop_duplicates(subset=['Id'], keep='first')
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        Hour, Minute, Second = timeStamp.split(":")
        fileName = "Attendance"+os.sep+"Attendance_"+date+".csv"
        attendance.to_csv(fileName, index=False,mode='a')
        print('Heloo')

        print("Attendance Successful")
        time.sleep(2)
    cam.release()
    cv2.destroyAllWindows()

