import urllib.request, json, os

def fetch_all():
    results = []
    round_num = 1
    while True:
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_num}"
        try:
            with urllib.request.urlopen(url, timeout=5) as r:
                data = json.loads(r.read())
            if data.get('returnValue') != 'success':
                break
            results.append({
                "round": data["drwNo"],
                "date": data["drwNoDate"],
                "nums": [data[f"drwtNo{i}"] for i in range(1,7)],
                "bonus": data["bnusNo"],
                "prize": data.get("firstWinamnt", 0),
                "winners": data.get("firstPrzwnerCo", 0)
            })
            round_num += 1
        except:
            break
    return results

data = fetch_all()
os.makedirs("data", exist_ok=True)
with open("data/lotto.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print(f"총 {len(data)}회차 수집 완료")
