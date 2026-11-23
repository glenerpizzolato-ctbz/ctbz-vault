import html, sys

TW, TH, ER, GD = 172, 58, 17, 24
HEAD = 64

def esc(s): return html.escape(s, quote=True)

def build(lanes, nodes, edges, height, sid):
    # lanes: list of (key, title, sub, width, cls)
    x = 0; L = {}
    for k, t, s, w, c in lanes:
        L[k] = (x, w, t, s, c); x += w
    W = x
    N = {}
    for n in nodes:
        k, typ, lane, y = n[:4]; label = n[4] if len(n) > 4 else ''
        opt = n[5] if len(n) > 5 else {}
        lx, lw = L[lane][0], L[lane][1]
        cx = lx + lw / 2 + opt.get('dx', 0)
        N[k] = dict(k=k, t=typ, lane=lane, x=cx, y=y, label=label, **opt)
    def half(n, axis):
        if n['t'] == 'task': return (TW/2 if axis == 'x' else TH/2)
        if n['t'] == 'gw': return GD
        return ER
    out = [f'<svg class="bpmn" viewBox="0 0 {W} {height}" role="img" aria-labelledby="{sid}-t"><title id="{sid}-t">{esc(sid)}</title>']
    out.append('<defs>'
      f'<marker id="{sid}-a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ah"/></marker>'
      f'<marker id="{sid}-m" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" class="ahm"/></marker>'
      f'<marker id="{sid}-o" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="7" markerHeight="7"><circle cx="5" cy="5" r="3.6" class="ahm-o"/></marker>'
      '</defs>')
    # lanes
    for k, (lx, lw, t, s, c) in L.items():
        out.append(f'<rect x="{lx}" y="0" width="{lw}" height="{height}" class="lane {c}"/>')
        out.append(f'<rect x="{lx}" y="0" width="{lw}" height="{HEAD}" class="lane-head {c}"/>')
        out.append(f'<text x="{lx+lw/2}" y="27" class="lane-t">{esc(t)}</text>')
        out.append(f'<text x="{lx+lw/2}" y="46" class="lane-s">{esc(s)}</text>')
        if lx > 0: out.append(f'<line x1="{lx}" y1="0" x2="{lx}" y2="{height}" class="lane-sep"/>')
    out.append(f'<rect x="0.5" y="0.5" width="{W-1}" height="{height-1}" class="pool"/>')
    labels = []
    # edges
    for e in edges:
        a, b, kind = N[e[0]], N[e[1]], e[2]
        lab = e[3] if len(e) > 3 else ''
        o = e[4] if len(e) > 4 else {}
        dy = o.get('dy', 0)
        cls = 'seq' if kind == 's' else 'msg'
        mk = f'marker-end="url(#{sid}-{"a" if kind=="s" else "m"})"' + (f' marker-start="url(#{sid}-o)"' if kind == 'm' else '')
        if abs(a['y'] - b['y']) < 1:
            d = 1 if b['x'] > a['x'] else -1
            x1 = a['x'] + d*half(a,'x'); x2 = b['x'] - d*half(b,'x'); y = a['y'] + dy
            pts = [(x1, y), (x2, y)]
            lp = ((x1+x2)/2, (y + 15) if dy > 0 else (y - 7), 'middle')
        elif abs(a['x'] - b['x']) < 1:
            y1 = a['y'] + half(a,'y'); y2 = b['y'] - half(b,'y')
            pts = [(a['x'], y1), (a['x'], y2)]
            lp = (a['x'] + 8, (y1+y2)/2 + 4, 'start')
        else:
            y1 = a['y'] + half(a,'y'); y2 = b['y'] - half(b,'y'); my = o.get('my', (y1+y2)/2)
            pts = [(a['x'], y1), (a['x'], my), (b['x'], my), (b['x'], y2)]
            lp = ((a['x']+b['x'])/2, my - 7, 'middle')
        path = 'M' + ' L'.join(f'{px:.1f},{py:.1f}' for px, py in pts)
        out.append(f'<path d="{path}" class="{cls}" {mk}/>')
        if lab:
            for i, line in enumerate(lab.split('\n')):
                labels.append(f'<text x="{lp[0]:.1f}" y="{lp[1] + i*13 - (len(lab.split(chr(10)))-1)*13*(0 if lp[2]=="start" else 1):.1f}" style="text-anchor:{lp[2]}" class="elab {cls}-l">{esc(line)}</text>')
    # nodes
    for n in N.values():
        x, y = n['x'], n['y']; lines = n['label'].split('\n') if n['label'] else []
        st = n.get('st', '')
        if n['t'] == 'task':
            out.append(f'<rect x="{x-TW/2}" y="{y-TH/2}" width="{TW}" height="{TH}" rx="9" class="task {st}"/>')
            fs = 12.5; base = y - (len(lines)-1)*fs*1.2/2 + 4 - (5 if n.get('loop') else 0)
            for i, l in enumerate(lines):
                out.append(f'<text x="{x}" y="{base + i*fs*1.2:.1f}" class="tt">{esc(l)}</text>')
            if n.get('loop'):
                out.append(f'<path d="M{x-5},{y+TH/2-8} a5,5 0 1,1 5,4" class="loop"/><path d="M{x+3},{y+TH/2-7} l2,3 l-4,1" class="loop"/>')
            if st == 'new':
                out.append(f'<rect x="{x+TW/2-34}" y="{y-TH/2-9}" width="34" height="16" rx="8" class="pill"/><text x="{x+TW/2-17}" y="{y-TH/2+3}" class="pill-t">novo</text>')
        elif n['t'] in ('start', 'end', 'msg'):
            c = {'start': 'ev-start', 'end': 'ev-end', 'msg': 'ev-msg'}[n['t']]
            out.append(f'<circle cx="{x}" cy="{y}" r="{ER}" class="{c} {st}"/>')
            if n['t'] == 'msg':
                out.append(f'<circle cx="{x}" cy="{y}" r="{ER-4}" class="ev-msg-in"/>')
                out.append(f'<rect x="{x-8}" y="{y-5.5}" width="16" height="11" class="env"/><path d="M{x-8},{y-5.5} L{x},{y+1} L{x+8},{y-5.5}" class="env"/>')
            side = n.get('lside', 'below')
            for i, l in enumerate(lines):
                if side == 'below':
                    out.append(f'<text x="{x}" y="{y+ER+15+i*13}" class="evl">{esc(l)}</text>')
                elif side == 'above':
                    out.append(f'<text x="{x}" y="{y-ER-8-(len(lines)-1-i)*13}" class="evl">{esc(l)}</text>')
                elif side == 'right':
                    out.append(f'<text x="{x+ER+7}" y="{y+4+(i-(len(lines)-1)/2)*13:.1f}" class="evl" style="text-anchor:start">{esc(l)}</text>')
                else:
                    out.append(f'<text x="{x-ER-7}" y="{y+4+(i-(len(lines)-1)/2)*13:.1f}" class="evl" style="text-anchor:end">{esc(l)}</text>')
        elif n['t'] == 'gw':
            out.append(f'<path d="M{x},{y-GD} L{x+GD},{y} L{x},{y+GD} L{x-GD},{y} z" class="gw"/>')
            out.append(f'<path d="M{x-8},{y-8} L{x+8},{y+8} M{x+8},{y-8} L{x-8},{y+8}" class="gwx"/>')
            for i, l in enumerate(lines):
                out.append(f'<text x="{x-GD-8}" y="{y+4+(i-(len(lines)-1)/2)*13:.1f}" class="evl" style="text-anchor:end">{esc(l)}</text>')
    out += labels
    out.append('</svg>')
    return '\n'.join(out)

