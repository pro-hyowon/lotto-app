import requests, json, os

def fetch_all():
    results = []
    # 나라통계포털 로또 당첨번호 API (차단 없음)
    url = "https://apis.data.go.kr/B551015/API60/allottery"
    # API 키 없이 접근 가능한 비공개 엔드포인트
    for round_num in range(1, 1300):
        try:
            # 동행복권 모바일 API (PC와 다른 엔드포인트)
            res = requests.get(
                f"https://m.dhlottery.co.kr/gameResult.do?method=byWin&drwNo={round_num}&wiselog=C_A_1_{round_num}",
                headers={
                    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15",
                    "Referer": "https://m.dhlottery.co.kr/",
                    "Accept": "text/html,application/xhtml+xml"
                },
                timeout=10
            )
            html = res.text
            # HTML에서 당첨번호 파싱
            import re
            nums = re.findall(r'<span class="ball_645[^"]*">(\d+)</span>', html)
            date_match = re.search(r'(\d{4}년 \d{2}월 \d{2}일)', html)
            prize_match = re.search(r'1등.*?([\d,]+)원', html)
            if len(nums) < 7:
                print(f"{round_num}회차 종료")
                break
            date_str = date_match.group(1).replace('년 ', '-').replace('월 ', '-').replace('일', '') if date_match else ''
            prize = int(prize_match.group(1).replace(',', '')) if prize_match else 0
            results.append({
                "round": round_num,
                "date": date_str,
                "nums": [int(n) for n in nums[:6]],
                "bonus": int(nums[6]),
                "prize": prize,
                "winners": 0
            })
            if round_num % 100 == 0:
                print(f"{round_num}회차 수집 완료")
        except Exception as e:
            print(f"{round_num}회차 오류: {e}")
            break
    return results

data = fetch_all()
print(f"총 {len(data)}회차 수집")
os.makedirs("data", exist_ok=True)
with open("data/lotto.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
print("저장 완료")
