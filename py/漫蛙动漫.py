#!/usr/bin/python
#coding=utf-8
import sys
sys.path.append('..')
from base.spider import Spider
from urllib.parse import quote

class Spider(Spider):
    def getName(self):
        return "漫蛙动漫"
    
    def init(self, extend=""):
        pass
    
    def homeContent(self, filter):
        return {
            'class': [
                {'type_name': '国漫', 'type_id': '2'},
                {'type_name': '日漫', 'type_id': '3'},
                {'type_name': '番漫', 'type_id': '1'},
                {'type_name': '其他', 'type_id': '4'}
            ]
        }
    
    def homeVideoContent(self):
        return {'list': []}
    
    def categoryContent(self, tid, pg, filter, extend):
        rsp = self.fetch(f"https://www.mwdm.cc/list/{tid}-{pg}/", headers=self.header)
        root = self.html(rsp.text)
        
        videos = []
        for item in root.xpath('//ul[@class="stui-vodlist clearfix"]/li'):
            try:
                link = item.xpath('.//a[@class="stui-vodlist__thumb lazyload"]/@href')[0]
                title = item.xpath('.//h4[@class="stui-vodlist__title"]/a/@title')[0]
                pic = item.xpath('.//a[@class="stui-vodlist__thumb lazyload"]/@data-original')[0]
                remark = item.xpath('.//span[@class="pic-text text-right"]/text()')[0]
                videos.append({
                    "vod_id": f"https://www.mwdm.cc{link}",
                    "vod_name": title,
                    "vod_pic": pic,
                    "vod_remarks": remark if remark else ""
                })
            except:
                continue
        
        page_info = root.xpath('//li[@class="active"]/span[@class="num"]/text()')
        total = int(page_info[0].split('/')[1]) if page_info else 999
        
        return {
            'list': videos,
            'page': pg,
            'pagecount': total,
            'limit': 12,
            'total': 999999
        }
    
    def detailContent(self, array):
        rsp = self.fetch(array[0], headers=self.header)
        root = self.html(rsp.text)
        
        vod = {
            "vod_id": array[0],
            "vod_name": root.xpath('//h3[@class="title"]/text()')[0] if root.xpath('//h3[@class="title"]/text()') else "",
            "vod_pic": root.xpath('//img[@class="img-responsive"]/@src')[0] if root.xpath('//img[@class="img-responsive"]/@src') else "",
            "vod_content": root.xpath('//span[@class="detail-content"]/text()')[0].strip() if root.xpath('//span[@class="detail-content"]/text()') else "暂无简介"
        }
        
        play_sources, play_urls = [], []
        for idx, section in enumerate(root.xpath('//div[@class="tab-pane fade in clearfix"]')):
            episodes = []
            for link in section.xpath('.//li/a'):
                ep_name = link.xpath('./text()')[0].strip() if link.xpath('./text()') else ""
                ep_url = self.full_url(link.xpath('./@href')[0]) if link.xpath('./@href') else ""
                if ep_name and ep_url:
                    episodes.append(f"{ep_name}${ep_url}")
            if episodes:
                play_sources.append(f"线路{idx+1}")
                play_urls.append("#".join(episodes))
        
        if play_sources:
            vod["vod_play_from"] = "$$$".join(play_sources)
            vod["vod_play_url"] = "$$$".join(play_urls)
        
        return {'list': [vod]}
    
    def searchContent(self, key, quick, pg=1):
        rsp = self.fetch(f"https://www.mwdm.cc/search/-------------/?wd={quote(key)}&page={pg}", headers=self.header)
        root = self.html(rsp.text)
        
        videos = []
        for item in root.xpath('//ul[@class="stui-vodlist clearfix"]/li'):
            try:
                link = item.xpath('.//a[@class="stui-vodlist__thumb lazyload"]/@href')[0]
                title = item.xpath('.//h4[@class="stui-vodlist__title"]/a/@title')[0]
                pic = item.xpath('.//a[@class="stui-vodlist__thumb lazyload"]/@data-original')[0]
                remark = item.xpath('.//span[@class="pic-text text-right"]/text()')[0]
                videos.append({
                    "vod_id": f"https://www.mwdm.cc{link}",
                    "vod_name": title,
                    "vod_pic": pic,
                    "vod_remarks": remark if remark else ""
                })
            except:
                continue
        
        return {'list': videos}
    
    def playerContent(self, flag, id, vipFlags):
        return {
            "parse": 1,
            "playUrl": "",
            "url": id,
            "header": self.header
        }
    
    def localProxy(self, param):
        return [200, "video/MP2T", "", ""]
    
    def full_url(self, path):
        return f"https://www.mwdm.cc{path}" if not path.startswith('http') else path
    
    header = {
        "User-Agent": "Mozilla/5.0",
        "Referer": "https://www.mwdm.cc/"
    }