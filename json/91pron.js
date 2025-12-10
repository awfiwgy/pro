var rule = {
    类型: '影视',//影视|听书|漫画|小说
    title: '91pron[密]',
    host: 'https://0601.9p47p.com',
    ///v.php?category=ori&viewtype=basic&page=2
    url: '/v.php?category=fyclass&viewtype=basic&page=fypage&cn_CN=cn_CN',
    class_name: '91原创&当前最热&本月最热&非付费&10分钟以上&20分钟以上&本月收藏&最近加精&高清&每月最热&本月讨论&收藏最多',
    class_url: 'ori&hot&top&nonpaid&long&longer&tf&rf&hd&top&md&mf',
    searchUrl: '/dm/search/q-**',
    searchable: 0,
    quickSearch: 0,
    filterable: 0,
    filter: {},
    filter_url: '',
    filter_def: {},
    headers: {
        'User-Agent': 'PC_UA',
    },
    timeout: 5000,
    cate_exclude: '',
    // class_parse: '.head_menu_a li:gt(0):lt(6);a&&Text;a&&href;.*/(.*?).html',
    play_parse: true,                
    lazy: '',                                              
    limit: 6,
    // 推荐: '.cbox_list;ul&&li;a&&title;a&&data-original;.vodlist_top&&Text;a&&href',
    double: true,
    一级: '.col-xs-12;.video-title&&Text;.img-responsive&&src;.duration&&Text;.col-xs-12 a&&href',
    二级:'*',
    搜索: '*',
    sniffer:1,
    //是否启用辅助嗅探: 1,0
    sniffer:1,
    // 辅助嗅探规则
    isVideo:"http((?!http).){26,}\\.(m3u8|mp4|flv|avi|mkv|wmv|mpg|mpeg|mov|ts|3gp|rm|rmvb|asf|m4a|mp3|wma)",
}