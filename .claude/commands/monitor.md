# 한국 증시 YouTube 채널 모니터링

등록된 YouTube 채널의 새 영상을 확인하고, 키워드 필터링 후 요약 → Slack 알림 → Notion 저장 파이프라인을 실행합니다.

## 실행 절차

### Step 1: 새 영상 확인

```bash
python3 scripts/fetch_new_videos.py
```

출력된 JSON 배열을 파싱합니다.

- 빈 배열 `[]`이면: "새 영상 없음" 보고 후 종료
- 영상이 있으면: Step 2로 진행

### Step 2: 각 영상 처리

JSON 배열의 각 영상에 대해 /process-video 스킬을 호출합니다.

각 영상의 JSON 데이터를 인자로 전달:
```
/process-video {"video_id": "...", "title": "...", "channel_name": "...", "channel_id": "...", "published": "...", "url": "..."}
```

### Step 3: 결과 요약

모든 영상 처리가 완료되면 최종 요약을 출력합니다:
- 확인된 새 영상 수
- 처리 성공한 영상 수
- 실패한 영상 (있을 경우 사유 포함)

## 에러 처리

- `fetch_new_videos.py` 실패 시: 에러 보고 후 종료 (다음 사이클에서 재시도)
- 개별 영상 처리 실패 시: 에러 로그 후 다음 영상으로 계속 진행
- 모니터링 루프 자체는 절대 중단하지 않음
