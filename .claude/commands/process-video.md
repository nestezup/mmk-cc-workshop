# 단일 YouTube 영상 처리

한국 증시 YouTube 영상 1개를 처리하는 전체 파이프라인입니다.

## 입력

$ARGUMENTS 에 다음 JSON 형식의 영상 정보가 포함되어 있습니다:
```json
{
  "video_id": "...",
  "title": "...",
  "channel_name": "...",
  "channel_id": "...",
  "published": "...",
  "url": "https://www.youtube.com/watch?v=..."
}
```

## 실행 절차

### Step 1: 영상 타입 확인

```bash
mmk youtube videotype "<url>"
```

결과가 "shorts"이면 "Skipped (Short)" 보고 후 종료합니다.

### Step 2: 자막 추출

```bash
mmk youtube transcript "<url>" --format json
```

실패하면 (자막 없는 영상) 에러 보고 후 종료합니다.

### Step 3: 요약 생성

추출된 자막을 바탕으로 한국어 요약을 생성합니다. 아래 구조로 작성:

- **핵심 요약**: 3~5개 핵심 포인트 (bullet points)
- **언급 종목**: 영상에서 언급된 종목명/티커 목록
- **시장 전망**: 강세/약세/중립 판단과 근거
- **주요 수치**: 언급된 구체적 수치, 가격, 비율

요약은 2000자 이내로 작성합니다.

### Step 4: Slack 알림

/notify-slack 스킬을 호출하여 요약을 전송합니다.
인자: 제목, 채널명, URL, 요약 내용

### Step 5: Notion 저장

/save-notion 스킬을 호출하여 데이터를 저장합니다.
인자: video_id, title, channel_name, url, published, 요약 내용

### Step 6: 처리 완료 기록

```bash
python3 scripts/mark_processed.py --video-id "<video_id>" --title "<title>" --channel "<channel_name>"
```

## 중요 사항

- Step 4, 5가 모두 완료된 후에 Step 6을 실행합니다.
- Slack 또는 Notion 중 하나가 실패해도 나머지는 계속 진행하고, Step 6은 실행합니다.
- 실패한 단계가 있으면 최종 보고에 포함합니다.
