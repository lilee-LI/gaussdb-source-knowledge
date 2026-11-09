"""Physical C++ coverage items inside semantic work packages, never task-per-function.

Intervals are conservative frozen-text regions, not compiler or understanding claims.
Every region needs its own evidence-backed explanation and published knowledge.
"""
import json
from pathlib import PurePosixPath
import re

from .store import canonical,digest,identity,require

CPP={'.cpp','.cc','.cxx','.c++'}
FIELDS=('behavior','conditions','state','consumers','cleanup','test_basis')
SCHEMA='''
CREATE TABLE IF NOT EXISTS implementation_items(program TEXT NOT NULL,id TEXT NOT NULL,asset TEXT NOT NULL,module TEXT,start INTEGER,end INTEGER,data TEXT NOT NULL,PRIMARY KEY(program,id));
CREATE INDEX IF NOT EXISTS implementation_asset ON implementation_items(program,asset,start);
CREATE INDEX IF NOT EXISTS implementation_module ON implementation_items(program,module);
CREATE TABLE IF NOT EXISTS implementation_dispositions(program TEXT NOT NULL,item TEXT NOT NULL,report TEXT NOT NULL,data TEXT NOT NULL,PRIMARY KEY(program,item));
'''


def enabled(store):
    from .curriculum import current
    return bool(current(store))


def ensure(store,program,*,region_lines=200):
    require(20<=region_lines<=400,'Implementation intervals must be 20..400 lines')
    store.db.executescript(SCHEMA)
    key='implementation-index:'+program['id']
    if store.get_meta(key):
        saved=store.get_meta(key)
        require(saved['region_lines']==region_lines,'This snapshot already has an immutable region partition. Keep region_lines or use a new workspace for a different partition.')
        return saved
    records=[];files=0;unavailable=[]
    for row in store.db.execute('SELECT asset,module FROM learning_assets WHERE program=? ORDER BY asset',(program['id'],)).fetchall():
        if PurePosixPath(row['asset']).suffix.lower() not in CPP:continue
        files+=1;a=store.asset(program['snapshot'],row['asset'])
        if a['status']!='frozen':
            unavailable.append(row['asset']);segments=[(0,0,[])]
        else:
            lines=store.source_lines(a.get('text_sha') or a['sha'])
            segments=[(i+1,min(i+region_lines,len(lines)),lines[i:i+region_lines]) for i in range(0,len(lines),region_lines)] or [(0,0,[])]
        for first,last,lines in segments:
            hints=[{'line':first+i,'text':line.strip()[:250]} for i,line in enumerate(lines)
                   if re.match(r'\s*#\s*(if|ifdef|ifndef|elif|else|endif)\b',line) or re.search(r'\b(class|struct|enum)\s+\w+',line)]
            value={'id':identity('implementation',[program['snapshot'],row['asset'],a.get('sha'),first,last]),
                'asset':row['asset'],'module':row['module'],'start':first,'end':last,'sha256':a.get('sha'),
                'basis':'frozen_text_interval','kind':'empty_source' if first==0 and a['status']=='frozen' else 'unavailable_source' if first==0 else 'implementation_region',
                'hints':hints[:40],'hints_truncated':len(hints)>40,'required_analysis':list(FIELDS),
                'compiler_validation':'not_inferred','status':'unreviewed'}
            records.append((program['id'],value['id'],row['asset'],row['module'],first,last,canonical(value)))
    with store.transaction():
        store.db.executemany('INSERT OR IGNORE INTO implementation_items VALUES(?,?,?,?,?,?,?)',records)
        result={'schema':'implementation-index/v1','cpp_files':files,'items':len(records),'region_lines':region_lines,
                'unavailable_files':unavailable,'coverage_meaning':'physical regions to explain, not function tasks or semantic approval'}
        store.set_meta(key,result)
    return result


def listing(store,module=None,asset=None,offset=0,limit=30):
    from . import whole
    require(offset>=0 and 1<=limit<=200,'Read 1..200 implementation items per page')
    require(enabled(store),'Initialize the 2.4 module curriculum with start before querying implementation coverage')
    p=whole.current(store);where='program=?';args=[p['id']]
    if module:where+=' AND module=?';args.append(module)
    if asset:where+=' AND asset=?';args.append(asset)
    total=store.db.execute('SELECT count(*) FROM implementation_items WHERE '+where,args).fetchone()[0]
    rows=store.db.execute('SELECT data FROM implementation_items WHERE '+where+' ORDER BY asset,start LIMIT ? OFFSET ?',(*args,limit,offset))
    items=[json.loads(r[0]) for r in rows];effective=evaluated(store,p,module=module,asset=asset,item_ids=[r['id'] for r in items])
    for item in items:
        state=effective.get(item['id'],{});item.update(state=state.get('state','unreviewed'),reviewed_explanation=state.get('disposition'))
    return {'schema':'implementation-page/v1','total':total,'items':items,
            'next_offset':offset+limit if offset+limit<total else None,'semantic_approval':'not_granted'}


def _covers(store,asset,start,end,refs):
    position=start
    spans=[]
    for ref in refs:
        a=store.record('anchors',ref)
        if a['asset']==asset:spans.append((a['start'],a['end']))
    for first,last in sorted(spans):
        if first<=position:position=max(position,last+1)
    return position>end


