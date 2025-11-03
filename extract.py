import cv2
import numpy as np
vid=cv2.VideoCapture("steged.avi")
def extract (video):
    fr_count=1
    ch=0
    text=[]
    while True:
        rend,frame=video.read()
        if not rend or frame is None:
            break
        flat=frame.reshape(-1,3)
        if ch<16 and fr_count%16==0:
            text.append(int(flat[0,0]))
            ch+=1
        fr_count+=1
    text=text[::-1]
    print(text)
    return text

def int_to_hexfile(ilist):
    c=open("fromAES.txt",'r')
    key=c.readlines()[1]
    hex_string = ''.join(f"{num:02x}" for num in ilist)
    with open("toAES.txt", "w") as f:
        f.write(f"{hex_string}\n{key}")
a=extract(vid)
int_to_hexfile(a)
