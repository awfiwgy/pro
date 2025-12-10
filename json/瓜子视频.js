

var rule = {
    title: '瓜子',
    host: 'https://api.8utdtcq.com',
    url: '/App/IndexList/indexList',
    searchUrl: '/App/Index/findMoreVod#**',
    searchable: 2,
    quickSearch: 1,
    filterable: 1,
    class_name: '动漫&电影&电视剧&综艺&短剧',
    class_url: '4&1&2&3&64',
    filter:'H4sIAAAAAAAAA+2a7U4aQRSG/3sVht/bZHf5WnorjWlo4YfphwlqE2NMtGoLWIsmFbRi2qYqoBgxtVVR8GZ2duUuOmchfuDuDHI2xJhD4hGYyTzv7hlm57yZ6aFh/gpogefDL5y38Jq+fuc0vklO8eZAPJWMB5S7Te/j75JebR/ibyeTd8Z1H/9mMBiJLZZb8+WusW7GhC5q4F7jzP3+Qsh2qbXxSQjpdMGSWrsb1umhkNTpgr6mXM06a4qvqd0FS7KqJbv5VUgyLxfsRsHKHyos+9NauuR3U2HNE7bZUKyFHP/E0hXF+rPmfOEMp/A/+HS1dOT827m0cwd2ZgOvtrBjFatCtZ0u6Fz/qHDp4ly3u2BJ5mmRLRfM+ndxupdrrL6rWPkaTwLb+sVveA3ubatStbZ2+B2GAdDTbvGfeZ4X62h3uU+6883I9adbCtxXoqlkPOW1Erm1PeKVSFf1kBDhdPCBEpRRgn5QdBlF94OiySiaHxRVRvEj+1pMQuEdfKAYMorhByUqo0T9oERklAiaoqnPtDA7O5aRwgoPIQhBCDoEDQJ+aqgq55vnvyUSVJXjVGCqQFdBhwqKVNCmRiBEIRgQ8HMp1ossLRZTFR40CDqEIIQQhDCECIQoBAMCXpbRmywDZBkgywBZBsgyQJYBsgyQZYAsA2QZeFnW5rFVqIhT6ONzcXzylddj0aXpET8VWbZsNop25rOIE0Zn52PVzq9KKHoMfTH5IsuUJJgIlmKnj6z5RQkliqaUVtnZuYRioBMzt2LN5iUUfF4yJfkd01T0xaTXzXpGhtF8+MnY32SZCeKnWX2PNdZkvxn0TbPnmq3vTdnVoCeanT20G3uyn6ZLbvpeocdSE55LtEtbf2u0fX7BVtLCNTrxcjSBf7wVZ3lxKeHEE4mJUX6FPsDs+QMJbPz1WAqPau2vs7TYHvJGeU0N591Ie0z+1H80fluxxr7UyW8jv438Nk8S+W2D8NugghOnk/y2Lgr5bQ+kkN9GfpurBPLbHiKL/LaB+W2bDbNeYpmS0D7Q/dk3yzBBfzbNMkzInx2zDIM3EJ19rAyD9lzam1gZBu3tWX9P2HZehsGbe86mWIZBu3vXu3ChteOC6XsxIGsHAXs61k6IrJ0uCFk7niSydtxJZO146CBrxxNC1g5ZO0IKWTvdFLJ2bkkga4esnYFaO+bpAVTC2bJ1sS8854A/g9I2KuQk9DGU4Y71Ike5eEl9J4tKbwTs6ZTeQSq9uyBUenuSqPR2J1Hp7aGDSm9PCJXeVHoLKVR6d1Oo9L4lgUpvKr0He6rC2Rfziu4qI9yl6+iDFXCqIlfrgYQ+W8H3f3xj1gPJp+MVPZBcTlj0PSuoxkfAnkCNPzTzH+StPxCsRAAA',
    play_parse: true,
    lazy: $js.toString(() => {
        let d = [];
        var vod_id = input.split("/")[0];
        var vurl_id = input.split("/")[1];
        var resolution=input.split("?")[1]
        function Encrypt(plainText) {
            let key = CryptoJS.enc.Utf8.parse("mvXBSW7ekreItNsT");
            let iv = CryptoJS.enc.Utf8.parse("2U3IrJL8szAKp0Fj");
            let encrypted = CryptoJS.AES.encrypt(plainText, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            let encryptedHex = encrypted.ciphertext.toString(CryptoJS.enc.Hex);
            return encryptedHex.toUpperCase();
        }
        function Decrypt(word, key, iv) {
            let encryptedHexStr = CryptoJS.enc.Hex.parse(word);
            let decrypt = CryptoJS.AES.decrypt({
                ciphertext: encryptedHexStr
            }, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
            return decryptedStr;
        }
        var timestamp = new Date().getTime() / 1000;
        var t = timestamp.toString().split('.')[0];
        var request_key = JSON.stringify({
            "domain_type": "8",
            "vod_id": vod_id,
            "type": "play",
            "resolution": resolution,
            "vurl_id": vurl_id
        });
        var request_key2 = Encrypt(request_key);
        var signature = 'token_id=,token=1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79,phone_type=1,request_key=' + request_key2 + ',app_id=1,time=' + t + ',keys=ZH8gpdp9bxjuG2NK97sol3o7Uiz+9eVEaVMlE2Fk3j7EResM3YHnECZUH7BONNTjpy7RVNi/YimGuNYriC7Cmswv4PNYiFYzw9QhlqZKwNfCM6IUpFZ0T4rZx8G78zkv2tNVbfYC4qNQedGi07nWZ33dlSuVxROVfY5JxOWHMI0=*&zvdvdvddbfikkkumtmdwqppp?|4Y!s!2br';
        var signature2 = md5(signature);
        var body = 'token=1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79&token_id=&phone_type=1&time=' + t + '&phone_model=xiaomi-22021211rc&keys=ZH8gpdp9bxjuG2NK97sol3o7Uiz%2B9eVEaVMlE2Fk3j7EResM3YHnECZUH7BONNTjpy7RVNi%2FYimGuNYriC7Cmswv4PNYiFYzw9QhlqZKwNfCM6IUpFZ0T4rZx8G78zkv2tNVbfYC4qNQedGi07nWZ33dlSuVxROVfY5JxOWHMI0%3D&request_key=' + request_key2 + '&signature=' + signature2 + '&app_id=1&ad_version=1';

        var html = fetch('https://api.8utdtcq.com/App/Resource/VurlDetail/showOne', {
            headers: {
                'Cache-Control': 'no-cache',
                'Version': '2406025',
                'PackageName': 'com.uf076bf0c246.qe439f0d5e.m8aaf56b725a.ifeb647346f',
                'Ver': '1.9.2',
                'Referer': 'https://api.8utdtcq.com',
                'X-Customer-Client-Ip': '127.0.0.1',
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'api.8utdtcq.com',
                'Connection': 'Keep-Alive',
                'User-Agent': 'okhttp/3.12.0'
            },
            body: body,
            method: 'POST',           
            rejectCoding: true
        });

        var data = JSON.parse(html).data;
        var response_key = data.response_key;
        var keys = data.keys;
        var bodykey = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGAe6hKrWLi1zQmjTT1ozbE4QdFeJGNxubxld6GrFGximxfMsMB6BpJhpcTouAqywAFppiKetUBBbXwYsYU1wNr648XVmPmCMCy4rY8vdliFnbMUj086DU6Z+/oXBdWU3/b1G0DN3E9wULRSwcKZT3wj/cCI1vsCm3gj2R5SqkA9Y0CAwEAAQKBgAJH+4CxV0/zBVcLiBCHvSANm0l7HetybTh/j2p0Y1sTXro4ALwAaCTUeqdBjWiLSo9lNwDHFyq8zX90+gNxa7c5EqcWV9FmlVXr8VhfBzcZo1nXeNdXFT7tQ2yah/odtdcx+vRMSGJd1t/5k5bDd9wAvYdIDblMAg+wiKKZ5KcdAkEA1cCakEN4NexkF5tHPRrR6XOY/XHfkqXxEhMqmNbB9U34saTJnLWIHC8IXys6Qmzz30TtzCjuOqKRRy+FMM4TdwJBAJQZFPjsGC+RqcG5UvVMiMPhnwe/bXEehShK86yJK/g/UiKrO87h3aEu5gcJqBygTq3BBBoH2md3pr/W+hUMWBsCQQChfhTIrdDinKi6lRxrdBnn0Ohjg2cwuqK5zzU9p/N+S9x7Ck8wUI53DKm8jUJE8WAG7WLj/oCOWEh+ic6NIwTdAkEAj0X8nhx6AXsgCYRql1klbqtVmL8+95KZK7PnLWG/IfjQUy3pPGoSaZ7fdquG8bq8oyf5+dzjE/oTXcByS+6XRQJAP/5ciy1bL3NhUhsaOVy55MHXnPjdcTX0FaLi+ybXZIfIQ2P4rb19mVq1feMbCXhz+L1rG8oat5lYKfpe8k83ZA==";
        var bodykeyiv = JSON.parse(RSA.decode(keys, bodykey));
        var key = CryptoJS.enc.Utf8.parse(bodykeyiv.key);
        var iv = CryptoJS.enc.Utf8.parse(bodykeyiv.iv);
        var html2 = Decrypt(response_key, key, iv);
        var url = JSON.parse(html2).url;
        input = {
            url: url,
            parse: 0,
            header: rule.headers
        }
        setResult(d)
    }),
    一级: $js.toString(() => {
        let d = [];
        function Encrypt(plainText) {
            let key = CryptoJS.enc.Utf8.parse("mvXBSW7ekreItNsT");
            let iv = CryptoJS.enc.Utf8.parse("2U3IrJL8szAKp0Fj");
            let encrypted = CryptoJS.AES.encrypt(plainText, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            let encryptedHex = encrypted.ciphertext.toString(CryptoJS.enc.Hex);
            return encryptedHex.toUpperCase();
        }
        function Decrypt(word, key, iv) {
            let encryptedHexStr = CryptoJS.enc.Hex.parse(word);
            let decrypt = CryptoJS.AES.decrypt({
                ciphertext: encryptedHexStr
            }, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
            return decryptedStr;
        }
        function getbody3(key, t) {
            var signature = 'token_id=,token=1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79,phone_type=1,request_key=' + key + ',app_id=1,time=' + t + ',keys=qDpotE2bedimK3QGqlyV5ieXXC3EhaPLQ+IOJyHnHflCj5w/7ESK7FgywMvrgjxbx0GklEFLI4+JshgySe633OIRstuktwdiCy3CT+fLSpuxBJDIlfXQDaeH3ig1wiB0JsZ601XHiFweGMu4tZfnSpHg3OnoL6nz/uurUif2OK4=*&zvdvdvddbfikkkumtmdwqppp?|4Y!s!2br';
            var signature2 = md5(signature).toUpperCase();
            var body = 'token=1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79&token_id=&phone_type=1&time=' + t + '&phone_model=xiaomi-22021211rc&keys=qDpotE2bedimK3QGqlyV5ieXXC3EhaPLQ%2BIOJyHnHflCj5w%2F7ESK7FgywMvrgjxbx0GklEFLI4%2BJshgySe633OIRstuktwdiCy3CT%2BfLSpuxBJDIlfXQDaeH3ig1wiB0JsZ601XHiFweGMu4tZfnSpHg3OnoL6nz%2FuurUif2OK4%3D&request_key=' + key + '&signature=' + signature2 + '&app_id=1&ad_version=1';
            return body
        }
        const bodykey = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGAe6hKrWLi1zQmjTT1ozbE4QdFeJGNxubxld6GrFGximxfMsMB6BpJhpcTouAqywAFppiKetUBBbXwYsYU1wNr648XVmPmCMCy4rY8vdliFnbMUj086DU6Z+/oXBdWU3/b1G0DN3E9wULRSwcKZT3wj/cCI1vsCm3gj2R5SqkA9Y0CAwEAAQKBgAJH+4CxV0/zBVcLiBCHvSANm0l7HetybTh/j2p0Y1sTXro4ALwAaCTUeqdBjWiLSo9lNwDHFyq8zX90+gNxa7c5EqcWV9FmlVXr8VhfBzcZo1nXeNdXFT7tQ2yah/odtdcx+vRMSGJd1t/5k5bDd9wAvYdIDblMAg+wiKKZ5KcdAkEA1cCakEN4NexkF5tHPRrR6XOY/XHfkqXxEhMqmNbB9U34saTJnLWIHC8IXys6Qmzz30TtzCjuOqKRRy+FMM4TdwJBAJQZFPjsGC+RqcG5UvVMiMPhnwe/bXEehShK86yJK/g/UiKrO87h3aEu5gcJqBygTq3BBBoH2md3pr/W+hUMWBsCQQChfhTIrdDinKi6lRxrdBnn0Ohjg2cwuqK5zzU9p/N+S9x7Ck8wUI53DKm8jUJE8WAG7WLj/oCOWEh+ic6NIwTdAkEAj0X8nhx6AXsgCYRql1klbqtVmL8+95KZK7PnLWG/IfjQUy3pPGoSaZ7fdquG8bq8oyf5+dzjE/oTXcByS+6XRQJAP/5ciy1bL3NhUhsaOVy55MHXnPjdcTX0FaLi+ybXZIfIQ2P4rb19mVq1feMbCXhz+L1rG8oat5lYKfpe8k83ZA==";
        function gethtml(u, body, headers) {
            var hd = fetch(u, {
                headers: headers,
                body: body,
                method: 'POST',
                rejectCoding: true
            });
            var banner = JSON.parse(hd).data;
            var response_key = banner.response_key;
            var keys = banner.keys;
            var bodykeyiv = JSON.parse(RSA.decode(keys, bodykey));
            var key = CryptoJS.enc.Utf8.parse(bodykeyiv.key);
            var iv = CryptoJS.enc.Utf8.parse(bodykeyiv.iv);
            var html = Decrypt(response_key, key, iv);
            return html
        }
        function hqsub(MY_CATE) {
            var subs = ["5", "12", "30", "22", ""]
            var tids = ["1", "2", "4", "3", "64"]
            let index = tids.indexOf(MY_CATE);
            if (index !== -1) {
                return subs[index];
            }
            return "";
        }
        var headers = {
            'Cache-Control': 'no-cache',
            'Version': '2406025',
            'PackageName': 'com.uf076bf0c246.qe439f0d5e.m8aaf56b725a.ifeb647346f',
            'Ver': '1.9.2',
            'Referer': 'https://api.8utdtcq.com',
            'X-Customer-Client-Ip': '127.0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'api.8utdtcq.com',
            'Connection': 'Keep-Alive',            'User-Agent': 'okhttp/3.12.0'
        }
        var tid = MY_CATE;
        var sub = hqsub(MY_CATE)
        var timestamp = new Date().getTime() / 1000;
        var t = timestamp.toString().split('.')[0];
        var request_key = JSON.stringify({ "area": (MY_FL.area || 0).toString(), "sub": (MY_FL.sub || sub).toString(), "year": (MY_FL.year || 0).toString(), "pageSize": "30", "sort": (MY_FL.sort || "d_id").toString(), "page": MY_PAGE, "tid": tid });
        var request_key2 = Encrypt(request_key);
        var body = getbody3(request_key2, t)
        var html2 = gethtml("https://api.8utdtcq.com/App/IndexList/indexList", body, headers)
        var list = JSON.parse(html2).list;
        list.forEach(data => {
            d.push({
                title: data.vod_name,
                desc: data.vod_continu == 0 ? '电影' : '更新至'+data.vod_continu+'集',
                year: data.vod_scroe,
                img: data.vod_pic,
                url: `${data.vod_id}/${data.vod_continu}`,
            })
        })
        setResult(d)
    }),
    二级: $js.toString(() => {
        function Encrypt(plainText) {
            let key = CryptoJS.enc.Utf8.parse("mvXBSW7ekreItNsT");
            let iv = CryptoJS.enc.Utf8.parse("2U3IrJL8szAKp0Fj");
            let encrypted = CryptoJS.AES.encrypt(plainText, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            let encryptedHex = encrypted.ciphertext.toString(CryptoJS.enc.Hex);
            return encryptedHex.toUpperCase();
        }
        function Decrypt(word, key, iv) {
            let encryptedHexStr = CryptoJS.enc.Hex.parse(word);
            let decrypt = CryptoJS.AES.decrypt({
                ciphertext: encryptedHexStr
            }, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
            return decryptedStr;
        }
        function getbody2(key, t) {
            var signature = 'token_id=,token=1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79,phone_type=1,request_key=' + key + ',app_id=1,time=' + t + ',keys=Qmxi5ciWXbQzkr7o+SUNiUuQxQEf8/AVyUWY4T/BGhcXBIUz4nOyHBGf9A4KbM0iKF3yp9M7WAY0rrs5PzdTAOB45plcS2zZ0wUibcXuGJ29VVGRWKGwE9zu2vLwhfgjTaaDpXo4rby+7GxXTktzJmxvneOUdYeHi+PZsThlvPI=*&zvdvdvddbfikkkumtmdwqppp?|4Y!s!2br';
            var signature2 = md5(signature);
            var body = 'token=1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79&token_id=&phone_type=1&time=' + t + '&phone_model=xiaomi-22021211rc&keys=Qmxi5ciWXbQzkr7o%2BSUNiUuQxQEf8%2FAVyUWY4T%2FBGhcXBIUz4nOyHBGf9A4KbM0iKF3yp9M7WAY0rrs5PzdTAOB45plcS2zZ0wUibcXuGJ29VVGRWKGwE9zu2vLwhfgjTaaDpXo4rby%2B7GxXTktzJmxvneOUdYeHi%2BPZsThlvPI%3D&request_key=' + key + '&signature=' + signature2 + '&app_id=1&ad_version=1';
            return body
        }
        const bodykey = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGAe6hKrWLi1zQmjTT1ozbE4QdFeJGNxubxld6GrFGximxfMsMB6BpJhpcTouAqywAFppiKetUBBbXwYsYU1wNr648XVmPmCMCy4rY8vdliFnbMUj086DU6Z+/oXBdWU3/b1G0DN3E9wULRSwcKZT3wj/cCI1vsCm3gj2R5SqkA9Y0CAwEAAQKBgAJH+4CxV0/zBVcLiBCHvSANm0l7HetybTh/j2p0Y1sTXro4ALwAaCTUeqdBjWiLSo9lNwDHFyq8zX90+gNxa7c5EqcWV9FmlVXr8VhfBzcZo1nXeNdXFT7tQ2yah/odtdcx+vRMSGJd1t/5k5bDd9wAvYdIDblMAg+wiKKZ5KcdAkEA1cCakEN4NexkF5tHPRrR6XOY/XHfkqXxEhMqmNbB9U34saTJnLWIHC8IXys6Qmzz30TtzCjuOqKRRy+FMM4TdwJBAJQZFPjsGC+RqcG5UvVMiMPhnwe/bXEehShK86yJK/g/UiKrO87h3aEu5gcJqBygTq3BBBoH2md3pr/W+hUMWBsCQQChfhTIrdDinKi6lRxrdBnn0Ohjg2cwuqK5zzU9p/N+S9x7Ck8wUI53DKm8jUJE8WAG7WLj/oCOWEh+ic6NIwTdAkEAj0X8nhx6AXsgCYRql1klbqtVmL8+95KZK7PnLWG/IfjQUy3pPGoSaZ7fdquG8bq8oyf5+dzjE/oTXcByS+6XRQJAP/5ciy1bL3NhUhsaOVy55MHXnPjdcTX0FaLi+ybXZIfIQ2P4rb19mVq1feMbCXhz+L1rG8oat5lYKfpe8k83ZA==";
        function gethtml(u, body, headers) {
            var hd = fetch(u, {
                headers: headers,
                body: body,
                method: 'POST',
                rejectCoding: true
            });
            var banner = JSON.parse(hd).data;
            var response_key = banner.response_key;
            var keys = banner.keys;
            var bodykeyiv = JSON.parse(RSA.decode(keys, bodykey));
            var key = CryptoJS.enc.Utf8.parse(bodykeyiv.key);
            var iv = CryptoJS.enc.Utf8.parse(bodykeyiv.iv);
            var html = Decrypt(response_key, key, iv);
            return html
        }
        const headers = {
            'Cache-Control': 'no-cache',
            'Version': '2406025',
            'PackageName': 'com.uf076bf0c246.qe439f0d5e.m8aaf56b725a.ifeb647346f',
            'Ver': '1.9.2',
            'Referer': 'https://api.8utdtcq.com',
            'X-Customer-Client-Ip': '127.0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'api.8utdtcq.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.12.0'
        }
        input = input.replace('https://api.8utdtcq.com/', '');
        var vod_id = input.split("/")[0];
        var timestamp = new Date().getTime() / 1000;
        var t = timestamp.toString().split('.')[0];
        var request_key = JSON.stringify({
            "token_id": "393668",
            "vod_id": vod_id,
            "mobile_time": t,
            "token": "1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79"
        });
        var request_key2 = Encrypt(request_key);
        var body = getbody2(request_key2, t)
        var html = gethtml("https://api.8utdtcq.com/App/IndexPlay/playInfo", body, headers)
        var data2 = JSON.parse(html).vodInfo;
        var request_key3 = JSON.stringify({
            "vurl_cloud_id": "2",
            "vod_d_id": vod_id
        });
        var request_key4 = Encrypt(request_key3);
        var body2 = getbody2(request_key4, t)
        var html3 = gethtml("https://api.8utdtcq.com/App/Resource/Vurl/show", body2, headers);
        var list = JSON.parse(html3).list;
        let nnnmm = [];
        list.forEach(item => {
            const playParams = Object.values(item.play);
            let lastParam = null;
            for (let i = playParams.length - 1; i >= 0; i--) {
                if (playParams[i].param) {
                    lastParam = playParams[i].param;
                    break;
                }
            }
            const vurlIdMatch = lastParam.match(/vurl_id=(\d+)/);
            const resolution=lastParam.match(/resolution=(\d+)/);
            if (vurlIdMatch) {
                nnnmm.push(`${item.title}$${vod_id}/${vurlIdMatch[1]}?${resolution[1]}`);
            }
        });
        VOD = {
            title: data2.vod_name,
            type: data2.videoTag.toString(),
            desc: data2.vod_use_content,
            vod_actor: data2.vod_actor,
            vod_area: data2.vod_area,
            vod_director: data2.vod_director,
            img: data2.vod_pic,
            vod_play_from: '摸鱼磕瓜子',
            vod_play_url: nnnmm.join('#')
        }
    }),
    搜索: $js.toString(() => {
        let d = [];
        function Encrypt(plainText) {
            let key = CryptoJS.enc.Utf8.parse("mvXBSW7ekreItNsT");
            let iv = CryptoJS.enc.Utf8.parse("2U3IrJL8szAKp0Fj");
            let encrypted = CryptoJS.AES.encrypt(plainText, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            let encryptedHex = encrypted.ciphertext.toString(CryptoJS.enc.Hex);
            return encryptedHex.toUpperCase();
        }
        function Decrypt(word, key, iv) {
            let encryptedHexStr = CryptoJS.enc.Hex.parse(word);
            let decrypt = CryptoJS.AES.decrypt({
                ciphertext: encryptedHexStr
            }, key, {
                iv: iv,
                mode: CryptoJS.mode.CBC,
                padding: CryptoJS.pad.Pkcs7
            });
            let decryptedStr = decrypt.toString(CryptoJS.enc.Utf8);
            return decryptedStr;
        }
        function getbody3(key, t) {
            var signature = 'token_id=,token=1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79,phone_type=1,request_key=' + key + ',app_id=1,time=' + t + ',keys=qDpotE2bedimK3QGqlyV5ieXXC3EhaPLQ+IOJyHnHflCj5w/7ESK7FgywMvrgjxbx0GklEFLI4+JshgySe633OIRstuktwdiCy3CT+fLSpuxBJDIlfXQDaeH3ig1wiB0JsZ601XHiFweGMu4tZfnSpHg3OnoL6nz/uurUif2OK4=*&zvdvdvddbfikkkumtmdwqppp?|4Y!s!2br';
            var signature2 = md5(signature);
            var body = 'token=1be86e8e18a9fa18b2b8d5432699dad0.ac008ed650fd087bfbecf2fda9d82e9835253ef24843e6b18fcd128b10763497bcf9d53e959f5377cde038c20ccf9d17f604c9b8bb6e61041def86729b2fc7408bd241e23c213ac57f0226ee656e2bb0a583ae0e4f3bf6c6ab6c490c9a6f0d8cdfd366aacf5d83193671a8f77cd1af1ff2e9145de92ec43ec87cf4bdc563f6e919fe32861b0e93b118ec37d8035fbb3c.59dd05c5d9a8ae726528783128218f15fe6f2c0c8145eddab112b374fcfe3d79&token_id=&phone_type=1&time=' + t + '&phone_model=xiaomi-22021211rc&keys=qDpotE2bedimK3QGqlyV5ieXXC3EhaPLQ%2BIOJyHnHflCj5w%2F7ESK7FgywMvrgjxbx0GklEFLI4%2BJshgySe633OIRstuktwdiCy3CT%2BfLSpuxBJDIlfXQDaeH3ig1wiB0JsZ601XHiFweGMu4tZfnSpHg3OnoL6nz%2FuurUif2OK4%3D&request_key=' + key + '&signature=' + signature2 + '&app_id=1&ad_version=1';
            return body
        }
        const bodykey = "MIICdgIBADANBgkqhkiG9w0BAQEFAASCAmAwggJcAgEAAoGAe6hKrWLi1zQmjTT1ozbE4QdFeJGNxubxld6GrFGximxfMsMB6BpJhpcTouAqywAFppiKetUBBbXwYsYU1wNr648XVmPmCMCy4rY8vdliFnbMUj086DU6Z+/oXBdWU3/b1G0DN3E9wULRSwcKZT3wj/cCI1vsCm3gj2R5SqkA9Y0CAwEAAQKBgAJH+4CxV0/zBVcLiBCHvSANm0l7HetybTh/j2p0Y1sTXro4ALwAaCTUeqdBjWiLSo9lNwDHFyq8zX90+gNxa7c5EqcWV9FmlVXr8VhfBzcZo1nXeNdXFT7tQ2yah/odtdcx+vRMSGJd1t/5k5bDd9wAvYdIDblMAg+wiKKZ5KcdAkEA1cCakEN4NexkF5tHPRrR6XOY/XHfkqXxEhMqmNbB9U34saTJnLWIHC8IXys6Qmzz30TtzCjuOqKRRy+FMM4TdwJBAJQZFPjsGC+RqcG5UvVMiMPhnwe/bXEehShK86yJK/g/UiKrO87h3aEu5gcJqBygTq3BBBoH2md3pr/W+hUMWBsCQQChfhTIrdDinKi6lRxrdBnn0Ohjg2cwuqK5zzU9p/N+S9x7Ck8wUI53DKm8jUJE8WAG7WLj/oCOWEh+ic6NIwTdAkEAj0X8nhx6AXsgCYRql1klbqtVmL8+95KZK7PnLWG/IfjQUy3pPGoSaZ7fdquG8bq8oyf5+dzjE/oTXcByS+6XRQJAP/5ciy1bL3NhUhsaOVy55MHXnPjdcTX0FaLi+ybXZIfIQ2P4rb19mVq1feMbCXhz+L1rG8oat5lYKfpe8k83ZA==";
        function gethtml(u, body, headers) {
            var hd = fetch(u, {
                headers: headers,
                body: body,
                method: 'POST',
                rejectCoding: true
            });
            var banner = JSON.parse(hd).data;
            var response_key = banner.response_key;
            var keys = banner.keys;
            var bodykeyiv = JSON.parse(RSA.decode(keys, bodykey));
            var key = CryptoJS.enc.Utf8.parse(bodykeyiv.key);
            var iv = CryptoJS.enc.Utf8.parse(bodykeyiv.iv);
            var html = Decrypt(response_key, key, iv);
            return html
        }
        var timestamp = new Date().getTime() / 1000;
        var t = timestamp.toString().split('.')[0];
        var url = input.split("#")[0];
        var request_key11 = input.split("#")[1]

        var request_key = JSON.stringify({ "keywords": request_key11, "order_val": "1" })
        var request_key2 = Encrypt(request_key);
        var body = getbody3(request_key2, t)
        var headers = {
            'Cache-Control': 'no-cache',
            'Version': '2406025',
            'PackageName': 'com.uf076bf0c246.qe439f0d5e.m8aaf56b725a.ifeb647346f',
            'Ver': '1.9.2',
            'Referer': 'https://api.8utdtcq.com',
            'X-Customer-Client-Ip': '127.0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Host': 'api.8utdtcq.com',
            'Connection': 'Keep-Alive',
            'User-Agent': 'okhttp/3.12.0'
        }
        var html = gethtml(url, body, headers)
        var list = JSON.parse(html).list;
        list.forEach(data => {
            d.push({
                title: data.vod_name,
                desc: data.vod_continu == 0 ? '电影' : '更新至'+data.vod_continu+'集',
                content: data.vod_addtime,
                img: data.vod_pic,
                url: `${data.vod_id}/${data.vod_continu}`,
            })
        })
        setResult(d)
    }),
}