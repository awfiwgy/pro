/*
@header({
  searchable: 1,
  filterable: 1,
  quickSearch: 1,
  title: '聚合短剧',
  lang: 'ds'
})
*/

// 全局配置
const aggConfig = {
  headers: {
    default: {
      'User-Agent': 'okhttp/3.12.11',
      'content-type': 'application/json; charset=utf-8'
    },
    niuniu: {
      'Cache-Control': 'no-cache',
      'Content-Type': 'application/json;charset=UTF-8',
      'User-Agent': 'okhttp/4.12.0'
    }
  },
  platform: {
    百度: {
      host: 'https://api.jkyai.top',
      url1: '/API/bddjss.php?name=fyclass&page=fypage',
      url2: '/API/bddjss.php?id=fyid',
      search: '/API/bddjss.php?name=**&page=fypage'
    },
    甜圈: {
      host: 'https://mov.cenguigui.cn',
      url1: '/duanju/api.php?classname',
      url2: '/duanju/api.php?book_id',
      search: '/duanju/api.php?name'
    },
    锦鲤: {
      host: 'https://api.jinlidj.com',
      search: '/api/search',
      url2: '/api/detail'
    },
    番茄: {
      host: 'https://reading.snssdk.com',
      url1: '/reading/bookapi/bookmall/cell/change/v',
      url2: 'https://fqgo.52dns.cc/catalog',
      search: 'https://fqgo.52dns.cc/search'
    },
    星芽: {
      host: 'https://app.whjzjx.cn',
      url1: '/cloud/v2/theater/home_page?theater_class_id',
      url2: '/v2/theater_parent/detail',
      search: '/v3/search',
      loginUrl: 'https://u.shytkjgs.com/user/v1/account/login'
    },
    西饭: {
      host: 'https://xifan-api-cn.youlishipin.com',
      url1: '/xifan/drama/portalPage',
      url2: '/xifan/drama/getDuanjuInfo',
      search: '/xifan/search/getSearchList'
    },
    七猫: {
      host: 'https://api-store.qmplaylet.com',
      url1: '/api/v1/playlet/index',
      url2: 'https://api-read.qmplaylet.com/player/api/v1/playlet/info',
      search: '/api/v1/playlet/search'
    },
    围观: {
      host: 'https://api.drama.9ddm.com',
      url1: '/drama/home/shortVideoTags',
      url2: '/drama/home/shortVideoDetail',
      search: '/drama/home/search'
    },
    碎片: {
      host: 'https://free-api.bighotwind.cc',
      url1: '/papaya/papaya-api/theater/tags',
      url2: '/papaya/papaya-api/videos/info',
      search: '/papaya/papaya-api/videos/page'
    }
  },
  platformList: [
    { name: '甜圈短剧', id: '甜圈' },
    { name: '锦鲤短剧', id: '锦鲤' },
    { name: '番茄短剧', id: '番茄' },
    { name: '星芽短剧', id: '星芽' },
    { name: '西饭短剧', id: '西饭' },
    { name: '七猫短剧', id: '七猫' },
    { name: '百度短剧', id: '百度' },
    { name: '围观短剧', id: '围观' },
    { name: '碎片剧场', id: '碎片' }
  ],
  search: {
    limit: 30,
    timeout: 6000
  }
};

// 过滤配置
const ruleFilterDef = {
  百度: { area: '逆袭' },
  甜圈: { area: '推荐榜' },
  锦鲤: { area: '' },
  番茄: { area: 'videoseries_hot' },
  星芽: { area: '1' },
  西饭: { area: '' },
  七猫: { area: '0' },
  围观: { area: '' },
  碎片: { area: '' }
};

// 星芽短剧token变量
let xingya_headers = {};

// 辅助函数：处理响应数据
function parseResponse(response) {
  try {
    console.log(`🔍原始响应类型: ${typeof response}`);
    
    if (typeof response === 'string') {
      // 如果是字符串，直接解析
      console.log(`🔍解析字符串响应`);
      return JSON.parse(response);
    } else if (response && typeof response === 'object') {
      // 如果是对象，检查是否有 content 字段
      console.log(`🔍响应是对象，检查结构...`);
      
      // 先检查是否是常见的HTTP响应对象
      if (response.content && typeof response.content === 'string') {
        console.log(`🔍解析content字段中的JSON`);
        return JSON.parse(response.content);
      }
      
      if (response.body && typeof response.body === 'string') {
        console.log(`🔍解析body字段中的JSON`);
        return JSON.parse(response.body);
      }
      
      if (response.data && typeof response.data === 'string') {
        console.log(`🔍解析data字段中的JSON`);
        return JSON.parse(response.data);
      }
      
      // 检查是否已经是解析好的数据对象
      if (response.code !== undefined || response.data !== undefined) {
        console.log(`🔍已经是解析好的数据对象，直接使用`);
        return response;
      }
      
      // 其他情况，尝试将对象转为JSON字符串再解析
      console.log(`🔍尝试将对象转为JSON字符串再解析`);
      try {
        const jsonString = JSON.stringify(response);
        console.log(`🔍转换后的字符串（前200字符）: ${jsonString.substring(0, 200)}`);
        return JSON.parse(jsonString);
      } catch (stringifyError) {
        console.log(`🔍对象转字符串失败，尝试直接作为响应对象`);
        return response;
      }
    } else {
      // 其他情况转为字符串再尝试
      console.log(`🔍将响应转为字符串再解析`);
      return JSON.parse(String(response));
    }
  } catch (error) {
    console.log(`❌解析响应失败: ${error.message}`);
    console.log(`❌原始响应值:`, response);
    return null;
  }
}

