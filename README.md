# Bidmad Inspector — 연결 점검 보고서 뷰어

BidmadSDK `InspectorAdapter` 연결 점검(linkcheck) 보고서를 퍼블리셔(앱)별로 보여 주는
단일 페이지. GitHub Pages(정적) + Cloudflare Worker(프록시) 구성.

**바로 열기:** https://bidmad.github.io/bidmad-inspector-reports-viewer/

## 구성

```
브라우저 (이 페이지, GitHub Pages — 토큰 없음)
   │  GET <Worker>/history?site=KEY&sig=…   (서명된 앱 전용 요청)
   ▼
Cloudflare Worker  (secret: GITHUB_TOKEN, LINK_SECRET)
   │  sig = HMAC(site, LINK_SECRET) 검증 → 그 앱 데이터만
   ▼
비공개 bidmad-inspector-reports  →  reports/<KEY>/…
```

GitHub 토큰은 Worker 에만 있고 이 페이지에는 없다. 각 퍼블리셔는 **서명된 전용 링크**
(`…/#site/<KEY>/<SIG>`)로만 접근하며, 그 서명은 자기 앱에만 유효하다 → 다른 앱 데이터는
받을 수 없다. 전체 목록 페이지는 없다(루트로 열면 "전용 링크로 접속" 안내만).

## 설정

1. Worker 배포 — 원본 저장소 `InspectorAdapter/viewer/worker/README.md` 참고.
2. 이 저장소 `index.html` 의 `CONFIG.apiBase` 를 Worker URL 로 바꾸고 커밋·푸시.
3. 퍼블리셔 링크 생성:
   `LINK_SECRET=… python3 tools/mint-link.py <site>` (원본 저장소 `InspectorAdapter/viewer/tools/`).

## 원본

이 저장소의 `index.html` 은 `BidmadSDK-AOS/InspectorAdapter/viewer/reports-viewer.html`
의 **사본(미러)** 이다. 원본이 바뀌면 다시 복사해 배포한다. 보고서 JSON 스키마는
원본 저장소의 `InspectorAdapter/viewer/linkcheck-report.schema.md` 참고.
