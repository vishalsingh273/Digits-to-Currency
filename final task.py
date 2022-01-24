import requests
import json
from datetime import datetime
import mysql.connector
from gtts import gTTS
import os, sys
from pydub import AudioSegment
import emails
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import subprocess
import pydub
import ffmpeg


url='https://www.boredapi.com/api/activity'
response = requests.get(url)
b=response.json();

c=b['key']



conn = mysql.connector.connect(user='root', password='ricky', host='localhost', database='vishal')


cursor = conn.cursor()
sql = "INSERT INTO Amount (Amount, EntryDate) VALUES (%s, %s)"


values = (c,datetime.now())
cursor.execute(sql,values)

conn.commit()

def number_to_word(number):
    def get_word(n):
        words={ 0:"", 1:"One", 2:"Two", 3:"Three", 4:"Four", 5:"Five", 6:"Six", 7:"Seven", 8:"Eight", 9:"Nine", 10:"Ten", 11:"Eleven", 12:"Twelve", 13:"Thirteen", 14:"Fourteen", 15:"Fifteen", 16:"Sixteen", 17:"Seventeen", 18:"Eighteen", 19:"Nineteen", 20:"Twenty", 30:"Thirty", 40:"Forty", 50:"Fifty", 60:"Sixty", 70:"Seventy", 80:"Eighty", 90:"Ninty" }
        if n<=20:
            return words[n]
        else:
            ones=n%10
            tens=n-ones
            return words[tens]+" "+words[ones]
            
    def get_all_word(n):
        d=[100,10,100,100]
        v=["","Hundred","Thousand","lakh"]
        w=[]
        for i,x in zip(d,v):
            t=get_word(n%i)
            if t!="":
                t+=" "+x
            w.append(t.rstrip(" "))
            n=n//i
        w.reverse()
        w=' '.join(w).strip()
       
        return w

    arr=str(number).split(".")
    number=int(arr[0])
    crore=number//10000000
    number=number%10000000
    word=""
    if crore>0:
        word+=get_all_word(crore)
        word+=" crore "
    word+=get_all_word(number).strip()+" Rupees"+" and "+"zero paisa only"
    
    return word
amountToCurrency=56879412
ss=number_to_word(amountToCurrency)
print(ss)

cursor = conn.cursor()
sql = "INSERT INTO amount2currency (Amount, Currency2TextEnglish) VALUES (%s, %s)"


values = (amountToCurrency,ss)
cursor.execute(sql,values)

conn.commit()

  

language = 'en'
  

myobj = gTTS(text=ss, lang=language, slow=False)

myobj.save("welcome.mp3")
file_name = 'welcome.mp3'
fname = os.path.join(os.path.abspath(__file__), file_name)

mypath = os.path.abspath(__file__)
mydir = os.path.dirname(mypath)
start = os.path.join(mydir, "welecome.mp3")


# Playing the converted file
os.system("welcome.mp3")

#converting mp3 to wav format

src = "welcome.mp3"
dst = "welcome.wav"
dir_path = os.path.dirname(os.path.realpath(__file__))
# subprocess.call(['ffmpeg','-i','welcome.mp3','welcome.wav'])
AudioSegment.converter = "C:\\Users\\visha\\Downloads\\ffmpeg-0.4.5-win32\\"


subprocess.call(['ffmpeg', '-i', 'C:/Users/visha/OneDrive/Desktop/python basics/welcome.mp3',
                   'C:/Users/visha/OneDrive/Desktop/python basics/file.wav'])

audSeg = AudioSegment.from_mp3(src)
audSeg.export(dst, format="wav")



 sender_email = ""
 receiver_email = ""
 message = MIMEMultipart()
 message["From"] = sender_email
 message['To'] = receiver_email
 message['Subject'] = "sending mail using python"
 file = "welcome.mp3"
 attachment = open(file,'rb')
 obj = MIMEBase('application','octet-stream')
 obj.set_payload((attachment).read())
 encoders.encode_base64(obj)
 obj.add_header('Content-Disposition',"attachment; filename= "+file)
 message.attach(obj)
 my_message = message.as_string()
 email_session = smtplib.SMTP('smtp.gmail.com',587)
 email_session.starttls()
 email_session.login(sender_email,'password')
 email_session.sendmail(sender_email,receiver_email,my_message)
 email_session.quit()
 print("YOUR MAIL HAS BEEN SENT SUCCESSFULLY")