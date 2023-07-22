# 导入需要的模块
import numpy as np
import librosa.display
import matplotlib.pyplot as plt
import os
import matplotlib.pyplot as plt
from tqdm import tqdm


# 定义预加重函数
def pre_fun(x, a):  # 定义预加重函数，增加一个参数a表示预加重系数
    signal_points = len(x)  # 获取语音信号的长度
    signal_points = int(signal_points)  # 把语音信号的长度转换为整型
    # s=x  # 把采样数组赋值给函数s方便下边计算
    for i in range(1, signal_points, 1):  # 对采样数组进行for循环计算
        x[i] = x[i] - a * x[i - 1]  # 一阶FIR滤波器，使用参数a作为预加重系数
    return x  # 返回预加重以后的采样数组


# 定义一个函数，用于遍历大文件夹下的所有小文件夹，并且找到所有的WAV文件
def process_wav_files(root_dir, output_dir):
    # 遍历根目录下的所有子目录和文件
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 遍历每个文件
        for filename in tqdm(filenames):
            # 判断文件是否是WAV格式
            if filename.endswith('.wav'):
                # 获取文件的完整路径
                file_path = os.path.join(dirpath, filename)
                # 获取文件的相对路径（相对于根目录）
                relative_path = os.path.relpath(file_path, root_dir)
                # 获取文件的不带扩展名的名字
                file_name = os.path.splitext(filename)[0]
                # 读取语音文件并绘制波形图
                times = librosa.get_duration(filename=file_path)  # 获取音频时长
                y, sr = librosa.load(file_path, sr=8000, offset=0.0, duration=None)  # 返回音频采样数组及采样率
                x = np.arange(0, times, 1 / sr)  # 时间刻度
                # 预加重，传入不同的预加重系数
                pre_emphasis_100 = pre_fun(y, 1.00)  # 预加重系数为1.00
                # 创建一个新的图像，并清除之前的图像
                fig, ax = plt.subplots(num=1, clear=True)
                plt.plot(x, pre_emphasis_100)  # 绘制预加重后的波形图，预加重系数为1.00
                plt.xlabel('times')  # x轴时间
                plt.ylabel('amplitude')  # y轴振幅
                plt.title(file_name + '.wav', fontsize=12, color='black')  # 标题名称、字体大小、颜色
                # 创建输出目录（如果不存在）
                output_path = os.path.join(output_dir, relative_path)
                output_dirname = os.path.dirname(output_path)
                if not os.path.exists(output_dirname):
                    os.makedirs(output_dirname)
                # 设置字体为SimHei
                plt.rcParams['font.sans-serif'] = ['SimHei']
                plt.rc('axes', unicode_minus=False)
                # 保存波形图到输出目录，并且命名为和原始文件相同的名字（或者加上前缀或后缀）
                plt.savefig(output_path + '_100.png')

                plt.close('all')


# 调用函数，传入根目录和输出目录
process_wav_files('C:/Users/admin/Desktop/audio-classification/杜鹃科声音',
                  'C:/Users/admin/Desktop/audio-classification/waveforms')
