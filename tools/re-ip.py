# 提取日志IP，去重。
import re

fo = open('7yuelog.txt', 'r')
c = r'\.'.join([r'\d{1,3}'] * 4)
ma = re.compile(c)
ip_list = ma.findall(fo.read())
ip_list = list(set(ip_list))
ip_list = [line + '\n' for line in ip_list]

fi = open('ip_list.txt', 'w')
fi.writelines(ip_list)
# for ip in ip_file:
#     ip_file.write(ip)
