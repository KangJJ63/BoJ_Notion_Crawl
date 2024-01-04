import requests

class NotionItem:       
    # 노션 토큰 설정
    NOTION_TOKEN = "secret_b7RieIIXp9vS4ixhGWZoHSrAF1wmKUfZbiTdvn24Tq3"
    # 데이터 베이스 ID 설정
    DATABASE_ID = "3b83171218224cbc884ba490903048de"
    # 문제 난이도별 텍스트 리스트
    LEVEL_NAME = ["Bronze","Silver","Gold"]
    # 문제 난이도별 숫자 텍스트
    LEVEL_GRADE = [1,5,4,3,2]
    # 노션 접속 헤더 설정
    HEADERS = {
        "Authorization": "Bearer " + NOTION_TOKEN,
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28",
    }

    """
    API 데이터를 통한 노션 데이터베이스 객체 생성
    """
    def __init__(self,probId,probName,link,level_num,tags):
        # 레벨 텍스트 설정
        level_grade = f"{NotionItem.LEVEL_NAME[(level_num-1)//5]}" if level_num else "Unrated"
        level_tier = f"{NotionItem.LEVEL_GRADE[level_num%5]}" if level_num else "0"
        # level_text = f"{NotionItem.LEVEL_NAME[(level_num-1)//5]} {NotionItem.LEVEL_GRADE[level_num%5]}" if level_num else "Unrated"
        # 새싹 여부 텍스트 설정
        # sak_txt = "O" if sak else "X"

        # 태그 서식에 맞게 재설정
        tags = [{"name":nm} for nm in tags]

        # 데이터베이스에 추가할 json 셋 설정
        self.data = {
        # "번호": {"title": [{"text": {"content": str(probId)}}]},
        "문제": {"title": [{"text": {"content": probName}}]},
        "번호" : {"rich_text": [{"text": {"content":str(probId) }}]},
        "링크":{"url":link},
        "등급":{"rich_text": [{"text": {"content": level_grade},"annotations":{"bold":True,"color":self.set_level_color(level_num)}}]},
        "티어":{"rich_text": [{"text": {"content": level_tier},"annotations":{"bold":True,"color":self.set_level_color(level_num)}}]},
        # "난이도":{"rich_text": [{"text": {"content": level_text},"annotations":{"bold":True,"color":self.set_level_color(level_num)}}]},
        # "새싹여부" :  {"rich_text": [{"text": {"content":sak_txt }}]},
        "태그": {"multi_select": tags},
        }


    """
    노션 데이터베이스에 삽입
    """
    def insert_data_to_notion(self):
        create_url = "https://api.notion.com/v1/pages"
        payload = {"parent": {"database_id": NotionItem.DATABASE_ID}, "properties": self.data}

        res = requests.post(create_url, headers=NotionItem.HEADERS, json=payload)
        print(res)

    """
    난이도별 색깔 변경 함수
    """
    def set_level_color(self,level_num):

        if not level_num:
            return "blue"
        elif level_num <6:
            return "brown"
        elif level_num < 11:
            return "gray"
        else:
            return "yellow"