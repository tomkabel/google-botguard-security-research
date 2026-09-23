import urllib.request, urllib.parse, json, xml.etree.ElementTree as ET, time, sys
UA={'User-Agent':'sok-lit-search/1.0 (mailto:research@example.org)'}
def get(u):
    return urllib.request.urlopen(urllib.request.Request(u,headers=UA),timeout=60).read()
out=[]
A='(abs:"bot detection" OR abs:"bot mitigation" OR abs:"anti-automation" OR abs:"browser fingerprinting" OR abs:CAPTCHA) AND (abs:attestation OR abs:cost OR abs:economics OR abs:architecture OR abs:"CAPTCHA solving" OR abs:"vision-language model" OR abs:VLM OR abs:"web agent" OR abs:"computer-use agent" OR abs:"GUI agent")'
u='http://export.arxiv.org/api/query?'+urllib.parse.urlencode({'search_query':A,'start':0,'max_results':500})
r=ET.fromstring(get(u)); ns={'a':'http://www.w3.org/2005/Atom'}
tot=r.find('{http://a9.com/-/spec/opensearch/1.1/}totalResults').text
for e in r.findall('a:entry',ns):
    out.append(dict(source='arXiv',id='arXiv:'+e.find('a:id',ns).text.split('/abs/')[-1],title=' '.join(e.find('a:title',ns).text.split()),year=e.find('a:published',ns).text[:4],query=A))
print('arxiv',tot,len(out))
S='("bot mitigation" | "bot detection" | "anti-automation" | "browser fingerprinting" | CAPTCHA) + (attestation | cost | economics | architecture | "CAPTCHA solving" | "vision-language model" | VLM | "web agent" | "computer-use agent" | "GUI agent")'
n0=len(out); tok=None; stot=None
while True:
    p={'query':S,'fields':'title,year,externalIds,venue'}
    if tok: p['token']=tok
    for i in range(5):
        try: j=json.loads(get('https://api.semanticscholar.org/graph/v1/paper/search/bulk?'+urllib.parse.urlencode(p))); break
        except Exception as ex: print('s2 retry',ex,file=sys.stderr); time.sleep(5*(i+1))
    else: break
    stot=j.get('total')
    for d in j.get('data',[]):
        ids=d.get('externalIds') or {}
        pid=('doi:'+ids['DOI']) if ids.get('DOI') else ('arXiv:'+ids['ArXiv']) if ids.get('ArXiv') else 's2:'+d['paperId']
        out.append(dict(source='SemanticScholar',id=pid,title=d['title'],year=str(d.get('year') or ''),query=S))
    tok=j.get('token')
    if not tok or len(out)-n0>=3000: break
    time.sleep(1.5)
print('s2',stot,len(out)-n0)


# ---- dedupe, match against paper references, write docs/corpus.csv ----
import re, csv, os
RUN_DATE = '2026-09-23'
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
# Coding only for records matched to an already-cited reference; everything else is "not screened".
CODE = {'30': ('attack (CAPTCHA/VLM)', 'VLM', 'benchmark/measurement'),
        '64': ('attack (CAPTCHA/VLM)', 'VLM', 'benchmark'),
        '76': ('attack (Type III/CAPTCHA)', 'pre-VLM', 'black-box study'),
        '29': ('attack (CAPTCHA/VLM)', 'VLM', 'measurement'),
        '19': ('attack (Type III/CAPTCHA)', 'pre-VLM', 'attack evaluation'),
        '17': ('background (economics)', 'pre-VLM', 'market measurement'),
        '63': ('background (economics)', 'pre-VLM', 'market measurement')}
norm = lambda t: re.sub(r'\W', '', (t or '').lower())[:40]
refs = open(os.path.join(ROOT, 'paper.md')).read().split('## References')[1]
reft = {norm(m.group(2)): m.group(1) for m in re.finditer(r'\*\*\[(\d+)\]\*\*.*?"(.+?)"', refs)}
rows = {}
for o in out:
    k = norm(o['title'])
    if k in rows:
        if o['source'] not in rows[k]['source']: rows[k]['source'] += '+' + o['source']
        continue
    rows[k] = dict(o)
for k, r in rows.items():
    n = reft.get(k)
    r.update(run_date=RUN_DATE, stage='identified', decision='not screened', reason='', type='', era='', evidence_kind='')
    if n:
        r.update(stage='title/abstract', decision='include (already cited as [%s])' % n, reason='matches existing reference')
        r['type'], r['era'], r['evidence_kind'] = CODE.get(n, ('', '', ''))
cols = ['id', 'title', 'year', 'source', 'query', 'run_date', 'stage', 'decision', 'reason', 'type', 'era', 'evidence_kind']
with open(os.path.join(ROOT, 'docs', 'corpus.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, cols, extrasaction='ignore'); w.writeheader(); w.writerows(rows.values())
matched = sum(r['decision'] != 'not screened' for r in rows.values())
assert len(rows) <= len(out) and matched <= len(reft)
# Reference numbers above follow paper.md; rerun after any renumbering and fail loudly if coding drifted.
assert all(r['type'] for r in rows.values() if r['decision'] != 'not screened'), 'CODE keys out of sync with paper.md numbering'
print('records', len(out), 'unique', len(rows), 'matched', matched)
