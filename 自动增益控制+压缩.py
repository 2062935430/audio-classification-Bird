import os
import soundfile as sf
import numpy as np
import scipy.signal as signal
import librosa
from tqdm import tqdm


class GainControl:
    def __init__(self, agc_threshold=0.01, compression_ratio=2.0):
        self.agc_threshold = agc_threshold
        self.compression_ratio = compression_ratio
        self.gain = 1.0

    def process(self, audio):
        # 计算音频信号的均方根值
        rms = np.sqrt(np.mean(audio ** 2))

        # 自动增益控制
        if rms > self.agc_threshold:
            self.gain = 1.0 / rms

        # 压缩
        audio *= self.compression_ratio

        # 应用增益
        audio *= self.gain

        return audio


def process_audio_files(input_folder, output_folder):
    # 创建增益控制对象
    gain_ctrl = GainControl(agc_threshold=0.01, compression_ratio=2.0)

    # 获取输入文件夹下所有音频文件的路径列表
    audio_files = []
    for root, dirs, files in os.walk(input_folder):
        for file in files:
            if file.endswith('.wav'):
                input_file = os.path.join(root, file)
                output_file = os.path.join(output_folder, file)
                audio_files.append((input_file, output_file))

    # 使用tqdm显示处理进度
    for input_file, output_file in tqdm(audio_files, desc='Processing'):
        # 从文件中加载音频数据
        audio, sample_rate = sf.read(input_file)

        # 处理音频数据
        processed_audio = gain_ctrl.process(audio)

        # 将处理后的音频保存到文件
        sf.write(output_file, processed_audio, sample_rate)


# 示例用法：将input_folder中的音频文件进行增益控制并保存到output_folder
process_audio_files('C:/Users/admin/Desktop/audio-classification/杜鹃科声音', 'C:/Users/admin/Desktop/audio-classification/output_folder')