LANE = 186
hoje = build(
    [('adm', 'Admin', 'contabilizei-front-admin', LANE, ''),
     ('fop', 'Folha', 'plataforma-fopag-worker', 230, ''),
     ('ps', 'Pub/Sub', 'contabilizei-experts-prd', LANE, 'bus'),
     ('fn', 'Function de envio', 'function-email-holerites', 200, 'gone'),
     ('pdf', 'Gerador de PDF', 'function-html-to-pdf', 230, ''),
     ('mx', 'Mandrill', 'Mailchimp Transactional', LANE, 'ext gone')],
    [('s', 'start', 'adm', 108, 'Folha\ncalculada', {'lside': 'left'}),
     ('t1', 'task', 'adm', 196, 'Clica “Liberar Folha\npara o cliente”'),
     ('t2', 'task', 'fop', 290, 'Recebe a liberação\nda folha'),
     ('g1', 'gw', 'fop', 388, 'Plano Expert e\ncolaboradores\nativos?', {'dx': 22}),
     ('eno', 'end', 'fop', 388, 'Não envia', {'dx': 88, 'lside': 'below'}),
     ('t3', 'task', 'fop', 490, 'Publica os dados\nda folha (sem PDF)', {'dx': 22}),
     ('eok', 'end', 'adm', 490, 'Folha liberada\n(200 OK)'),
     ('m1', 'msg', 'ps', 490, 'functions.\nemail-holerites', {'lside': 'above'}),
     ('t4', 'task', 'fn', 596, 'Recebe a folha'),
     ('t5', 'task', 'fn', 690, 'Monta o HTML de\ncada holerite'),
     ('t6', 'task', 'fn', 790, 'Pede o PDF de\ncada colaborador', {'loop': True}),
     ('p1', 'task', 'pdf', 790, 'Converte\nHTML → PDF', {'dx': 25}),
     ('t7', 'task', 'fn', 890, 'Envia o e-mail\ncom os PDFs'),
     ('x1', 'task', 'mx', 890, 'Entrega ao\nresponsável'),
     ('xe', 'end', 'mx', 986, 'E-mail na caixa'),
     ('t8', 'task', 'fn', 986, 'Registra o resultado\nno log'),
     ('fe', 'end', 'fn', 1076, 'Fim')],
    [('s', 't1', 's'), ('t1', 't2', 'm', 'REST GET'), ('t2', 'g1', 's', '', {}),
     ('g1', 'eno', 's', 'Não'), ('g1', 't3', 's', 'Sim'),
     ('t3', 'eok', 'm', 'resposta'), ('t3', 'm1', 'm', 'publica'),
     ('m1', 't4', 'm', 'push HTTP'), ('t4', 't5', 's'), ('t5', 't6', 's'),
     ('t6', 'p1', 'm', 'HTML', {'dy': -10}), ('p1', 't6', 'm', 'PDF', {'dy': 10}),
     ('t6', 't7', 's'), ('t7', 'x1', 'm', 'API Mandrill'), ('x1', 'xe', 's'), ('t7', 't8', 's'), ('t8', 'fe', 's')],
    1130, 'Fluxo de hoje')

