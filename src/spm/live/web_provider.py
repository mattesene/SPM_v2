"""HTTP provider adapters for public fixture endpoints."""
from __future__ import annotations
import json,re
from datetime import date,datetime,timedelta,timezone
from html import unescape
from html.parser import HTMLParser
from urllib.error import HTTPError,URLError
from urllib.request import Request,urlopen
from spm.live.normalization import RawFixture

class FixtureProviderError(RuntimeError): pass
class JSONFixtureProvider:
 def __init__(self,url,*,timeout=20): self.url,self.timeout=url,timeout
 def fetch_fixtures(self,from_date):
  try:
   with urlopen(Request(self.url,headers={"User-Agent":"Mozilla/5.0","Accept":"application/json"}),timeout=self.timeout) as r:p=json.load(r)
  except HTTPError as e: raise FixtureProviderError(f"HTTP {e.code} from fixture source") from e
  except URLError as e: raise FixtureProviderError(f"fixture source unavailable: {e.reason}") from e
  rows=p.get("fixtures",p) if isinstance(p,dict) else p
  if not isinstance(rows,list): raise FixtureProviderError("fixture source returned an invalid payload")
  try:return [RawFixture(x["home"],x["away"],date.fromisoformat(x["kickoff"])) for x in rows if date.fromisoformat(x["kickoff"])>=from_date]
  except (KeyError,TypeError,ValueError) as e: raise FixtureProviderError("fixture source contains an invalid row") from e

class SofaScoreFixtureProvider:
 BASE_URL="https://api.sofascore.com/api/v1/sport/football/scheduled-events/{day}"
 ALLOWED_TOURNAMENTS={"Premier League","Championship","Bundesliga","Serie A","LaLiga"}
 def __init__(self,*,days=7,timeout=20): self.days=max(1,days);self.timeout=timeout
 def fetch_fixtures(self,from_date):
  out=[];seen=set();h={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36","Accept":"application/json, text/plain, */*","Referer":"https://www.sofascore.com/","Origin":"https://www.sofascore.com"}
  for i in range(self.days):
   d=from_date+timedelta(days=i)
   try:
    with urlopen(Request(self.BASE_URL.format(day=d.isoformat()),headers=h),timeout=self.timeout) as r:p=json.load(r)
   except HTTPError as e: raise FixtureProviderError(f"SofaScore HTTP {e.code} for {d}") from e
   except URLError as e: raise FixtureProviderError(f"SofaScore unavailable for {d}: {e.reason}") from e
   for e in p.get("events",[]):
    if (e.get("status") or {}).get("type") not in {None,"notstarted"}:continue
    t=((e.get("tournament") or {}).get("name") or "").strip();u=((e.get("tournament") or {}).get("uniqueTournament") or {}).get("name","")
    if t not in self.ALLOWED_TOURNAMENTS and u not in self.ALLOWED_TOURNAMENTS:continue
    a=((e.get("homeTeam") or {}).get("name") or "").strip();b=((e.get("awayTeam") or {}).get("name") or "").strip()
    if not a or not b:continue
    ts=e.get("startTimestamp");k=datetime.fromtimestamp(int(ts),tz=timezone.utc).date() if ts else d;key=(k,a,b)
    if k>=from_date and key not in seen:seen.add(key);out.append(RawFixture(a,b,k))
  return out

class _VisibleTextParser(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.parts=[];self.skip=0
 def handle_starttag(self,t,a):
  if t.lower() in {"script","style","noscript"}:self.skip+=1
 def handle_endtag(self,t):
  if t.lower() in {"script","style","noscript"} and self.skip:self.skip-=1
 def handle_data(self,d):
  if not self.skip:
   x=" ".join(unescape(d).split())
   if x:self.parts.append(x)
 def text(self):return " ".join(self.parts)

def _parse_diretta_text(text,from_date,latest):
 pat=re.compile(r"(\d{1,2})\s*/\s*(\d{1,2})\s+([A-Za-zÀ-ÖØ-öø-ÿ0-9.'’&()\- ]{2,80}?)\s+[-–—]\s+([A-Za-zÀ-ÖØ-öø-ÿ0-9.'’&()\- ]{2,80}?)(?=\s*,\s*\d{1,2}\s*/\s*\d{1,2}|\s*$)")
 out=[]
 for m in pat.finditer(text):
  try:k=date(from_date.year,int(m.group(2)),int(m.group(1)))
  except ValueError:continue
  if from_date<=k<=latest:
   a=" ".join(m.group(3).split()).strip(" ,");b=" ".join(m.group(4).split()).strip(" ,")
   if a and b and a.lower()!=b.lower():out.append(RawFixture(a,b,k))
 return out

class DirettaFixtureProvider:
 CALENDAR_URLS=("https://www.diretta.it/serie-a/La/news/calendario/","https://www.diretta.it/calcio/inghilterra/premier-league/calendario/","https://www.diretta.it/calcio/inghilterra/championship/calendario/","https://www.diretta.it/calcio/germania/bundesliga/calendario/","https://www.diretta.it/calcio/spagna/laliga/calendario/")
 def __init__(self,*,days=7,timeout=20):self.days=max(1,days);self.timeout=timeout
 def fetch_fixtures(self,from_date):
  h={"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/131.0 Safari/537.36","Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8","Accept-Language":"it-IT,it;q=0.9,en;q=0.8"};out=[];seen=set();latest=from_date+timedelta(days=self.days-1)
  for url in self.CALENDAR_URLS:
   try:
    with urlopen(Request(url,headers=h),timeout=self.timeout) as r:status=getattr(r,"status",200);ct=r.headers.get("Content-Type","");html=r.read().decode("utf-8",errors="replace")
   except HTTPError as e:raise FixtureProviderError(f"Diretta.it HTTP {e.code}") from e
   except URLError as e:raise FixtureProviderError(f"Diretta.it unavailable: {e.reason}") from e
   textp=_VisibleTextParser();textp.feed(html);text=textp.text();n=len(re.findall(r"\b\d{1,2}\s*/\s*\d{1,2}\b",text));print(f"Diretta.it: status={status}, content_type={ct}, bytes={len(html)}, visible_chars={len(text)}, calendar_patterns={n}")
   for f in _parse_diretta_text(text,from_date,latest):
    key=(f.kickoff,f.home,f.away)
    if key not in seen:seen.add(key);out.append(f)
  if not out:raise FixtureProviderError("Diretta.it returned no usable upcoming fixtures")
  return out

class FallbackFixtureProvider:
 def __init__(self,primary,fallback):self.primary,self.fallback=primary,fallback
 def fetch_fixtures(self,from_date):
  try:
   r=self.primary.fetch_fixtures(from_date)
   if r:return r
  except FixtureProviderError as e:print(f"WARNING: primary Live provider failed: {e}")
  try:
   r=self.fallback.fetch_fixtures(from_date)
   if r:print(f"Live fixture fallback: {len(r)} fixtures from Diretta.it");return r
  except FixtureProviderError as e:raise FixtureProviderError(f"primary and fallback providers failed: {e}") from e
  raise FixtureProviderError("primary and fallback providers returned no fixtures")
