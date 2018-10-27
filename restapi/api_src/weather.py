import requests
from bs4 import BeautifulSoup

seoul_weather_web_url = 'https://weather.naver.com/'


def get_seoul_weather():
    try:
        # 1. requests를 이용하여 크롤링하기
        r = requests.get(seoul_weather_web_url)

        # Check the status code
        if r.status_code != 200:
            raise Exception("Can't crawl the html. {} status code".format(r.status_code))

        text = r.text

        # 2. beautifulsoup로 파싱
        soup = BeautifulSoup(text, 'html.parser')
        cur_temp = round(float(soup.select("#content > div.m_zone1 > table > tbody > tr:nth-of-type(1) > td.info > p > span.temp > strong")[0].text))
        min_temp = round(float(soup.select("#content > div.m_zone1 > table > tbody > tr:nth-of-type(2) > td.info > p > span.temp > strong")[0].text))
        max_temp = round(float(soup.select("#content > div.m_zone1 > table > tbody > tr:nth-of-type(3) > td.info > p > span.temp > strong")[0].text))

        # 내일 날씨
        tomorrow_min_temp = round(float(soup.select("#content > div.m_zone1 > table > tbody > tr:nth-of-type(4) > td.info > p > span.temp > strong")[0].text))
        tomorrow_max_temp = round(float(soup.select("#content > div.m_zone1 > table > tbody > tr:nth-of-type(5) > td.info > p > span.temp > strong")[0].text))

        msg = "오늘 서울의 현재 온도는 {}도입니다. (최저 {}도, 최고 {}도)\n".format(cur_temp, min_temp, max_temp)
        msg += "내일은 최저 {}도, 최고 {}도로 예상됩니다.".format(tomorrow_min_temp, tomorrow_max_temp)
        return msg
    except:
        return "날씨 api에 문제가 생겼습니다. 나중에 다시 시도해주세요!"


if __name__ == "__main__":
    print(get_seoul_weather())
