import os, sys, json, yaml
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.dart_client import DartClient
from src.analyzer import analyze

ROOT=Path(__file__).resolve().parents[1]
cfg=yaml.safe_load((ROOT/"config/settings.yml").read_text(encoding="utf-8"))
client=DartClient(corp_code=cfg["company"]["corp_code"])

current=datetime.now().year
years=list(range(current-cfg["dart"]["years_back"]+1,current+1))
# Business reports are annual. If current year's annual report is not yet available,
# the API can return an error; we skip unavailable years.
year_rows={}
for y in years:
    try:
        rows=client.annual_financials(y, cfg["dart"]["report_type"], "CFS")
        if rows: year_rows[y]=rows
    except Exception as e:
        print(f"{y} CFS skipped: {e}")
        try:
            rows=client.annual_financials(y, cfg["dart"]["report_type"], "OFS")
            if rows: year_rows[y]=rows
        except Exception as e2:
            print(f"{y} OFS skipped: {e2}")

analysis=analyze(year_rows)
payload={
 "company":cfg["company"],
 "updated_at":datetime.utcnow().isoformat()+"Z",
 "source":"OpenDART",
 "rss_used":False,
 "years":analysis,
 "notes":[
  "오스템임플란트는 RSS 대신 OpenDART 공시/재무 API를 사용합니다.",
  "EBITDA와 이자부차입금은 계정과목 매핑이 필요하므로 자동 계산 대상에서 보수적으로 제외했습니다.",
  "연결(CFS) 우선, 불가하면 별도(OFS)를 사용합니다."
 ]
}
(ROOT/"data/latest.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding="utf-8")
print("updated", list(analysis))
