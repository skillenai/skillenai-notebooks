import html, re, json
TAG = re.compile(r"<[^>]{1,400}>")
WS  = re.compile(r"\s+")
def clean(t):
    if not t: return ""
    t = html.unescape(html.unescape(t))      # double-escaped in places
    t = TAG.sub(" ", t)
    t = t.replace("’","'").replace("‘","'").replace("“",'"').replace("”",'"')
    t = t.replace("—"," - ").replace("–"," - ")
    return WS.sub(" ", t).strip()
SENT = re.compile(r"(?<=[.!?;:])\s+|\s*[•▪●\|]\s*|\n+")
def sentences(t):
    return [s.strip() for s in SENT.split(t) if 15 < len(s.strip()) < 600]
def load(path, limit=None):
    rows=[]
    for i,line in enumerate(open(path)):
        if limit and i>=limit: break
        d=json.loads(line); d["text"]=clean(d.get("extractedText") or ""); d.pop("extractedText",None)
        rows.append(d)
    return rows