def validate(store,program,task,rows,available,reads):
    from .knowledge import content_hash
    require(isinstance(rows,list) and len(rows)<=2000,'Implementation rows must be a bounded list')
    out=[];seen=set()
    for source in rows:
        row=dict(source);item=row.get('item')
        require(item not in seen,'Repeated implementation item');seen.add(item)
        record=store.db.execute('SELECT data FROM implementation_items WHERE program=? AND id=?',(program['id'],item)).fetchone()
        require(record,'Unknown implementation item');spec=json.loads(record[0])
        require(spec['module']==task['bundle'].get('module'),'Implementation item outside assigned module')
        require(row.get('state') in {'explained','open','no_implementation'},'Implementation state must be explained/open/no_implementation')
        require(isinstance(row.get('reason'),str) and row['reason'].strip(),'Implementation reason required')
        require(isinstance(row.get('unknowns',[]),list),'Implementation unknowns must be a list')
        if row['state']=='no_implementation':
            require(spec['kind']=='empty_source' and row.get('sha256')==spec['sha256'],'Only an actual frozen empty file can close without implementation evidence; cite its exact hash')
            require(not row.get('unknowns'),'Unresolved empty-file classification cannot be closed')
        if row['state']=='explained':
            require(spec['kind']=='implementation_region','Unavailable/empty source needs explicit scope review, not a fabricated explanation')
            analysis=row.get('analysis',{})
            require(isinstance(analysis,dict) and all(isinstance(analysis.get(k),str) and len(analysis[k].strip())>=8 for k in FIELDS),
                    'Explain behavior/conditions/state/consumers/cleanup/test_basis; not-involved needs a concrete reason')
            ids=row.get('unit_ids',[]);refs=row.get('evidence_refs',[])
            require(ids and set(ids)<=set(available),'Implementation explanation needs real staged/accepted knowledge')
            require(any(available[uid].get('kind') in {'mechanism','claim','contract','flow','requirement','test_obligation'} for uid in ids),'Implementation needs substantive mechanism knowledge, not just a feature/module label')
            require(refs and set(refs)<=reads,'Implementation evidence was not fully read in this lease')
            cited={r for uid in ids for r in available[uid].get('source_refs',[])}
            require(set(refs)<=cited and _covers(store,spec['asset'],spec['start'],spec['end'],refs),
                    'Implementation item must be fully supported by its knowledge citations')
            row['unit_hashes']={uid:content_hash(available[uid]) for uid in ids}
        out.append(row)
    return out


def apply_locked(store,program,report_id,rows):
    for row in rows:
        store.db.execute('INSERT OR REPLACE INTO implementation_dispositions VALUES(?,?,?,?)',
                         (program['id'],row['item'],report_id,canonical(row)))


def evaluated(store,p,module=None,asset=None,item_ids=None):
    from . import whole
    from .knowledge import content_hash
    params=[p['id']];where='i.program=?'
    if module:where+=' AND i.module=?';params.append(module)
    if asset:where+=' AND i.asset=?';params.append(asset)
    if item_ids is not None:
        if not item_ids:return {}
        require(len(item_ids)<=200,'Bound the implementation evaluation page')
        where+=' AND i.id IN ('+','.join('?' for _ in item_ids)+')';params.extend(item_ids)
    rows=store.db.execute('SELECT i.id,i.asset,i.module,i.data,d.data disposition FROM implementation_items i '
        'LEFT JOIN implementation_dispositions d ON d.program=i.program AND d.item=i.id WHERE '+where+' ORDER BY i.asset,i.start',params).fetchall()
    dispositions={r['id']:json.loads(r['disposition']) for r in rows if r['disposition']}
    wanted={uid for d in dispositions.values() for uid in d.get('unit_ids',[])}
    units=whole.reference_units(store,wanted);out={}
    for r in rows:
        d=dispositions.get(r['id']);state='unreviewed'
        if d:
            state=d['state']
            if state=='explained':
                if not all(uid in units and whole._applicable(store,units[uid],p) and content_hash(units[uid])==d.get('unit_hashes',{}).get(uid) for uid in d.get('unit_ids',[])):
                    state='pending_knowledge'
                elif d.get('unknowns'):state='explained_with_gaps'
        out[r['id']]={'item':r['id'],'asset':r['asset'],'state':state,'disposition':d}
    return out


def audit(store,module=None):
    from . import whole
    if not enabled(store):return {'enabled':False}
    p=whole.current(store);rows=evaluated(store,p,module);states={};missing=[];files={}
    closed={'explained','no_implementation'}
    for r in rows.values():
        state=r['state'];states[state]=states.get(state,0)+1;files.setdefault(r['asset'],[]).append(state)
        if state not in closed and len(missing)<30:missing.append({k:r[k] for k in ('item','asset','state')})
    return {'enabled':True,'cpp_files':len(files),'cpp_files_explained':sum(all(x=='explained' for x in s) for s in files.values()),
            'cpp_files_closed':sum(all(x in closed for x in s) for s in files.values()),
            'items':len(rows),'states':states,'unclosed_items':sum(n for k,n in states.items() if k not in closed),
            'examples':missing,'meaning':'evidence-backed region explanations; actual semantic review still required'}
