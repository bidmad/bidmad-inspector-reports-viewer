# Bidmad Inspector — 연결 점검 보고서 뷰어

BidmadSDK `InspectorAdapter` 의 연결 점검(linkcheck) 보고서(`linkcheck-*.json`)를 사람이 읽기 좋게 보여 주는 단일 페이지 뷰어입니다.

**바로 열기:** https://bidmad.github.io/bidmad-inspector-reports-viewer/

## 쓰는 법

1. 점검을 켜고 실행합니다(adb 전용):
   ```bash
   adb shell setprop debug.bidmad.inspect <앱 패키지명>
   # 재실행: adb shell setprop debug.bidmad.inspect.run $(date +%s)
   ```
2. 기기에서 보고서를 꺼냅니다:
   ```bash
   adb pull /storage/emulated/0/Android/data/<앱 패키지명>/files/bidmad_inspector/
   ```
3. 위 페이지를 열고 `linkcheck-<시각>.json` 파일을 창에 **끌어다 놓습니다**.

보고서는 브라우저 안에서만 열립니다 — 어디에도 업로드되지 않으며, 서버로 전송하지 않습니다.

## 내용물

- `index.html` — 뷰어(클라이언트 전용, 외부 의존성·네트워크 호출 없음).

이 저장소의 `index.html` 은 원본
`BidmadSDK-AOS/InspectorAdapter/viewer/linkcheck-viewer.html` 의 **사본(미러)** 입니다.
원본이 바뀌면 수동으로 다시 복사해 갱신합니다.

## 보고서 형식

보고서 JSON 스키마(`bidmad.inspector.linkcheck/2`)는 원본 저장소의
`InspectorAdapter/viewer/linkcheck-report.schema.md` 를 참고하세요.
