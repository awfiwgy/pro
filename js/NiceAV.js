var rule = {
    //发布页：https://fuliwz.neocities.org/niceav
    title: 'NiceAV',
    host: 'https://www.nice9110.cyou/',
    url: 'https://www.nice9110.cyou/index.php/vod/type/id/fyclass/page/fypage.html',
    searchUrl: 'https://www.nice9110.cyou/index.php/vod/search/page/fypage/wd/**.html',
    class_name: '日本无码&激情动漫&中文字幕&日本有码&AV解说&cosplay&黑丝诱惑&SWAG&自拍偷拍&网红主播&探花系列&三级伦理&VR视角&国产传媒&素人搭讪&门事件',
    class_url: '3&9&1&2&4&5&6&7&8&10&11&12&13&14&15&16',
    searchable: 2,
    quickSearch: 0,
    filterable: 0,
    headers: {
        'User-Agent': 'MOBILE_UA',
    },
    play_parse: true,
    lazy: $js.toString(() => {
        let url=JSON.parse(jsp.pdfh(request(input),'.img-box&&script&&Html').replace('var player_aaaa=', '')).url
        input=url

    }),
    limit: 6,
    推荐: '*',
    double: true,
    一级: '.img-box;img&&alt;img&&data-src;.label&&Text;a&&href',
    二级: '*',
    搜索: '*',
}