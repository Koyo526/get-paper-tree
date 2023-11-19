import requests
import json
from requests.exceptions import RequestException, ConnectionError, HTTPError, Timeout

class Reference():
    def __init__(self,id):
        self.paperId = id
        self.endpoint = f'https://api.semanticscholar.org/graph/v1/paper/{self.paperId}/references'
        self.fields = ('title', 'year', 'referenceCount', 'citationCount','influentialCitationCount',
                       'isOpenAccess', 'fieldsOfStudy', 'authors','abstract')
        self.params = {
            'fields': ','.join(self.fields),
            'limit': 10
            }
        
    def search_refer_papers(self):
        try:
            res = requests.get(url=self.endpoint, params=self.params)
            print(res)
            print(res.status_code)
            print(res.encoding)
            print(res.raise_for_status())
            res_dict = json.loads(res.text)
            return res_dict
        except ConnectionError as ce:
            print("Connection Error:", ce)
        except HTTPError as he:
            print("HTTP Error:", he)
        except Timeout as te:
            print("Timeout Error:", te)
        except RequestException as re:
            print("Error:", re)

    def print_refer_papers(self,r_dict):
        data = r_dict['data']
        for d in data:
            print('---------------')
            d = d['citedPaper']
            for fi in self.fields:
                if fi == 'authors':
                    print(f'{fi}: {list(map(lambda a: a["name"], d[fi]))}')
                else:
                    print(f'{fi}: {d[fi]}')
            print(f'paperID:{d["paperId"]}')

if __name__ == "__main__": 
    keyword = "b55c5259ad167ab476521395f8dadb7b9d97a65f"
    S = Reference(keyword) 
    dic = S.search_refer_papers()
    S.print_refer_papers(dic)