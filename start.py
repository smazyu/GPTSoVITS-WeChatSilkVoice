import itchat
import sys
import io

# 确保输出流使用 UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 使用热登入
itchat.auto_login()

# 获取好友列表
friends = itchat.get_friends()

# 打印好友列表，供用户选择
print("好友列表：")
for idx, friend in enumerate(friends[1:], start=1):  # friends[1:] 跳过自己
    print(f"{idx}. {friend['NickName']}")


def send_message():
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

        # 输入消息
        message = input(f"请输入要发送给 {selected_friend['NickName']} 的消息：")

        # 发送消息
        itchat.send(message, toUserName=selected_friend['UserName'])
        print(f"消息已发送给 {selected_friend['NickName']}: {message}")
def send_voice_file():
    itchat.send_file(amr_path, toUserName=selected_friend['UserName'])
    print(f"已发送语音文件 '{amr_path}' 给 {selected_friend['NickName']}")