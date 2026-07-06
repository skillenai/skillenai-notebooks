import duckdb, re
con = duckdb.connect()
q = r"""
WITH b AS (
 SELECT usajobsControlNumber AS id, title, text,
  regexp_extract(text, 'Job family \(Series\)\.\s*(\d{4})', 1) AS series,
  regexp_extract(text, 'Pay scale & grade\.\s*([A-Z]{2})', 1) AS payplan,
  TRY_CAST(regexp_extract(text, 'Pay scale & grade\.\s*[A-Z]{2}\s*([0-9]{1,2})', 1) AS INT) AS grade,
  TRY_CAST(replace(regexp_extract(text, 'Salary\.\s*\$([0-9,]+)\s*-\s*\$([0-9,]+)\s*per year', 1),',','') AS INT) AS sal_lo,
  TRY_CAST(replace(regexp_extract(text, 'Salary\.\s*\$[0-9,]+\s*-\s*\$([0-9,]+)\s*per year', 1),',','') AS INT) AS sal_hi,
  regexp_extract(text, 'Salary\.\s*\$[0-9,.]+\s*-\s*\$[0-9,.]+\s*per (year|hour)', 1) AS sal_unit,
  trim(regexp_extract(text, 'Security clearance\.\s*([A-Za-z/ -]+?)\.\s*(Drug test|Position sensitivity|Trust|Financial|Relocation)', 1)) AS clearance,
  regexp_extract(text, 'Telework eligible\.\s*(Yes|No)', 1) AS telework,
  regexp_extract(text, 'Remote job\.\s*(Yes|No)', 1) AS remote,
  regexp_extract(text, 'dates\.\s*([0-9]{2}/[0-9]{2}/[0-9]{4})\s*to', 1) AS open_date
 FROM read_parquet('hf_parquet/*.parquet')
)
SELECT * FROM b WHERE series IN ('2210','1550','1560','0854','0855','1515','1529','1530')
"""
df = con.execute(q).df()
print("tech federal rows:", len(df))

def duties_slice(t):
    if not isinstance(t, str):
        return ""
    s = re.search(r'Duties\.\s*Help', t)
    if s:
        a = s.start()
    else:
        ds = [m.start() for m in re.finditer(r'\bDuties\b', t)]
        a = ds[1] if len(ds) >= 2 else (ds[0] if ds else 0)
    tail = t[a + 20:]
    e = re.search(r'(How to [Aa]pply|Required documents|How you will be evaluated)\.\s*Help', tail)
    b = a + 20 + e.start() if e else min(len(t), a + 15000)
    return t[a:min(b, a + 15000)]

df['duties'] = df['text'].map(duties_slice)
df['dlen'] = df['duties'].str.len()
df = df.drop(columns=['text'])
df.to_parquet("federal_tech_hf.parquet")
print("duties slice median len:", int(df.dlen.median()), "| p10", int(df.dlen.quantile(.1)), "| p90", int(df.dlen.quantile(.9)))
print("populated: series %.0f%% grade %.0f%% sal_hi %.0f%% clearance %.0f%% telework %.0f%%" % (
    100*(df.series != '').mean(), 100*df.grade.notna().mean(), 100*df.sal_hi.notna().mean(),
    100*(df.clearance != '').mean(), 100*(df.telework != '').mean()))
print("\nSERIES:", df.series.value_counts().to_dict())
print("months:", df.open_date.str[-4:].value_counts().to_dict() if df.open_date.notna().any() else "n/a")
