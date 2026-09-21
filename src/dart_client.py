import os, io, zipfile, requests
from datetime import datetime, timedelta

BASE = "https://opendart.fss.or.kr/api"

class DartClient:
    def __init__(self, api_key=None, corp_code="00341916"):
        self.api_key = api_key or os.getenv("DART_API_KEY")
        if not self.api_key:
            raise RuntimeError("DART_API_KEY 환경변수가 없습니다.")
        self.corp_code = corp_code

    def get(self, endpoint, params):
        params = {"crtfc_key": self.api_key, **params}
        r = requests.get(f"{BASE}/{endpoint}.json", params=params, timeout=60)
        r.raise_for_status()
        data = r.json()
        if str(data.get("status")) != "000":
            raise RuntimeError(f"DART API 오류: {data.get('status')} {data.get('message')}")
        return data

    def disclosures(self, start_date, end_date):
        return self.get("list", {
            "corp_code": self.corp_code,
            "bgn_de": start_date, "end_de": end_date,
            "page_count": 100
        }).get("list", [])

    def annual_financials(self, year, report_code="11011", fs_div="CFS"):
        return self.get("fnlttSinglAcntAll", {
            "corp_code": self.corp_code,
            "bsns_year": str(year),
            "reprt_code": report_code,
            "fs_div": fs_div
        }).get("list", [])

def save_disclosure_index(client, years, out_file):
    rows = []
    for y in years:
        rows.extend(client.disclosures(f"{y}0101", f"{y}1231"))
    import json
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)