prop = build(
    [('adm', 'Admin', 'contabilizei-front-admin', 176, ''),
     ('fop', 'Folha', 'plataforma-fopag-worker', 220, ''),
     ('ps', 'Pub/Sub', 'contabilizei-experts-prd', 170, 'bus'),
     ('fn', 'Function de envio', 'function-email-holerites', 210, 'chg'),
     ('pdf', 'Gerador de PDF', 'function-html-to-pdf', 220, ''),
     ('es', 'email-service', 'atendimento-canais-prd', 240, 'new'),
     ('hs', 'HubSpot', 'API SMTP transacional', 190, 'ext new')],
    [('s', 'start', 'adm', 108, 'Folha\ncalculada', {'lside': 'left'}),
     ('t1', 'task', 'adm', 196, 'Clica “Liberar Folha\npara o cliente”'),
     ('t2', 'task', 'fop', 290, 'Recebe a liberação\nda folha'),
     ('g1', 'gw', 'fop', 388, 'Plano Expert e\ncolaboradores\nativos?', {'dx': 22}),
     ('eno', 'end', 'fop', 388, 'Não envia', {'dx': 86}),
     ('t3', 'task', 'fop', 490, 'Publica os dados\nda folha (sem PDF)', {'dx': 22}),
     ('eok', 'end', 'adm', 490, 'Folha liberada\n(200 OK)'),
     ('m1', 'msg', 'ps', 490, 'functions.\nemail-holerites', {'lside': 'above'}),
     ('t4', 'task', 'fn', 596, 'Recebe a folha'),
     ('t5', 'task', 'fn', 690, 'Monta o HTML de\ncada holerite'),
     ('t6', 'task', 'fn', 790, 'Pede o PDF de\ncada colaborador', {'loop': True}),
     ('p1', 'task', 'pdf', 790, 'Converte\nHTML → PDF', {'dx': 20}),
     ('n1', 'task', 'fn', 890, 'Sobe cada PDF\nno email-service', {'st': 'new', 'loop': True}),
     ('f1', 'task', 'es', 890, 'Guarda o PDF\ne devolve o fileId'),
     ('n2', 'task', 'fn', 990, 'Pede o envio do e-mail\n(template, NOME,\nPERIODO, fileIds)', {'st': 'new'}),
     ('m2', 'msg', 'es', 990, 'email-service.p2p.\nsend-email', {'lside': 'above'}),
     ('t8', 'task', 'fn', 1090, 'Registra o resultado\nno log'),
     ('fe', 'end', 'fn', 1180, 'Fim'),
     ('v1', 'task', 'es', 1090, 'Valida template\ne variáveis'),
     ('g2', 'gw', 'es', 1184, 'Válido?'),
     ('ebad', 'end', 'es', 1184, 'Erro no\ncallback', {'dx': 86}),
     ('v2', 'task', 'es', 1280, 'Grava o envio em\nemail_replications'),
     ('v3', 'task', 'es', 1376, 'Baixa os PDFs\ne monta o e-mail'),
     ('h1', 'task', 'hs', 1376, 'Entrega ao\nresponsável'),
     ('he', 'end', 'hs', 1472, 'E-mail na caixa'),
     ('v4', 'task', 'es', 1472, 'Publica o status\n(SENT / falha)'),
     ('ve', 'end', 'es', 1562, 'Fim')],
    [('s', 't1', 's'), ('t1', 't2', 'm', 'REST GET'), ('t2', 'g1', 's'),
     ('g1', 'eno', 's', 'Não'), ('g1', 't3', 's', 'Sim'),
     ('t3', 'eok', 'm', 'resposta'), ('t3', 'm1', 'm', 'publica'),
     ('m1', 't4', 'm', 'push HTTP'), ('t4', 't5', 's'), ('t5', 't6', 's'),
     ('t6', 'p1', 'm', 'HTML', {'dy': -10}), ('p1', 't6', 'm', 'PDF', {'dy': 10}),
     ('t6', 'n1', 's'),
     ('n1', 'f1', 'm', 'REST (base64)', {'dy': -10}), ('f1', 'n1', 'm', 'fileId', {'dy': 10}),
     ('n1', 'n2', 's'), ('n2', 'm2', 'm', 'publica (Pub/Sub)'), ('n2', 't8', 's'), ('t8', 'fe', 's'),
     ('m2', 'v1', 's'), ('v1', 'g2', 's'), ('g2', 'ebad', 's', 'Não'), ('g2', 'v2', 's', 'Sim'),
     ('v2', 'v3', 's'), ('v3', 'h1', 'm', 'SMTP'), ('h1', 'he', 's'), ('v3', 'v4', 's'), ('v4', 've', 's')],
    1616, 'Fluxo proposto')

tpl = open(sys.argv[1]).read()
open(sys.argv[2], 'w').write(tpl.replace('%%HOJE%%', hoje).replace('%%PROP%%', prop))
