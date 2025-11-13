# ptt_ssh_utf8.py
import paramiko
import time
import sys

# 確保 stdout 是 UTF-8
try:
    sys.stdout.reconfigure(encoding='utf-8')
except AttributeError:
    pass  # Python <3.7 忽略

host = "ptt.cc"
port = 22
ssh_user = "bbsu"  # 固定的 SSH 使用者名稱

# 你的 PTT 帳號密碼列表
users = ["{user1}", "{user2}"]
passwords = ["{pwd1}}", "{pwd2}}"]

accounts = list(zip(users, passwords))


def login_ptt(account):
    username, password = account
    print(f"=== 登入帳號: {username} ===")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=ssh_user, password=password)

        chan = ssh.invoke_shell()
        time.sleep(1)

        # 讀初始畫面
        output = chan.recv(4096).decode('big5', 'ignore')
        #print(output)
        sys.stdout.buffer.write(output.encode('utf-8'))
        sys.stdout.buffer.flush()

        # 輸入帳號
        chan.send(username + "\r\n")
        time.sleep(1)
        output = chan.recv(4096).decode('big5', 'ignore')
        #print(output)
        #sys.stdout.buffer.write(output.encode('utf-8'))
        #sys.stdout.buffer.flush()

        # 輸入密碼
        chan.send(password + "\r\n")
        time.sleep(2)
        output = chan.recv(8192).decode('big5', 'ignore')
        #print(output)
        #sys.stdout.buffer.write(output.encode('utf-8'))
        #sys.stdout.buffer.flush()

        # 這裡可以進一步做其他操作，例如進入看板、閱讀文章、發文
        # 範例：按任意鍵進入主選單
        chan.send("\r\n")
        time.sleep(1)
        output = chan.recv(8192).decode('big5', 'ignore')
        #print(output)
        #sys.stdout.buffer.write(output.encode('utf-8'))
        #sys.stdout.buffer.flush()

        # 關閉
        chan.close()
        ssh.close()
        print(f"=== {username} 登入完成 ===\n")

    except Exception as e:
        print(f"登入 {username} 失敗:", e)


if __name__ == "__main__":
    for account in accounts:
        login_ptt(account)

