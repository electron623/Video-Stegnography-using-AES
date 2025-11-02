import cv2
import os

def video_info(path):
    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"❌ Cannot open {path}")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    duration = frame_count / fps if fps > 0 else 0
    fourcc = int(cap.get(cv2.CAP_PROP_FOURCC))
    codec = "".join([chr((fourcc >> 8 * i) & 0xFF) for i in range(4)])
    size = os.path.getsize(path) / (1024 * 1024)  # in MB

    print(f"🎬 {os.path.basename(path)}")
    print(f"    Codec: {codec}")
    print(f"    Resolution: {width}x{height}")
    print(f"    FPS: {fps}")
    print(f"    Frames: {frame_count}")
    print(f"    Duration: {duration:.2f} sec")
    print(f"    File Size: {size:.2f} MB")
    print("-" * 40)
    cap.release()

video_info("video.mp4")
video_info("steged.avi")
