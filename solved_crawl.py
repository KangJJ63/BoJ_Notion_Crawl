import requests, time, json
from notion_item import NotionItem

INCLUDE_TYPES = {'수학'
                 ,'구현'
                 ,'자료 구조'
                 ,'다이나믹 프로그래밍'
                 ,'그래프 이론'
                 ,'그래프 탐색'
                 ,'그리디 알고리즘'
                 ,'문자열'
                 ,'브루트포스 알고리즘'
                 ,'정렬'
                 ,'트리'
                 ,'이분 탐색'
                 ,'시뮬레이션'
                 ,'너비 우선 탐색'
                 ,'깊이 우선 탐색'
                 ,'최단 경로'
                 ,'데이크스트라'
                 ,'백트래킹'
                 ,'두 포인터'}


def crawl(page):
    url = "https://solved.ac/api/v3/search/problem"
    querystring = {"query": " ", "page": f"{page}"}

    headers = {"Content-Type": "application/json"}
    response = requests.request("GET", url, headers=headers, params=querystring)

    temp = dict()
    temp["item"] = json.loads(response.text).get("items")

    # 각 Item(문제) 별로 조건 설정 후 표 넣기
    for item in temp["item"]:
        # 난이도 (0:Unrated, 1-5:Bronze, 6-10:Silver, 11-15:Gold)
        level = item.get("level")

        # 문제가 한글이 아니면 종료
        langs = [lang.get("language") for lang in item.get("titles")]
        if "ko" not in langs:
            return
        
        # 플래티넘 난이도는 pass
        if level > 15:
            continue

        # 레이팅 주지 않는 문제 pass
        if item.get("givesNoRating"):
            continue




        #문제ID
        problemId = item.get("problemId")
        #문제 링크
        link = f"https://www.acmicpc.net/problem/{problemId}"
        #문제 제목
        probName = item.get("titleKo")
        #새싹 여부
        # sak = item.get("sprout")
        #문제 태그
        tags = list()
        #태그 정보들
        info = item.get("tags")
        length = len(info)
        for idx, tag in enumerate(info):
            temp_tag = tag.get("displayNames")
            select_tag = temp_tag[0].get("short")
            if select_tag in INCLUDE_TYPES:
                tags.append(select_tag)

            if idx == length - 1:
                continue

        prob = NotionItem(problemId,probName,link,level,tags)
        prob.insert_data_to_notion()

def notion_item():
    for i in range(1, 2):
        print(f"crawling {i} page now still {1 - i} to go")
        crawl(i)

        time.sleep(12)

if __name__ == "__main__":
    notion_item()