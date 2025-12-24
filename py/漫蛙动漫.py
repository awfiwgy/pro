#!/usr/bin/python
#coding=utf-8
import sys
sys.path.append('..') 
from base.spider import Spider
import re
from urllib.parse import quote

class Spider(Spider):
    def getName(self):
        return "漫蛙动漫"
    
    def init(self, extend=""):
        pass
    
    def homeContent(self, filter):
        classes = [
            {'type_name':'国漫','type_id':'2'},
            {'type_name':'日漫','type_id':'3'},
            {'type_name':'番漫','type_id':'1'},
            {'type_name':'其他','type_id':'4'}
        ]
        return {'class':classes}
    
    def homeVideoContent(self):
        return {'list':[]}
    
    def categoryContent(self, tid, pg, filter, extend):
        url = f"https://www.mwdm.cc/list/{tid}-{pg}/"
        rsp = self.fetch(url, headers=self.header)
        root = self.html(rsp.text)
        
        videos = []
        for item in root.xpath('//ul[@class="stui-vodlist clearfix"]/li'):
            link = item.xpath('.//a[@class="stui-vodlist__thumb lazyload"]/@href')[0]
            title = item.xpath('.//h4[@class="stui-vodlist__title"]/a/@title')[0]
            pic = item.xpath('.//a[@class="stui-vodlist__thumb lazyload"]/@data-original')[0]
            remark = item.xpath('.//span[@class="pic-text text-right"]/text()')
            
            videos.append({
                "vod_id": f"https://www.mwdm.cc{link}",
                "vod_name": title,
                "vod_pic": pic,
                "vod_remarks": remark[0] if remark else ""
            })
        
        # 获取总页数
        page_info = root.xpath('//li[@class="active"]/span[@class="num"]/text()')
        total = int(page_info[0].split('/')[1]) if page_info else 999
        
        return {
            'list': videos,
            'page': pg,
            'pagecount': total,
            'limit': len(videos),
            'total': 999999
        }
    
    def detailContent(self, array):
        url = array[0]
        rsp = self.fetch(url, headers=self.header)
        root = self.html(rsp.text)
        
        # 基本信息
        title = root.xpath('//h3[@class="title"]/text()')[0]
        cover = root.xpath('//img[@class="img-responsive"]/@src')[0]
        
        # 详细信息
        info_text = root.xpath('//p[@class="data"]/text()')
        info = {k.strip():v.strip() for k,v in (item.split(':',1) for item in info_text if ':' in item)}
        
        # 剧情介绍
        desc = root.xpath('//span[@class="detail-content"]/text()') or root.xpath('//span[@class="detail-sketch"]/text()')
        
        # 播放地址
        play_sources, play_urls = [], []
        for idx, section in enumerate(root.xpath('//div[@class="tab-pane fade in clearfix"]')):
            episodes = [f"{link.xpath('./text()')[0].strip()}${self.full_url(link.xpath('./@href')[0])}" 
                       for link in section.xpath('.//li/a')]
            if episodes:
                play_sources.append(f"线路{idx+1}")
                play_urls.append("#".join(episodes))
        
        vod = {
            "vod_id": url,
            "vod_name": title,
            "vod_pic": cover,
            "vod_year": info.get('时间','').split('-')[0],
            "vod_area": info.get('地区',''),
            "vod_actor": info.get('主演',''),
            "vod_director": info.get('导演',''),
            "vod_content": desc[0].strip() if desc else "暂无简介"
        }
        
        if play_sources:
            vod["vod_play_from"] = "$$$".join(play_sources)
            vod["vod_play_url"] = "$$$".join(play_urls)
        
        return {'list':[vod]}
    
    def searchContent(self, key, quick):
        url = f"https://www.mwdm.cc/search/-------------/?wd={quote(key)}"
        rsp = self.fetch(url, headers=self.header)
        root = self.html(rsp.text)
        
        videos = []
        for item in root.xpath('//ul[@class="stui-vodlist clearfix"]/li'):
            link = item.xpath('.//a[@class="stui-vodlist__thumb lazyload"]/@href')[0]
            title = item.xpath('.//h4[@class="stui-vodlist__title"]/a/@title')[0]
            pic = item.xpath('.//a[@class="stui-vodlist__thumb lazyload"]/@data-original')[0]
            remark = item.xpath('.//span[@class="pic-text text-right"]/text()')
            
            videos.append({
                "vod_id": f"https://www.mwdm.cc{link}",
                "vod_name": title,
                "vod_pic": pic,
                "vod_remarks": remark[0] if remark else ""
            })
        
        return {'list':videos}
    
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
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Referer": "https://www.mwdm.cc/"
    }