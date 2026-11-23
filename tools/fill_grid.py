"""Grid filler (research tool, not run in CI). Needs: pip install wordfreq english-words.
Usage: python fill_grid.py <pattern_index> <seed> <min_zipf> <seconds>  (reads pats6.json + used6.json, writes fill6c_*.json)
Known limit: web2 + wordfreq still admit names/obscure words; a curated word list is needed before shipping 6x6+ faces."""
import random,sys,time,json
from wordfreq import top_n_list, zipf_frequency as z
from english_words import get_english_words_set
idx,seed,zmin,tl=int(sys.argv[1]),int(sys.argv[2]),float(sys.argv[3]),float(sys.argv[4])
P=json.load(open('pats6.json'))[idx];N=len(P);random.seed(seed)
USED=set(json.load(open('used6.json')))
D={w for w in get_english_words_set(['web2'],lower=False) if w.islower()}
BAD=set('penis anus sex rna dna porn nazi tsar erie agar alas ado ere ahem til donna pedro tate dee ted thy rex tee eyed para dye noel amino roma lisa anna alan ada ago eddie yale tyre scan brad roger chad honda troy lee tom temp ken mac mob nap papa spa'.split())
ws=[w for w in top_n_list('en',70000) if w.isalpha() and w.isascii() and 3<=len(w)<=N and z(w,'en')>=zmin and w in D and w not in BAD and w not in USED]
byl={n:[w for w in ws if len(w)==n] for n in range(3,N+1)}
blk=lambda r,c:r<0 or c<0 or r>=N or c>=N or P[r][c]=='#'
S=[]
for r in range(N):
    for c in range(N):
        if blk(r,c):continue
        for d,(dr,dc) in (('A',(0,1)),('D',(1,0))):
            if blk(r-dr,c-dc):
                s=[];a,b=r,c
                while not blk(a,b):s.append((a,b));a+=dr;b+=dc
                S.append(s)
SETS={n:set(byl[n]) for n in byl};g={};used=set();t0=time.time();out=[]
def cands(s):
    pat=[g.get(x) for x in s]
    return [w for w in byl[len(s)] if w not in used and all(p is None or p==ch for p,ch in zip(pat,w))]
def rec():
    if len(out)>=6 or time.time()-t0>tl:return
    full=[''.join(g[x] for x in s) for s in S if all(x in g for x in s)]
    if any(w not in SETS[len(w)] for w in full) or len(set(full))!=len(full):return
    open_=[s for s in S if any(x not in g for x in s)]
    if not open_:
        words=[''.join(g[x] for x in s) for s in S]
        out.append((round(min(z(w,'en') for w in words),2),words,[''.join(g.get((r,c),'#') for c in range(N)) for r in range(N)]));return
    best=None
    for s in open_:
        c=cands(s)
        if not c:return
        if best is None or len(c)<len(best[1]):best=(s,c)
    s,c=best;random.shuffle(c)
    for w in c[:40]:
        new=[x for x in s if x not in g]
        for x,ch in zip(s,w):g[x]=ch
        used.add(w);rec();used.discard(w)
        for x in new:del g[x]
        if len(out)>=6 or time.time()-t0>tl:return
rec();json.dump(out,open(f'fill6c_{idx}_{seed}.json','w'));print(idx,'found',len(out),[o[:2] for o in out[:1]])
