"""Signed module transfer of native child work and physical learning obligations."""
import gzip
import json
from pathlib import Path
import tempfile
import unittest

from platform_fixture import workspace
from unified_knowledge import assistant_session, curriculum, dispatch, implementation, knowledge, planner, study, team, whole, workkit
from unified_knowledge.store import Store, canonical, read_json


class CurriculumTeamTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(); self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.hub, self.plan, _ = workspace(self.root); self.addCleanup(self.hub.close)
        self.program = whole.ensure(self.hub, 'generic')
        self.module = 'server/optimizer'; self.principal = 'assigned-human'
        self.manifest = {'schema':'learning-inputs/v1', 'digest':'fixture-inputs',
            'features':[{'id':'feature:increment','name':'Increment','status':'not_located','module_hint':'optimizer'}],
            'compile_contexts':[], 'summary':{'features':1}, 'issues':[]}
        with self.hub.transaction():self.hub.set_meta('learning_inputs', self.manifest)
        self.course = curriculum.ensure(self.hub)
        self.order = self.root/'order.json'; self.archive = self.root/'kit.zip'; self.home = self.root/'member'
        team.assign(self.hub, self.module, self.principal, self.order)

    def open_member(self):
        workkit.pack(self.hub,self.order,self.archive)
        workkit.open_kit(self.home,self.archive)
        member = Store(self.home); self.addCleanup(member.close)
        return member

    def child_submission(self, member, *, close_before_submit=False, release=False):
        parent = 'actual-parent-session'
        assistant_session._save(assistant_session.handle_file(member.home,parent),{
            'schema':'current-assistant-session/v1','session':parent,'worker':self.principal,
            'snapshot':self.plan['snapshot'],'paths':None,'active':None})
        batch = dispatch.begin(member,parent,None,[self.module],parallel=1)
        child = batch['handoffs'][0]
        handle = read_json(assistant_session.handle_file(member.home,child['session']))
        tid = child['task']['id']; token = handle['active']['token']; worker = child['worker']
        if close_before_submit:dispatch.close(member,batch['batch'],release=release)
        key = study.current(member)['modules'][self.module]['files'][0]
        ref = whole.read_source(member,tid,worker,token,key,1,400)['id']
        unit = {'id':'mechanism:child-increment','kind':'mechanism','title':'Synthetic increment mechanism',
            'body':'Synthetic fixture source explains an increment; this verifies the protocol only.', 'source_refs':[ref]}
        drafts = planner.stage_research_unit(member,tid,worker,token,unit)
        items = implementation.listing(member,self.module)['items']
        progress = whole.stage_progress(member,tid,worker,token,{
            'inventory_complete':True,
            'assets':[{'asset':key,'disposition':'deferred','reason':'Inventory complete; interpretation remains subject to review','evidence_refs':[ref],'unit_ids':[]}],
            'implementations':[{'item':item['id'],'state':'explained','reason':'Read the complete synthetic source interval',
                'analysis':{field:'Synthetic interval source checked for '+field for field in implementation.FIELDS},
                'unit_ids':[unit['id']],'evidence_refs':[ref],'unknowns':[]} for item in items],
            'feature_mappings':[{'feature_id':'feature:increment','state':'mapped','modules':[self.module],
                'reason':'Synthetic fixture implements the named increment','unit_ids':[unit['id']],'evidence_refs':[ref]}]})
        finished = planner.finish_research(member,tid,worker,token,[{
            'question':'What does the source demonstrate?','status':'answered','explanation':'Read synthetic increment source',
            'evidence_refs':[ref]}],drafts['drafts_digest'],progress['progress_digest'])
        return batch,child,tid,finished

    def publish(self, task, result_digest):
        planner.review_task(self.hub,task,{'reviewer':'synthetic-reviewer','mode':'independent_review','verdict':'accept',
            'notes':'Protocol fixture review only','result_digest':result_digest})
        proposal = team.propose_task(self.hub,task)
        context = knowledge.review_context(self.hub,proposal['id'],'synthetic-publisher',max_chars=1000000)
        knowledge.review(self.hub,proposal['id'],{'reviewer':'synthetic-publisher','mode':'independent_review','verdict':'accept',
            'notes':'Protocol evidence binding verified','proposal_digest':context['proposal_digest']})

    def test_scoped_kit_retains_curriculum_inputs_native_tasks_and_physical_items(self):
        member = self.open_member()
        scoped = curriculum.current(member,True)
        self.assertEqual(scoped['id'],self.course['id'])
        self.assertEqual(scoped['revision'],self.course['revision'])
        self.assertEqual({p['module'] for p in scoped['packages']},{self.module})
        self.assertEqual(member.get_meta('learning_inputs'),self.manifest)
        self.assertEqual(whole.current(member)['id'],self.program['id'])
        self.assertEqual(set(whole.current(member)['modules']),{self.module})
        self.assertEqual({r[0] for r in member.db.execute('SELECT DISTINCT module FROM implementation_items')},{self.module})
        local_task = study.current(member)['modules'][self.module]['task']
        self.assertEqual(member.get_meta('coordinator-task-map')[self.plan['modules'][self.module]['task']],local_task)
        self.assertNotEqual(local_task,self.plan['modules'][self.module]['task'])

    def test_initial_kit_carries_published_external_prerequisite_reference_proof(self):
        # The module shard has no accepted global knowledge revision of its own;
        # signed exact references must make the native publication gate usable.
        unit = self.hub.units(ids=['fixture:increment'])['fixture:increment']
        with self.hub.transaction():
            dep = planner.create_task(self.hub,snapshot=self.plan['snapshot'],run=self.plan['run'],profile=self.plan['profile'],
                kind='shared_research',bundle={'plan_id':self.plan['id'],'module':'server/executor','question':'Published external prerequisite'})
            self.hub.db.execute("UPDATE tasks SET status='accepted',result=? WHERE id=?",(canonical({'worker':'prior-worker','claims':[unit]}),dep))
            self.hub.db.execute('INSERT INTO task_edges VALUES(?,?)',(self.plan['modules'][self.module]['task'],dep))
        member = self.open_member()
        self.assertIn('fixture:increment',whole.reference_units(member,['fixture:increment']))
        task = study.current(member)['modules'][self.module]['task']
        self.assertFalse(curriculum.prerequisites(member,planner.task_status(member,task)))
        self.assertEqual(planner.lease(member,task,self.principal)['status'],'leased')

    def test_child_submission_transfers_without_impersonation_and_feedback_syncs_review_and_new_task(self):
        member = self.open_member(); _,child,tid,_ = self.child_submission(member)
        packet = self.root/'result.gz'; team.export_result(member,self.home/'order.json',tid,packet)
        data = team._read_packet(packet)['data']
        self.assertEqual(data['worker'],child['worker'])
        self.assertEqual(data['principal_worker'],self.principal)
        self.assertNotEqual(data['worker'],self.principal)
        received = team.receive(self.hub,packet)
        target = self.plan['modules'][self.module]['task']
        self.assertEqual(received['task'],target)
        result = planner.task_status(self.hub,target)['result']
        self.assertEqual(result['worker'],child['worker'])
        self.assertEqual(result['principal_worker'],self.principal)
        self.assertEqual(len(result['progress']['implementations']),1)
        self.publish(target,received['result_digest'])
        created = whole.advance(self.hub)['created_or_reused']
        self.assertTrue(created)
        feedback = self.root/'feedback.gz'; team.feedback(self.hub,self.order,feedback)
        team.sync_feedback(member,feedback)
        self.assertEqual(implementation.audit(member,self.module)['states'],{'explained':1})
        mapping = member.get_meta('coordinator-task-map')
        self.assertIn(created[0]['task'],mapping)
        self.assertTrue(any(mapping[created[0]['task']] in p['tasks'] for p in curriculum.current(member)['packages']))

    def test_stale_or_inconsistent_delegation_and_native_scope_are_rejected(self):
        member = self.open_member(); batch,child,tid,_ = self.child_submission(member)
        packet = self.root/'result.gz'; team.export_result(member,self.home/'order.json',tid,packet)
        original = team._read_packet(packet)
        ticket = read_json(self.order)
        for field,value in [('snapshot','stale-snapshot'),('principal_worker','someone-else')]:
            forged = json.loads(json.dumps(original)); forged['data']['delegation'][field] = value
            forged['hmac'] = team._signed(ticket['secret'],forged['data'])
            path = self.root/(field+'.gz'); path.write_bytes(gzip.compress(canonical(forged).encode()))
            with self.assertRaisesRegex(ValueError,'delegation'):team.receive(self.hub,path)
        forged = json.loads(json.dumps(original))
        forged['data']['task_scope']['bundle']['question'] = 'Different native task question'
        forged['data']['delegation']['task_scope'] = forged['data']['task_scope']
        forged['hmac'] = team._signed(ticket['secret'],forged['data'])
        path = self.root/'scope.gz'; path.write_bytes(gzip.compress(canonical(forged).encode()))
        with self.assertRaisesRegex(ValueError,'identity/scope'):team.receive(self.hub,path)
        dispatch.close(member,batch['batch'])
        actor = member.get_meta('dispatch-actor:'+child['worker'])
        with member.transaction():member.set_meta('dispatch-actor:'+child['worker'],{**actor,'allowed_tasks':[]})
        with self.assertRaisesRegex(ValueError,'stale persisted'):team.export_result(member,self.home/'order.json',tid,self.root/'stale-grant.gz')

    def test_closed_batch_submitted_result_still_exports_and_receives_but_cannot_claim(self):
        member = self.open_member(); batch,child,tid,_ = self.child_submission(member)
        dispatch.close(member,batch['batch'],release=True)
        self.assertEqual(planner.task_status(member,tid)['status'],'submitted')
        packet = self.root/'closed-result.gz'; team.export_result(member,self.home/'order.json',tid,packet)
        data = team._read_packet(packet)['data']
        self.assertFalse(data['delegation']['active'])
        self.assertEqual(data['delegation']['authorization'],'submitted_native_result')
        self.assertEqual(data['delegation']['native_submission']['digest'],data['submission_digest'])
        received = team.receive(self.hub,packet)
        self.assertEqual(received['worker'],child['worker'])
        result = planner.task_status(self.hub,received['task'])['result']
        self.assertEqual(result['worker'],child['worker'])
        self.assertEqual(result['principal_worker'],self.principal)
        plan = study.current(member)
        with member.transaction():
            new_task = planner.create_task(member,snapshot=plan['snapshot'],run=plan['run'],profile=plan['profile'],
                kind='feature_research',bundle={'plan_id':plan['id'],'module':self.module,'question':'A future task after closure'})
        with self.assertRaisesRegex(ValueError,'outside its active task scope'):planner.lease(member,new_task,child['worker'])
        with self.assertRaisesRegex(ValueError,'closed'):dispatch.next_batch(member,batch['batch'])

    def test_valid_lease_can_finish_after_batch_close_without_release(self):
        member = self.open_member()
        batch,child,tid,_ = self.child_submission(member,close_before_submit=True)
        closed = member.get_meta('dispatch:'+batch['batch'])['closed_at']
        self.assertGreater(planner.task_status(member,tid)['result']['submitted'],closed)
        packet = self.root/'late-result.gz'; team.export_result(member,self.home/'order.json',tid,packet)
        signed = team._read_packet(packet); capture = signed['data']['delegation']['native_submission']
        self.assertLessEqual(capture['claimed'],closed)
        self.assertGreater(capture['submitted'],closed)
        self.assertGreater(capture['claim_receipt'],0)
        # A forged claim dated after revocation is rejected even if its packet
        # signature is otherwise valid for the assignment.
        forged = json.loads(json.dumps(signed))
        forged['data']['delegation']['native_submission']['claimed'] = capture['submitted']
        forged['hmac'] = team._signed(read_json(self.order)['secret'],forged['data'])
        bad = self.root/'late-claim.gz'; bad.write_bytes(gzip.compress(canonical(forged).encode()))
        with self.assertRaisesRegex(ValueError,'delegation'):team.receive(self.hub,bad)
        received = team.receive(self.hub,packet)
        self.assertEqual(received['worker'],child['worker'])

    def test_close_with_release_revokes_lease_and_prevents_native_finish(self):
        member = self.open_member()
        with self.assertRaisesRegex(ValueError,'Invalid, expired or superseded task lease'):
            self.child_submission(member,close_before_submit=True,release=True)
        tid = study.current(member)['modules'][self.module]['task']
        task = planner.task_status(member,tid)
        self.assertEqual(task['status'],'queued')
        self.assertNotIn('result',task)
        with self.assertRaisesRegex(ValueError,'Export a submitted research task'):
            team.export_result(member,self.home/'order.json',tid,self.root/'released.gz')

    def test_receive_requires_published_prerequisite_knowledge(self):
        member = self.open_member(); _,_,tid,_ = self.child_submission(member)
        packet = self.root/'result.gz'; team.export_result(member,self.home/'order.json',tid,packet)
        target = self.plan['modules'][self.module]['task']
        with self.hub.transaction():
            dep = planner.create_task(self.hub,snapshot=self.plan['snapshot'],run=self.plan['run'],profile=self.plan['profile'],
                kind='shared_research',bundle={'plan_id':self.plan['id'],'module':self.module,'question':'Unpublished prerequisite'})
            self.hub.db.execute("UPDATE tasks SET status='accepted',result=? WHERE id=?",(canonical({'worker':'prior-worker',
                'claims':[{'id':'mechanism:unpublished','kind':'mechanism','title':'Not published','body':'No accepted knowledge revision','source_refs':[]}]}),dep))
            self.hub.db.execute('INSERT INTO task_edges VALUES(?,?)',(target,dep))
        with self.assertRaisesRegex(ValueError,'not published/applicable'):team.receive(self.hub,packet)
        self.assertEqual(planner.task_status(self.hub,target)['status'],'queued')

    def test_coordinator_refinement_syncs_but_local_only_refinement_needs_reconciliation(self):
        member = self.open_member()
        files = self.plan['modules'][self.module]['files']
        def package(title):
            return [{'id':'increment-package','title':title,'question':'Explain the actual increment source and downstream consumers',
                'files':files,'feature_ids':['feature:increment'],'mainline_ids':[]}]
        refined = curriculum.refine(self.hub,self.module,package('Coordinator behavior package'),'actual-planner',self.course['revision'])
        feedback = self.root/'refinement.gz'; team.feedback(self.hub,self.order,feedback)
        team.sync_feedback(member,feedback)
        current = curriculum.current(member)
        self.assertEqual(current['revision'],refined['revision'])
        self.assertEqual(current['packages'][0]['title'],'Coordinator behavior package')
        self.assertEqual(current['packages'][0]['depends_on'],[study.current(member)['modules'][self.module]['task']])
        curriculum.refine(member,self.module,package('Local unmerged package'),'local-planner',current['revision'])
        # A local planner cannot silently overwrite the coordinator's immutable
        # task scopes through a result or overwrite local decisions with feedback.
        self.assertTrue(team.sync_feedback(member,feedback)['replayed'])
        curriculum.refine(self.hub,self.module,package('Updated coordinator package'),'actual-planner',refined['revision'])
        later = self.root/'later-refinement.gz'; team.feedback(self.hub,self.order,later)
        with self.assertRaisesRegex(ValueError,'reconciliation'):team.sync_feedback(member,later)


if __name__ == '__main__':unittest.main()
