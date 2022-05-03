import yt_live_dl
import upload2drive

print('starting stream download')
# resetting list
with open('tsList.txt', 'w') as f:
    f.write('')

url = "https://www.youtube.com/watch?v=N88ZGvXqJ7M"
# dl_stream_infinite(url, "live")
# yt_live_dl.dl_num_stream_chunks(url, "live", 5)
# yt_live_dl.convertTsFilesToMp4()
upload2drive.main()