#!/usr/bin/python3

import os
from os.path import splitext, dirname, join, basename
import subprocess
import re
import argparse

#################################################################################################

audio_extract_string = 'ffmpeg -i "{0}" -acodec pcm_s16le -ac 2 -ab 191k -vn -y "{1}.wav"'
audio_convert_string = 'lame --preset cd "{0}.wav" "{1}.mp3"'

#################################################################################################

def get_new_name(dir):
    p = r'(^[^\d]{1,})([\d]*)'
    m = re.search(p, dir)
    chars = m.group(1)
    digits = m.group(2)
    if digits == '':
        digits = '0'
    digits = '{0}'.format(int(digits)+1)
    return chars+digits


def get_all_video_files(dir):
    list_files = list()
    for root, subFolders, files in os.walk(dir):
        for file in files:
            list_files.append(os.path.join(root, file))
    for file in list_files[:]:
        ext = splitext(file)[1]
        if ext not in ['.avi', '.mp4', '.ogg']:
            list_files.remove(file)
    return list_files


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Скрипт ищет в текущей директории и ее поддерикториях '
                                                 'видеофайлы и извлекает из них аудио в формате mp3 с битрейтом 191k.'
                                                 'Текущая директория - это директория из которой был запущен скрипт.\n'
                                                 'Скрипт параметров не имеет.')
    parser.parse_args()

    working_dir = os.getcwd()
    video_files = get_all_video_files(working_dir)
    if not len(video_files):
        print('Не найдено ни одного видеофайла :(')
        exit(1)

    extracted_audio_dir = join(working_dir, 'Extracted audio')
    while True:
        if not os.path.exists(extracted_audio_dir):
            os.mkdir(extracted_audio_dir)
            break
        extracted_audio_dir = get_new_name(extracted_audio_dir)

    print('Найденные видео файлы: {0}'.format(video_files))
    for vfile in video_files:
        wavaudio = join(dirname(vfile), splitext(basename(vfile))[0])
        mp3audio = join(extracted_audio_dir, splitext(basename(vfile))[0])

        process = subprocess.Popen(
            audio_extract_string.format(vfile, wavaudio),
            shell=True,
            stdout=subprocess.PIPE
        )
        process.wait()

        process = subprocess.Popen(
            audio_convert_string.format(wavaudio, mp3audio),
            shell=True,
            stdout=subprocess.PIPE
        )
        process.wait()
        os.remove(wavaudio + '.wav')