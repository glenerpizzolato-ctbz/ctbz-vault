import csv,sys,collections,datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font,PatternFill,Alignment
from openpyxl.utils import get_column_letter
import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
D=sys.argv[1]
rows=list(csv.DictReader(open(f'{D}/envios_holerite_prd.csv')))
DEPLOY='2026-11-25 16:36:31'
LBL={'original':'1º envio da folha','duplicado_tecnico':'Duplicado técnico (≤15 min)','reenvio_posterior':'Reenvio posterior (>15 min)'}
for r in rows: r['apos_p1']='sim' if r['data_hora_brt']>=DEPLOY else 'não'
folhas=collections.defaultdict(list)
for r in rows: folhas[(r['cnpj'],r['periodo'])].append(r)
def agg(keyf):
    a=collections.defaultdict(collections.Counter)
    for r in rows: a[keyf(r)][r['classificacao']]+=1
    fd=collections.defaultdict(set); fa=collections.defaultdict(set)
    for (c,p),ev in folhas.items():
        k=keyf(ev[0]); fa[k].add((c,p))
        if any(e['classificacao']=='duplicado_tecnico' for e in ev): fd[k].add((c,p))
    return a,fa,fd
mes=lambda r:r['data_hora_brt'][:7]
def semana(r):
    d=dt.date.fromisoformat(r['data_hora_brt'][:10]); return (d-dt.timedelta(days=d.weekday())).isoformat()
wb=Workbook(); H=Font(bold=True,color='FFFFFF'); F=PatternFill('solid',fgColor='1B64BE')
def sheet(ws,head,data,widths=None):
    ws.append(head)
    for c in ws[1]: c.font=H; c.fill=F; c.alignment=Alignment(wrap_text=True,vertical='center')
    for d in data: ws.append(d)
    ws.freeze_panes='A2'; ws.auto_filter.ref=ws.dimensions
    for i,h in enumerate(head,1): ws.column_dimensions[get_column_letter(i)].width=(widths or {}).get(i,max(14,len(h)+2))
out={}
for nome,kf in (('Resumo por mês',mes),('Resumo por semana',semana)):
    a,fa,fd=agg(kf); data=[]
    for k in sorted(a):
        tot=sum(a[k].values()); dup=a[k]['duplicado_tecnico']
        data.append([k,len(fa[k]),tot,dup,a[k]['reenvio_posterior'],len(fd[k]),round(100*len(fd[k])/len(fa[k]),1) if fa[k] else 0,round(100*dup/tot,1)])
    out[nome]=data
    ws=wb.active if nome=='Resumo por mês' else wb.create_sheet(nome); ws.title=nome
    sheet(ws,['Mês' if 'mês' in nome else 'Semana (seg)','Folhas (empresa+período)','E-mails enviados','Duplicados técnicos (≤15 min)','Reenvios posteriores (>15 min)','Folhas com duplicado técnico','% folhas com duplicado','% e-mails que são duplicados'],data)
ws=wb.create_sheet('Folhas com duplicado')
fl=[]
for (c,p),ev in folhas.items():
    nd=sum(e['classificacao']=='duplicado_tecnico' for e in ev)
    if nd: fl.append([ev[0]['data_hora_brt'],c,p,len(ev),nd,sum(e['classificacao']=='reenvio_posterior' for e in ev),', '.join(e['data_hora_brt'][11:] for e in ev[:8])])
fl.sort()
sheet(ws,['1º envio (BRT)','CNPJ','Período','Total de e-mails da folha','Duplicados técnicos','Reenvios posteriores','Horários dos envios (BRT)'],fl,{7:60})
ws=wb.create_sheet('Todos os envios')
sheet(ws,['Data/hora (BRT)','CNPJ','Período','Nº do envio da folha','Total de envios da folha','Classificação','Segundos desde o envio anterior','emailId (email-service)','Após a P1 (sub nova)'],
      [[r['data_hora_brt'],r['cnpj'],r['periodo'],int(r['n_envio_da_folha']),int(r['total_envios_da_folha']),LBL[r['classificacao']],int(r['segundos_desde_envio_anterior']) if r['segundos_desde_envio_anterior'] else None,r['emailId'] or None,r['apos_p1']] for r in rows])
ws=wb.create_sheet('Como ler')
for l in ['Fonte: logs "Holerites enviados por email" da function-email-holerites em contabilizei-experts-prd (Cloud Logging, retenção de 30 dias: 26/10 a 25/11/2026). Cada linha é um e-mail entregue ao Mandrill (até 24/11) ou ao email-service (desde 24/11).',
          'Folha = empresa (CNPJ) + período. 1º envio = primeiro e-mail daquela folha na janela.',
          'Duplicado técnico = novo e-mail da mesma folha até 15 min depois do anterior: reentrega do Pub/Sub (ack de 10 s da subscription do Eventarc), sem ação de ninguém. Mediana de 14 s entre os envios.',
          'Reenvio posterior = novo e-mail da mesma folha mais de 15 min depois: em geral nova liberação da folha pelo admin (pode ser legítima), não entra na conta de duplicados.',
          'Após a P1 = depois do deploy da subscription nova em prd (25/11/2026 16:36 BRT). Até remover o trigger do Eventarc, as duas subscriptions entregam e o duplicado continua.',
          'Sem nome de pessoa; só CNPJ e período.']:
    ws.append([l])
ws.column_dimensions['A'].width=160
wb.save(f'{D}/holerites-duplicados-prd-PRD-178821.xlsx')
# gráfico semanal
data=out['Resumo por semana']
lab=[dt.date.fromisoformat(d[0]).strftime('%d/%m') for d in data]
orig=[d[1] for d in data]; dup=[d[3] for d in data]; ree=[d[4] for d in data]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10})
fig,ax=plt.subplots(figsize=(8,4.2),dpi=150)
x=range(len(lab)); w=0.62
ax.bar(x,orig,w,color='#257de0',label='1º envio da folha',edgecolor='white',linewidth=1.5)
ax.bar(x,dup,w,bottom=orig,color='#f47230',label='Duplicado técnico (≤15 min)',edgecolor='white',linewidth=1.5)
ax.bar(x,ree,w,bottom=[a+b for a,b in zip(orig,dup)],color='#00b894',label='Reenvio posterior (>15 min)',edgecolor='white',linewidth=1.5)
for i,d in enumerate(data):
    ax.text(i,orig[i]+dup[i]/2,f'{dup[i]}',ha='center',va='center',fontsize=9,color='#111111',fontweight='bold')
    ax.text(i,orig[i]+dup[i]+ree[i]+8,f'{d[6]}% das folhas\ncom duplicado',ha='center',va='bottom',fontsize=8,color='#444444')
ax.set_xticks(list(x)); ax.set_xticklabels([f'sem. {l}' for l in lab])
ax.set_ylabel('E-mails de holerite enviados',color='#444444')
for s in ('top','right'): ax.spines[s].set_visible(False)
for s in ('left','bottom'): ax.spines[s].set_color('#bbbbbb')
ax.yaxis.grid(True,color='#eeeeee'); ax.set_axisbelow(True)
ax.set_ylim(0,max(a+b+c for a,b,c in zip(orig,dup,ree))*1.22)
ax.set_title('Holerites por e-mail em prd, por semana (26/10 a 25/11/2026)',loc='left',fontsize=11,color='#111111')
ax.legend(frameon=False,loc='upper right',fontsize=8.5)
fig.tight_layout(); fig.savefig(f'{D}/holerites-duplicados-semana.png')
for k,v in out.items():
    print(k); [print(' ',r) for r in v]
print('folhas com dup',len(fl))
