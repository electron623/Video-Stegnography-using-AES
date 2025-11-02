import cv2
import numpy as np
vid=cv2.VideoCapture("video.mp4")
f= open("video_pixel.txt",'w')
l= open("steg pixel.txt",'w')
s=open("demo.txt",'w')
steg=cv2.VideoCapture("steged.avi")

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
            
            if pas!=0 and frm_count%16==0:
                pixel_value = np.uint8(np.clip(text[pas-1], 0, 255))
                frmod[0, 0, 0] = pixel_value
                print(f"Frame {frm_count}: Embedded value {int(pixel_value)} (original: {text[pas-1]})")
                pas-=1
            
            # Write frame - ensure it's uint8 and contiguous
            if not frmod.flags['C_CONTIGUOUS']:
                frmod = np.ascontiguousarray(frmod, dtype=np.uint8)
            out.write(frmod)
            frm_count+=1
            # Write the pixel value after embedding (before compression)
            # Use flat array for consistent indexing
            flat = frmod.reshape(-1, 3)
            l.write(f'{int(flat[0,0])}\n')
    except Exception as e:
        print(f"Error during embedding: {e}")
    finally:
        vid.release()
        out.release()
show_1stpix(steg,s)

def extract(steg):
    fps=steg.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    Tframes=steg.get(cv2.CAP_PROP_FRAME_COUNT)
    width=int(steg.get(cv2.CAP_PROP_FRAME_WIDTH))
    height=int(steg.get(cv2.CAP_PROP_FRAME_HEIGHT))
    print(f"""Properties of Video:-
      Frames per second:-{fps}
      Total pixels in each frame:-{width*height}
      Total Frames:-{Tframes}
      """)
    # text=[]
    try:
        fr_count=1
        pas=0  
        while True:
            rend,frame=steg.read()
            if not rend or frame is None:
                break
            flat=frame.reshape(-1,3)
            if ch<16 and fr_count%16==0:
                print(f"{int(flat[0,0])}\n")
                text.append(int(flat[0,0]))
                ch+=1
            fr_count+=1
            return text
    except ArithmeticError as e:
        print("Done")
    except Exception as e:
        print(f"Error during extraction: {e}")    
    return text
text=[23, 187, 54, 201, 8, 142, 77, 250, 6, 129, 214, 33, 90, 176, 5, 248]
# embeding(text,vid)
# show_1stpix(steg,f)

# ans=extract(steg)
# print(ans)

