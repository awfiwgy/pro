# -*- coding: utf-8 -*-
import sys,json,re,requests; from pyquery import PyQuery as pq; sys.path.append('..'); from base.spider import Spider
class Spider(Spider):
    host='https://www.mwju.cc'
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36','Referer':'https://www.mwju.cc','X-Requested-With':'XMLHttpRequest','Content-Type':'application/json'}
    def init(self,extend='{}'):pass
    def destroy(self):pass
    def homeContent(self,filter):
        res=self.fetch(self.host+'/cate/',headers=self.headers); doc=pq(res.content)
        classes=[{'type_name':n,'type_id':str(i+1)} for i,n in enumerate(['国产','日韩','欧美','港台','动漫','里番'])]
        filters={}; tags=[{'n':i.text(),'v':i.attr('data-value')} for i in doc(".ctag .filter-options a").items()]
        status=[{'n':i.text(),'v':i.attr('data-value')} for i in doc(".szt .filter-options a").items()]
        years=[{'n':i.text(),'v':i.attr('data-value')} for i in doc(".sgx .filter-options a").items()]
        sorts=[{'n':i.text(),'v':i.attr('data-value')} for i in doc(".spx .filter-options a").items()]
        for c in classes: filters[c['type_id']]=[{'key':'tag','name':'剧情','value':tags},{'key':'status','name':'状态','value':status},{'key':'year','name':'年份','value':years},{'key':'sort','name':'排序','value':sorts}]
        return {'class':classes,'list':self.getvs(pq(self.fetch(self.host,headers=self.headers).content)(".books-row .item")),'filters':filters}
    def getvs(self,items):
        v=[]
        for i in items.items():
            img=i(".thumb_img"); p=img.attr("data-src") or img.attr("data-original") or img.attr("src")
            if p: p="https:"+p if p.startswith("//") else (self.host+p if p.startswith("/") else p)
            v.append({'vod_id':i("a").eq(0).attr('href'),'vod_name':i(".title").text().strip(),'vod_pic':p,'vod_remark':i(".badge").text().strip() or i(".desc").text().strip()})
        return v
    def categoryContent(self,tid,pg,filter,extend):
        pg=int(pg); payload={"page":{"page":pg,"pageSize":36},"category":"video","sort":int(extend.get('sort',0)),"comic":{"status":-1,"day":0,"year":0,"tag":""},"video":{"year":int(extend.get('year',0)) if extend.get('year','0').isdigit() else 0,"typeId":int(tid),"area":"","lang":"","status":int(extend.get('status',-1)),"tag":extend.get('tag','')},"novel":{"status":-1,"day":0,"sortId":0}}
        res=self.post(self.host+'/api/cate/',headers=self.headers,data=json.dumps(payload)); data=json.loads(res.content); items=data.get('data',{}).get('list',[]); v=[]
        for i in items:
            p=i.get('pic',''); p="https:"+p if p.startswith("//") else (self.host+p if p.startswith("/") and not p.startswith("//") else p)
            v.append({'vod_id':i.get('url'),'vod_name':i.get('title'),'vod_pic':p,'vod_remark':i.get('tags','')})
        total=data.get('data',{}).get('total',0); return {'list':v,'page':pg,'pagecount':(total//36)+(1 if total%36>0 else 0),'limit':36,'total':total}
    def detailContent(self,ids):
        doc=pq(self.fetch(self.host+ids[0],headers=self.headers).content)
        m={d.text().split("：")[0].strip():d.text().split("：")[1].strip() for d in doc(".comic-meta > div").items() if "：" in d.text()}
        lns=[o.text().strip() for o in doc("#lineSelect option").items()] or ["默认线路"]; pf=[]; pu=[]
        for i,n in enumerate(lns):
            eps=doc(f"#grid-{i} .episode-item") or doc(".episode-grid .episode-item"); el=[f"{e.text().strip()}${e.attr('href')}" for e in eps.items() if e.attr('href')]
            if el: pf.append(n); pu.append("#".join(el))
        p=doc(".comic-cover").attr("src"); p="https:"+p if p and p.startswith("//") else (p if p else "")
        return {'list':[{'vod_id':ids[0],'vod_name':doc(".comic-title").text(),'vod_pic':p,'vod_type':" / ".join([t.text() for t in doc(".comic-tags .tag").items()]),'vod_year':m.get("年份",""),'vod_director':m.get("导演",""),'vod_actor':m.get("主演",""),'vod_remark':m.get("状态",""),'vod_content':doc(".comic-desc").text().strip(),'vod_play_from':"$$$".join(pf),'vod_play_url':"$$$".join(pu)}]}
    def searchContent(self,key,quick,pg="1"):
        pg=int(pg); api_url=f'{self.host}/api/search'; params={'keyword':key,'type':'mh','page':pg,'pageSize':20}
        try:
            res=self.fetch(api_url,headers=self.headers,params=params); data=json.loads(res.content); v=[]
            if data.get('code')==200 and data.get('data'):
                for i in data.get('data',{}).get('list',[]):
                    p=i.get('cover','') or i.get('pic',''); p="https:"+p if p.startswith("//") else (self.host+p if p.startswith("/") and not p.startswith("//") else p)
                    st=i.get('status'); rem="完结" if st==2 else ("连载" if st==1 else str(i.get('tags','')))
                    v.append({'vod_id':i.get('url'),'vod_name':i.get('title'),'vod_pic':p,'vod_remark':rem})
            return {'list':v,'page':pg}
        except: return {'list':[],'page':pg}
    def playerContent(self,flag,id,vipFlags):
        return {'parse':1,'url':self.host+id if id.startswith('/') else id,'header':self.headers}
