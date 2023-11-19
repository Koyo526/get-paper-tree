import requests
import json
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

class Search():
    def __init__(self,words):
        self.endpoint = 'https://api.semanticscholar.org/graph/v1/paper/search'
        self.keyword = words
        self.fields = ('title', 'year', 'referenceCount', 'citationCount','influentialCitationCount',
                       'isOpenAccess', 'fieldsOfStudy', 'authors','abstract')
        self.params = {
            'query': self.keyword,
            'fields': ','.join(self.fields),
            'limit': 10
            }

    def search_papers(self):
        try:
            #easy to do
            #res = requests.get(url=self.endpoint, params=self.params)
            #real
            session = requests.Session()
            retries = Retry(total=5,backoff_factor=1,status_forcelist=[500, 502, 503, 504]) 
            session.mount("https://", HTTPAdapter(max_retries=retries))
            res = session.get(url=self.endpoint, params=self.params,stream=True,timeout=(10.0, 30.0))
            print(res.status_code)
            print(res.encoding)
            print(res.raise_for_status())
            res_dict = json.loads(res.text)
            dir = "results.json"
            data = res_dict	# 任意のdict型変数
            with open(dir, mode="wt", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return res_dict
        except ConnectionError as ce:
            print("Connection Error:", ce)
        except HTTPError as he:
            print("HTTP Error:", he)
        except Timeout as te:
            print("Timeout Error:", te)
        except RequestException as re:
            print("Error:", re)

    def print_papers(self,r_dict):
        total = r_dict['total']
        print(f'Total search result: {total}')
        data = r_dict['data']
        for d in data:
            print('---------------')
            for fi in self.fields:
                if fi == 'authors':
                    print(f'{fi}: {list(map(lambda a: a["name"], d[fi]))}')
                else:
                    print(f'{fi}: {d[fi]}')
            print(f'paperID:{d["paperId"]}')

if __name__ == "__main__": 
    keyword = "Python&AI"
    S = Search(keyword) 
    dic = S.search_papers()
    S.print_papers(dic)