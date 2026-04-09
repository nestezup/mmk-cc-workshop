# Claude Code 워크샵 스타터

강의 실습용 Claude Code 워크샵 스타터 프로젝트입니다.

## 프로젝트 목적

이 프로젝트를 fork하여 Claude Code 웹에서 바로 자동화 바이브 코딩을 시작할 수 있습니다.

## mmk CLI

mmk (Magic Meal Kits)는 YouTube 자막 추출, 메타데이터 조회 등을 지원하는 CLI 도구입니다.

**중요: 현재 토큰은 YouTube 전용입니다. `mmk youtube` 명령어만 사용하세요.**
`mmk notion`, `mmk paymint` 등 다른 명령어는 권한이 없어 실패합니다 (403 insufficient_scope).

### 설정

```bash
export MMK_SERVER="https://magic-meal-kits-r7fpfharja-uw.a.run.app"
export MMK_TOKEN="<강사가 제공한 토큰>"
```

### 사용 가능한 명령어

```bash
# YouTube 자막 추출
mmk youtube transcript <youtube-url>
mmk youtube transcript <youtube-url> --format json
mmk youtube transcript <youtube-url> --format srt

# YouTube 메타데이터 조회
mmk youtube metadata <youtube-url>

# YouTube 영상 타입 확인 (일반 영상 vs Short)
mmk youtube videotype <youtube-url>
```

### 사용 불가 명령어 (토큰 권한 없음)

- `mmk notion ...` — 사용 불가
- `mmk paymint ...` — 사용 불가
- `mmk threads ...` — 사용 불가

## 한국 증시 YouTube 모니터링 시스템

등록된 YouTube 채널에서 키워드 기반으로 영상을 필터링하고, 자막 추출 → 요약 → Slack 알림 + Notion 저장을 자동으로 수행합니다.

### 사용 가능한 스킬

| 스킬 | 설명 |
|------|------|
| `/monitor` | 전체 모니터링 파이프라인 실행 (새 영상 확인 → 처리) |
| `/process-video` | 단일 영상 처리 (자막 추출 → 요약 → Slack → Notion) |
| `/notify-slack` | Slack 채널에 영상 요약 전송 |
| `/save-notion` | Notion 데이터베이스에 영상 데이터 저장 |

### 스케줄링

```
/loop 60m /monitor
```

### 설정 파일

- `config/config.json` — 채널 목록, 필터 키워드, Slack/Notion ID
- `data/processed_videos.json` — 처리 완료된 영상 ID (중복 방지)

### Python 스크립트

- `scripts/fetch_new_videos.py` — RSS 피드 수집 + 키워드 필터 + 중복 체크
- `scripts/mark_processed.py` — 영상 처리 완료 기록

### 채널/키워드 추가

`config/config.json`의 `channels` 배열에 새 채널을 추가하거나, `filter.keywords`에 키워드를 추가합니다.

## 세션 시작 시

세션이 시작되면 `.claude/scripts/check-env.sh` 스크립트가 자동 실행되어 환경 정보를 출력합니다:
- 호스트명, OS, CPU, 메모리, 디스크
- Git, Python, Node, mmk 버전
- 원격 환경 여부
