# -*- coding: utf-8 -*-

"""
这个模块用于生成生物声学识别和分类的数据列表。

函数：
    gene_data_list(data_path, list_txt_path, val_rate): 从音频文件中生成训练和验证数据列表。

"""

import os
import logging

import librosa
import numpy as np
from pydub import AudioSegment
from tqdm import tqdm
import shutil

# 设置音频转换器的路径
AudioSegment.converter = "C:\\Users\\admin\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffmpeg = "C:\\Users\\admin\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffmpeg.exe"
AudioSegment.ffprobe = "C:\\Users\\admin\\AppData\\Local\\ffmpegio\\ffmpeg-downloader\\ffmpeg\\bin\\ffprobe.exe"


def gene_data_list(data_path, list_txt_path, val_rate):
    """
      从音频文件中生成训练和验证数据列表。

      参数：
          data_path: 存放音频文件的文件夹的路径。
          list_txt_path: 存放输出txt文件的文件夹的路径。
          val_rate: 验证数据占总数据的比例。

      返回：
          None
      """
    # 设置日志
    logging.basicConfig(filename="gene_data_list.log", level=logging.INFO,
                        format="%(asctime)s - %(levelname)s - %(message)s")
    logging.info("开始生成数据列表")

    # 获取数据路径下的子文件夹
    folders = os.listdir(data_path)

    # 打开训练和验证txt文件进行写入
    train_txt = open(os.path.join(list_txt_path, 'train_list.txt'), 'w')
    val_txt = open(os.path.join(list_txt_path, 'val_list.txt'), 'w')

    # 统计数据路径下的文件总数
    num_total = 0
    for _, _, files in os.walk(data_path):  # 遍历并计数
        for _ in files:
            num_total += 1  # 计算文件夹中的文件数

    # 初始化验证标记和步长
    val_marker = 0
    num_val = num_total * val_rate
    val_step = num_total / num_val

    # 初始化类别编号
    class_num = 0

    # 创建一个进度条用于显示文件夹处理情况
    bar = tqdm(folders, desc="处理文件夹", unit="个")

    # 循环遍历每个文件夹
    for folder in bar:
        # 获取文件夹中的声音文件
        sounds = os.listdir(os.path.join(data_path, folder))

        # 循环遍历每个声音文件
        for sound in sounds:
            # 使用os.path.splitext获取文件名和扩展名
            filename, extension = os.path.splitext(sound)

            # 获取原始文件和保存文件的路径
            origin_path = os.path.join(data_path, folder, sound)
            save_path = os.path.join(data_path, folder, filename + ".wav")

            # 如果保存路径不存在，尝试使用pydub将mp3转换为wav
            if not os.path.exists(save_path):
                try:
                    wav = AudioSegment.from_mp3(origin_path)
                    wav.export(save_path, format="wav")
                except Exception as e:
                    logging.error('数据错误: %s, 消息: %s' % (origin_path, e))
                    continue

                # 尝试使用librosa获取wav文件的时长
                try:
                    duration = librosa.get_duration(filename=save_path)
                except Exception as e:
                    logging.error('数据错误：%s, 消息：%s' % (save_path, e))
                    continue

                # 删除原始文件
                os.remove(origin_path)

                # 如果时长小于3秒，跳过这个文件
                if duration < 3:
                    continue

            # 获取npy路径，将.wav替换为.npy
            npy_path = save_path.replace(".wav", ".npy")

            # 如果验证标记能被验证步长整除，写入验证txt文件，
            # 否则写入训练txt文件，并用制表符分隔文件路径和类别编号
            if val_marker % val_step == 0:
                val_txt.write('%s\t%d\n' % (npy_path, class_num))
            else:
                train_txt.write('%s\t%d\n' % (npy_path, class_num))

            # 验证标记加1
            val_marker += 1

        # 类别编号加1
        class_num += 1

    # 关闭进度条和txt文件
    bar.close()
    train_txt.close()
    val_txt.close()

    # 记录完成信息
    logging.info("完成生成数据列表")


if __name__ == '__main__':
    # 调用gene_data_list函数，传入参数
    gene_data_list(data_path='C:/Users/admin/Desktop/audio-classification/杜鹃科声音',
                   list_txt_path='./TxtListFiles/',
                   val_rate=0.2)

