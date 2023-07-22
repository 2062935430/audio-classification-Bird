import os
import numpy as np
import scipy.signal as signal
import soundfile as sf
from tqdm import tqdm
from scipy.io import wavfile


def bandpass_filter(input_file, output_file, center_freq, bandwidth):
    # 读取音频文件
    audio_data, sample_rate = sf.read(input_file)

    # 计算滤波器参数
    nyquist_freq = 0.5 * sample_rate
    normalized_center = center_freq / nyquist_freq
    normalized_bandwidth = bandwidth / nyquist_freq

    # 设计带通滤波器
    b, a = signal.butter(4, [normalized_center - 0.5 * normalized_bandwidth,
                             normalized_center + 0.5 * normalized_bandwidth], btype='band')

    # 应用滤波器
    filtered_audio = signal.lfilter(b, a, audio_data)

    # 保存滤波后的音频文件
    sf.write(output_file, filtered_audio, sample_rate)


def process_audio_folder(input_folder, output_folder, center_freq, bandwidth):
    # 统计音频文件数量
    total_files = sum([len(files) for _, _, files in os.walk(input_folder) if files])

    # 遍历输入文件夹及其子文件夹中的音频文件，并显示进度
    with tqdm(total=total_files, desc="Filtering Audio", unit="file") as pbar:
        for dirpath, dirnames, filenames in os.walk(input_folder):
            for filename in filenames:
                if filename.endswith(".wav"):  # 仅处理wav格式的音频文件，可根据实际需求修改
                    input_file = os.path.join(dirpath, filename)
                    relative_path = os.path.relpath(input_file, input_folder)
                    output_file = os.path.join(output_folder, relative_path)

                    # 创建输出文件夹（如果不存在）
                    os.makedirs(os.path.dirname(output_file), exist_ok=True)

                    # 应用带通滤波器并保存为输出文件
                    bandpass_filter(input_file, output_file, center_freq, bandwidth)

                    pbar.update(1)  # 更新进度条


def process_audio_list(input_list_file, output_folder, center_freq, bandwidth):
    # 使用TxtListFiles加载数据列表
    file_paths = TxtListFiles(input_list_file)

    # 统计音频文件数量
    total_files = len(file_paths)

    # 遍历数据列表中的音频文件，并显示进度
    with tqdm(total=total_files, desc="Filtering Audio", unit="file") as pbar:
        for input_file in file_paths:
            if input_file.endswith(".wav"):
                relative_path = os.path.relpath(input_file, os.path.dirname(input_list_file))
                output_file = os.path.join(output_folder, relative_path)

                # 创建输出文件夹（如果不存在）
                os.makedirs(os.path.dirname(output_file), exist_ok=True)

                # 读取音频文件
                sample_rate, audio_data = wavfile.read(input_file)

                # 应用带通滤波器并保存为输出文件
                bandpass_filter(input_file, output_file, center_freq, bandwidth)

                pbar.update(1)  # 更新进度条


# 示例用法
input_folder = "C:/Users/admin\Desktop/audio-classification/杜鹃科声音"  # 输入文件夹的路径
output_folder = "C:/Users/admin\Desktop/audio-classification/output_folder"  # 输出文件夹的路径
center_freq = 3000  # 带通滤波器的中心频率
bandwidth = 1000  # 带通滤波器的带宽

# 创建数据列表
txt_file = "data_list.txt"
with open(txt_file, 'w') as f:
    for dirpath, dirnames, filenames in os.walk(input_folder):
        for filename in filenames:
            if filename.endswith(".wav"):
                file_path = os.path.join(dirpath, filename)
                f.write(file_path + '\n')

# 使用数据列表加载处理音频数据
process_audio_list(txt_file, output_folder, center_freq, bandwidth)