import os
import tkinter as tk
from pytubefix import YouTube
from pytubefix.cli import on_progress
import subprocess

def convert_mp4_to_m4a(input_path, output_path):
    # FFmpeg 命令
    ffmpeg_cmd = [
        "ffmpeg",
        "-i", input_path,  # 輸入文件
        "-vn",             # 排除視頻流
        "-acodec", "copy", # 保持音頻編碼
        output_path        # 輸出文件
    ]
    
    # 執行 FFmpeg 命令
    try:
        subprocess.run(ffmpeg_cmd, check=True)
        print(f"轉換成功！音訊文件儲存為: {output_path}")
    except subprocess.CalledProcessError as e:
        print(f"轉換失敗！錯誤信息: {e}")

def rbVideo():
    global getvideo
    labelMsg.config(text="")
    getvideo = videorb.get()
    labelMsg.config(text=f"當前選擇: {getvideo}")

def clickDown_video():
    global getvideo, strftype, listradio
    labelMsg.config(text="")
    if(url.get() == ""):
        labelMsg.config(text="網址欄位必須輸入!")
        return

    if(path.get() == ""):
        pathdir = "Downloads"

    else:
        pathdir = path.get()
        pathdir = pathdir.replace("\\","\\\\")

    try:
        yt = YouTube(url.get(), on_progress_callback = on_progress)
        #print(yt.streams.filter)
        video_stream = yt.streams.filter(file_extension='mp4', res=getvideo, adaptive=True).first()
        audio_stream = yt.streams.filter(file_extension='mp4', res="360p").first()

        if os.path.exists( f"output_dir/{yt.title}.mp4") == False:
            print("正在下載影像流...")
            labelMsg.config(text="正在下載影像流...")
            video_stream.download(output_path="output_dir", filename="video")
            video_path = os.path.join("output_dir/video.mp4")
            print("影像下載完成！")
            labelMsg.config(text="影像下載完成！")

            print("正在下載音訊流...")
            labelMsg.config(text="正在下載音訊流...")
            audio_stream.download(output_path="output_dir", filename="audio")    
            input_path = os.path.join("output_dir/audio.mp4")
            convert_mp4_to_m4a("output_dir/audio.mp4", "output_dir/audio.m4a")
            audio_path = os.path.join("output_dir/audio.m4a")
            print("音訊下載完成！")
            labelMsg.config(text="音訊下載完成！")

            output_path = os.path.join(f"output_dir/{yt.title}.mp4")

            print("正在合併影像和音訊...")
            labelMsg.config(text="正在合併影像和音訊...")
            ffmpeg_cmd = [
                "ffmpeg",
                "-i", video_path,        # 視訊輸入
                "-i", audio_path,        # 音訊輸入
                "-c:v", "copy",          # 保持原始影像編碼
                "-c:a", "aac",           # 音訊使用 AAC 編碼
                "-strict", "experimental",
                output_path              # 合成後的輸出檔案
            ]

            # 執行 FFmpeg 命令
            subprocess.run(ffmpeg_cmd, check=True)
            print(f"合成完成！檔案儲存至: {output_path}")
            labelMsg.config(text=f"合成完成！檔案儲存至: {output_path}")
        os.remove(video_path)
        os.remove(audio_path)
        os.remove(input_path)

        full_path = os.path.join(output_path)
        if os.path.exists(full_path):
            print("下載完成!")
            labelMsg.config(text="下載完成!")

        elif os.path.exists( f"output_dir/{yt.title}.mp4") == True:
            print("已有此檔案!")

    except:
        if os.path.exists( f"output_dir/{yt.title}.mp4") == True:
            print("已有此檔案!")
            labelMsg.config(text="已有此檔案!")
        else:
            labelMsg.config(text="影片無法下載!")
    
    
def clickDown_audio():
    global getvideo
    labelMsg.config(text="")
    if(url.get() == ""):
        labelMsg.config(text="網址欄位必須輸入!")
        return

    if(path.get() == ""):
        pathdir = "Downloads"

    else:
        pathdir = path.get()
        pathdir = pathdir.replace("\\","\\\\")

    try:
        yt = YouTube(url.get(), on_progress_callback = on_progress)
        audio_stream = yt.streams.filter(file_extension='mp4', res="360p").first()
        print("正在下載音訊流...")
        labelMsg.config(text="正在下載音訊流...")
        audio_stream.download(output_path="output_dir", filename="audio")    
        input_path = os.path.join("output_dir/audio.mp4")

        if os.path.exists( f"output_dir/{yt.title}.m4a") == False:
            convert_mp4_to_m4a("output_dir/audio.mp4", f"output_dir/{yt.title}.m4a")
            audio_path = os.path.join(f"output_dir/{yt.title}.m4a")
            print("音訊下載完成！")
        elif os.path.exists( f"output_dir/{yt.title}.m4a") == True:
            print("已有此檔案!")

        os.remove(input_path)
        full_path = os.path.join(audio_path)
        if os.path.exists(full_path):
            print("下載完成!")
            labelMsg.config(text="下載完成!")
        os.remove(input_path)
    
    except:
        if os.path.exists( f"output_dir/{yt.title}.m4a") == True:
            print("已有此檔案!")
            labelMsg.config(text="已有此檔案!")
        else:
            labelMsg.config(text="音訊無法下載!")
    

win = tk.Tk()
win.geometry("560x280")
win.title("yt-dl")
videorb = tk.StringVar(value="360p")
url = tk.StringVar()
path = tk.StringVar()

label_1 = tk.Label(win, text="Youtube url:")
label_1.place(x=123, y=30)
enteryUrl = tk.Entry(win, textvariable=url)
enteryUrl.config(width=45)
enteryUrl.place(x=220, y=30)

label_2 = tk.Label(win, text="存檔路徑(預設為Downloads資料夾):")
label_2.place(x=10, y=70)
enteryPath = tk.Entry(win, textvariable=path)
enteryPath.config(width=45)
enteryPath.place(x=220, y=70)

btvDown = tk.Button(win, text="下載影片", command=clickDown_video)
btvDown.place(x=200, y=110)

rb_1 = tk.Radiobutton(win, text='360p, mp4', variable=videorb, value='360p', command=rbVideo)
rb_1.place(x=180, y=150)

rb_2 = tk.Radiobutton(win, text='720p, mp4', variable=videorb, value='720p', command=rbVideo)
rb_2.place(x=180, y=180)

rb_3 = tk.Radiobutton(win, text='1080p, mp4', variable=videorb, value='1080p', command=rbVideo)
rb_3.place(x=180, y=210)

btaDown = tk.Button(win, text="下載音訊", command=clickDown_audio)
btaDown.place(x=320, y=110)

rb_4 = tk.Radiobutton(win, text='m4a', variable=videorb, value='audio', command=rbVideo)
rb_4.place(x=320, y=150)

labelMsg = tk.Label(win, text="", fg="red")
labelMsg.place(x=200, y=240)

win.mainloop()