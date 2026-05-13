import requests, json, os, time

def fetch_all():
    results = []
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.dhlottery.co.kr/',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Language': 'ko-KR,ko;q=0.9',
        'X-Requested-With': 'XMLHttpRequest',
    })

    # 먼저 메인 페이지 방문해서 쿠키 획득
    try:
        session.get('https://www.dhlottery.co.kr/', timeout=10)
        time.sleep(1)
    except:
        pass

    round_num = 1
    fail_count = 0
    while fail_count < 3:
        url = f"https://www.dhlottery.co.kr/common.do?method=getLottoNumber&drwNo={round_num}"
        try:
            res = session.get(url, timeout=10)
            data = res.json()
            if data.get('returnValue') != 'success':
                fail_count += 1
                time.sleep(2)
                continue
            fail_count = 0
            results.append({
                "round": data["drwNo"],
                "date": data["drwNoDate"],
                "nums": [data[f"drwtNo{i}"] for i in range(1,7)],
                "bonus": data["bnusNo"],
                "prize": data.get("firstWinamnt", 0),
                "winners": data.get("firstPrzwnerCo", 0)
            })
            round_num += 1
            if round_num % 200 == 0:
                print(f"{round_num}회차 수집 중...")
                time.sleep(1)
        except Exception as e:
            print(f"오류: {e}")
            fail_count += 1
            time.sleep(2)

    return results

data = fetch_all()
print(f"총 {len(data)}회차 수집")
os.makedirs("data", exist_ok=True)
with open("data/lotto.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("저장 완료")
