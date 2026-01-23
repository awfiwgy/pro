import re, json
from base.spider import Spider

class Spider(Spider):
    def __init__(self):
        self.name, self.host = '4015视频', 'https://wwrf.kfoxy55d.cyou'
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36','Referer': self.host}
    def getName(self): return self.name
    def init(self, extend=""): pass
    def isVideoFormat(self, url): return False
    def manualVideoCheck(self): return False
    def homeContent(self, filter):
        c = [{'type_id': '83', 'type_name': '唯美港姐'},{'type_id': '69', 'type_name': '欧美精品'},{'type_id': '74', 'type_name': '成人动漫'},{'type_id': '443', 'type_name': '果冻传媒'},{'type_id': '19', 'type_name': '日韩无码'},{'type_id': '375', 'type_name': '国产自拍'},{'type_id': '405', 'type_name': '催眠洗脑'},{'type_id': '8', 'type_name': '日本无码'},{'type_id': '320', 'type_name': 'VR视角'},{'type_id': '298', 'type_name': '中文字幕'},{'type_id': '138', 'type_name': '自拍偷拍'},{'type_id': '373', 'type_name': '巨乳美乳'},{'type_id': '163', 'type_name': '三级伦理'},{'type_id': '82', 'type_name': '韩国御姐'},{'type_id': '412', 'type_name': 'TS专区'},{'type_id': '58', 'type_name': '日本无码'},{'type_id': '85', 'type_name': '欺辱凌辱'},{'type_id': '132', 'type_name': '杏吧资源'},{'type_id': '91', 'type_name': '古装扮演'},{'type_id': '73', 'type_name': '伦理三级'},{'type_id': '51', 'type_name': '黑料吃瓜'},{'type_id': '303', 'type_name': '强奸乱伦'},{'type_id': '159', 'type_name': '欧美精品'},{'type_id': '134', 'type_name': '国产精品'},{'type_id': '292', 'type_name': 'SM调教'},{'type_id': '13', 'type_name': '强奸乱伦'},{'type_id': '64', 'type_name': '主播直播'},{'type_id': '27', 'type_name': '制服诱惑'},{'type_id': '421', 'type_name': '泰国风情'},{'type_id': '171', 'type_name': '短视频'},{'type_id': '290', 'type_name': '三级伦理'},{'type_id': '136', 'type_name': '欧美精品'},{'type_id': '145', 'type_name': 'SM重味'},{'type_id': '37', 'type_name': '教师学生'},{'type_id': '438', 'type_name': 'SA国际传媒'},{'type_id': '144', 'type_name': 'AV明星'},{'type_id': '150', 'type_name': '教师学生'},{'type_id': '63', 'type_name': '国产色情'},{'type_id': '142', 'type_name': '制服诱惑'},{'type_id': '423', 'type_name': '麻豆资源'},{'type_id': '147', 'type_name': '颜射系列'},{'type_id': '70', 'type_name': '强奸乱伦'},{'type_id': '382', 'type_name': '黄色仓库'},{'type_id': '176', 'type_name': '翹臀美尻'},{'type_id': '170', 'type_name': '美乳巨乳'},{'type_id': '430', 'type_name': '精东影业'},{'type_id': '392', 'type_name': '美乳巨乳'},{'type_id': '410', 'type_name': '其他区'},{'type_id': '351', 'type_name': '无码专区'},{'type_id': '50', 'type_name': '华语AV'},{'type_id': '16', 'type_name': 'AV解说'},{'type_id': '400', 'type_name': '少女萝莉'},{'type_id': '369', 'type_name': '偷拍自拍'},{'type_id': '268', 'type_name': '奶香香资源'},{'type_id': '31', 'type_name': '巨乳系列'},{'type_id': '293', 'type_name': '女同性恋'}]
        return {'class': c}
    def homeVideoContent(self): return self.categoryContent('83', '1', None, None)
    def categoryContent(self, tid, pg, filter, extend): return self._get_videos(f'{self.host}/vodtype/{tid}-{pg}/')
    def detailContent(self, ids):
        try:
            res = self.fetch(f'{self.host}{ids[0]}', headers=self.headers)
            n = re.search(r'<title>(.*?)-', res.text).group(1) if re.search(r'<title>(.*?)-', res.text) else "视频播放"
            p = re.findall(r'href="(/vodplay/.*?/)"', res.text)
            urls = [f"播放源{i+1}${l}" for i, l in enumerate(p)] if p else [f"正片${ids[0].replace('voddetail','vodplay')}"]
            return {'list': [{'vod_id': ids[0], 'vod_name': n, 'vod_play_from': '4015专线', 'vod_play_url': '#'.join(urls)}]}
        except: return {'list': []}
    def playerContent(self, flag, id, vipFlags):
        try:
            res = self.fetch(f'{self.host}{id}', headers=self.headers)
            m = re.search(r'var\s+player_data\s*=\s*(\{.*?\})', res.text)
            if m: return {'parse': 0, 'url': json.loads(m.group(1)).get('url', '').replace('\\/', '/'), 'header': self.headers}
        except: pass
        return {'parse': 0, 'url': ''}
    def searchContent(self, key, quick, pg="1"): return self._get_videos(f'{self.host}/vodsearch/{key}----------{pg}---/')
    def _get_videos(self, url):
        try:
            res, v = self.fetch(url, headers=self.headers), []
            for i in re.findall(r'<dt class="preview-item">.*?</dd>', res.text, re.S):
                v_id, v_pic, v_name = re.search(r'href="(/voddetail/.*?/)"', i), re.search(r'data-original="(.*?)"', i), re.search(r'<h3>(.*?)</h3>', i)
                if v_id and v_name: v.append({'vod_id': v_id.group(1), 'vod_name': v_name.group(1), 'vod_pic': v_pic.group(1) if v_pic else "", 'vod_remarks': ""})
            return {'list': v}
        except: return {'list': []}
