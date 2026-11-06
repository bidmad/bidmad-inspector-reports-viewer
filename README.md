# Bidmad Inspector — 연결 점검 보고서 뷰어

BidmadSDK `InspectorAdapter` 연결 점검(linkcheck) 보고서를 퍼블리셔(앱)별로 보여 주는
단일 페이지 대시보드. GitHub Pages 로 배포된다.

**바로 열기:** https://bidmad.github.io/bidmad-inspector-reports-viewer/

## 쓰는 법

퍼블리셔가 서로의 존재를 알 수 없도록 **전체 목록 페이지는 없다.** 각 앱은 자기 전용
링크로만 접근한다 — `…/#site/<key>` (예: `#site/10474`). 그 링크는 해당 앱의 **실행 이력**
→ **상세 보고서**만 보여 준다. `<key>` 는 보통 앱의 Bidmad siteId.

- **퍼블리셔에게:** 그 앱의 `…/#site/<key>` 링크만 전달한다.
- **ADOP 내부:** 어떤 앱이 있고 key 가 무엇인지는 비공개 저장소의 `reports/index.json`
  (ADOP 전용 색인)에서 확인한다 — 공개 페이지는 이 색인을 읽지 않는다.
- 주소를 key 없이 열면(루트) 데이터 없이 "앱 전용 링크로 접속하라"는 안내만 나온다.

## 데이터 흐름

보고서는 비공개 저장소 **`bidmad/bidmad-inspector-reports`** 에 있고, 이 페이지가
**읽기 전용 PAT** 로 GitHub Contents API 에서 읽어 온다. 보고서를 드래그&드롭하지 않는다.

```
비공개 bidmad-inspector-reports   (reports/<key>/… + index.json)
        │  읽기 전용 PAT (Contents: Read)
        ▼
이 페이지 index.html  →  퍼블리셔 목록 → 실행 이력 → 상세
```

## 보안 (중요)

이 페이지에 심긴 PAT 는 XOR+base64 로 **난독화**돼 있을 뿐 암호화가 아니다. 이 페이지를
여는 사람은 누구나 토큰을 복원해 비공개 저장소의 **모든** 보고서를 읽을 수 있다. 퍼블리셔
간 격리는 "공유 링크 수준"일 뿐이다. 그래서 토큰은 반드시:

- **fine-grained PAT**, **Contents: Read-only**, 대상 저장소 **`bidmad-inspector-reports` 1개**로만 제한.
- 절대 쓰기 권한·다른 저장소 권한을 주지 않는다.

## 토큰 심기 / 교체

```bash
# 읽기 전용 PAT 를 뷰어에 난독화해 삽입 (토큰은 stdin 으로 — 셸 기록에 안 남게)
python3 tools/embed-token.py index.html < token.txt
git add index.html && git commit -m "rotate read token" && git push
```

## 원본

이 저장소의 `index.html` 은
`BidmadSDK-AOS/InspectorAdapter/viewer/reports-viewer.html` 의 **사본(미러)** 이다.
원본이 바뀌면 다시 복사하고(`tools/embed-token.py` 로 토큰을 다시 심어) 배포한다.
보고서 JSON 스키마는 원본 저장소의 `InspectorAdapter/viewer/linkcheck-report.schema.md` 참고.
