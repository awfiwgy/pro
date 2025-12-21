# coding=utf-8
import re
from urllib.parse import urljoin
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "果冻视频"

    def init(self, extend=""):
        self.host = "https://zvz.gdpjb8.work"

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "主播网红": "20",
            "偷拍自拍": "21",
            "人妻熟女": "22",
            "强奸乱伦": "23",
            "制服丝袜": "24",
            "自慰变态": "25",
            "国产精品": "26",
            "亚洲情色": "27",
            "卡通动漫": "28",
            "三级伦理": "29",
            "欧美精品": "30"
        }
        classes = []
        for k in cateManual:
            classes.append({'type_name': k, 'type_id': cateManual[k]})
        result['class'] = classes
        return result

    def homeVideoContent(self):
        url = self.host + "/cn/home/web/"
        rsp = self.fetch(url)
        root = self.html(self.cleanText(rsp.text))
        
        # 根据实际结构优化：容器为 well well-sm 或仅 well-sm
        items = root.xpath("//div[contains(@class,'well-sm')]")
        videos = []
        for item in items:
            try:
                a = item.xpath(".//a")[0]
                href = a.xpath("./@href")[0]
                
                name = item.xpath(".//span[contains(@class,'video-title')]/text()")[0].strip()
                
                pic = item.xpath(".//img/@src")[0]
                
                remark = item.xpath(".//div[contains(@class,'duration')]/text()")[0].strip()
                
                sid_match = re.search(r"id/(\d+)", href)
                sid = sid_match.group(1) if sid_match else ""
                
                if sid:
                    videos.append({
                        "vod_id": sid,
                        "vod_name": name,
                        "vod_pic": urljoin(self.host, pic),
                        "vod_remarks": remark
                    })
            except:
                continue
        return {'list': videos}

    def categoryContent(self, tid, pg, filter, extend):
        if int(pg) == 1:
            page = ""
        else:
            page = f"/page/{pg}"
        url = f"{self.host}/cn/home/web/index.php/vod/type/id/{tid}{page}.html"
        rsp = self.fetch(url)
        root = self.html(self.cleanText(rsp.text))
        
        items = root.xpath("//div[contains(@class,'well-sm')]")
        videos = []
        for item in items:
            try:
                a = item.xpath(".//a")[0]
                href = a.xpath("./@href")[0]
                
                name = item.xpath(".//span[contains(@class,'video-title')]/text()")[0].strip()
                
                pic = item.xpath(".//img/@src")[0]
                
                remark = item.xpath(".//div[contains(@class,'duration')]/text()")[0].strip()
                
                sid_match = re.search(r"id/(\d+)", href)
                sid = sid_match.group(1) if sid_match else ""
                
                if sid:
                    videos.append({
                        "vod_id": sid,
                        "vod_name": name,
                        "vod_pic": urljoin(self.host, pic),
                        "vod_remarks": remark
                    })
            except:
                continue
        return {'list': videos}

    def detailContent(self, array):
        tid = array[0]
        # 修复后的播放页地址（注意 nid/1 而非 mid/1）
        play_url = f"{self.host}/cn/home/web/index.php/vod/play/id/{tid}/sid/1/nid/1.html"
        
        vod = {
            "vod_id": tid,
            "vod_name": "视频播放",
            "vod_pic": "",
            "type_name": "果冻视频",
            "vod_year": "",
            "vod_area": "",
            "vod_remarks": "",
            "vod_actor": "",
            "vod_director": "",
            "vod_content": "",
            "vod_play_from": "果冻解析",
            "vod_play_url": "全屏播放$" + play_url
        }
        return {'list': [vod]}

    def playerContent(self, flag, id, vipFlags):
        # 使用嗅探模式，适合 AJAX 动态加载播放地址的站点
        return {
            "parse": 1,
            "playUrl": "",
            "url": id,
            "header": {
                "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1",
                "Referer": self.host
            }
        }

    def searchContent(self, key, quick, page):
        if int(page) == 1:
            pg = ""
        else:
            pg = f"/page/{page}"
        url = f"{self.host}/cn/home/web/index.php/vod/search{pg}/wd/{key}.html"
        rsp = self.fetch(url)
        root = self.html(self.cleanText(rsp.text))
        
        items = root.xpath("//div[contains(@class,'well-sm')]")
        videos = []
        for item in items:
            try:
                a = item.xpath(".//a")[0]
                href = a.xpath("./@href")[0]
                
                name = item.xpath(".//span[contains(@class,'video-title')]/text()")[0].strip()
                
                pic = item.xpath(".//img/@src")[0]
                
                remark = item.xpath(".//div[contains(@class,'duration')]/text()")[0].strip()
                
                sid_match = re.search(r"id/(\d+)", href)
                sid = sid_match.group(1) if sid_match else ""
                
                if sid:
                    videos.append({
                        "vod_id": sid,
                        "vod_name": name,
                        "vod_pic": urljoin(self.host, pic),
                        "vod_remarks": remark
                    })
            except:
                continue
        return {'list': videos}