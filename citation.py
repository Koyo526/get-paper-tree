import requests
import json
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout
from urllib3.util import Retry
from requests.adapters import HTTPAdapter

class Citation():
    def __init__(self,id):
        self.paperId = id
        self.endpoint = f'https://api.semanticscholar.org/graph/v1/paper/{self.paperId}/citations'
        self.fields = ('title', 'year', 'referenceCount', 'citationCount','influentialCitationCount',
                       'isOpenAccess', 'fieldsOfStudy', 'authors','abstract')
        self.params = {
            'fields': ','.join(self.fields),
            'limit': 10
            }
        
    def search_citing_papers(self):
        try:
            session = requests.Session()
            retries = Retry(total=5,backoff_factor=1,status_forcelist=[500, 502, 503, 504]) 
            session.mount("https://", HTTPAdapter(max_retries=retries))
            res = session.get(url=self.endpoint, params=self.params,stream=True,timeout=(10.0, 30.0))
            print(res.status_code)
            print(res.encoding)
            print(res.raise_for_status())
            res_dict = json.loads(res.text)
            dir = "citations.json"
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

    def print_citing_papers(self,r_dict):
        data = r_dict['data']
        for d in data:
            print('---------------')
            d = d['citingPaper']
            for fi in self.fields:
                if fi == 'authors':
                    print(f'{fi}: {list(map(lambda a: a["name"], d[fi]))}')
                else:
                    print(f'{fi}: {d[fi]}')
            print(f'paperID:{d["paperId"]}')

if __name__ == "__main__": 
    keyword = "a97ab7839888fe563f8f1fc7add057cbc8249510"
    S = Citation(keyword) 
    dic = S.search_citing_papers()
    S.print_citing_papers(dic)