import urllib.request, json, os

def fetch_all():
    results = []
    # 무료 로또 API (GitHub Actions에서 접근 가능)
    for round_num in range(1, 1300):
        url = f"https://lotto.ntck.co.kr/api/lotto/{round_num}"
        try:
            req = urllib.request.Request(url, headers={'User-Agent':'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            if not data or 'drwtNo1' not in data:
                break
            results.append({
                "round": data["drwNo"],
                "date": data["drwNoDate"],
                "nums": [data[f"drwtNo{i}"] for i in range(1,7)],
                "bonus": data["bnusNo"],
                "prize": data.get("firstWinamnt", 0),
                "winners": data.get("firstPrzwnerCo", 0)
            })
        except:
            break
    return results

data = fetch_all()
os.makedirs("data", exist_ok=True)
with open("data/lotto.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print(f"총 {len(data)}회차 수집 완료")
