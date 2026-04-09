# Notion DB 저장

한국 증시 YouTube 영상 데이터와 요약을 Notion 데이터베이스에 저장합니다.

## 입력

$ARGUMENTS 에 다음 정보가 포함되어 있습니다:
- video_id, title, channel_name, url, published
- 요약 내용 (핵심 요약, 언급 종목, 시장 전망)

## 실행 절차

1. `config/config.json`에서 `notion.database_id` 값을 읽습니다.

2. MCP 도구 `mcp__965e95ff-1299-4b18-b636-87bc81868a9b__notion-fetch`로 데이터베이스 스키마를 확인합니다.
   - resource: `database`, id: config에서 읽은 database_id

3. 스키마에 맞춰 MCP 도구 `mcp__965e95ff-1299-4b18-b636-87bc81868a9b__notion-create-pages`로 페이지를 생성합니다.
   - parent database_id: config에서 읽은 database_id
   - 제목(title 속성): 영상 제목
   - 기타 속성은 DB 스키마에 맞춰 매핑
   - 페이지 본문에 요약 내용을 마크다운으로 작성

4. 성공/실패 결과와 생성된 페이지 URL을 보고합니다.
