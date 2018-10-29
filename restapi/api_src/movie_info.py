import requests
from bs4 import BeautifulSoup
import operator

naver_movie_web_url = 'https://movie.naver.com/movie/running/current.nhn'


def get_movie_info():
    try:
        # 1. requests를 이용하여 크롤링하기
        r = requests.get(naver_movie_web_url)

        # Check the status code
        if r.status_code != 200:
            raise Exception("Can't crawl the html. {} status code".format(r.status_code))

        text = r.text

        # 2. beautifulsoup로 파싱
        soup = BeautifulSoup(text, 'html.parser')

        movie_list = soup.body.find(class_ = 'lst_detail_t1').find_all('li')

        movie_sort = {}

        movie_dict = {}


        cnt = 0
        for movie in movie_list:
            cnt += 1
            if(cnt > 15):
                break
            movie_title = movie.find(class_='tit').find('a').text
            movie_score = movie.find(class_='info_star').find(class_='num').text
            try:
                movie_adr = movie.find(class_='info_exp').find(class_='num').text
            except:
                continue
            movie_sort[movie_title] = float(movie_adr)
            movie_dict[movie_title] = movie_score
           
        movie_list = sorted(movie_sort.items(), key=operator.itemgetter(1), reverse=True)

        msg = ''

        for movie, rate in movie_list:
            msg += "{} : {}\n".format(movie, movie_dict[movie])
        
        # 마지막에 rstrip()을 통해 추가적인 개행 제거
        msg = msg.rstrip()

        return msg
    except Exception as e:
        print(e)
        return "영화 api에 문제가 생겼습니다. 나중에 다시 시도해주세요!"


if __name__ == "__main__":
    print(get_movie_info())
