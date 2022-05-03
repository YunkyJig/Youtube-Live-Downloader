import urllib
import m3u8
import streamlink
import os
import sys

# source from 
# https://stackoverflow.com/questions/55631634/recording-youtube-live-stream-to-file-in-python

# to convert ts to mp4
# https://superuser.com/questions/692990/use-ffmpeg-copy-codec-to-combine-ts-files-into-a-single-mp4

# ffmpeg with python
# https://stackoverflow.com/questions/42438380/ffmpeg-in-python-script

# TODO create script to find livestream of a channel
# TODO pipe ffmpeg output elsewhere

def convertTsFilesToMp4():
    os.system("rm all.mp4")
    os.system("ffmpeg -f concat -i tsList.txt -c copy all.ts")
    print("Converting ts files to final mp4")
    os.system("ffmpeg -i all.ts -acodec copy -vcodec copy all.mp4")
    print('deleting ts files...')
    os.system("rm *.ts")
    print('done')

def errorHandler(errorType='unknown'):
    if(errorType == 'unknown'):
        convertTsFilesToMp4()
        sys.exit(1)
    else:
        if(input('Shutting down the stream download.\nWould you like to convert the downloaded ts files to an mp4?(y/n):') == 'n'):
            sys.exit(1)
        else:
            convertTsFilesToMp4()
            sys.exit(1)

def get_stream(url):
    """
    Get upload chunk url
    """
    streams = streamlink.streams(url)
    stream_url = streams["best"]

    m3u8_obj = m3u8.load(stream_url.args['url'])
    return m3u8_obj.segments[0]

def dl_stream(url, filename, pre_time_stamp):
    try:
        stream_segment = get_stream(url)
        
        cur_time_stamp = \
            stream_segment.program_date_time.strftime("%Y%m%d-%H%M%S")

        if pre_time_stamp == cur_time_stamp:
            return pre_time_stamp
        else:
            print(cur_time_stamp)
            file = open(filename + '_' + str(cur_time_stamp) + '.ts', 'ab+')
            with urllib.request.urlopen(stream_segment.uri) as response:
                html = response.read()
                file.write(html)
            pre_time_stamp = cur_time_stamp

            fileToAdd = filename + '_' + str(cur_time_stamp) + '.ts'
            with open('tsList.txt', 'a+') as f:
                f.write('file ' + '\'' + fileToAdd + '\'' + '\n')
            print('file added to list')

        return pre_time_stamp
    except KeyboardInterrupt:
        errorHandler('keyboardInterrupt')
    except:
        errorHandler()

def dl_num_stream_chunks(url, filename, chunks):
    """
    Download a finite amount of chunks
    """
    pre_time_stamp = 0
    for i in range(chunks+1):
        pre_time_stamp = dl_stream(url, filename, pre_time_stamp)

def dl_stream_infinite(url, filename):
    """
    Download stream chunks until stream ends/user interrupt
    """
    pre_time_stamp = 0
    while(1):
        pre_time_stamp = dl_stream(url, filename, pre_time_stamp)