import csv, datetime as dt, html, re, urllib.request, xml.etree.ElementTree as ET
from pathlib import Path

FEEDS = {
    'Gitcoin Blog': 'https://www.gitcoin.co/blog/rss.xml',
    'Ethereum Foundation': 'https://blog.ethereum.org/feed.xml',
    'Superteam Earn': 'https://earn.superteam.fun/feed',
}
KEYWORDS = {'bounty':4,'airdrop':4,'reward':2,'quest':2,'hackathon':2,'grant':1,'testnet':1,'earn':1}
RED_FLAGS = ('deposit', 'send funds', 'seed phrase', 'private key', 'guaranteed profit')

def clean(s):
    return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]*>', ' ', s or ''))).strip()

def fetch(url):
    req=urllib.request.Request(url,headers={'User-Agent':'OpportunityResearchBot/0.1 (+personal research)'})
    with urllib.request.urlopen(req,timeout=15) as resp:
        return resp.read(2_000_000)

def entries(root):
    for item in root.findall('.//item'):
        yield clean(item.findtext('title')), clean(item.findtext('link')), clean(item.findtext('description'))
    ns={'a':'http://www.w3.org/2005/Atom'}
    for item in root.findall('.//a:entry',ns):
        link=item.find('a:link',ns)
        yield clean(item.findtext('a:title',default='',namespaces=ns)), (link.attrib.get('href','') if link is not None else ''), clean(item.findtext('a:summary',default='',namespaces=ns))

def main():
    rows=[]; errors=[]
    for source,url in FEEDS.items():
        try:
            root=ET.fromstring(fetch(url))
            for title,link,description in entries(root):
                content=(title+' '+description).lower()
                score=sum(weight for word,weight in KEYWORDS.items() if word in content)
                if score:
                    flags=[word for word in RED_FLAGS if word in content]
                    rows.append({'source':source,'title':title,'url':link,'score':score,'flags':', '.join(flags),'note':'Perlu verifikasi manual: kelayakan, biaya, deadline, dan aturan bot'})
        except Exception as e:
            errors.append(f'{source}: {type(e).__name__}: {e}')
    rows.sort(key=lambda r:r['score'],reverse=True)
    Path('output').mkdir(exist_ok=True)
    with open('output/opportunities.csv','w',newline='',encoding='utf-8-sig') as f:
        writer=csv.DictWriter(f,fieldnames=['source','title','url','score','flags','note']);writer.writeheader();writer.writerows(rows)
    with open('output/report.md','w',encoding='utf-8') as f:
        f.write('# Opportunity scanner report\n\nGenerated UTC: '+dt.datetime.now(dt.timezone.utc).isoformat()+'\n\n')
        f.write('**Warning:** Matches are leads, NOT confirmed active, free, eligible, or payable opportunities. Never disclose wallet secrets.\n\n')
        for r in rows[:30]:
            f.write(f"- **{r['title']}** ({r['source']}, score {r['score']}) — {r['url']}"+ (f" — Risk keywords: {r['flags']}" if r['flags'] else '')+'\n')
        if not rows:f.write('No matching entries from reachable feeds.\n')
        if errors:f.write('\n## Feed errors\n'+''.join('- '+e+'\n' for e in errors))
    print(f'Found {len(rows)} candidate entries; {len(errors)} feed errors')

if __name__=='__main__':main()
