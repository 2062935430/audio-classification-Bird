import os
import numpy as np
import librosa
from scipy.io import wavfile

from tqdm import tqdm


def framing_and_windowing(audio_signal, sample_rate, frame_length, frame_shift):
    frame_length = int(frame_length * sample_rate)
    frame_shift = int(frame_shift * sample_rate)

    # 分帧
    frames = librosa.util.frame(audio_signal, frame_length, frame_shift)

    # 加窗
    window = np.hamming(frame_length)
    frames = frames * window.reshape((-1, 1))

    return frames


def process_audio_folder(input_folder, output_folder, sample_rate, frame_length, frame_shift):
    # 获取输入文件夹下的所有子文件夹和音频文件
    audio_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith(".wav"):
                audio_files.append(os.path.join(root, file))

    # 使用tqdm循环迭代处理音频文件
    for audio_file in tqdm(audio_files, desc="Processing audio"):
        # 构建输出文件的完整路径
        file_name = os.path.basename(audio_file)
        output_file = os.path.join(output_folder, file_name)

        # 调用分帧加窗函数处理单个音频文件
        process_audio_file(audio_file, output_file, sample_rate, frame_length, frame_shift)


def process_audio_file(input_file, output_file, sample_rate, frame_length, frame_shift):
    # 读取音频文件
    audio_signal, _ = librosa.load(input_file, sr=sample_rate)

    # 分帧加窗
    frames = framing_and_windowing(audio_signal, sample_rate, frame_length, frame_shift)

    # 保存处理后的帧为音频文件
    wavfile.write(output_file, sample_rate, frames.astype(np.float32))


input_folder = 'C:/Users/admin/Desktop/audio-classification/杜鹃科声音'
output_folder = 'C:/Users/admin/Desktop/audio-classification/output_folder'
sample_rate = 16000
frame_length = 0.025
frame_shift = 0.01

process_audio_folder(input_folder, output_folder, sample_rate, frame_length, frame_shift)