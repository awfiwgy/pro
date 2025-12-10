# -*- coding: utf-8 -*-
# by @嗷呜
import json
import sys
from base64 import b64decode, b64encode
from pyquery import PyQuery as pq
from requests import Session
sys.path.append('..')
from base.spider import Spider


class Spider(Spider):

    def init(self, extend=""):
        self.host = self.gethost()
        self.headers['referer'] = f'{self.host}/'
        self.session = Session()
        self.session.headers.update(self.headers)
        pass

    def getName(self):
        pass

    def isVideoFormat(self, url):
        pass

    def manualVideoCheck(self):
        pass

    def destroy(self):
        pass

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-full-version': '"133.0.6943.98"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-platform': '"Windows"',
        'sec-ch-ua-platform-version': '"19.0.0"',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-full-version-list': '"Not(A:Brand";v="99.0.0.0", "Google Chrome";v="133.0.6943.98", "Chromium";v="133.0.6943.98"',
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'sec-fetch-site': 'none',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'priority': 'u=0, i'
    }

    def homeContent(self, filter):
        result = {}
        cateManual = {
            "4K": "/4k",
            "国产": "two_click_/categories/chinese",
            "最新": "/newest",
            "最佳": "/best",
            "频道": "/channels",
            "类别": "/categories",
            "明星": "/pornstars"
        }
        classes = []
        filters = {}
        for k in cateManual:
            classes.append({
                'type_name': k,
                'type_id': cateManual[k]
            })
            if k !='4K':filters[cateManual[k]]=[{'key':'type','name':'类型','value':[{'n':'4K','v':'/4k'}]}]
        result['class'] = classes
        result['filters'] = filters
        return result

    def homeVideoContent(self):
        data = self.getpq()
        return {'list': self.getlist(data(".thumb-list--sidebar .thumb-list__item"))}

    def categoryContent(self, tid, pg, filter, extend):
        vdata = []
        result = {}
        result['page'] = pg
        result['pagecount'] = 9999
        result['limit'] = 90
        result['total'] = 999999
        if tid in ['/4k', '/newest', '/best'] or 'two_click_' in tid:
            if 'two_click_' in tid: tid = tid.split('click_')[-1]
            data = self.getpq(f'{tid}{extend.get("type","")}/{pg}')
            vdata = self.getlist(data(".thumb-list--sidebar .thumb-list__item"))
        elif tid == '/channels':
            data = self.getpq(f'{tid}/{pg}')
            jsdata = self.getjsdata(data)
            for i in jsdata['channels']:
                vdata.append({
                    'vod_id': f"two_click_" + i.get('channelURL'),
                    'vod_name': i.get('channelName'),
                    'vod_pic': i.get('siteLogoURL'),
                    'vod_year': f'videos:{i.get("videoCount")}',
                    'vod_tag': 'folder',
                    'vod_remarks': f'subscribers:{i["subscriptionModel"].get("subscribers")}',
                    'style': {'ratio': 1.33, 'type': 'rect'}
                })
        elif tid == '/categories':
            result['pagecount'] = pg
            data = self.getpq(tid)
            self.cdata = self.getjsdata(data)
            for i in self.cdata['layoutPage']['store']['popular']['assignable']:
                vdata.append({
                    'vod_id': "one_click_" + i.get('id'),
                    'vod_name': i.get('name'),
                    'vod_pic': '',
                    'vod_tag': 'folder',
                    'style': {'ratio': 1.33, 'type': 'rect'}
                })
        elif tid == '/pornstars':
            data = self.getpq(f'{tid}/{pg}')
            pdata = self.getjsdata(data)
            for i in pdata['pagesPornstarsComponent']['pornstarListProps']['pornstars']:
                vdata.append({
                    'vod_id': f"two_click_" + i.get('pageURL'),
                    'vod_name': i.get('name'),
                    'vod_pic': i.get('imageThumbUrl'),
                    'vod_remarks': i.get('translatedCountryName'),
                    'vod_tag': 'folder',
                    'style': {'ratio': 1.33, 'type': 'rect'}
                })
        elif 'one_click' in tid:
            result['pagecount'] = pg
            tid = tid.split('click_')[-1]
            for i in self.cdata['layoutPage']['store']['popular']['assignable']:
                if i.get('id') == tid:
                    for j in i['items']:
                        vdata.append({
                            'vod_id': f"two_click_" + j.get('url'),
                            'vod_name': j.get('name'),
                            'vod_pic': j.get('thumb'),
                            'vod_tag': 'folder',
                            'style': {'ratio': 1.33, 'type': 'rect'}
                        })
        result['list'] = vdata
        return result

    def detailContent(self, ids):
        data = self.getpq(ids[0])
        vn = data('meta[property="og:title"]').attr('content')
        dtext = data('#video-tags-list-container')
        href = dtext('a').attr('href')
        title = dtext('span[class*="body-bold-"]').eq(0).text()
        pdtitle = ''
        if href:
            pdtitle = '[a=cr:' + json.dumps({'id': 'two_click_' + href, 'name': title}) + '/]' + title + '[/a]'
        vod = {
            'vod_name': vn,
            'vod_director': pdtitle,
            'vod_remarks': data('.rb-new__info').text(),
            'vod_play_from': 'Xhamster',
            'vod_play_url': ''
        }
        try:
            plist = []
            html_content = data.outerHtml()
            
            # 尝试从页面中提取视频URL
            import re
            hls_urls = set()
            
            # 只匹配m3u8格式链接
            hls_patterns = [
                r'setVideoHLS\(["\']([^"\']+\.m3u8)["\']\)',
                r'"hlsUrl"\s*:\s*["\']([^"\']+\.m3u8)["\']',
                r'hls\s*:\s*[{\s]*url\s*:\s*["\']([^"\']+\.m3u8)["\']',
                r'["\'](https?:\/\/[^"\']+\.m3u8)["\']'
            ]
            
            # 尝试所有HLS模式
            for pattern in hls_patterns:
                matches = re.findall(pattern, html_content)
                for match in matches:
                    hls_urls.add(match)
            
            # 如果找到HLS链接，尝试从中提取所有画质
            if hls_urls:
                for hls_url in hls_urls:
                    # 解析m3u8文件获取所有画质
                    hls_qualities = self._parse_hls_qualities(hls_url)
                    
                    # 如果成功解析出多个画质
                    if hls_qualities:
                        for quality, url in hls_qualities.items():
                            encoded = self.e64(f'{0}@@@@{url}')
                            plist.append(f"{quality}${encoded}")
                    else:
                        # 如果无法解析画质，添加原始HLS链接
                        encoded = self.e64(f'{0}@@@@{hls_url}')
                        plist.append(f"HLS${encoded}")

        except Exception as e:
            plist = [f"{vn}${self.e64(f'{1}@@@@{ids[0]}')}"]
            print(f"获取视频信息失败: {str(e)}")
        
        if plist:
            # 按质量排序
            def custom_sort_key(url):
                quality = url.split('$')[0]
                number = ''.join(filter(str.isdigit, quality))
                number = int(number) if number else 0
                return -number, quality
            
            plist.sort(key=custom_sort_key)
            vod['vod_play_url'] = '#'.join(plist)
        
        return {'list': [vod]}
        
    def _parse_hls_qualities(self, m3u8_url):
        """解析m3u8文件，提取所有画质选项"""
        try:
            # 发送请求获取m3u8内容
            response = self.session.get(m3u8_url, headers=self.headers, timeout=5)
            response.encoding = 'utf-8'
            m3u8_content = response.text
            
            # 解析m3u8内容中的画质信息
            qualities = {}
            # 查找EXT-X-STREAM-INF标签，这通常包含不同画质的信息
            import re
            stream_inf_pattern = r'#EXT-X-STREAM-INF:.*?RESOLUTION=([\d]+x[\d]+).*?\n([^\n]+)'
            matches = re.findall(stream_inf_pattern, m3u8_content)
            
            for resolution, path in matches:
                # 从分辨率中提取高度作为画质标识（如1080p, 720p等）
                height = resolution.split('x')[1]
                quality = f"{height}p"
                
                # 构建完整的URL
                if path.startswith('http'):
                    full_url = path
                else:
                    # 处理相对路径
                    from urllib.parse import urlparse, urljoin
                    base_url = urlparse(m3u8_url).scheme + '://' + urlparse(m3u8_url).netloc
                    full_url = urljoin(m3u8_url, path)
                
                qualities[quality] = full_url
            
            # 如果找到画质信息，按清晰度从高到低排序
            if qualities:
                sorted_qualities = {}
                for quality in sorted(qualities.keys(), key=lambda x: int(''.join(filter(str.isdigit, x))), reverse=True):
                    sorted_qualities[quality] = qualities[quality]
                return sorted_qualities
            
            return None
        except Exception as e:
            print(f"解析HLS画质失败: {str(e)}")
            return None

    def searchContent(self, key, quick, pg="1"):
        data = self.getpq(f'/search/{key}?page={pg}')
        return {'list': self.getlist(data(".thumb-list--sidebar .thumb-list__item")), 'page': pg}

    def playerContent(self, flag, id, vipFlags):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.5410.0 Safari/537.36',
            'pragma': 'no-cache',
            'cache-control': 'no-cache',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua': '"Not(A:Brand";v="99", "Google Chrome";v="133", "Chromium";v="133"',
            'dnt': '1',
            'sec-ch-ua-mobile': '?0',
            'origin': self.host,
            'sec-fetch-site': 'cross-site',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'{self.host}/',
            'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'priority': 'u=1, i',
        }
        ids = self.d64(id).split('@@@@')
        return {'parse': int(ids[0]), 'url': ids[1], 'header': headers}

    def localProxy(self, param):
        pass

    def gethost(self):
        try:
            response = self.fetch('https://xhamster.com', headers=self.headers, allow_redirects=False)
            return response.headers['Location']
        except Exception as e:
            print(f"获取主页失败: {str(e)}")
            return "https://zh.xhamster1.desi/"

    def e64(self, text):
        try:
            text_bytes = text.encode('utf-8')
            encoded_bytes = b64encode(text_bytes)
            return encoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64编码错误: {str(e)}")
            return ""

    def d64(self, encoded_text):
        try:
            encoded_bytes = encoded_text.encode('utf-8')
            decoded_bytes = b64decode(encoded_bytes)
            return decoded_bytes.decode('utf-8')
        except Exception as e:
            print(f"Base64解码错误: {str(e)}")
            return ""

    def getlist(self, data):
        vlist = []
        for i in data.items():
            vlist.append({
                'vod_id': i('.role-pop').attr('href'),
                'vod_name': i('.video-thumb-info a').text(),
                'vod_pic': i('.role-pop img').attr('src'),
                'vod_year': i('.video-thumb-info .video-thumb-views').text().split(' ')[0],
                'vod_remarks': i('.role-pop div[data-role="video-duration"]').text(),
                'style': {'ratio': 1.33, 'type': 'rect'}
            })
        return vlist

    def getpq(self, path=''):
        h = '' if path.startswith('http') else self.host
        response = self.session.get(f'{h}{path}').text
        try:
            return pq(response)
        except Exception as e:
            print(f"{str(e)}")
            return pq(response.encode('utf-8'))

    def getjsdata(self, data):
        vhtml = data("script[id='initials-script']").text()
        jst = json.loads(vhtml.split('initials=')[-1][:-1])
        return jst

