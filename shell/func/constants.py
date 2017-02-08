import os
SHELL_ATATUS_STOP=0
SHELL_ATATUS_RUN=1

#获取当前用户根目录
HISTORY_PATH=os.path.expanduser('~')+os.sep+'.test_shell_history'

print("history文件路径",HISTORY_PATH)
