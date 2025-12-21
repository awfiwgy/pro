from base.spider import Spider
from urllib.parse import unquote
import requests
import json
import re

base_url = "https://www.mandao.cc"
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': base_url
}

class Spider(Spider):
    
    def getName(self):
        return "漫岛动漫"
    
    def init(self, extend):
        pass
    
    def isVideoFormat(self, url):
        return any(fmt in url for fmt in ['.m3u8', '.mp4', '.flv', '.avi', '.mkv', '.ts'])
    
    def manualVideoCheck(self):
        return False
    
    def homeContent(self, filter):
        return {
            "class": [
                {"type_id": "1", "type_name": "国产动漫"},
                {"type_id": "2", "type_name": "日本动漫"},
                {"type_id": "3", "type_name": "欧美动漫"},
                {"type_id": "5", "type_name": "动漫电影"}
            ]
        }
    
    def homeVideoContent(self):
        videos = []
        try:
            response = requests.get(f"{base_url}/vod/type/id/1.html", headers=headers, timeout=10)
            response.encoding = 'utf-8'
            items = re.findall(r'<li class="stui-vodlist__item">.*?href="([^"]+)".*?title="([^"]+)".*?data-original="([^"]+)".*?pic-text[^>]*>([^<]+)<', response.text, re.DOTALL)
            
            for link, title, img, remark in items[:20]:
                vod_id = link.split('/')[-1].replace('.html', '')
                videos.append({
                    "vod_id": vod_id if vod_id.isdigit() else link,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
                
        except Exception as e:
            print(f"获取首页视频失败: {e}")
        
        return {'list': videos}
    
    def categoryContent(self, cid, pg, filter, ext):
        try:
            if 'id/' in cid:
                url = cid if 'page/' in cid else f"{cid.replace('.html', '')}/page/{pg}.html"
            else:
                url = f"{base_url}/vod/type/id/{cid}/page/{pg}.html" if pg != "1" else f"{base_url}/vod/type/id/{cid}.html"
            
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            html = response.text
            
            videos = []
            items = re.findall(r'<li class="stui-vodlist__item">.*?href="([^"]+)".*?title="([^"]+)".*?data-original="([^"]+)".*?pic-text[^>]*>([^<]+)<', html, re.DOTALL)
            
            for link, title, img, remark in items:
                vod_id = link.split('/dm/')[1].replace('.html', '') if '/dm/' in link else link
                videos.append({
                    "vod_id": vod_id,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_remarks": remark
                })
            
            page_match = re.search(r'<li class="active visible-xs"><span class="num">(\d+)/(\d+)</span></li>', html)
            if page_match:
                current_page = int(page_match.group(1))
                total_pages = int(page_match.group(2))
            else:
                current_page = int(pg)
                total_pages = 999 if videos else 1
            
            return {
                'list': videos,
                'page': current_page,
                'pagecount': total_pages,
                'total': 999999,
                'limit': len(videos)
            }
            
        except Exception as e:
            print(f"获取分类内容失败: {e}")
            return {'list': [], 'page': 1, 'pagecount': 1, 'total': 0, 'limit': 0}
    
    def detailContent(self, ids):
        try:
            vid = ids[0]
            url = vid if vid.startswith('http') else f"{base_url}/dm/{vid}.html" if vid.isdigit() else f"{base_url}/{vid}"
            
            response = requests.get(url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            html = response.text
            
            # 提取详情区域
            detail_section = re.search(r'<div class="stui-content__detail">(.*?)</div>', html, re.DOTALL)
            if not detail_section:
                return {'list': []}
            
            detail_text = detail_section.group(1)
            
            # 提取标题
            title_match = re.search(r'<h3 class="title">([^<]+)</h3>', detail_text)
            title = title_match.group(1).strip() if title_match else f"动漫 {vid}"
            
            # 提取描述
            desc_match = re.search(r'<p class="desc[^>]*>(.*?)</p>', detail_text, re.DOTALL)
            if desc_match:
                desc = re.sub(r'<a[^>]*>.*?</a>', '', desc_match.group(1)).strip()
            else:
                desc = ""
            
            # 提取图片
            img_match = re.search(r'data-original="([^"]+)"', html)
            img = img_match.group(1) if img_match else ""
            
            # 提取播放源
            play_sources, play_urls = self._extract_play_sources(html)
            
            # 提取视频信息
            vod_info = self._extract_vod_info(detail_text)
            
            return {
                'list': [{
                    "vod_id": vid,
                    "vod_name": title,
                    "vod_pic": img,
                    "vod_content": desc,
                    "vod_year": vod_info.get('year', ''),
                    "vod_area": vod_info.get('area', ''),
                    "vod_type": vod_info.get('type', ''),
                    "vod_actor": vod_info.get('actor', ''),
                    "vod_director": vod_info.get('director', ''),
                    "vod_play_from": '$$$'.join(play_sources) if play_sources else "默认",
                    "vod_play_url": '$$$'.join(play_urls) if play_urls else ""
                }]
            }
            
        except Exception as e:
            print(f"获取详情失败: {e}")
            return {'list': []}
    
    def _extract_play_sources(self, html):
        """提取播放源"""
        play_sources = []
        play_urls = []
        
        sources = re.findall(r'<div class="stui-pannel__head[^>]*>.*?<h3 class="title">([^<]+)</h3>.*?</div>.*?<ul class="stui-content__playlist[^>]*>(.*?)</ul>', html, re.DOTALL)
        
        for source_name, source_content in sources:
            episodes = re.findall(r'<li[^>]*>.*?<a[^>]*href="([^"]+)"[^>]*>([^<]+)</a>', source_content, re.DOTALL)
            if episodes:
                play_sources.append(source_name)
                episode_list = []
                for ep_url, ep_name in episodes:
                    full_url = ep_url if ep_url.startswith('http') else base_url + (ep_url if ep_url.startswith('/') else '/' + ep_url)
                    episode_list.append(f"{ep_name}${full_url}")
                play_urls.append('#'.join(episode_list))
        
        # 尝试从script中提取
        if not play_sources:
            script_match = re.search(r'var player_aaaa\s*=\s*({.*?});', html, re.DOTALL)
            if script_match:
                try:
                    player_data = json.loads(script_match.group(1))
                    play_sources = ["默认"]
                    if 'url' in player_data:
                        play_urls = [f"第{player_data.get('nid', '1')}集${player_data['url']}"]
                except:
                    pass
        
        return play_sources, play_urls
    
    def _extract_vod_info(self, detail_text):
        """提取视频信息"""
        info = {}
        
        # 提取类型
        type_matches = re.findall(r'class="[^"]*">([^<]+)</a>', detail_text)
        if type_matches:
            info['type'] = '/'.join(type_matches[:3])
        
        # 提取年份
        year_match = re.search(r'year/(\d{4})\.html', detail_text)
        if year_match:
            info['year'] = year_match.group(1)
        
        # 提取地区
        area_match = re.search(r'area/([^/]+)\.html', detail_text)
        if area_match:
            info['area'] = unquote(area_match.group(1))
        
        # 提取演员
        actor_match = re.search(r'<span>主演：</span>([^<]+)</p>', detail_text)
        if actor_match:
            info['actor'] = actor_match.group(1).strip()
        
        # 提取导演
        director_match = re.search(r'<span>导演：</span>([^<]+)</p>', detail_text)
        if director_match:
            info['director'] = director_match.group(1).strip()
        
        return info
    
    def playerContent(self, flag, id, vipFlags):
        try:
            if any(fmt in id for fmt in ['.m3u8', '.mp4', '.flv', '.avi', '.mkv']):
                return {
                    "parse": 0,
                    "playUrl": "",
                    "url": id,
                    "header": json.dumps(headers)
                }
            
            play_url = id if id.startswith('http') else base_url + (id if id.startswith('/') else '/' + id)
            
            response = requests.get(play_url, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            html = response.text
            
            script_match = re.search(r'var player_aaaa\s*=\s*({.*?});', html, re.DOTALL)
            if script_match:
                try:
                    player_data = json.loads(script_match.group(1))
                    if 'url' in player_data:
                        video_url = player_data['url']
                        return {
                            "parse": 0 if any(fmt in video_url for fmt in ['.mp4', '.flv', '.avi', '.mkv']) else 1,
                            "playUrl": "",
                            "url": video_url,
                            "header": json.dumps(headers)
                        }
                except:
                    pass
            
            return {
                "parse": 1,
                "playUrl": "",
                "url": play_url,
                "header": json.dumps(headers)
            }
            
        except Exception as e:
            print(f"播放解析失败: {e}")
            return {"parse": 0, "playUrl": "", "url": "", "header": ""}
    
    def searchContent(self, key, quick, pg="1"):
        try:
            search_data = {'wd': key, 'submit': '搜索'}
            response = requests.post(f"{base_url}/vodsearch.html", data=search_data, headers=headers, timeout=10)
            response.encoding = 'utf-8'
            html = response.text
            
            videos = []
            items = re.findall(r'<li class="stui-vodlist__item">.*?href="([^"]+)".*?title="([^"]+)".*?data-original="([^"]+)".*?pic-text[^>]*>([^<]+)<', html, re.DOTALL)
            
            for link, title, img, remark in items:
                if key.lower() in title.lower():
                    vod_id = link.split('/dm/')[1].replace('.html', '') if '/dm/' in link else link
                    videos.append({
                        "vod_id": vod_id,
                        "vod_name": title,
                        "vod_pic": img,
                        "vod_remarks": remark
                    })
            
            return {
                'list': videos,
                'page': int(pg),
                'pagecount': 1,
                'total': len(videos),
                'limit': 90
            }
            
        except Exception as e:
            print(f"搜索失败: {e}")
            return {'list': [], 'page': 1, 'pagecount': 1, 'total': 0, 'limit': 0}
    
    def searchContentPage(self, key, quick, pg):
        return self.searchContent(key, quick, pg)
    
    def localProxy(self, params):
        if params['type'] == "m3u8":
            return self.proxyM3u8(params)
        elif params['type'] == "media":
            return self.proxyMedia(params)
        elif params['type'] == "ts":
            return self.proxyTs(params)
        return None