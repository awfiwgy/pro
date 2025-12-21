"""
@header({
  "searchable": 1,
  "filterable": 1,
  "quickSearch": 1,
  "title": "小红影视",
  "lang": "hipy"
})
"""

import sys
import json
import re
import base64
import datetime
from urllib.parse import quote_plus, unquote, urljoin
from lxml import etree

sys.path.append('..')
from base.spider import Spider


class Spider(Spider):
    def getName(self):
        return "小红影视"

    def init(self, extend=""):
        self.base_url = "https://www.xiaohys.com"
        self.header = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive",
            "Referer": self.base_url,
            "Upgrade-Insecure-Requests": "1"
        }
        # 分类映射（type_name: type_id）
        self.cate_map = {
            "电影": "1",
            "电视剧": "2",
            "综艺": "3",
            "动漫": "4"
        }
        # 反向映射（type_id: 分类关键词）
        self.id_to_category = {
            "1": "movie",
            "2": "tv",
            "3": "variety",
            "4": "anime"
        }

    def homeContent(self, filter):
        result = {}
        # 构建分类列表
        classes = [{'type_name': k, 'type_id': v} for k, v in self.cate_map.items()]
        result['class'] = classes
        return result

    def _parse_video_item(self, data):
        """解析单个视频项（API返回数据）"""
        try:
            return {
                "vod_id": str(data.get('vod_id', '')),
                "vod_name": data.get('vod_name', '未知视频'),
                "vod_pic": self._format_image_url(data.get('vod_pic', '')),
                "vod_remarks": data.get('vod_remarks', '') or data.get('vod_score', ''),
                "vod_year": data.get('vod_year', ''),
                "vod_area": data.get('vod_area', '')
            }
        except Exception:
            return None

    def _format_image_url(self, img_url):
        """格式化图片URL"""
        if not img_url:
            return ''
        if img_url.startswith('//'):
            return 'https:' + img_url
        elif img_url.startswith('/'):
            return urljoin(self.base_url, img_url)
        return img_url

    def _parse_html(self, rsp):
        """解析HTML响应"""
        try:
            parser = etree.HTMLParser(encoding='utf-8', recover=True, remove_blank_text=True)
            if hasattr(rsp, 'content'):
                return etree.HTML(rsp.content, parser=parser)
            return etree.HTML(rsp.text.encode('utf-8', errors='ignore'), parser=parser)
        except Exception:
            return None

    def homeVideoContent(self):
        """首页推荐视频"""
        recommend_list = []
        try:
            # 调用API获取首页数据（默认电视剧分类）
            api_url = f"{self.base_url}/index.php/api/vod"
            params = {
                'ac': 'list',
                't': 2,  # 电视剧
                'pg': 1,
                'h': 30  # 返回30条推荐
            }
            rsp = self.fetch(api_url, params=params, headers=self.header)
            if not rsp or not rsp.text:
                return {'list': recommend_list}

            data = json.loads(rsp.text)
            if data.get('code') == 1 and 'list' in data:
                seen = set()
                for item in data['list']:
                    video_item = self._parse_video_item(item)
                    if video_item and video_item["vod_id"] not in seen:
                        seen.add(video_item["vod_id"])
                        recommend_list.append(video_item)
        except Exception:
            pass
        return {'list': recommend_list}

    def _build_category_api_params(self, tid, pg, ext):
        """构建分类API参数"""
        params = {
            'ac': 'list',
            't': tid,
            'pg': pg,
            'h': 40,
            'sort': 'time'
        }
        # 处理筛选条件
        if ext and isinstance(ext, (str, dict)):
            try:
                filter_dict = json.loads(ext) if isinstance(ext, str) else ext
                if filter_dict.get('area'):
                    params['area'] = filter_dict['area']
                if filter_dict.get('year'):
                    params['year'] = filter_dict['year']
                if filter_dict.get('sort'):
                    sort_map = {'time': 'time', 'hits': 'hits', 'score': 'score'}
                    params['sort'] = sort_map.get(filter_dict['sort'], 'time')
            except Exception:
                pass
        return params

    def categoryContent(self, tid, pg, filter, extend):
        """分类视频内容"""
        if tid == '0':
            return self.homeVideoContent()
        
        result = {'list': [], 'page': int(pg) if pg else 1, 'pagecount': 9999, 'limit': 40, 'total': 999999}
        try:
            # 构建API参数
            params = self._build_category_api_params(tid, pg, extend)
            api_url = f"{self.base_url}/index.php/api/vod"
            
            rsp = self.fetch(api_url, params=params, headers=self.header)
            if not rsp or not rsp.text:
                return result

            data = json.loads(rsp.text)
            if data.get('code') == 1 and 'list' in data:
                videos = []
                seen = set()
                for item in data['list']:
                    video_item = self._parse_video_item(item)
                    if video_item and video_item["vod_id"] not in seen:
                        seen.add(video_item["vod_id"])
                        videos.append(video_item)
                
                # 更新分页信息
                result['list'] = videos
                result['page'] = int(data.get('page', pg))
                result['pagecount'] = int(data.get('pagecount', 1))
                result['total'] = int(data.get('total', len(videos)))
                result['limit'] = int(data.get('limit', 40))
        except Exception:
            # API失败时尝试解析HTML备用
            try:
                category = self.id_to_category.get(tid, 'tv')
                page_str = '' if str(pg) in ('', '1') else f'/page/{pg}'
                url = f"{self.base_url}/show/{category}{page_str}/"
                rsp = self.fetch(url, headers=self.header)
                if not rsp or not rsp.text:
                    return result
                
                root = self._parse_html(rsp)
                if not root:
                    return result
                
                # 解析HTML中的视频列表
                videos = []
                seen = set()
                item_pattern = r'<a[^>]*href="([^"]*/detail/(\d+)/)"[^>]*>.*?<img[^>]*src="([^"]+)"[^>]*alt="([^"]+)"'
                matches = re.findall(item_pattern, rsp.text, re.DOTALL)
                for href, vid, pic, name in matches:
                    if vid not in seen:
                        seen.add(vid)
                        videos.append({
                            "vod_id": vid,
                            "vod_name": name.strip(),
                            "vod_pic": self._format_image_url(pic),
                            "vod_remarks": ""
                        })
                result['list'] = videos
            except Exception:
                pass
        
        return result

    def _extract_play_urls(self, html, vod_id):
        """从详情页HTML提取播放地址"""
        play_from = []
        play_list = []
        try:
            # 方法1: 解析API返回的播放数据
            api_url = f"{self.base_url}/index.php/api/vod"
            params = {'ac': 'detail', 'ids': vod_id}
            rsp = self.fetch(api_url, params=params, headers=self.header)
            if rsp and rsp.text:
                data = json.loads(rsp.text)
                if data.get('code') == 1 and 'list' in data and len(data['list']) > 0:
                    item = data['list'][0]
                    if 'vod_play_from' in item and 'vod_play_url' in item:
                        from_list = item['vod_play_from'].split('$$$')
                        url_list = item['vod_play_url'].split('$$$')
                        for i in range(min(len(from_list), len(url_list))):
                            play_from.append(from_list[i])
                            play_list.append(url_list[i])
                    return play_from, play_list
            
            # 方法2: 解析HTML中的iframe和JS数据
            # 查找iframe播放地址
            iframe_pattern = r'<iframe[^>]*src="([^"]+)"[^>]*class="[^"]*player[^"]*"'
            iframe_matches = re.findall(iframe_pattern, html, re.DOTALL)
            if iframe_matches:
                play_from.append("默认线路")
                play_list.append(f"播放1${iframe_matches[0]}")
            
            # 查找m3u8地址
            m3u8_pattern = r'(http[^\s"\']+\.m3u8[^\s"\']*)'
            m3u8_match = re.search(m3u8_pattern, html)
            if m3u8_match and not play_from:
                play_from.append("高清线路")
                play_list.append(f"播放1${m3u8_match.group(0)}")
        except Exception:
            pass
        return play_from, play_list

    def detailContent(self, ids):
        """视频详情"""
        if not ids:
            return {'list': []}
        vod_id = str(ids[0]).strip()
        url = f"{self.base_url}/detail/{vod_id}/"
        try:
            rsp = self.fetch(url, headers=self.header)
            if not rsp or not rsp.text:
                return {'list': []}
            html = rsp.text
            root = self._parse_html(rsp)
            if not root:
                return {'list': []}
        except Exception:
            return {'list': []}
        
        # 提取基本信息
        title = ''
        try:
            title_nodes = root.xpath('//h1/text() | //title/text()')
            title = title_nodes[0].split(' - ')[0].strip() if title_nodes else ''
        except Exception:
            title = f"视频_{vod_id}"
        
        pic = ''
        try:
            pic_patterns = [
                r'data-pic=["\']([^"\']+)["\']',
                r'<meta[^>]*property="og:image"[^>]*content="([^"]+)"',
                r'<img[^>]*class="[^"]*detail-pic[^"]*"[^>]*src="([^"]+)"'
            ]
            for pattern in pic_patterns:
                match = re.search(pattern, html, re.I)
                if match:
                    pic = self._format_image_url(match.group(1))
                    break
        except Exception:
            pic = ''
        
        detail = ''
        try:
            detail = re.search(r'<meta name="description" content="([^"]+)"', html)
            detail = detail.group(1).strip() if detail else ''
            if not detail:
                detail_nodes = root.xpath('//div[contains(@class, "content") or contains(@class, "intro")]//text()')
                detail = '\n'.join([x.strip() for x in detail_nodes if x.strip()])
        except Exception:
            detail = ''
        
        # 提取演员、导演等信息
        info_patterns = {
            'vod_actor': r'主演[：:]\s*([^<]+)',
            'vod_director': r'导演[：:]\s*([^<]+)',
            'vod_year': r'年份[：:]\s*([^<]+)',
            'vod_area': r'地区[：:]\s*([^<]+)',
            'vod_remarks': r'更新[：:]\s*([^<]+)'
        }
        info = {}
        for key, pattern in info_patterns.items():
            match = re.search(pattern, html)
            if match:
                info[key] = match.group(1).strip()
        
        # 提取播放地址
        play_from, play_list = self._extract_play_urls(html, vod_id)
        
        vod = {
            "vod_id": vod_id,
            "vod_name": title,
            "vod_pic": pic,
            "type_name": "",
            "vod_year": info.get('vod_year', ''),
            "vod_area": info.get('vod_area', ''),
            "vod_remarks": info.get('vod_remarks', ''),
            "vod_actor": info.get('vod_actor', ''),
            "vod_director": info.get('vod_director', ''),
            "vod_content": detail,
            "vod_play_from": '$$$'.join(play_from) if play_from else "默认线路",
            "vod_play_url": '$$$'.join(play_list) if play_list else f"播放1${url}"
        }
        
        return {'list': [vod]}

    def searchContent(self, key, quick, pg='1'):
        """搜索功能"""
        videos = []
        pg = int(pg) if pg else 1
        try:
            api_url = f"{self.base_url}/index.php/api/vod"
            params = {
                'ac': 'list',
                'wd': key,
                'pg': pg,
                'h': 20
            }
            
            rsp = self.fetch(api_url, params=params, headers=self.header)
            if not rsp or not rsp.text:
                return {'list': []}
            
            data = json.loads(rsp.text)
            if data.get('code') == 1 and 'list' in data:
                seen = set()
                for item in data['list']:
                    video_item = self._parse_video_item(item)
                    if video_item and video_item["vod_id"] not in seen:
                        seen.add(video_item["vod_id"])
                        videos.append(video_item)
            else:
                # API搜索失败时尝试HTML搜索
                search_url = f"{self.base_url}/search/?wd={quote_plus(key)}&page={pg}"
                rsp = self.fetch(search_url, headers=self.header)
                if not rsp or not rsp.text:
                    return {'list': []}
                
                root = self._parse_html(rsp)
                if not root:
                    return {'list': []}
                
                # 解析搜索结果
                item_pattern = r'<a[^>]*href="([^"]*/detail/(\d+)/)"[^>]*>.*?<img[^>]*src="([^"]+)"[^>]*alt="([^"]+)"'
                matches = re.findall(item_pattern, rsp.text, re.DOTALL)
                seen = set()
                for href, vid, pic, name in matches:
                    if vid not in seen:
                        seen.add(vid)
                        videos.append({
                            "vod_id": vid,
                            "vod_name": name.strip(),
                            "vod_pic": self._format_image_url(pic),
                            "vod_remarks": ""
                        })
        except Exception:
            pass
        return {'list': videos}

    def _decode_play_url(self, raw_url):
        """解码播放地址"""
        try:
            if 'base64' in raw_url.lower():
                base64_str = raw_url.split('base64,')[-1]
                return base64.b64decode(base64_str).decode('utf-8')
            if raw_url.startswith('//'):
                return 'https:' + raw_url
            elif raw_url.startswith('/'):
                return urljoin(self.base_url, raw_url)
            return raw_url
        except Exception:
            return raw_url

    def playerContent(self, flag, id, vipFlags):
        """播放器地址解析"""
        # id格式：vod_id-sid-epid 或 直接播放地址
        play_url = id
        try:
            # 如果是剧集ID，构建播放页URL
            if '-' in id and not any(ext in id for ext in ['.m3u8', '.mp4', '.flv']):
                play_url = f"{self.base_url}/vodplay/{id}.html"
            
            # 访问播放页获取真实地址
            rsp = self.fetch(play_url, headers=self.header, timeout=45)
            if not rsp or not rsp.text:
                return {"parse": 0, "url": play_url, "header": self.header}
            
            # 提取m3u8地址
            m3u8_pattern = r'(http[^\s"\']+\.m3u8[^\s"\']*)'
            m3u8_match = re.search(m3u8_pattern, rsp.text)
            if m3u8_match:
                real_url = self._decode_play_url(m3u8_match.group(0))
                return {"parse": 1, "url": real_url, "header": self.header}
            
            # 提取iframe地址
            iframe_pattern = r'<iframe[^>]*src="([^"]+)"[^>]*class="[^"]*player[^"]*"'
            iframe_match = re.search(iframe_pattern, rsp.text)
            if iframe_match:
                real_url = self._decode_play_url(iframe_match.group(1))
                return {"parse": 0 if 'http' in real_url else 1, "url": real_url, "header": self.header}
        except Exception:
            pass
        
        # 直接返回解码后的地址
        real_url = self._decode_play_url(play_url)
        return {"parse": 1 if real_url.endswith('.m3u8') else 0, "url": real_url, "header": self.header}

    def localProxy(self, params):
        """本地代理（预留）"""
        pass

    def isVideoFormat(self, url):
        """判断是否为视频格式"""
        return any(ext in url.lower() for ext in ['.m3u8', '.mp4', '.flv', '.avi', '.mov'])

    def manualVideoCheck(self):
        """手动视频校验（预留）"""
        return []

    def destroy(self):
        """销毁资源（预留）"""
        pass

    def getProxyUrl(self, local=True):
        """获取代理URL"""
        return 'http://127.0.0.1:9978/proxy?do=py'
