import os
import sys
import shlex
# shlex模块实现了一个类来解析简单的类shell语法，可以用来编写领域特定的语言，或者解析加引号的字符串。
import getpass
import socket
import signal
# 进程信号
import subprocess
# 执行外部的命令和程序
import platform
# platform模块给我们提供了很多方法去获取操作系统的信息
from func import *


# 字典表，存储命令和函数的映射
built_in_cmds = {}


def register_command(name, func):
    # 注册命令，是命令与相应的处理函数建立映射关系
    built_in_cmds[name] = func


def init():
    register_command("cd", cd)
    register_command("exit", exit)
    register_command("getenv", getenv)
    register_command("history", history)


def display_cmd_prompt():
    # 获取用户名
    user = getpass.getuser()
    # 获取主机名
    hostname = socket.gethostname()
    # 获取路径
    cwd = os.getcwd()
    # 获取路径目录名
    base_dir = os.path.basename(cwd)
    # 获取用户根目录
    home_dir = os.path.expanduser('~')
    if cwd == home_dir:
        base_dir = '~'
    # 输出命令提示符
    if platform.system() != 'Windows':
        sys.stdout.write("[\033[1;33m%s\033[0;0m@%s \033[1;36m%s\033[0;0m] $ " %
                         (user, hostname, base_dir))
    else:
        sys.stdout.write("[%s@%s %s]$ " % (user, hostname, base_dir))
    sys.stdout.flush()


def ignore_signals():
    if platform.system() != 'Windows':
        # 忽略ctrl-z/c信号
        signal.signal(signal.SIGTSTP, signal.SIG_IGN)
    signal.signal(signal.SIGINT, signal.SIG_IGN)
# signal.SIGTSTP 表示任务中断信号，可由组合键 Ctrl-Z 产生，属于 Unix 平台特有；
# signal.SIGINT 表示强制中断信号，可由组合键 Ctrl-C 产生。
# signal.SIG_IGN 的时候表示采取忽略

def tokenize(string):
    return shlex.split(string)


def preprocess(tokens):
    # 用于存储处理之后的token
    processed_token = []
    for token in tokens:
        if token.startswith('$'):
            processed_token.append(os.getenv(token[1:]))
        else:
            processed_token.append(token)
    return processed_token


def handler_kill(signum, frame):
    raise OSError("Killed!")


def execute(cmd_tokens):
    with open(HISTORY_PATH, 'a') as history_file:
        history_file.write(''.join(cmd_tokens)+os.linesep)
    if cmd_tokens:
        #获取命令
        cmd_name=cmd_tokens[0]
        #获取命令参数
        cmd_args=cmd_tokens[1:]
        if cmd_name in built_in_cmds:
            return built_in_cmds[cmd_name](cmd_args)
        #监听ctrl-c信号
        signal.signal(signal.SIGINT,handler_kill)
        #如果当前系统不是Windows，则创建子系统
        if platform.system()!="Windows":
            p=subprocess.Popen(cmd_tokens)
            p.communicate()
        else:
            command=""
            command=''.join(cmd_tokens)
            os.system(command)
    return SHELL_ATATUS_RUN
def shell_loop():
    status = SHELL_ATATUS_RUN

    while status == SHELL_ATATUS_RUN:
        # 打印命令提示符
        display_cmd_prompt()
        # 忽略ctrl-z/c
        ignore_signals()

        try:
            # 读取命令
            cmd = sys.stdin.readline()
            # 解析命令
            # 将命令铲粪，返回一个列表
            cmd_tokens = tokenize(cmd)
            # 预处理函数
            # 将命令中的环境变量使用真实值进行替换
            cmd_tokens = preprocess(cmd_tokens)
            # 执行命令，并返回shell状态
            status = execute(cmd_tokens)
        except:
            # sys.exc_info()

            _, err, _ = sys.exc_info()
            print(err)


def main():
    # 首先初始化，建立命令和函数映射关系表
    init()

    # 主程序
    shell_loop()

if __name__ == '__main__':
    main()
