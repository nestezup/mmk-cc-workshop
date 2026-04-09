# Slack 알림 전송

한국 증시 YouTube 영상 요약을 Slack에 전송합니다.

## 입력

$ARGUMENTS 에 다음 정보가 포함되어 있습니다:
- 영상 제목, 채널명, 영상 URL
- 요약 내용 (핵심 요약, 언급 종목, 시장 전망)

## 실행 절차

1. `config/config.json`에서 `slack.channel_name` 값을 읽습니다.

2. MCP 도구 `mcp__b16dc569-6b6b-4f9f-a21f-173ee5676ced__slack_search_channels`로 채널을 검색하여 채널 ID를 확인합니다.

3. 아래 형식으로 메시지를 구성합니다:

```
📈 *[채널명] 새 영상 요약*

*제목*: <영상 제목>
*링크*: <영상 URL>

<요약 내용>

---
_자동 요약 by YouTube Monitor_
```

4. MCP 도구 `mcp__b16dc569-6b6b-4f9f-a21f-173ee5676ced__slack_send_message`로 메시지를 전송합니다.

5. 성공/실패 결과를 보고합니다.
