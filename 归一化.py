import os
from pathlib import Path
from pydub import AudioSegment
from tqdm import tqdm


def from_files(cls, file_list, format=None, codec=None, parameters=None, start_second=None, duration=None, **kwargs):
    """这是一个自定义的类方法，用于一次性导入多个音频文件，并返回一个 AudioSegment 对象的列表"""
    # 创建一个空列表，用于存储导入的音频对象
    audio_segments = []
    # 遍历文件列表中的每个文件
    for file in file_list:
        # 调用标准的 from_file 方法，导入单个音频文件，并将返回的音频对象添加到列表中
        audio_segment = cls.from_file(file, format=format, codec=codec, parameters=parameters, start_second=start_second,
                                      duration=duration, **kwargs)
        audio_segments.append(audio_segment)
    # 返回音频对象列表
    return audio_segments


def normalize_audio_files(input_audio_files, output_folder):
    """对音频文件列表进行归一化处理并保存为新文件"""
    # 一次性导入所有的音频文件，返回一个 AudioSegment 对象的列表
    # 这里使用了自定义的 from_files 方法，需要将 AudioSegment 类作为第一个参数传入
    audio_segments = from_files(AudioSegment, input_audio_files)
    # 创建一个空白的音频对象，用于叠加归一化后的音频文件
    normalized_audio = AudioSegment.silent()
    # 创建一个进度条对象，用于显示处理过程的百分比和时间
    progress_bar = tqdm(total=len(audio_segments), desc="Processing audio files")
    # 遍历列表中的所有音频对象，并对每个音频对象进行归一化处理
    for audio_segment in audio_segments:
        normalized_segment = audio_segment.apply_gain(-audio_segment.max_dBFS)
        # 将归一化后的音频对象叠加到空白对象上，形成一个新的音频对象
        normalized_audio = normalized_audio.overlay(normalized_segment)
        progress_bar.update(1)  # 更新进度条
    # 关闭进度条
    progress_bar.close()
    # 将归一化后的音频对象导出为一个新的文件，格式为 wav
    normalized_audio.export(output_folder / "normalized.wav", format="wav")


def main():
    """主函数，用于调用其他函数"""
    # 定义数据文件夹的路径和音频文件的格式
    data_folder = Path("C:/Users/admin/Desktop/audio-classification/杜鹃科声音")

    # 定义输出文件夹的路径，运行代码的人可以根据需要修改这个变量的值
    output_folder = Path("C:/Users/admin/Desktop/audio-classification/normalized")

    # 检查输出文件夹是否存在，如果不存在，创建它
    if not output_folder.exists():
        output_folder.mkdir()

    # 检查输出文件夹是否有写入权限，如果没有，修改它
    os.chmod(output_folder, 0o777)

    # 使用glob模块查找数据文件夹下的所有指定格式的音频文件，并存储到一个列表中
    audio_files = list(data_folder.glob(f"**/*.wav"))

    # 调用之前定义的函数，对音频文件列表进行归一化预处理，并保存到输出文件夹中
    normalize_audio_files(audio_files, output_folder)

    # 打印处理完成的提示
    print("所有音频文件处理完毕！")


# 如果这个模块是作为主程序运行，而不是被导入到其他模块中，那么就执行主函数
if __name__ == "__main__":
    main()
