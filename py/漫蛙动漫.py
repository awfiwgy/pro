# -*- coding: utf-8 -*-
import sys
from pyquery import PyQuery as pq
sys.path.append('..')
from base.spider import Spider
#https://www.su7.la
#http://manwaku.cc
class Spider(Spider):
    host = 'https://www.mwju.cc'
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36','Referer': 'https://www.mwju.cc'}

    def init(self, extend='{}'): pass
    def destroy(self): pass

    def getvs(self, items):
        v = []
        for i in items.items():
            a, img = i("a").eq(0), i(".thumb_img")
            p = img.attr("data-original") or img.attr("data-src") or img.attr("src")
            if p: p = "https:" + p if p.startswith("//") else (self.host + p if p.startswith("/") else p)
            v.append({'vod_id': a.attr('href'),'vod_name': i(".title").text() or a.attr('title'),'vod_pic': p,'vod_remark': i(".badge").text() or i(".desc").text()})
        return v

    def homeContent(self, filter):
        r = {'class': [{'type_name': t, 'type_id': f'/cate?typeid={i}'} for i, t in enumerate(['国产','日韩','欧美','港台','动漫','里番'], 1)]}
        res = self.fetch(self.host, headers=self.headers)
        r['list'] = self.getvs(pq(res.content)(".books-row .item"))
        return r

    def categoryContent(self, tid, pg, filter, extend):
        pg = int(pg)
        if pg == 1:
            res = self.fetch(self.host + tid, headers=self.headers)
            return {'list': self.getvs(pq(res.content)("#dataList .item")), 'page': 1, 'pagecount': 999, 'limit': 36, 'total': 9999}
        
        else:
            tags_map = {'1': '国产', '2': '日韩', '3': '欧美', '4': '港台', '5': '动漫', '6': '里番'}
            m = re.search(r'typeid=(d+)', tid)
            tag_name = tags_map.get(m.group(1), "动漫") if m else "动漫"

            api_url = self.host + '/api/cate/'
            payload = {
                "page": {"page": pg, "pageSize": 36},
                "category": "video",
                "sort": 0,
                "comic": {"status": -1, "day": 0, "year": 0, "tag": ""},
                "video": {"year": 0, "typeId": 0, "area": "", "lang": "", "status": -1, "tag": tag_name},
                "novel": {"status": -1, "day": 0, "sortId": 0}
            }

            headers = self.headers.copy()
            headers['Content-Type'] = 'application/json'
            
            try:
                res = self.post(api_url, headers=headers, data=json.dumps(payload))
                data = json.loads(res.content)
            except:
                res = requests.post(api_url, headers=headers, json=payload, timeout=10)
                data = res.json()
            
            items = data.get('data', {}).get('list', [])
            v = []
            for i in items:
                p = i.get('pic', '')
                if p.startswith("//"): p = "https:" + p
                elif p.startswith("/") and not p.startswith("//"): p = self.host + p
                
                v.append({
                    'vod_id': i.get('url'),
                    'vod_name': i.get('title'),
                    'vod_pic': p,
                    'vod_remark': i.get('tags', '')
                })
            return {'list': v, 'page': pg, 'pagecount': 999, 'limit': 36, 'total': data.get('data', {}).get('total', 9999)}

    def detailContent(self, ids):
        res = self.fetch(self.host + ids[0], headers=self.headers)
        doc = pq(res.content)
        m = {d.text().split("：")[0].strip(): d.text().split("：")[1].strip() for d in doc(".comic-meta > div").items() if "：" in d.text()}
        lns = [o.text().strip() for o in doc("#lineSelect option").items()] or ["默认线路"]
        pf, pu = [], []
        for i, n in enumerate(lns):
            eps = doc(f"#grid-{i} .episode-item") or doc(".episode-grid .episode-item")
            el = [f"{e.text().strip()}${e.attr('href')}" for e in eps.items() if e.attr('href')]
            if el: (pf.append(n), pu.append("#".join(el)))
        p = doc(".comic-cover").attr("src")
        return {'list': [{'vod_id': ids[0], 'vod_name': doc(".comic-title").text(), 'vod_pic': "https:"+p if p.startswith("//") else p, 'vod_type': " / ".join([t.text() for t in doc(".comic-tags .tag").items()]), 'vod_year': m.get("年份", ""), 'vod_director': m.get("导演", ""), 'vod_actor': m.get("主演", ""), 'vod_remark': m.get("状态", ""), 'vod_content': doc(".comic-desc").text().strip(), 'vod_play_from': "$$$".join(pf), 'vod_play_url': "$$$".join(pu)}]}

    def searchContent(self, key, quick, pg="1"):
        res = self.fetch(f'{self.host}/search/', headers=self.headers, params={'searchkey': key, 'page': pg})
        return {'list': self.getvs(pq(res.content)(".books-row .item")), 'page': pg}

    def playerContent(self, flag, id, vipFlags):
        return {'parse': 1, 'url': self.host + id if id.startswith('/') else id, 'header': self.headers}
