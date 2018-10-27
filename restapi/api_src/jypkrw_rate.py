import requests
from bs4 import BeautifulSoup

jpykrw_web_url = "https://finance.naver.com/marketindex/exchangeDetail.nhn?marketindexCd=FX_JPYKRW"


def get_exchange():
    try:
        # 1. requests를 이용하여 크롤링하기
        r = requests.get(jpykrw_web_url)

        # Check the status code
        if r.status_code != 200:
            raise Exception("Can't crawl the html. {} status code".format(r.status_code))

        text = r.text

        # 2. beautifulsoup로 파싱
        soup = BeautifulSoup(text, 'html.parser')
        result = soup.select("#content > div.section_calculator > table:nth-of-type(1) > tbody > tr > td:nth-of-type(1)")
        assert len(result) == 1
        jpykrw_rate = result[0].text
        msg = "현재 환율은 100엔에 {}원입니다.".format(jpykrw_rate)
        return msg
    except:
        return "환율 api에 문제가 생겼습니다. 나중에 다시 시도해주세요!"


if __name__ == "__main__":
    print(get_exchange())
