# 发起POST请求

```javascript
function handler() {
  const content = fetch(url, {
    method: 'POST',
    headers: {
      'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.63 Safari/537.36',
      'Accept-Language': 'en',
    },
    body: 'birth_day=23&birth_month=11&birth_year=2000&collect_personal_info=undefined&creation_flow=&creation_point=https%253A%252F%252Fwww.spotify.com%252Fhk-en%252F&displayname=Gay%2520Lord&gender=male&iagree=1&key=a1e486e2729f46d6bb368d6b2bcda326&platform=www&referrer=&send-email=0&thirdpartyemail=0&identifier_token=AgE6YTvEzkReHNfJpO114514',
    noRedir: false,
    retry: 3,
    timeout: 5000,
  });
  return "失败"
}
```
