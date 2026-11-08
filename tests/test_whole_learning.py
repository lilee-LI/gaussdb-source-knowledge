"""Whole curriculum protocol tests; synthetic source, no product/model accuracy claims."""
import json
from pathlib import Path
import tempfile
import sys
import unittest

from platform_fixture import workspace,accept
from unified_knowledge import whole,planner,team,workkit,study,knowledge,service
from unified_knowledge.store import Store,digest


class WholeLearningTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.hub,self.plan,_=workspace(self.root);self.addCleanup(self.hub.close)
        self.program=whole.ensure(self.hub,'generic')

    def research(self,store,module,*,propose=False,task=None,worker='learner',publish=True,legacy_evidence=False):
        plan=study.current(store);task=task or plan['modules'][module]['task']
        lease=planner.lease(store,task,worker);token=lease['token'];refs=[];assets=[];draft=None
        for key in plan['modules'][module]['files']:
            read=whole.read_source(store,task,worker,token,key,1,400);refs.append(read['id'])
            assets.append({'asset':key,'disposition':'studied','reason':'Synthetic full-file protocol research','evidence_refs':[read['id']],'unit_ids':['mechanism:'+module]})
        if legacy_evidence:
            symbol=next(json.loads(r['data']) for r in store.lookup_symbols(plan['run'],'cg_compute',limit=4) if json.loads(r['data']).get('definition'))
            planner.read_for_task(store,task,worker,token,symbol['evidence']);refs.append(symbol['evidence'])
        unit={'id':'mechanism:'+module,'kind':'mechanism','title':module+' fixture mechanism','body':'The frozen synthetic fixture was read; this is a protocol test.',
              'source_refs':refs,'conditions':['Synthetic fixture only'],'counterexamples':['No real database semantics certified'],'symbol_refs':[]}
        draft=planner.stage_research_unit(store,task,worker,token,unit)
        report={'inventory_complete':True,'assets':assets}
        if propose:
            key=plan['modules'][module]['files'][0]
            report['proposals']=[{'id':'mechanism-A','title':'Follow-up source question','question':'Which boundary needs deeper evidence?',
                     'owner_module':module,'reason':'Real reviewed research proposal','evidence':[{'asset':key,'start':1,'end':1}]}]
        progress=whole.stage_progress(store,task,worker,token,report)
        finished=planner.finish_research(store,task,worker,token,[{'question':'What is covered?','status':'answered','explanation':'Frozen source cited','evidence_refs':refs}],draft['drafts_digest'],progress['progress_digest'])
        if publish:
            self.approve(store,task,finished['result_digest'])
        return task,finished,report

    def approve(self,store,task,signature):
        planner.review_task(store,task,{'reviewer':'protocol-reviewer','mode':'independent_review','verdict':'accept','notes':'Synthetic software review, no real product acceptance','result_digest':signature})
        p=team.propose_task(store,task);ctx=knowledge.review_context(store,p['id'],'knowledge-reviewer',max_chars=1000000)
        knowledge.review(store,p['id'],{'reviewer':'knowledge-reviewer','mode':'independent_review','verdict':'accept','notes':'Synthetic exact-evidence protocol check','proposal_digest':ctx['proposal_digest']})

    def test_review_publication_use_checks_and_stale_signoff(self):
        self.assertEqual(whole.status(self.hub)['assets'],4)
        task,finished,_=self.research(self.hub,'server/optimizer',publish=False)
        self.assertEqual(whole.status(self.hub)['asset_states'],{'unreviewed':4})
        planner.review_task(self.hub,task,{'reviewer':'reviewer','mode':'independent_review','verdict':'accept','notes':'Read the synthetic source','result_digest':finished['result_digest']})
        self.assertEqual(whole.status(self.hub)['asset_states']['pending_knowledge'],1)
        self.assertFalse(whole.advance(self.hub)['created_or_reused'])
        # Publish the already reviewed task without a second task review.
        p=team.propose_task(self.hub,task);ctx=knowledge.review_context(self.hub,p['id'],'k-reviewer')
        knowledge.review(self.hub,p['id'],{'reviewer':'k-reviewer','mode':'independent_review','verdict':'accept','notes':'Synthetic software evidence check','proposal_digest':ctx['proposal_digest']})
        for module in self.plan['modules']:
            if module!='server/optimizer':self.research(self.hub,module)
        audit=whole.audit(self.hub)
        self.assertEqual({b['kind'] for b in audit['blockers']},{'consumer_use_cases'})
        cases=[{'id':module+role,'module':module,'role':role,'query':module+' fixture mechanism','required_units':['mechanism:'+module]} for module in self.plan['modules'] for role in ('coding','test_generation','review')]
        self.assertEqual(whole.verify_uses(self.hub,cases)['status'],'passed')
        ready=whole.audit(self.hub);self.assertFalse(ready['blockers'])
        whole.accept(self.hub,ready['digest'],'coverage-reviewer','Verified every synthetic asset and actual retrieval checks')
        self.assertEqual(whole.audit(self.hub)['status'],'accepted')
        changed=self.hub.units(ids=['mechanism:server/optimizer'])['mechanism:server/optimizer']
        changed={k:v for k,v in changed.items() if k not in {'_binding','review','content_hash','version'}};changed['body']+=' A revised interpretation.'
        accept(self.hub,changed)
        self.assertEqual(whole.audit(self.hub)['status'],'incomplete')
        self.assertIn('pending_knowledge',whole.status(self.hub)['asset_states'])

    def test_partial_evidence_supporting_abuse_and_unreviewed_progress_are_rejected(self):
        module='server/optimizer';task=self.plan['modules'][module]['task'];lease=planner.lease(self.hub,task,'learner');token=lease['token']
        read=whole.read_source(self.hub,task,'learner',token,'server/optimizer/producer.cpp',1,1)
        unit={'id':'mechanism:partial','kind':'mechanism','title':'Partial','body':'Only a line was read','source_refs':[read['id']]}
        planner.stage_research_unit(self.hub,task,'learner',token,unit)
        row={'asset':'server/optimizer/producer.cpp','disposition':'studied','reason':'Too optimistic','unit_ids':[unit['id']],'evidence_refs':[read['id']]}
        with self.assertRaisesRegex(ValueError,'full frozen evidence span'):whole.stage_progress(self.hub,task,'learner',token,{'assets':[row]})
        with self.assertRaisesRegex(ValueError,'supporting data'):whole.stage_progress(self.hub,task,'learner',token,{'assets':[{**row,'disposition':'supporting'}]})
        with self.assertRaisesRegex(ValueError,'lease'):whole.stage_progress(self.hub,task,'learner','bad',{'assets':[]})
        self.assertEqual(whole.status(self.hub)['reviewed_progress_reports'],0)

    def test_bounded_continuation_uses_reviewed_mechanisms_and_wip(self):
        task,finished,report=self.research(self.hub,'server/optimizer',propose=True,publish=False)
        self.assertFalse(whole.advance(self.hub)['created_or_reused'])
        self.approve(self.hub,task,finished['result_digest'])
        first=whole.advance(self.hub,max_tasks=1)
        self.assertEqual(len(first['created_or_reused']),1)
        self.assertFalse(whole.advance(self.hub,max_tasks=1)['created_or_reused'])
        nxt=whole.next_task(self.hub,'learner','server/optimizer');self.assertEqual(nxt['state'],'ready')
        planner.lease(self.hub,nxt['task']['id'],'learner')
        self.assertEqual(whole.next_task(self.hub,'learner','server/optimizer')['state'],'in_progress')

    def test_multiple_results_signed_feedback_rework_and_replay(self):
        module='server/optimizer';order=self.root/'order.json';kit=self.root/'kit.zip';worker=self.root/'member'
        team.assign(self.hub,module,'member',order);workkit.pack(self.hub,order,kit);workkit.open_kit(worker,kit)
        with Store(worker) as local:
            t,finished,_=self.research(local,module,worker='member',publish=False,legacy_evidence=True)
            packet=self.root/'result-1.gz';team.export_result(local,worker/'order.json',t,packet)
            received=team.receive(self.hub,packet);self.assertEqual(received['task'],self.plan['modules'][module]['task'])
            self.assertTrue(team.receive(self.hub,packet)['replayed'])
            self.approve(self.hub,received['task'],received['result_digest'])
            feedback=self.root/'feedback-1.gz';team.feedback(self.hub,order,feedback)
            synced=team.sync_feedback(local,feedback);self.assertEqual(synced['updated'][0]['status'],'accepted')
            self.assertTrue(team.sync_feedback(local,feedback)['replayed'])
            self.assertEqual(whole.status(local)['modules'][0]['states'],{'studied':1})
            extra=self.root/'extra.gz';team.feedback(self.hub,order,extra,['server/tools/idle.cpp'])
            expanded=team.sync_feedback(local,extra)
            self.assertNotEqual(expanded['epoch'],synced['epoch'])
            self.assertEqual(local.asset(self.plan['snapshot'],'server/tools/idle.cpp')['status'],'frozen')
            with self.hub.transaction():
                hub_next=planner.create_task(self.hub,snapshot=self.plan['snapshot'],run=self.plan['run'],profile=self.plan['profile'],kind='coverage_research',
                    bundle={'module':module,'plan_id':self.plan['id'],'question':'Second result for same assignment','source_anchor_refs':[]})
            delta=self.root/'task-delta.gz';team.feedback(self.hub,order,delta);team.sync_feedback(local,delta)
            next_id=local.get_meta('coordinator-task-map')[hub_next]
            t,_,_=self.research(local,module,worker='member',task=next_id,publish=False)
            packet2=self.root/'result-2.gz';team.export_result(local,worker/'order.json',t,packet2)
            second=team.receive(self.hub,packet2)
            self.assertEqual(second['task'],hub_next)
            self.assertNotEqual(second['task'],received['task'])
            planner.review_task(self.hub,second['task'],{'reviewer':'reviewer','mode':'independent_review','verdict':'reject','notes':'Synthetic rework path verification','result_digest':second['result_digest']})
            feedback2=self.root/'feedback-2.gz';team.feedback(self.hub,order,feedback2);team.sync_feedback(local,feedback2)
            self.assertEqual(planner.task_status(local,t)['status'],'needs_research')
            self.research(local,module,worker='member',task=t,publish=False)
            packet3=self.root/'result-3.gz';team.export_result(local,worker/'order.json',t,packet3)
            third=team.receive(self.hub,packet3);self.assertEqual(third['task'],second['task'])

    def test_semantic_template_gap_and_read_tools(self):
        # Data-only policy is configurable; a missing source match becomes a scope task, not silent N/A.
        policy=whole.policy('generic');policy['templates']=[{'id':'T1','title':'Unlocated mechanism','question':'Where is it?', 'kind':'shared_research','patterns':['missing/*'],'depends_on':[]}]
        p=whole.ensure(self.hub,policy);self.assertEqual(p['templates'][0]['scope_status'],'needs_scope_decision')
        self.assertIn('program_item',{b['kind'] for b in whole.audit(self.hub)['blockers']})
        self.assertIn('read_source',{t['name'] for t in service.tools('researcher')})
        self.assertNotIn('stage_progress',{t['name'] for t in service.tools('query')})

    def test_partial_source_spans_accumulate_only_after_both_reviews(self):
        module='server/optimizer';key='server/optimizer/producer.cpp';tid=self.plan['modules'][module]['task']
        for n in (1,2):
            if n==2:
                created=whole.advance(self.hub)['created_or_reused'];self.assertEqual(len(created),1);tid=created[0]['task']
            lease=planner.lease(self.hub,tid,'learner');token=lease['token']
            ref=whole.read_source(self.hub,tid,'learner',token,key,n,1)['id']
            u={'id':'mechanism:span-'+str(n),'kind':'mechanism','title':'Frozen span '+str(n),'body':'Synthetic incremental source evidence','source_refs':[ref]}
            d=planner.stage_research_unit(self.hub,tid,'learner',token,u)
            p=whole.stage_progress(self.hub,tid,'learner',token,{'inventory_complete':True,'assets':[{'asset':key,'disposition':'partial','reason':'Source span '+str(n),'unit_ids':[u['id']],'evidence_refs':[ref]}]})
            result=planner.finish_research(self.hub,tid,'learner',token,[{'question':'Span mechanism','status':'answered','explanation':'Synthetic source span','evidence_refs':[ref]}],d['drafts_digest'],p['progress_digest'])
            self.approve(self.hub,tid,result['result_digest'])
            state=whole.module_assets(self.hub,module)['items'][0]['state']
            self.assertEqual(state,'partial' if n==1 else 'studied')

    def test_cross_module_contract_cannot_pass_one_sided(self):
        symbols={name:self.hub.lookup_symbols(self.plan['run'],name,limit=4) for name in ('cg_compute','cg_consume')}
        prod=next(json.loads(r['data']) for r in symbols['cg_compute'] if json.loads(r['data']).get('definition'))
        cons=next(json.loads(r['data']) for r in symbols['cg_consume'] if json.loads(r['data']).get('definition'))
        contract={'id':'contract:fixture-cross','kind':'contract','title':'Synthetic producer consumer','body':'Fixture contract for protocol checks',
             'conditions':['Synthetic source only'],'counterexamples':['No runtime verification'],'source_refs':[prod['evidence'],cons['evidence']],
             'producers':[prod['id']],'consumers':[cons['id']],'requires':['Representable input'],'ensures':['Caller receives result'],'invariants':['No runtime claim']}
        accept(self.hub,contract)
        self.assertIn('unverified_cross_module_contract',{b['kind'] for b in whole.audit(self.hub)['blockers']})
        for module,side in (('server/optimizer','producer'),('server/executor','consumer')):
            tid=self.plan['modules'][module]['task'];lease=planner.lease(self.hub,tid,'learner');token=lease['token']
            key=self.plan['modules'][module]['files'][0];ref=whole.read_source(self.hub,tid,'learner',token,key,1,100)['id']
            progress=whole.stage_progress(self.hub,tid,'learner',token,{'contracts':[{'unit':contract['id'],'side':side,'module':module,
                'producer_module':'server/optimizer','consumer_module':'server/executor','reason':'Actual frozen endpoint checked','evidence_refs':[ref]}]})
            result=planner.finish_research(self.hub,tid,'learner',token,[{'question':'Endpoint','status':'answered','explanation':'Source endpoint read','evidence_refs':[ref]}],progress_digest=progress['progress_digest'])
            planner.review_task(self.hub,tid,{'reviewer':'reviewer','mode':'independent_review','verdict':'accept','notes':'Synthetic endpoint source review','result_digest':result['result_digest']})
            kinds={b['kind'] for b in whole.audit(self.hub)['blockers']}
            self.assertEqual('one_sided_contract' in kinds,side=='producer')

    def test_native_session_failure_never_accepts_work_and_resume_cannot_steal(self):
        from unified_knowledge.continuation import run
        (self.hub.home/'researcher.mcp.json').write_text('{"mcpServers":{}}',encoding='utf-8')
        # Python deliberately rejects Claude CLI switches: a real local process failure, no model.
        result=run(self.hub,worker='learner',module='server/optimizer',executable=sys.executable,timeout=10)
        self.assertEqual(result['stopped'],'session_needs_attention')
        self.assertEqual(result['sessions'][0]['task_status'],'queued')
        tid=self.plan['modules']['server/optimizer']['task'];planner.lease(self.hub,tid,'learner')
        with self.assertRaisesRegex(ValueError,'active, unexpired'):
            run(self.hub,worker='another-worker',resume_task=tid,executable=sys.executable,timeout=10)

    def test_frozen_literal_search_does_not_fabricate_read_receipts(self):
        tid=self.plan['modules']['server/optimizer']['task'];lease=planner.lease(self.hub,tid,'learner');token=lease['token']
        hits=service.invoke(self.hub,'search_source',{'task':tid,'worker':'learner','token':token,'query':'return value','asset_patterns':['server/optimizer/*']},role='researcher')
        self.assertTrue(hits['matches']);ref=hits['matches'][0]['evidence']
        unit={'id':'mechanism:search','kind':'mechanism','title':'Search proof','body':'Synthetic source search','source_refs':[ref]}
        with self.assertRaisesRegex(ValueError,'not fully read'):planner.stage_research_unit(self.hub,tid,'learner',token,unit)
        planner.read_for_task(self.hub,tid,'learner',token,ref)
        planner.stage_research_unit(self.hub,tid,'learner',token,unit)
        cursor=0;line=0;found=[]
        for _ in range(4):
            page=whole.search_source(self.hub,tid,'learner',token,'e',['server/optimizer/*'],limit=1,offset=cursor,line_offset=line)
            found.extend(m['line'] for m in page['matches'])
            if page['next_file_offset'] is None:break
            cursor=page['next_file_offset'];line=page['next_line_offset']
        self.assertEqual(found,[1,2])


if __name__=='__main__':unittest.main()
