"""Scrape published timestamps from a list of URLs by parsing meta tags + JSON-LD."""
import json, re, sys, urllib.request, urllib.parse, concurrent.futures, time, gzip, io

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Skillenai-Analysis"

# Meta-tag patterns in priority order
META_PATTERNS = [
    r'<meta[^>]+property=["\']article:published_time["\'][^>]+content=["\']([^"\']+)["\']',
    r'<meta[^>]+content=["\']([^"\']+)["\'][^>]+property=["\']article:published_time["\']',
    r'<meta[^>]+name=["\']article:published_time["\'][^>]+content=["\']([^"\']+)["\']',
    r'<meta[^>]+itemprop=["\']datePublished["\'][^>]+content=["\']([^"\']+)["\']',
    r'<meta[^>]+name=["\']pubdate["\'][^>]+content=["\']([^"\']+)["\']',
    r'<meta[^>]+name=["\']publishdate["\'][^>]+content=["\']([^"\']+)["\']',
    r'<meta[^>]+name=["\']date["\'][^>]+content=["\']([^"\']+)["\']',
    r'<meta[^>]+property=["\']og:article:published_time["\'][^>]+content=["\']([^"\']+)["\']',
    # JSON-LD
    r'"datePublished"\s*:\s*"([^"]+)"',
    # <time datetime="..." pubdate>
    r'<time[^>]+datetime=["\']([^"\']+)["\'][^>]*pubdate',
    r'<time[^>]+pubdate[^>]+datetime=["\']([^"\']+)["\']',
]

def fetch(url, timeout=15):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip, identity"})
        with urllib.request.urlopen(req, timeout=timeout) as r:
            raw = r.read()
            if r.headers.get("Content-Encoding") == "gzip":
                raw = gzip.decompress(raw)
            return raw.decode("utf-8", errors="ignore"), r.status, r.geturl()
    except Exception as e:
        return None, f"ERR:{type(e).__name__}:{e}", url

def extract_published(html):
    if not html: return None, None
    head = html[:200_000]  # only look at first 200KB
    for i, pat in enumerate(META_PATTERNS):
        m = re.search(pat, head, re.IGNORECASE)
        if m:
            return m.group(1).strip(), f"pattern_{i}"
    return None, None

def process(url):
    html, status, final_url = fetch(url)
    if html is None:
        return {"url": url, "status": status, "published": None, "via": None, "final_url": final_url}
    ts, via = extract_published(html)
    return {"url": url, "status": status, "published": ts, "via": via, "final_url": final_url}

if __name__ == "__main__":
    urls = [l.strip() for l in sys.stdin if l.strip()]
    out = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for r in ex.map(process, urls):
            out.append(r)
            print(json.dumps(r), flush=True)
    json.dump(out, open("/tmp/fable5/scraped_published.json","w"), indent=2)
