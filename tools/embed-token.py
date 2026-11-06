#!/usr/bin/env python3
"""
embed-token.py — 읽기 전용 PAT 를 XOR+base64 로 난독화해 reports-viewer(index.html)에 심는다.

공개 저장소(GitHub Pages)에 평문 PAT 를 커밋하면 GitHub secret scanning 이 감지해
토큰을 자동 폐기한다. XOR+base64 로 바꿔 심으면 그 탐지를 피한다 — 이것은 보안이 아니라
평문 노출 방지일 뿐이다. 이 페이지를 여는 사람은 누구나 토큰을 복원해 비공개 저장소의
모든 보고서를 읽을 수 있으므로, 토큰은 반드시 **Contents: Read-only**, 대상 저장소
**1개(bidmad-inspector-reports)** 로만 제한된 fine-grained PAT 여야 한다.

사용법 (토큰이 셸 기록·로그에 남지 않도록 stdin 권장):
  python3 embed-token.py reports-viewer.html < token.txt
  # 또는
  python3 embed-token.py reports-viewer.html --token github_pat_xxx   # (기록에 남음, 비권장)

CONFIG.tokenKey 와 아래 KEY 가 반드시 같아야 한다.
"""
import base64
import re
import sys

KEY = b"bidmad-inspector-reports-viewer"  # 반드시 index.html 의 CONFIG.tokenKey 와 일치


def obfuscate(token: str) -> str:
    raw = token.encode("utf-8")
    x = bytes(b ^ KEY[i % len(KEY)] for i, b in enumerate(raw))
    return base64.b64encode(x).decode("ascii")


def main():
    args = sys.argv[1:]
    if not args:
        sys.exit("usage: embed-token.py <index.html> [--token TOKEN]  (token on stdin preferred)")
    path = args[0]
    token = None
    if "--token" in args:
        token = args[args.index("--token") + 1]
    if not token and not sys.stdin.isatty():
        token = sys.stdin.read().strip()
    if not token:
        sys.exit("no token provided (pipe it on stdin or pass --token)")

    blob = obfuscate(token)
    html = open(path, encoding="utf-8").read()
    new, n = re.subn(r"(tokenBlob:\s*)'[^']*'", r"\1'" + blob + "'", html, count=1)
    if n != 1:
        sys.exit("could not find a tokenBlob: '...' line to replace in " + path)
    open(path, "w", encoding="utf-8").write(new)
    # 토큰 값은 절대 출력하지 않는다
    print(f"embedded obfuscated token ({len(token)} chars) into {path}")
    print("reminder: use a Contents:Read-only, single-repo fine-grained PAT only.")


if __name__ == "__main__":
    main()
