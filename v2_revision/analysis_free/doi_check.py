import sys
import json, urllib.request, urllib.parse
sys.stdout.reconfigure(encoding='utf-8') if hasattr(sys.stdout,'reconfigure') else None
DOIS={
"Northcutt2021":"10.48550/arXiv.2103.14749","Gema2025":"10.18653/v1/2025.naacl-long.262","Vendrow2025":"10.48550/arXiv.2502.03461",
"Bean2025":"10.48550/arXiv.2511.04703","BowmanDahl2021":"10.18653/v1/2021.naacl-main.385","Zou2023":"10.18653/v1/2023.acl-long.798",
"Ahuja2025":"10.48550/arXiv.2504.11900","KimSchuster2023":"10.18653/v1/2023.acl-long.213","Dwyer1999":"10.1145/302405.302672",
"Newcombe1998":"10.1002/(SICI)1097-0258(19981130)17:22<2635::AID-SIM954>3.0.CO;2-C","FieldWelsh2007":"10.1111/j.1467-9868.2007.00593.x",
"Lakens2017":"10.1177/1948550617697177","Miller2024":"10.48550/arXiv.2411.00640","Gururangan2018":"10.18653/v1/N18-2017",
"PavlickKwiatkowski2019":"10.1162/tacl_a_00293","Ribeiro2020":"10.18653/v1/2020.acl-main.442","KarakasSimsek2026(skip)":"10.18653/v1/2026.acl-srw.71"}
out={}
for k,d in DOIS.items():
    u="https://doi.org/"+urllib.parse.quote(d,safe="/():<>;-.")
    req=urllib.request.Request(u,headers={"Accept":"application/vnd.citationstyles.csl+json","User-Agent":"doi-check/1.0"})
    try:
        j=json.load(urllib.request.urlopen(req,timeout=30))
        au=[a.get("family") for a in j.get("author",[])][:4]
        ti=j.get("title"); yr=(j.get("issued",{}).get("date-parts") or [[None]])[0][0]
        out[k]={"status":"OK","title":ti,"authors_first4":au,"year":yr,"venue":j.get("container-title") or j.get("publisher"),"pages":j.get("page"),"vol":j.get("volume"),"issue":j.get("issue")}
    except Exception as e:
        out[k]={"status":"FAIL","error":str(e)[:100]}
    print(k,out[k])
json.dump(out,open("doi_check.json","w",encoding="utf-8"),indent=1,ensure_ascii=False)
