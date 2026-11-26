import json,re,sys,collections,datetime as dt
src,out=sys.argv[1],sys.argv[2]
rx=re.compile(r'De "(?P<nome>.*?) \((?P<cnpj>[^)]*)\)", período "(?P<per>[^"]*)"(?:, emailId "(?P<id>[^"]*)")?')
rows=[]
for e in json.load(open(src)):
    m=(e.get('jsonPayload') or {}).get('message') or e.get('textPayload') or ''
    r=rx.search(m)
    if not r: continue
    tsr=e['timestamp'].rstrip('Z'); base,_,frac=tsr.partition('.'); ts=dt.datetime.fromisoformat(base+('.'+(frac+'000000')[:6] if frac else '')+'+00:00')
    rows.append((r['cnpj'],r['per'],ts,r['id'] or ''))
g=collections.defaultdict(list)
for c,p,t,i in rows: g[(c,p)].append((t,i))
JAN=dt.timedelta(minutes=15)
det=[]; stats=collections.Counter()
for (c,p),ev in g.items():
    ev.sort()
    for k,(t,i) in enumerate(ev):
        if k==0: tipo='original'
        else:
            d=t-ev[k-1][0]
            tipo='duplicado_tecnico' if d<=JAN else 'reenvio_posterior'
        det.append((c,p,t,i,k+1,len(ev),tipo,'' if k==0 else round((t-ev[k-1][0]).total_seconds())))
det.sort(key=lambda x:(x[2]))
import csv
with open(f'{out}/envios_holerite_prd.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['data_hora_brt','cnpj','periodo','n_envio_da_folha','total_envios_da_folha','classificacao','segundos_desde_envio_anterior','emailId'])
    for c,p,t,i,n,tot,tipo,s in det:
        w.writerow([(t-dt.timedelta(hours=3)).strftime('%Y-%m-%d %H:%M:%S'),c,p,n,tot,tipo,s,i])
# resumo
mes=collections.defaultdict(collections.Counter)
for c,p,t,i,n,tot,tipo,s in det:
    b=(t-dt.timedelta(hours=3))
    mes[b.strftime('%Y-%m')][tipo]+=1
    if n==1: mes[b.strftime('%Y-%m')]['folhas']+=1
    if n==2 and tipo=='duplicado_tecnico': mes[b.strftime('%Y-%m')]['folhas_com_dup']+=1
# folhas com dup tecnico (any)
fd=collections.Counter(); folhas=collections.Counter()
for (c,p),ev in g.items():
    m=(ev[0][0]-dt.timedelta(hours=3)).strftime('%Y-%m'); folhas[m]+=1
    if any((ev[k][0]-ev[k-1][0])<=JAN for k in range(1,len(ev))): fd[m]+=1
print('total envios',len(det),'folhas',len(g))
for m in sorted(mes): print(m, dict(mes[m]), 'folhas',folhas[m],'folhas_com_dup_tecnico',fd[m])
gaps=sorted(x[7] for x in det if x[6]=='duplicado_tecnico'); print('gaps dup (s): min/med/max',gaps[0] if gaps else None, gaps[len(gaps)//2] if gaps else None, gaps[-1] if gaps else None)
rg=sorted(x[7] for x in det if x[6]=='reenvio_posterior'); print('reenvio posterior gaps h:',[round(x/3600,1) for x in rg[:10]], '...', len(rg))
# semanal
wk=collections.defaultdict(collections.Counter)
for c,p,t,i,n,tot,tipo,s in det:
    b=(t-dt.timedelta(hours=3)); wk[(b-dt.timedelta(days=b.weekday())).strftime('%Y-%m-%d')][tipo]+=1
for w_ in sorted(wk): print('sem',w_,dict(wk[w_]))
json.dump({'mes':{m:dict(mes[m]) for m in mes},'folhas':folhas,'folhas_dup':fd,'semana':{w_:dict(wk[w_]) for w_ in wk}},open(f'{out}/resumo.json','w'),default=str)
