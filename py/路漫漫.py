import requests
from bs4 import BeautifulSoup
import re
from base.spider import Spider

xurl = "https://www.lmm50.com"

headerx = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': xurl
}

class Spider(Spider):
    def getName(self):
        return "路漫漫动漫"

    def init(self, extend):
        pass

    def homeContent(self, filter):
        return {
            "class": [
                {"type_id": "guochandongman", "type_name": "国产动漫"},
                {"type_id": "dongtaiman", "type_name": "动态漫画"},
                {"type_id": "ribendongman", "type_name": "日本动漫"},
                {"type_id": "guochandonghuadianying", "type_name": "国产动画电影"},
                {"type_id": "ribendonghuadianying", "type_name": "日本动画电影"},
                {"type_id": "teshepian", "type_name": "日本特摄剧"},
                {"type_id": "oumeidongman", "type_name": "欧美动漫"},
                {"type_id": "oumeidonghuadianying", "type_name": "欧美动画电影"}
            ]
        }

    def _extract_video_item(self, item):
        """提取列表页视频信息"""
        try:
            title_node = item.find('h6', class_='title') or item.find('div', class_='module-item-title')
            if not title_node: 
                return None
            
            a_tag = title_node.find('a')
            name = a_tag.text.strip()
            href = a_tag['href']

            img_tag = item.find('img')
            pic = img_tag.get('data-src') or img_tag.get('src', '')
            if pic.startswith('//'): 
                pic = "https:" + pic

            remark = ""
            remark_node = item.find('span', class_=['label', 'module-item-note'])
            if remark_node: 
                remark = remark_node.text.strip()

            return {
                "vod_id": href,
                "vod_name": name,
                "vod_pic": pic,
                "vod_remarks": remark
            }
        except:
            return None

    def categoryContent(self, cid, pg, filter, ext):
        videos = []
        pg = int(pg) if pg else 1
        url = f'{xurl}/type/{cid}_{pg}.html' if pg > 1 else f'{xurl}/type/{cid}.html'
        
        try:
            res = requests.get(url=url, headers=headerx, timeout=10)
            res.encoding = "utf-8"
            doc = BeautifulSoup(res.text, "lxml")
            
            items = doc.find_all('div', class_=['col-6', 'module-item'])
            for item in items:
                video = self._extract_video_item(item)
                if video: 
                    videos.append(video)

            # 分页逻辑
            pagecount = pg
            pg_node = doc.find('ul', class_='pagination')
            if pg_node:
                last_pg = pg_node.find('a', text=re.compile(r'最后|尾页'))
                if last_pg:
                    m = re.search(r'_(\d+)\.html', last_pg['href'])
                    if m: 
                        pagecount = int(m.group(1))

            return {'list': videos, 'page': pg, 'pagecount': pagecount, 'limit': 20, 'total': 999}
        except:
            return {'list': [], 'page': pg, 'pagecount': pg}

    def _extract_playlist_info(self, doc):
        """提取播放列表信息，统一线路名为线路一、线路二..."""
        all_play_urls = []
        
        # 提取所有播放列表容器
        playlist_containers = doc.find_all('div', class_=['module-player-list', 'module-list'])
        
        for container in playlist_containers:
            urls = []
            links = container.find_all('a', href=re.compile(r'/play/'))
            for link in links:
                span = link.find('span')
                episode_name = span.text.strip() if span else link.text.strip()
                href = link.get('href')
                if href:
                    full_url = href if href.startswith('http') else xurl + href
                    urls.append(f"{episode_name}${full_url}")
            
            if urls:
                all_play_urls.append("#".join(urls))

        # 生成统一的线路名：线路一、线路二、线路三...
        from_names = []
        chinese_numbers = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十']
        
        for i in range(len(all_play_urls)):
            if i < 10:
                from_names.append(f"线路{chinese_numbers[i]}")
            else:
                from_names.append(f"线路{i+1}")
        
        return "$$$".join(from_names), "$$$".join(all_play_urls)

    def detailContent(self, ids):
        did = ids[0]
        url = xurl + did if did.startswith('/') else did
        
        try:
            res = requests.get(url=url, headers=headerx, timeout=10)
            res.encoding = "utf-8"
            doc = BeautifulSoup(res.text, "lxml")
            
            # 标题提取
            title = ""
            title_node = doc.find('h1', class_='page-title') or doc.find('h4')
            if title_node:
                title = title_node.text.strip().split(' - ')[0]
                title = re.sub(r'第\d+集.*$', '', title).strip()

            # 演员导演提取
            actors = []
            directors = []
            
            # 查找所有信息项
            info_containers = doc.find_all('div', class_=['video-info-items', 'video-info-item'])
            for container in info_containers:
                item_title = container.find('span', class_='video-info-itemtitle')
                if item_title:
                    text = item_title.text
                    if '主演' in text or '演员' in text:
                        actor_links = container.find_all('a')
                        actors = [a.text.strip() for a in actor_links if a.text.strip()]
                    elif '导演' in text:
                        director_links = container.find_all('a')
                        directors = [d.text.strip() for d in director_links if d.text.strip()]

            # 简介提取
            content = ""
            c_node = doc.find('div', class_='video-info-content')
            if c_node:
                content = c_node.text.strip()

            # 图片提取
            pic = ""
            pic_node = doc.find('img', class_='url_img') or doc.find('img', class_='lazyload')
            if pic_node:
                pic = pic_node.get('src') or pic_node.get('data-src', '')
                if pic.startswith('//'):
                    pic = "https:" + pic

            # 提取播放列表信息
            vod_play_from, vod_play_url = self._extract_playlist_info(doc)
            
            video = {
                "vod_id": did,
                "vod_name": title,
                "vod_pic": pic,
                "vod_actor": " / ".join(actors) if actors else "暂无",
                "vod_director": " / ".join(directors) if directors else "暂无",
                "vod_content": content,
                "vod_play_from": vod_play_from,
                "vod_play_url": vod_play_url
            }
            return {'list': [video]}
        except Exception as e:
            return {'list': []}

    def playerContent(self, flag, id, vipFlags):
        """嗅探模式播放"""
        # 构建播放URL
        if id.startswith('http'):
            url = id
        elif id.startswith('/'):
            url = xurl + id
        else:
            parts = id.split('_')
            if len(parts) == 3:
                url = f"{xurl}/play/{parts[0]}_{parts[1]}_{parts[2]}.html"
            else:
                url = f"{xurl}/play/{id}.html"
        
        # 统一返回嗅探模式
        return {
            'parse': 0,
            'playUrl': '',
            'url': f"video://{url}",
            'header': headerx
        }

    def searchContent(self, key, quick):
        url = f'{xurl}/vod/search.html?wd={key}'
        try:
            res = requests.get(url=url, headers=headerx, timeout=10)
            res.encoding = "utf-8"
            doc = BeautifulSoup(res.text, "lxml")
            
            videos = []
            containers = doc.find_all('div', class_=['video-img-box', 'module-item'])
            for container in containers:
                v = self._extract_video_item(container)
                if v: 
                    videos.append(v)
            
            return {'list': videos}
        except:
            return {'list': []}