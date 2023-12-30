import re

import chompjs
import requests
from tenacity import retry, stop_after_attempt

url = "https://lens.google.com/v3/upload?hl=vi&re=df&st=1703918855905&vpw=1687&vph=1169&ep=gsbubb"
headers = {
    'Cache-Control': 'max-age=0',
    'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-full-version': '"120.0.6099.129"',
    'sec-ch-ua-arch': '"arm"',
    'sec-ch-ua-platform': '"macOS"',
    'sec-ch-ua-platform-version': '"14.1.2"',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-bitness': '"64"',
    'sec-ch-ua-wow64': '?0',
    'Sec-Fetch-Site': 'same-site',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Referer': 'https://www.google.com/',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7',
}


@retry(stop=stop_after_attempt(5))
def solve_with_google_lens(image):
    payload = {}
    files = {
        'encoded_image': image
        # 'encoded_image': ('75643.png', open('./images/637691.png', 'rb'), 'image/png')
    }
    response = requests.request("POST", url, headers=headers, data=payload, files=files)
    pattern = re.compile(r'AF_initDataCallback\((.*?)\);')
    matches = pattern.findall(response.text)
    if not matches:
        raise Exception('Solve error')
    py_obj = chompjs.parse_js_object(matches[0])
    res = py_obj['data'][3][4][0][0][0]
    if res == 'n':
        raise Exception('Solve error')
    return res
