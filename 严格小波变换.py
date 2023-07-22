# 导入需要的库
import numpy as np  # 用于处理数值数组
from pydub import AudioSegment  # 用于读取和保存音频文件
from scipy.io import wavfile  # 用于读取和写入wav格式的音频文件
import pywt  # 用于进行小波变换和阈值处理
import os  # 用于操作文件和目录


# 定义一个函数，用于对音频数据进行小波阈值降噪处理
def wavelet_denoise(audio_data, wavelet, threshold):
    # 使用小波变换将音频数据分解为不同尺度的系数
    coeffs = pywt.wavedec(audio_data, wavelet)
    # 对每一层的系数进行软阈值处理，去除低能量的噪声成分
    thresholded_coeffs = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]
    # 使用逆小波变换将处理后的系数重构为降噪后的音频数据
    denoised_data = pywt.waverec(thresholded_coeffs, wavelet)

    return denoised_data


# 定义一个函数，用于对一个音频文件进行小波阈值降噪处理，并保存为新的文件
def denoise_audio_file(input_audio_file, output_audio_file):
    # 使用pydub库从输入文件中读取音频数据，并转换为wav格式，保存为临时文件
    audio = AudioSegment.from_file(input_audio_file)
    audio.export("temp_audio.wav", format="wav")

    # 使用scipy.io库从临时文件中读取wav格式的音频数据，并转换为浮点数类型，方便进行小波处理
    sample_rate, audio_data = wavfile.read("temp_audio.wav")
    audio_data = audio_data.astype(np.float64)

    # 调用之前定义的函数，对音频数据进行小波阈值降噪处理，需要指定小波类型和阈值大小
    wavelet = "db8"  # 这是一种常用的小波类型，叫做Daubechies 8
    threshold = 10  # 这是一个经验值，可以根据实际情况调整
    denoised_data = wavelet_denoise(audio_data, wavelet, threshold)

    # 将处理后的音频数据转换回整数类型，并使用scipy.io库将其保存为wav格式的临时文件
    denoised_data = denoised_data.astype(np.int16)
    wavfile.write("temp_denoised_audio.wav", sample_rate, denoised_data)

    # 使用pydub库从临时文件中读取降噪后的音频数据，并转换为原始格式，保存为输出文件
    denoised_audio = AudioSegment.from_file("temp_denoised_audio.wav")
    denoised_audio.export(output_audio_file, format="wav")


# 定义你的数据文件夹的路径和音频文件的格式
data_folder = "C:/Users/admin/Desktop/audio-classification/杜鹃科声音"
audio_format = "wav"

# 统计数据文件夹下有多少个音频文件，用于计算进度条百分比
total_files = 0  # 初始化总文件数为0
for subfolder in os.listdir(data_folder):
    subfolder_path = os.path.join(data_folder, subfolder)  # 拼接子文件夹的完整路径
    if os.path.isdir(subfolder_path):  # 判断是否是一个目录
        for audio_file in os.listdir(subfolder_path):  # 遍历子文件夹下的所有文件
            if audio_file.endswith(audio_format):  # 判断是否是指定格式的音频文件
                total_files += 1  # 总文件数加1

# 遍历数据文件夹下的所有子文件夹和音频文件，并记录已处理过的文件数，用于计算进度条百分比
processed_files = 0  # 初始化已处理文件数为0
for subfolder in os.listdir(data_folder):
    subfolder_path = os.path.join(data_folder, subfolder)  # 拼接子文件夹的完整路径
    if os.path.isdir(subfolder_path):  # 判断是否是一个目录
        for audio_file in os.listdir(subfolder_path):  # 遍历子文件夹下的所有文件
            if audio_file.endswith(audio_format):  # 判断是否是指定格式的音频文件
                input_audio_file = os.path.join(subfolder_path, audio_file)  # 拼接输入音频文件的完整路径
                output_audio_file = input_audio_file.replace(audio_format, "denoised." + audio_format)
                # 拼接输出音频文件的完整路径，添加"denoised."前缀以区分原始文件
                denoise_audio_file(input_audio_file, output_audio_file)  # 调用之前定义的函数，对音频文件进行降噪处理
                processed_files += 1  # 已处理文件数加1
                progress = processed_files / total_files * 100  # 计算进度条百分比
                print("已处理音频文件：", input_audio_file, "进度：",
                      "{:.2f}%".format(progress))  # 打印处理过的音频文件的路径和进度条百分比，保留两位小数

print("所有音频文件处理完毕！")  # 打印处理完成的提示
