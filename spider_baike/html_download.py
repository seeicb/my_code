# html下载器
import urllib.request


class Htmldownloader(object):
    def download(self, url):
        if url is None:
            return None
        response = urllib.request.urlopen(url)
        # 打开url,赋值为response
        if response.getcode() != 200:
            return None
        # 打印页面内容
        # print(response.read().decode("utf8"))
        return response.read()
