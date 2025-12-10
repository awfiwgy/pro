var rule = {
    title:'91麻豆',
    host:'http://www.md91.cc/',
    searchUrl:'',
    url:'/index.php/vod/type/id/fyclass/page/fypage.html',
    headers:{
        'User-Agent':'MOBILE_UA'
    },
    searchable: 1,//是否启用全局搜索,
    quickSearch: 1,//是否启用快速搜索,
    filterable: 1,//是否启用分类筛选,
      推荐: 'body&&.video-item;.title&&Text;.lazy&&src;.time&&Text;a&&href',
       class_parse:'.navs-body&&.nav-item;a&&Text;a&&href;/(\\d+).html',
    limit:6,
    play_parse:true,
    lazy:'',
    一级:'.video-list&&.video-item;.title&&Text;.lazy&&src;.time&&Text;a&&href',
  二级:"*",
搜索: '*',
       
}