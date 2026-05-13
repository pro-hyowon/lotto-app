import requests, json, os

def fetch_all():
    # 공개된 로또 데이터 GitHub raw 파일 활용
    urls = [
        "https://raw.githubusercontent.com/roeniss/lotto-numbers/main/numbers.json",
        "https://raw.githubusercontent.com/kimjunil/lotto/master/lotto.json",
    ]
    
    for url in urls:
        try:
            res = requests.get(url, timeout=15)
            if res.status_code == 200:
                data = res.json()
                if data and len(data) > 100:
                    print(f"성공: {len(data)}회차 수집")
                    return data
        except Exception as e:
            print(f"실패: {e}")
            continue
    
    # 위가 모두 실패하면 직접 크롤링 시도
    results = []
    for round_num in range(1, 1300):
        try:
            res = requests.get(
                "https://www.dhlottery.co.kr/common.do",
                params={"method": "getLottoNumber", "drwNo": round_num},
                headers={"User-Agent": "lotto-tracker/1.0"},
                timeout=10
            )
            data = res.json()
            if data.get("returnValue") != "success":
                break
            results.append({
                "round": data["drwNo"],
                "date": data["drwNoDate"],
                "nums": [data[f"drwtNo{i}"] for i in range(1, 7)],
                "bonus": data["bnusNo"],
                "prize": data.get("firstWinamnt", 0),
                "winners": data.get("firstPrzwnerCo", 0)
            })
            if round_num % 100 == 0:
                print(f"{round_num}회차 완료")
        except Exception as e:
            print(f"{round_num}회차 오류: {e}")
            break
    return results

data = fetch_all()

# 데이터 형식 통일
normalized = []
for d in data:
    if isinstance(d, dict):
        normalized.append(d)

print(f"총 {len(normalized)}회차 저장")
os.makedirs("data", exist_ok=True)
with open("data/lotto.json", "w", encoding="utf-8") as f:
    json.dump(normalized, f, ensure_ascii=False)
print("완료")
