import requests, json, os

def fetch_all():
    results = []
    # 동행복권 API 우회 - JSON 직접 파싱 방식
    for round_num in range(1, 1300):
        url = "https://www.dhlottery.co.kr/common.do"
        params = {
            "method": "getLottoNumber",
            "drwNo": round_num
        }
        proxies = {
            "http": None,
            "https": None
        }
        try:
            res = requests.get(
                url,
                params=params,
                proxies=proxies,
                headers={
                    "User-Agent": "Mozilla/5.0",
                    "Accept": "*/*",
                    "Connection": "keep-alive"
                },
                timeout=15,
                verify=False
            )
            data = res.json()
            if data.get("returnValue") != "success":
                print(f"{round_num}회차에서 종료")
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
                print(f"{round_num}회차 수집 완료")
        except Exception as e:
            print(f"{round_num}회차 오류: {e}")
            break

    return results

# SSL 경고 무시
import urllib3
urllib3.disable_warnings()

data = fetch_all()
print(f"총 {len(data)}회차 수집")
os.makedirs("data", exist_ok=True)
with open("data/lotto.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("저장 완료")
