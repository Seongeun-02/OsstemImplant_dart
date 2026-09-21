import re, math

def num(x):
    if x is None: return None
    s = str(x).replace(",", "").strip()
    if s in ("", "-", "nan", "None"): return None
    try: return float(s)
    except: return None

ALIASES = {
 "total_assets":["자산총계"],
 "cash_and_equivalents":["현금및현금성자산","현금및현금성자산"],
 "accounts_receivable":["매출채권","매출채권및기타채권"],
 "inventories":["재고자산"],
 "property_plant_equipment":["유형자산"],
 "total_liabilities":["부채총계"],
 "equity":["자본총계"],
 "revenue":["매출액","수익(매출액)","영업수익"],
 "gross_profit":["매출총이익"],
 "selling_general_admin":["판매비와관리비","판매비및관리비"],
 "operating_income":["영업이익"],
 "profit_before_tax":["법인세비용차감전순이익","세전이익"],
 "net_income":["당기순이익"],
 "controlling_interest_net_income":["지배기업의 소유주에게 귀속되는 당기순이익","지배기업소유주지분순이익"],
 "operating_cash_flow":["영업활동현금흐름"],
 "investing_cash_flow":["투자활동현금흐름"],
 "financing_cash_flow":["재무활동현금흐름"],
}

def extract(rows):
    out={}
    for key, aliases in ALIASES.items():
        found=None
        for row in rows:
            name=(row.get("account_nm") or "").strip()
            if name in aliases:
                # annual amount: use thstrm_amount first
                found=num(row.get("thstrm_amount"))
                if found is not None: break
        out[key]=found
    # DART does not reliably expose EBITDA / interest-bearing debt as one standard line.
    # They are left null unless future account mappings are added.
    out["ebitda"]=None
    out["interest_bearing_debt"]=None
    return out

def avg(a,b):
    if a is None or b is None: return None
    return (a+b)/2

def ratio(a,b):
    if a is None or b in (None,0): return None
    return a/b

def analyze(year_rows):
    raw={y:extract(rows) for y,rows in year_rows.items()}
    years=sorted(raw)
    result={}
    for i,y in enumerate(years):
        d=raw[y]
        prev=raw[years[i-1]] if i else {}
        r={}
        r["gross_margin"]=ratio(d["gross_profit"],d["revenue"])
        r["operating_margin"]=ratio(d["operating_income"],d["revenue"])
        r["net_margin"]=ratio(d["net_income"],d["revenue"])
        r["ebitda_margin"]=ratio(d["ebitda"],d["revenue"])
        r["roa"]=ratio(d["net_income"],avg(d["total_assets"],prev.get("total_assets")))
        r["roe"]=ratio(d["net_income"],avg(d["equity"],prev.get("equity")))
        r["current_ratio"]=None
        r["quick_ratio"]=None
        r["debt_to_equity"]=ratio(d["total_liabilities"],d["equity"])
        r["equity_ratio"]=ratio(d["equity"],d["total_assets"])
        r["debt_dependency"]=ratio(d["interest_bearing_debt"],d["total_assets"])
        r["interest_coverage"]=None
        r["net_debt_to_ebitda"]=None
        r["asset_turnover"]=ratio(d["revenue"],avg(d["total_assets"],prev.get("total_assets")))
        r["revenue_growth"]=ratio(d["revenue"],prev.get("revenue"))-1 if d["revenue"] is not None and prev.get("revenue") not in (None,0) else None
        r["cfo_to_net_income"]=ratio(d["operating_cash_flow"],d["net_income"])
        result[y]={"raw":d,"ratios":r}
    return result