// 工具函数
function getRandomItem(items) {
  return items[Math.random() * items.length | 0];
}

function guid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
    var r = Math.random() * 16 | 0,
      v = c == 'x' ? r : (r & 0x3 | 0.8);
    return v.toString(16);
  });
}

// 初始化星芽短剧token
async function init(cfg) {
  try {
    const data = {
      'device': '24250683a3bdb3f118dff25ba4b1cba1a'
    };
    const options = {
      method: 'POST',
      headers: {
        'User-Agent': 'okhttp/4.10.0',
        'platform': '1',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    };
    let html = await req(aggConfig.platform.星芽.loginUrl, options);
    const res = JSON.parse(html);
    const token = res?.data?.token || res?.data?.data?.token;
    xingya_headers = { ...aggConfig.headers.default, authorization: token };
    console.log('星芽短剧token获取成功');
  } catch (e) {
    console.log(`星芽短剧token获取失败: ${e.message}`);
  }
  return true;
}

// 首页分类
async function home(filter) {
  const classes = aggConfig.platformList.map(item => ({
    type_name: item.name,
    type_id: item.id
  }));

  return JSON.stringify({
    class: classes
  });
}

// 首页推荐
async function homeVod(params) {
  return await recommend();
}

// 推荐
async function recommend() {
  let recommendList = [];

  if (aggConfig.platformList && aggConfig.platformList.length > 0) {
    const randomPlat = getRandomItem(aggConfig.platformList);
    console.log(`✅随机选择平台: ${randomPlat.name}`);
    const platBaseConfig = aggConfig.platform[randomPlat.id];
    const platDefaultFilter = ruleFilterDef[randomPlat.id] || {};
    const defaultArea = platDefaultFilter.area || '';

    try {
      let platContentList = [];

      if (randomPlat.id === '百度') {
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1.replace('fyclass', defaultArea).replace('fypage', '1')}`;
        const response = await req(requestUrl, { headers: aggConfig.headers.default });
        const res = parseResponse(response);
        if (res && res.data) {
          platContentList = res.data.map(item => ({
            vod_id: `百度@${item.id}`,
            vod_name: item.title,
            vod_pic: item.cover,
            vod_remarks: `更新至${item.totalChapterNum}集`
          }));
        }
      } else if (randomPlat.id === '甜圈') {
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}=${defaultArea}&offset=1`;
        const response = await req(requestUrl, { headers: aggConfig.headers.default });
        const res = parseResponse(response);
        if (res && res.data) {
          platContentList = res.data.map(item => ({
            vod_id: `甜圈@${item.book_id}`,
            vod_name: item.title,
            vod_pic: item.cover,
            vod_remarks: item.copyright || '未知'
          }));
        }
      } else if (randomPlat.id === '锦鲤') {
        const requestBody = JSON.stringify({
          page: 1,
          limit: 10,
          type_id: defaultArea,
          year: '',
          keyword: ''
        });
        const response = await req(
          `${platBaseConfig.host}${platBaseConfig.search}`,
          { method: 'POST', body: requestBody }
        );
        const res = parseResponse(response);
        if (res && res.data && res.data.list) {
          platContentList = res.data.list.map(item => ({
            vod_id: `锦鲤@${item.vod_id}`,
            vod_name: item.vod_name || '未知短剧',
            vod_pic: item.vod_pic || '',
            vod_remarks: `${item.vod_total || 0}集`
          }));
        }
      } else if (randomPlat.id === '番茄') {
        const fmSessionId = new Date().toISOString().slice(0, 16).replace(/-|T:/g, '');
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}?change_type=0&selected_items=${defaultArea}&tab_type=8&cell_id=6952850996422770718&version_tag=video_feed_refactor&device_id=1423244030195267&aid=1967&app_name=novelapp&ssmix=a&session_id=${fmSessionId}`;
        const response = await req(requestUrl, { headers: aggConfig.headers.default });
        const res = parseResponse(response);
        const fmItems = res?.data?.cell_view?.cell_data || [];
        platContentList = fmItems.map(item => {
          const videoInfo = item.video_data?.[0] || item;
          return {
            vod_id: `番茄@${videoInfo.series_id || videoInfo.book_id || ''}`,
            vod_name: videoInfo.title || '未知标题',
            vod_pic: videoInfo.cover || videoInfo.horiz_cover || '',
            vod_remarks: '未知'
          };
        });
      } else if (randomPlat.id === '星芽') {
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}=${defaultArea}&type=1&class2_ids=0&page_num=1&page_size=10`;
        const response = await req(requestUrl, { headers: xingya_headers });
        const res = parseResponse(response);
        if (res && res.data && res.data.list) {
          platContentList = res.data.list.map(item => {
            const detailUrl = `${platBaseConfig.host}${platBaseConfig.url2}?theater_parent_id=${item.theater.id}`;
            return {
              vod_id: `星芽@${detailUrl}`,
              vod_name: item.theater.title,
              vod_pic: item.theater.cover_url,
              vod_remarks: `${item.theater.total || 0}集`
            };
          });
        }
      } else if (randomPlat.id === '西饭') {
        const [typeId, typeName] = defaultArea.split('@');
        const ts = Math.floor(Date.now() / 1000);
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}?reqType=aggregationPage&offset=0&categoryId=${typeId}&quickEngineVersion=-1&scene=&categoryNames=${encodeURIComponent(typeName)}&categoryVersion=1&density=1.5&pageID=page_theater&version=2001001&androidVersionCode=28&requestId=${ts}aa498144140ef297&appId=drama&teenMode=false&userBaseMode=false&session=eyJpbmZvIjp7InVpZCI6IiIsInJ0IjoiMTc0MDY1ODI5NCIsInVuIjoiT1BHXzFlZGQ5OTZhNjQ3ZTQ1MjU4Nzc1MTE2YzFkNzViN2QwIiwiZnQiOiIxNzQwNjU4Mjk0In19&feedssession=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dHlwIjowLCJidWlkIjoxNjMzOTY4MTI2MTQ4NjQxNTM2LCJhdWQiOiJkcmFtYSIsInZlciI6MiwicmF0IjoxNzQwNjU4Mjk0LCJ1bm0iOiJPUEdfMWVkZDk5NmE2NDdlNDUyNTg3NzUxMTZjMWQ3NWI3ZDAiLCJpZCI6IjNiMzViZmYzYWE0OTgxNDQxNDBlZjI5N2JkMDY5NGNhIiwiZXhwIjoxNzQxMjYzMDk0LCJkYyI6Imd6cXkifQ.JS3QY6ER0P2cQSxAE_OGKSMIWNAMsYUZ3mJTnEpf-Rc`;
        const response = await req(requestUrl, { headers: aggConfig.headers.default });
        const res = parseResponse(response);
        const xfElements = res.result.elements || [];
        platContentList = [];
        xfElements.forEach(soup => {
          soup.contents.forEach(vod => {
            const dj = vod.duanjuVo;
            platContentList.push({
              vod_id: `西饭@${dj.duanjuId}#${dj.source}`,
              vod_name: dj.title,
              vod_pic: dj.coverImageUrl,
              vod_remarks: `${dj.total || 0}集`
            });
          });
        });
      } else if (randomPlat.id === '七猫') {
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.url1}?tag_id=${defaultArea}&playlet_privacy=1&operation=1`;
        const response = await req(requestUrl, { headers: aggConfig.headers.default });
        const res = parseResponse(response);
        platContentList = (res?.data?.list || []).map(item => ({
          vod_id: `七猫@${encodeURIComponent(item.playlet_id)}`,
          vod_name: item.title || '未知标题',
          vod_pic: item.image_link || '',
          vod_remarks: `${item.total_episode_num || 0}集`
        }));
      } else if (randomPlat.id === '围观') {
        const postData = JSON.stringify({
          "audience": "",
          "page": 1,
          "pageSize": 10,
          "searchWord": "",
          "subject": ""
        });
        const response = await req(
          `${platBaseConfig.host}${platBaseConfig.search}`,
          { method: 'POST', body: postData }
        );
        const res = parseResponse(response);
        if (res && res.data) {
          platContentList = res.data.map(it => ({
            vod_id: `围观@${it.oneId}`,
            vod_name: it.title,
            vod_pic: it.vertPoster,
            vod_remarks: `集数:${it.episodeCount} 播放:${it.viewCount}`
          }));
        }
      } else if (randomPlat.id === '碎片') {
        const requestUrl = `${platBaseConfig.host}${platBaseConfig.search}?type=5&tagId=&pageNum=1&pageSize=10`;
        const response = await req(requestUrl, { headers: aggConfig.headers.default });
        const res = parseResponse(response);
        if (res && res.list) {
          platContentList = res.list.map(it => {
            let compoundId = it.itemId + '@' + it.videoCode;
            return {
              vod_id: `碎片@${compoundId}`,
              vod_name: it.title,
              vod_pic: "https://speed.hiknz.com/papaya/papaya-file/files/download/" + it.imageKey + "/" + it.imageName,
              vod_remarks: `集数:${it.episodesMax} 播放:${it.hitShowNum}`
            };
          });
        }
      }

      recommendList.push(...platContentList.slice(0, 10));
      console.log(`✅从${randomPlat.name}获取${platContentList.length}条推荐，显示前10条`);
    } catch (error) {
      console.log(`❌随机推荐拉取失败（平台：${randomPlat.name}）：${error.message}`);
      recommendList.push({
        vod_id: '',
        vod_name: '推荐加载失败',
        vod_pic: '',
        vod_remarks: `当前平台（${randomPlat.name}）数据获取异常，请稍后重试`
      });
    }
  }

  return JSON.stringify({
    list: recommendList
  });
}

// 分类列表
async function category(tid, pg, filter, extend) {
  const videos = [];
  const page = pg || 1;
  const plat = aggConfig.platform[tid];
  const area = filter && filter.area ? filter.area : ruleFilterDef[tid]?.area || '';

  if (!plat) {
    console.log(`❌未知的平台: ${tid}`);
    return JSON.stringify({
      list: videos,
      page: page,
      pagecount: 1,
      limit: 0,
      total: 0
    });
  }

  switch (tid) {
    case '百度': {
      const url = `${plat.host}${plat.url1.replace('fyclass', area).replace('fypage', page)}`;
      console.log(`✅百度分类请求URL: ${url}`);
      const response = await req(url, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      if (res && res.data) {
        res.data.forEach(it => {
          videos.push({
            vod_id: `百度@${it.id}`,
            vod_name: it.title,
            vod_pic: it.cover,
            vod_remarks: `更新至${it.totalChapterNum}集`
          });
        });
      }
      break;
    }
    case '甜圈': {
      const url = `${plat.host}${plat.url1}=${area}&offset=${page}`;
      console.log(`✅甜圈分类请求URL: ${url}`);
      const response = await req(url, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      if (res && res.data) {
        res.data.forEach(it => {
          videos.push({
            vod_id: `甜圈@${it.book_id}`,
            vod_name: it.title,
            vod_pic: it.cover,
            vod_remarks: it.copyright
          });
        });
      }
      break;
    }
    case '锦鲤': {
      const body = JSON.stringify({ page: page, limit: 24, type_id: area, year: '', keyword: '' });
      const response = await req(plat.host + plat.search, { method: 'POST', body });
      const res = parseResponse(response);
      if (res && res.data && res.data.list) {
        res.data.list.forEach(item => {
          videos.push({
            vod_id: `锦鲤@${item.vod_id}`,
            vod_name: item.vod_name || '',
            vod_pic: item.vod_pic,
            vod_remarks: `${item.vod_total}集`
          });
        });
      }
      break;
    }
    case '番茄': {
      const sessionId = new Date().toISOString().slice(0, 16).replace(/-|T:/g, '');
      let url = `${plat.host}${plat.url1}?change_type=0&selected_items=${area}&tab_type=8&cell_id=6952850996422770718&version_tag=video_feed_refactor&device_id=1423244030195267&aid=1967&app_name=novelapp&ssmix=a&session_id=${sessionId}`;
      if (page > 1) url += `&offset=${(page - 1) * 12}`;

      console.log(`✅番茄分类请求URL: ${url}`);
      const response = await req(url, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      
      let items = [];
      if (res?.data?.cell_view?.cell_data) items = res.data.cell_view.cell_data;
      else if (res?.search_tabs) items = res.search_tabs.find(t => t.title === '短剧' && t.data)?.data || [];
      else if (Array.isArray(res?.data)) items = res.data;
      else if (res?.data) items = [res.data];
      else items = [res || {}];

      items.forEach(item => {
        const videoData = item.video_data?.[0] || item;
        videos.push({
          vod_id: `番茄@${videoData.series_id || videoData.book_id || videoData.id || ''}`,
          vod_name: videoData.title || '未知短剧',
          vod_pic: videoData.cover || videoData.horiz_cover || '',
          vod_remarks: videoData.sub_title || videoData.rec_text || ''
        });
      });
      break;
    }
    case '星芽': {
      const url = `${plat.host}${plat.url1}=${area}&type=1&class2_ids=0&page_num=${page}&page_size=24`;
      console.log(`✅星芽分类请求URL: ${url}`);
      const response = await req(url, { headers: xingya_headers });
      const res = parseResponse(response);
      if (res && res.data && res.data.list) {
        res.data.list.forEach(it => {
          const id = `${plat.host}${plat.url2}?theater_parent_id=${it.theater.id}`;
          videos.push({
            vod_id: `星芽@${id}`,
            vod_name: it.theater.title,
            vod_pic: it.theater.cover_url,
            vod_remarks: `${it.theater.total}集`
          });
        });
      }
      break;
    }
    case '西饭': {
      const [typeId, typeName] = area.split('@');
      const ts = Math.floor(Date.now() / 1000);
      const url = `${plat.host}${plat.url1}?reqType=aggregationPage&offset=${(page - 1) * 30}&categoryId=${typeId}&quickEngineVersion=-1&scene=&categoryNames=${encodeURIComponent(typeName)}&categoryVersion=1&density=1.5&pageID=page_theater&version=2001001&androidVersionCode=28&requestId=${ts}aa498144140ef297&appId=drama&teenMode=false&userBaseMode=false&session=eyJpbmZvIjp7InVpZCI6IiIsInJ0IjoiMTc0MDY1ODI5NCIsInVuIjoiT1BHXzFlZGQ5OTZhNjQ3ZTQ1MjU4Nzc1MTE2YzFkNzViN2QwIiwiZnQiOiIxNzQwNjU4Mjk0In19&feedssession=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dHlwIjowLCJidWlkIjoxNjMzOTY4MTI2MTQ4NjQxNTM2LCJhdWQiOiJkcmFtYSIsInZlciI6MiwicmF0IjoxNzQwNjU4Mjk0LCJ1bm0iOiJPUEdfMWVkZDk5NmE2NDdlNDUyNTg3NzUxMTZjMWQ3NWI3ZDAiLCJpZCI6IjNiMzViZmYzYWE0OTgxNDQxNDBlZjI5N2JkMDY5NGNhIiwiZXhwIjoxNzQxMjYzMDk0LCJkYyI6Imd6cXkifQ.JS3QY6ER0P2cQSxAE_OGKSMIWNAMsYUZ3mJTnEpf-Rc`;

      console.log(`✅西饭分类请求URL: ${url}`);
      const response = await req(url, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      if (res && res.result && res.result.elements) {
        res.result.elements.forEach(soup => {
          soup.contents.forEach(vod => {
            const dj = vod.duanjuVo;
            videos.push({
              vod_id: `西饭@${dj.duanjuId}#${dj.source}`,
              vod_name: dj.title,
              vod_pic: dj.coverImageUrl,
              vod_remarks: `${dj.total}集`
            });
          });
        });
      }
      break;
    }
    case '七猫': {
      const url = `${plat.host}${plat.url1}?tag_id=${area}&playlet_privacy=1&operation=1`;
      console.log(`✅七猫分类请求URL: ${url}`);
      const response = await req(url, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      if (res?.data?.list) {
        (res.data.list || []).forEach(item => {
          videos.push({
            vod_id: `七猫@${encodeURIComponent(item.playlet_id)}`,
            vod_name: item.title || '',
            vod_pic: item.image_link || '',
            vod_remarks: `${item.total_episode_num || 0}集`
          });
        });
      }
      break;
    }
    case '围观': {
      const postData = JSON.stringify({
        "audience": "全部受众",
        "page": page,
        "pageSize": 30,
        "searchWord": "",
        "subject": "全部主题"
      });
      console.log(`✅围观分类请求URL: ${plat.host}${plat.search}`);
      const response = await req(`${plat.host}${plat.search}`, { 
        method: 'POST', 
        headers: aggConfig.headers.default, 
        body: postData 
      });
      const res = parseResponse(response);
      if (res && res.data) {
        res.data.forEach(it => {
          videos.push({
            vod_id: `围观@${it.oneId}`,
            vod_name: it.title,
            vod_pic: it.vertPoster,
            vod_remarks: `集数:${it.episodeCount} 播放:${it.viewCount}`
          });
        });
      }
      break;
    }
    case '碎片': {
      const requestUrl = `${plat.host}${plat.search}?type=5&tagId=&pageNum=${page}&pageSize=24`;
      console.log(`✅碎片分类请求URL: ${requestUrl}`);
      const response = await req(requestUrl, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      if (res && res.list) {
        res.list.forEach(it => {
          let compoundId = it.itemId + '@' + it.videoCode;
          videos.push({
            vod_id: `碎片@${compoundId}`,
            vod_name: it.title,
            vod_pic: "https://speed.hiknz.com/papaya/papaya-file/files/download/" + it.imageKey + "/" + it.imageName,
            vod_remarks: `集数:${it.episodesMax} 播放:${it.hitShowNum}`
          });
        });
      }
      break;
    }
  }

  return JSON.stringify({
    list: videos,
    page: page,
    pagecount: page + 1,
    limit: videos.length,
    total: videos.length * (page + 1)
  });
}

