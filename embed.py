import cv2
import numpy as np
vid=cv2.VideoCapture("video.mp4")
l= open("steg pixel.txt",'w')
steg=cv2.VideoCapture("steged.avi")
def extract_payload(database):
    with open("fromAES.txt", "r") as f:
        hex_data = f.readlines()[0].strip()
        print(hex_data)
    text=[]
    for i in range(0, len(hex_data),2):
        text.append(int(hex_data[i:i+2],16))
    return text

def show_1stpix(video,filee):
    while True:
        rend,frame=video.read()
        if not rend or frame is None:
            break
        frmod=frame.copy()
        flat=frmod.reshape(-1,3)
        filee.write(f"{int(flat[0,0])}\n")
def embeding(text,vid):
    fps=vid.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'FFV1')
    Tframes=vid.get(cv2.CAP_PROP_FRAME_COUNT)
    width=int(vid.get(cv2.CAP_PROP_FRAME_WIDTH))
    height=int(vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"""Properties of Video:-
      Frames per second:-{fps}
      Total pixels in each frame:-{width*height}
      Total Frames:-{Tframes}
      """)
    pas=len(text)
    print(f"Total values to embed: {pas}")
    out = cv2.VideoWriter("steged.avi", fourcc, fps, (width, height))
    frm_count=1
    try:
        while True:
            rend,frame=vid.read()
            if not rend or frame is None:
                break
            frmod = np.array(frame.copy(), dtype=np.uint8)
            #  embedid the encryption into the video 
            if pas!=0 and frm_count%16==0:
                pixel_value = np.uint8(np.clip(text[pas-1], 0, 255))
                print(pixel_value)
                frmod[0, 0, 0] = pixel_value
                print(f"Frame {frm_count}: Embedded value {int(pixel_value)} (original: {text[pas-1]})")
                pas-=1
        # Ensur that the frames a continous to prevent video getting corrupted
            if not frmod.flags['C_CONTIGUOUS']:
                frmod = np.ascontiguousarray(frmod, dtype=np.uint8)
            out.write(frmod)
            frm_count+=1

            flat = frmod.reshape(-1, 3)
            l.write(f'{int(flat[0,0])}\n')
    except Exception as e:
        print(f"Error during embedding: {e}")
    finally:
        vid.release()
        out.release()
# ========================================================================================================================
f= open("fromAES.txt",'r')
text=extract_payload(f)
print(text)
embeding(text,vid)



