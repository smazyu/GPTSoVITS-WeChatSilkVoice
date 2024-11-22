import itchat
import sys
import io
import os
import subprocess
import requests
from pydub import AudioSegment
from pydub.exceptions import CouldntDecodeError
from typing import Optional
import pilk  # 假设有 pilk 库来编码 SILK 格式

# 设置 ffmpeg 路径
AudioSegment.ffmpeg = r"F:\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"  # 替换成你自己的路径

# 确保输出流使用 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 使用热登入
itchat.auto_login()

# 获取好友列表
friends = itchat.get_friends()

下载音频
def download_audio_segment(mp3_url: str) -> str:
    filename = mp3_url.split('/')[-1]
    save_path = os.path.join(".", filename)

    response = requests.get(mp3_url)
    with open(save_path, 'wb') as file:
        file.write(response.content)

    return save_path

# 检查音频文件是否损坏
def check_mp3_corruption(audio_path: str) -> bool:
    try:
        audio = AudioSegment.from_mp3(audio_path)
        return len(audio) == 0
    except CouldntDecodeError:
        return True

# 获取音频文件时长
def get_duration(audio_file_path: str) -> float:
    file_extension = os.path.splitext(audio_file_path)[1].lower().replace('.', '')

    if file_extension == 'pcm':
        audio = AudioSegment(
            data=open(audio_file_path, 'rb').read(),
            sample_width=2,
            frame_rate=24000,
            channels=1
        )
    else:
        audio = AudioSegment.from_file(audio_file_path, format=file_extension)

    duration_in_ms = len(audio)
    duration_in_s = duration_in_ms / 1000
    return duration_in_s

# 将 MP3 转换为 SILK 格式
def convert_mp3_to_silk(mp3_file_path: str, silk_file_path: str) -> bool:
    try:
        ffmpeg = "ffmpeg"
        pcm_file_path = "intermediate.pcm"
        # 使用 ffmpeg 将 MP3 转换为 PCM 格式
        command = [ffmpeg, "-y", "-i", mp3_file_path, "-f", "s16le", "-ar", "24000", "-ac", "1", pcm_file_path]
        subprocess.run(command, check=True)

        # 使用 pilk 将 PCM 转换为 SILK 格式
        silk_data = pilk.encode(pcm_file_path, 24000)
        with open(silk_file_path, 'wb') as silk_file:
            silk_file.write(silk_data)

        return True
    except Exception as e:
        print(f"转换失败：{e}")
        return False

# 主逻辑
def main(mp3_url: str, silk_file_path: str) -> Optional[float]:
    save_path = download_audio_segment(mp3_url)
    print("下载音频片段")
    if not os.path.exists(save_path):
        return None

    check_result = check_mp3_corruption(save_path)
    print("检查 MP3 是否损坏")
    if check_result:
        return None

    convert_bool = convert_mp3_to_silk(save_path, silk_file_path)
    print("转换 MP3 为 SILK 格式")
    if not convert_bool:
        return None

    duration = get_duration("intermediate.pcm")
    print("获取时长")
    print(f"转换成功：{save_path} -> {silk_file_path}")
    print(f"MP3 时长为 {duration} 秒.")
    return duration

if __name__ == '__main__':
    mp3_url = "https://private.vhost205.dlvip.com.cn/silk/Aria.mp3"
    silk_file_path = "test.silk"
    main(mp3_url, silk_file_path)

# 打印好友列表，供用户选择
print("好友列表：")
for idx, friend in enumerate(friends[1:], start=1):  # friends[1:] 跳过自己
    print(f"{idx}. {friend['NickName']}")

# 进入输入循环，允许用户动态输入文本
while True:
    # 选择好友
    try:
        friend_choice = int(input("请输入你想发送消息的好友编号（输入 'exit' 退出）："))
        if friend_choice < 1 or friend_choice >= len(friends):
            print("无效的好友编号，请重新选择。")
            continue
    except ValueError:
        if input("请输入 'exit' 退出：").lower() == 'exit':
            print("程序已退出。")
            break
        else:
            print("请输入有效的数字编号。")
            continue

    selected_friend = friends[friend_choice]

    # 输入 SILK 文件路径
    silk_path = input("请输入要发送的 SILK 语音（SILK 格式）文件路径：")

    # 发送 SILK 语音消息
    itchat.send_file(silk_path, toUserName=selected_friend['UserName'])
    print(f"已发送语音文件 '{silk_path}' 给 {selected_friend['NickName']}")