// 详情页
async function detail(id) {
  const parts = id.split('@');
  const platform = parts[0];
  const did = parts.slice(1).join('@');
  const plat = aggConfig.platform[platform];
  let vod = {};

  if (!plat) {
    console.log(`❌未知的平台: ${platform}`);
    return JSON.stringify({
      list: [{
        vod_id: id,
        vod_name: '平台不支持',
        vod_pic: '',
        vod_remarks: '该平台暂不支持',
        vod_content: '',
        vod_play_from: '',
        vod_play_url: ''
      }]
    });
  }

  switch (platform) {
    case '百度': {
      const response = await req(`${plat.host}${plat.url2.replace('fyid', did)}`);
      const res = parseResponse(response);
      if (res) {
        vod = {
          vod_id: id,
          vod_name: res.title,
          vod_pic: res.data?.[0]?.cover || '',
          vod_remarks: `更新至:${res.total || 0}集`,
          vod_content: '',
          vod_play_from: '百度短剧',
          vod_play_url: res.data ? res.data.map(item => `${item.title}$${item.video_id}`).join("#") : ''
        };
      }
      break;
    }
    case '甜圈': {
      const response = await req(`${plat.host}${plat.url2}=${did}`);
      const res = parseResponse(response);
      if (res) {
        vod = {
          vod_id: id,
          vod_name: res.book_name || res.title || '未知标题',
          vod_pic: res.book_pic || res.cover || '',
          vod_remarks: `更新时间:${res.time || '未知'}`,
          vod_content: res.desc || '',
          vod_play_from: '甜圈短剧',
          vod_play_url: res.data && Array.isArray(res.data) 
            ? res.data.map(item => `${item.title || '第1集'}$${item.video_id || item.id || ''}`).join('#')
            : ''
        };
      }
      break;
    }
    case '锦鲤': {
      const response = await req(`${plat.host}${plat.url2}/${did}`);
      const res = parseResponse(response);
      if (res && res.data) {
        const list = res.data;
        const playUrls = list.player ? Object.keys(list.player).map(key => `${key}$${list.player[key]}`) : [];
        vod = {
          vod_id: id,
          vod_name: list.vod_name || '暂无名称',
          vod_pic: list.vod_pic || '暂无图片',
          vod_remarks: list.vod_remarks || '暂无备注',
          vod_content: '',
          vod_play_from: '锦鲤短剧',
          vod_play_url: playUrls.join('#')
        };
      }
      break;
    }
    case '番茄': {
      const response = await req(`${plat.url2}?book_id=${did}`);
      const res = parseResponse(response);
      if (res && res.data) {
        const bookInfo = res.data.book_info;
        const playList = res.data.item_data_list ? 
          res.data.item_data_list.map(item => `${item.title}$${item.item_id}`).join('#') : '';
        vod = {
          vod_id: id,
          vod_name: bookInfo.book_name,
          vod_pic: bookInfo.thumb_url || bookInfo.audio_thumb_uri || '',
          vod_remarks: `更新至${res.data.item_data_list?.length || 0}集`,
          vod_content: '',
          vod_play_from: '番茄短剧',
          vod_play_url: playList
        };
      }
      break;
    }
    case '星芽': {
      const response = await req(did, { headers: xingya_headers });
      const res = parseResponse(response);
      if (res && res.data) {
        const data = res.data;
        const playUrls = data.theaters ? 
          data.theaters.map(it => `${it.num}$${it.son_video_url}`) : [];
        vod = {
          vod_id: id,
          vod_name: data.title,
          vod_pic: data.cover_url || '',
          vod_remarks: data.desc_tags + '',
          vod_content: '',
          vod_play_from: '星芽短剧',
          vod_play_url: playUrls.join('#')
        };
      }
      break;
    }
    case '西饭': {
      const [duanjuId, source] = did.split('#');
      const url = `${plat.host}${plat.url2}?duanjuId=${duanjuId}&source=${source}&openFrom=homescreen&type=&pageID=page_inner_flow&density=1.5&version=2001001&androidVersionCode=28&requestId=1740658944980aa498144140ef297&appId=drama&teenMode=false&userBaseMode=false&session=eyJpbmZvIjp7InVpZCI6IiIsInJ0IjoiMTc0MDY1ODI5NCIsInVuIjoiT1BHXzFlZGQ5OTZhNjQ3ZTQ1MjU4Nzc1MTE2YzFkNzViN2QwIiwiZnQiOiIxNzQwNjU4Mjk0In19&feedssession=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1dHlwIjowLCJidWlkIjoxNjMzOTY4MTI2MTQ4NjQxNTM2LCJhdWQiOiJkcmFtYSIsInZlciI6MiwicmF0IjoxNzQwNjU4Mjk0LCJ1bm0iOiJPUEdfMWVkZDk5NmE2NDdlNDUyNTg3NzUxMTY2YzFkNzViN2QwIiwiZXhwIjoxNzQxMjYzMDk0LCJkYyI6Imd6cXkifQ.JS3QY6ER0P2cQSxAE_OGKSMIWNAMsYUZ3mJTnEpf-Rc`;

      const response = await req(url, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      if (res && res.result) {
        const data = res.result;
        const playUrls = data.episodeList ? 
          data.episodeList.map(ep => `${ep.index}$${ep.playUrl}`) : [];
        vod = {
          vod_id: id,
          vod_name: data.title,
          vod_pic: data.coverImageUrl || '',
          vod_remarks: data.updateStatus === 'over' ? `${data.total}集 已完结` : `更新${data.total}集`,
          vod_content: '',
          vod_play_from: '西饭短剧',
          vod_play_url: playUrls.join('#')
        };
      }
      break;
    }
    case '七猫': {
      const didDecoded = decodeURIComponent(did);
      const url = `${plat.url2}?playlet_id=${didDecoded}`;
      const response = await req(url, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      if (res && res.data) {
        const data = res.data;
        vod = {
          vod_id: id,
          vod_name: data.title || '未知标题',
          vod_pic: data.image_link || '未知图片',
          vod_remarks: `${data.tags || ''} ${data.total_episode_num || 0}集`,
          vod_content: '',
          vod_play_from: '七猫短剧',
          vod_play_url: data.play_list ? data.play_list.map(it => `${it.sort}$${it.video_url}`).join('#') : ''
        };
      }
      break;
    }
    case '围观': {
      const response = await req(
        `${plat.host}${plat.url2}?oneId=${did}&page=1&pageSize=1000`,
        { headers: aggConfig.headers.default }
      );
      const res = parseResponse(response);
      if (res && res.data && res.data.length > 0) {
        const data = res.data;
        const firstEpisode = data[0];
        vod = {
          vod_id: id,
          vod_name: firstEpisode.title,
          vod_pic: firstEpisode.vertPoster || '',
          vod_remarks: `共${data.length}集`,
          vod_content: '',
          vod_play_from: '围观短剧',
          vod_play_url: data.map(episode => {
            return `${episode.title}第${episode.playOrder}集$${episode.playSetting}`;
          }).join('#')
        };
      }
      break;
    }
    case '碎片': {
      const [itemId, videoCode] = did.split('@');
      const requestUrl = `${plat.host}${plat.url2}?videoCode=${videoCode}&itemId=${itemId}`;
      const response = await req(requestUrl, { headers: aggConfig.headers.default });
      const res = parseResponse(response);
      if (res) {
        const data = res.data || res;
        vod = {
          vod_id: id,
          vod_name: data.title,
          vod_pic: "https://speed.hiknz.com/papaya/papaya-file/files/download/" + data.imageKey + "/" + data.imageName,
          vod_remarks: `共${data.episodesMax || 0}集`,
          vod_content: '',
          vod_play_from: '碎片剧场',
          vod_play_url: (data.episodesList || []).map(episode => {
            let episodeTitle = `第${episode.episodes}集`;
            let playUrl = "";

            if (episode.resolutionList && episode.resolutionList.length > 0) {
              episode.resolutionList.sort((a, b) => b.resolution - a.resolution);
              let bestResolution = episode.resolutionList[0];
              playUrl = `https://speed.hiknz.com/papaya/papaya-file/files/download/${bestResolution.fileKey}/${bestResolution.fileName}`;
            }
            return playUrl ? `${episodeTitle}$${playUrl}` : null;
          }).filter(item => item !== null).join('#')
        };
      }
      break;
    }
  }

  return JSON.stringify({
    list: [vod]
  });
}

// 播放地址
async function play(flag, id, flags) {
  if (/百度/.test(flag)) {
    const response = await req(`https://api.jkyai.top/API/bddjss.php?video_id=${id}`);
    const item = parseResponse(response);
    if (item && item.data && item.data.qualities) {
      let qualities = item.data.qualities;
      let urls = [];

      const qualityOrder = ["1080p", "sc", "sd"];
      const qualityNames = {
        "1080p": "蓝光",
        "sc": "超清",
        "sd": "标清"
      };

      qualityOrder.forEach(qualityKey => {
        let quality = qualities.find(q => q.quality === qualityKey);
        if (quality) {
          urls.push(qualityNames[qualityKey], quality.download_url);
        }
      });

      return JSON.stringify({
        parse: 0,
        url: urls
      });
    }
  }
  if (/甜圈/.test(flag)) {
    return JSON.stringify({ 
      parse: 0, 
      url: `https://mov.cenguigui.cn/duanju/api.php?video_id=${id}&type=mp4` 
    });
  }
  if (/锦鲤/.test(flag)) {
    try {
      const html = await req(`${id}&auto=1`, { headers: { referer: 'https://www.jinlidj.com/' } });
      const match = html.match(/let data\s*=\s*({[^;]*});/);
      if (match) {
        const data = JSON.parse(match[1]);
        return JSON.stringify({ parse: 0, url: data.url });
      }
    } catch (error) {
      console.log(`锦鲤播放地址获取失败: ${error.message}`);
    }
  }
  if (/番茄/.test(flag)) {
    const response = await req(`https://fqgo.52dns.cc/video?item_ids=${id}`, { headers: aggConfig.headers.default });
    const res = parseResponse(response);
    if (res && res.data && res.data[id]) {
      const videoModel = JSON.parse(res.data[id].video_model);
      const url = videoModel?.video_list?.video_1 ? atob(videoModel.video_list.video_1.main_url) : '';
      return JSON.stringify({ parse: 0, url });
    }
  }
  if (/围观/.test(flag)) {
    let playSetting;
    try {
      playSetting = typeof id === 'string' ? JSON.parse(id) : id;
    } catch (e) {
      return JSON.stringify({ parse: 0, url: id });
    }
    let urls = [];
    if (playSetting.super) {
      urls.push("超清", playSetting.super);
    }
    if (playSetting.high) {
      urls.push("高清", playSetting.high);
    }
    if (playSetting.normal) {
      urls.push("流畅", playSetting.normal);
    }
    return JSON.stringify({ parse: 0, url: urls });
  }
  return JSON.stringify({ parse: 0, url: id });
}

// 搜索
async function search(wd, quick, pg) {
  const videos = [];
  const page = pg || 1;
  const searchLimit = aggConfig.search.limit || 20;
  const searchTimeout = aggConfig.search.timeout || 6000;

  const searchPromises = aggConfig.platformList.map(async (platform) => {
    try {
      const plat = aggConfig.platform[platform.id];
      let results = [];

      switch (platform.id) {
        case '百度': {
          const url = `${plat.host}${plat.search.replace('**', encodeURIComponent(wd)).replace('fypage', page)}`;
          const response = await req(url, { headers: aggConfig.headers.default, timeout: searchTimeout });
          const res = parseResponse(response);
          if (res && res.data) {
            results = res.data.map(item => ({
              vod_id: `百度@${item.id}`,
              vod_name: item.title,
              vod_pic: item.cover,
              vod_remarks: `百度短剧｜更新至${item.totalChapterNum}集`
            }));
          }
          break;
        }
        case '甜圈': {
          const url = `${plat.host}${plat.search}=${encodeURIComponent(wd)}&offset=${page}`;
          const response = await req(url, { headers: aggConfig.headers.default, timeout: searchTimeout });
          const res = parseResponse(response);
          if (res && res.data) {
            results = res.data.map(item => ({
              vod_id: `甜圈@${item.book_id}`,
              vod_name: item.title,
              vod_pic: item.cover,
              vod_remarks: `甜圈短剧｜${item.copyright || '未知'}`
            }));
          }
          break;
        }
        case '锦鲤': {
          const body = JSON.stringify({ page: page, limit: searchLimit, type_id: '', year: '', keyword: wd });
          const response = await req(plat.host + plat.search, { method: 'POST', body, timeout: searchTimeout });
          const res = parseResponse(response);
          if (res && res.data && res.data.list) {
            results = res.data.list.map(item => ({
              vod_id: `锦鲤@${item.vod_id}`,
              vod_name: item.vod_name || '未知短剧',
              vod_pic: item.vod_pic || '',
              vod_remarks: `锦鲤短剧｜${item.vod_total || 0}集`
            }));
          }
          break;
        }
        case '番茄': {
          const url = `${plat.search}?keyword=${encodeURIComponent(wd)}&page=${page}`;
          const response = await req(url, { headers: aggConfig.headers.default, timeout: searchTimeout });
          const res = parseResponse(response);
          if (res && res.data && Array.isArray(res.data)) {
            results = res.data.map(item => ({
              vod_id: `番茄@${item.series_id || ''}`,
              vod_name: item.title || '未知标题',
              vod_pic: item.cover || '',
              vod_remarks: `番茄短剧｜${item.sub_title || '未知'}`
            }));
          }
          break;
        }
        case '七猫': {
          let signStr = `operation=2playlet_privacy=1search_word=${wd}${aggConfig.keys}`;
          const sign = await md5(signStr);
          const url = `${plat.host}${plat.search}?search_word=${encodeURIComponent(wd)}&playlet_privacy=1&operation=2&sign=${sign}`;
          const headers = { ...await getHeaderX(), ...aggConfig.headers.default };
          const response = await req(url, { method: 'GET', headers, timeout: searchTimeout });
          const res = parseResponse(response);
          if (res && res.data && res.data.list) {
            results = res.data.list.map(item => ({
              vod_id: `七猫@${encodeURIComponent(item.playlet_id)}`,
              vod_name: item.title || '未知标题',
              vod_pic: item.image_link || '',
              vod_remarks: `七猫短剧｜${item.total_episode_num || 0}集`
            }));
          }
          break;
        }
        case '碎片': {
          let openId = (await md5(guid())).substring(0, 16);
          let api = "https://free-api.bighotwind.cc/papaya/papaya-api/oauth2/uuid";
          let body = JSON.stringify({ "openId": openId });
          let key = encHex(Date.now().toString());
          
          const tokenResponse = await req(api, {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              "key": key
            },
            body: body,
            timeout: searchTimeout
          });
          
          const tokenRes = parseResponse(tokenResponse);
          if (tokenRes && tokenRes.data && tokenRes.data.token) {
            const headers = { ...aggConfig.headers.default, 'Authorization': tokenRes.data.token };
            const requestUrl = `${plat.host}${plat.search}?type=5&tagId=&pageNum=${page}&pageSize=${searchLimit}&title=${encodeURIComponent(wd)}`;
            const response = await req(requestUrl, { headers, timeout: searchTimeout });
            const res = parseResponse(response);
            
            if (res && res.list) {
              results = res.list.map(it => {
                let compoundId = it.itemId + '@' + it.videoCode;
                return {
                  vod_id: `碎片@${compoundId}`,
                  vod_name: it.title,
                  vod_pic: "https://speed.hiknz.com/papaya/papaya-file/files/download/" + it.imageKey + "/" + it.imageName,
                  vod_remarks: `碎片剧场｜集数:${it.episodesMax} 播放:${it.hitShowNum}`
                };
              });
            }
          }
          break;
        }
      }
      
      return { platform: platform.name, results };
    } catch (error) {
      return { platform: platform.name, results: [] };
    }
  });

  try {
    const searchResults = await Promise.allSettled(searchPromises);
    
    searchResults.forEach(result => {
      if (result.status === 'fulfilled' && result.value.results && result.value.results.length > 0) {
        videos.push(...result.value.results);
      }
    });
  } catch (error) {
  }

  const filteredResults = videos.filter(item => {
    const title = item.vod_name || '';
    return title.toLowerCase().includes(wd.toLowerCase());
  });

  return JSON.stringify({
    list: filteredResults,
    page: page,
    pagecount: page + 1,
    limit: filteredResults.length,
    total: filteredResults.length * (page + 1)
  });
}


// 导出函数
export function __jsEvalReturn() {
  return {
    init: init,
    home: home,
    homeVod: homeVod,
    category: category,
    detail: detail,
    play: play,
    proxy: null,
    search: search
  };
}