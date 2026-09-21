# OsstemImplant_dart

OpenDART API 기반 오스템임플란트 재무 분석 Agent.

## RSS
오스템임플란트 RSS 주소를 사용하지 않습니다. OpenDART 공시검색 API와 정기보고서 재무 API를 사용합니다.

## 설정
GitHub Repository Settings → Secrets and variables → Actions → New repository secret

Name:
`DART_API_KEY`

Value:
OpenDART에서 발급받은 40자리 인증키.

## 실행
Actions → Update DART financials → Run workflow

자동 실행은 매일 한국시간 오전 6시(UTC 21:00)입니다.

## Dashboard
GitHub Pages에서 `dashboard/index.html`을 배포합니다.
Settings → Pages → GitHub Actions 방식으로 설정하세요.

## 분석 기준
첨부된 '재무제표 및 재무비율 실무 가이드'를 기준으로 핵심 재무수치와 비율 구조를 반영했습니다.
가이드가 제시하는 주요 흐름은 매출 성장 → 이익률 → 현금흐름 → 차입 부담 → 투자수익률 → 주가 수준입니다.

현재 시장지표(PER/PBR/EV/EBITDA/FCF yield)는 OpenDART 재무 API만으로 주가/시가총액을 안정적으로 구성하기 어려워 별도 시장데이터 연동이 필요합니다.
