# -*- coding: utf-8 -*-
import sys, requests, urllib.parse, base64, json
from lxml import etree
sys.path.append('..')
from base.spider import Spider

class Spider(Spider):
    def getName(self):
        return "KanAV"
#https://kanav.ad
    def init(self, extend):
        self.home_url = 'https://v1.kanav.fit'
        self.header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Referer": self.home_url
        }

    def get_list(self, html):
        try:
            root = etree.HTML(html)
            cards = root.xpath('//div[contains(@class, "video-item")]')
            videos = []
            for c in cards:
                try:
                    link_node = c.xpath('.//a[contains(@href, "/vod/play/")]')
                    if not link_node:
                        continue
                    link = link_node[0].get('href')

                    img_node = c.xpath('.//img')
                    img = ""
                    if img_node:
                        img = img_node[0].get('data-original') or img_node[0].get('src') or ""
                        if img.startswith('//'):
                            img = 'https:' + img

                    title_node = c.xpath('.//div[contains(@class, "entry-title")]//a/text()')
                    if title_node:
                        name = title_node[0]
                    elif img_node:
                        name = img_node[0].get('alt')

                    cat = c.xpath('.//span[@class="model-view-left"]/text()')
                    dur = c.xpath('.//span[@class="model-view"]/text()')
                    remarks = f"{cat[0] if cat else ''} {dur[0] if dur else ''}".strip()

                    videos.append({
                        'vod_id': link,
                        'vod_name': name.strip(),
                        'vod_pic': img,
                        'vod_remarks': remarks
                    })
                except Exception as e:
                    continue
            return videos
        except Exception as e:
            return []

    def homeContent(self, filter):
        return {'class': [
            {'type_name': '中文字幕', 'type_id': '/index.php/vod/type/id/1.html'},
            {'type_name': '日韩有码', 'type_id': '/index.php/vod/type/id/2.html'},
            {'type_name': '日韩无码', 'type_id': '/index.php/vod/type/id/3.html'},
            {'type_name': '国产AV', 'type_id': '/index.php/vod/type/id/4.html'},
            {'type_name': '流出自拍', 'type_id': '/index.php/vod/type/id/22.html'},
            {'type_name': '自拍泄密', 'type_id': '/index.php/vod/type/id/30.html'},
            {'type_name': '探花约炮', 'type_id': '/index.php/vod/type/id/31.html'},
            {'type_name': '主播录制', 'type_id': '/index.php/vod/type/id/32.html'},
            {'type_name': '动漫番剧', 'type_id': '/index.php/vod/type/id/20.html'},
            {'type_name': '里番', 'type_id': '/index.php/vod/type/id/25.html'},
            {'type_name': '泡面番', 'type_id': '/index.php/vod/type/id/26.html'},
            {'type_name': '动漫', 'type_id': '/index.php/vod/type/id/27.html'},
            {'type_name': '同人作品', 'type_id': '/index.php/vod/type/id/29.html'},
            {'type_name': '3D动画', 'type_id': '/index.php/vod/type/id/28.html'}
        ]}

    def homeVideoContent(self):
        try:
            r = requests.get(self.home_url, headers=self.header)
            r.encoding = 'utf-8'
            return {'list': self.get_list(r.text), 'parse': 0, 'jx': 0}
        except:
            return {'list': [], 'parse': 0, 'jx': 0}

    def categoryContent(self, cid, page, filter, ext):
        try:
            if page == '1':
                url = f"{self.home_url}{cid}"
            else:
                if cid.endswith('.html'):
                    url = f"{self.home_url}{cid.replace('.html', f'/page/{page}.html')}"
                else:
                    url = f"{self.home_url}{cid}/page/{page}.html"
            
            r = requests.get(url, headers=self.header)
            r.encoding = 'utf-8'
            return {'list': self.get_list(r.text), 'parse': 0, 'jx': 0}
        except:
            return {'list': [], 'parse': 0, 'jx': 0}

    def detailContent(self, did):
        try:
            ids = did[0] if isinstance(did, list) else did
            url = f"{self.home_url}{ids}"
            r = requests.get(url, headers=self.header)
            r.encoding = 'utf-8'
            html = r.text
            
            play_url = ""
            vod_name = ""
            
            start_str = 'var player_aaaa='
            if start_str in html:
                try:
                    start_idx = html.find(start_str) + len(start_str)
                    end_idx = html.find('</script>', start_idx)
                    json_str = html[start_idx:end_idx].strip().rstrip(';')
                    data = json.loads(json_str)
                    
                    encrypted_url = data.get('url', '')
                    vod_name = data.get('vod_data', {}).get('vod_name', '')
                    
                    if encrypted_url:
                        decoded_b64 = base64.b64decode(encrypted_url).decode('utf-8')
                        play_url = urllib.parse.unquote(decoded_b64)
                except Exception as e:
                    pass

            root = etree.HTML(html)
            if not vod_name:
                title_node = root.xpath('//h1/text()')
                vod_name = title_node[0] if title_node else "Unknown"
            
            tags = root.xpath('//div[contains(@class, "video-countext-tags")]//a/text()')
            desc = f"Tags: {', '.join(tags)}" if tags else ""

            return {
                "list": [{
                    'vod_id': ids,
                    'vod_name': vod_name,
                    'vod_play_from': 'KanAV',
                    'vod_play_url': f"播放${play_url}",
                    'vod_content': desc
                }],
                'parse': 0,
                'jx': 0
            }
        except Exception as e:
            return {'list': []}

    def searchContent(self, key, quick, page='1'):
        try:
            url = f"{self.home_url}/index.php/vod/search.html?wd={key}&page={page}"
            r = requests.get(url, headers=self.header)
            r.encoding = 'utf-8'
            return {'list': self.get_list(r.text), 'parse': 0, 'jx': 0}
        except:
            return {'list': [], 'parse': 0, 'jx': 0}

    def playerContent(self, flag, pid, vipFlags):
        return {'url': pid, "header": self.header, 'parse': 0, 'jx': 0}

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def getDependence(self):
        return []

    def localProxy(self, params):
        pass

    def destroy(self):
        return 'Destroy'
