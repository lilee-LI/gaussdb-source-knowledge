"""Native dispatch protocol tests; synthetic actors and source, never an LLM."""
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
import tempfile
import time
import unittest

from platform_fixture import workspace, accept
from unified_knowledge import assistant_session, curriculum, dispatch, planner, study, team, whole
from unified_knowledge.store import Store, read_json


class NativeDispatchTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.store,self.plan,self.base_unit=workspace(self.root);self.addCleanup(self.store.close)
        self.program=whole.ensure(self.store,'generic')
        self.parent='host-parent';self.principal='real-member'
        assistant_session._save(assistant_session.handle_file(self.store.home,self.parent),{
            'schema':'current-assistant-session/v1','session':self.parent,'worker':self.principal,
            'snapshot':self.plan['snapshot'],'paths':None,'active':None})

    def begin(self,modules=None,parallel=3,**options):
        return dispatch.begin(self.store,self.parent,None,modules or list(self.plan['modules']),parallel,**options)

    def handle(self,child):
        return read_json(assistant_session.handle_file(self.store.home,child['session']))

    def test_parallel_native_leases_private_handles_and_restart(self):
        batch=self.begin();self.assertEqual(len(batch['handoffs']),3)
        tasks=[x['task']['id'] for x in batch['handoffs']]
        self.assertEqual(len(set(tasks)),3)
        self.assertEqual(len({x['session'] for x in batch['children']}),3)
        self.assertEqual(len({x['worker'] for x in batch['children']}),3)
        self.assertFalse(batch['model_process_started']);self.assertFalse(batch['automatic_acceptance'])
        self.assertEqual(batch['principal_worker'],self.principal)
        for child in batch['handoffs']:
            handle=self.handle(child);self.assertTrue(handle['active']['token'])
            self.assertIn('--home',child['context_command'])
            self.assertNotIn(handle['active']['token'],json.dumps(batch))
            self.assertNotEqual(child['session'],self.parent)
        restarted=self.begin()
        self.assertEqual(restarted['batch'],batch['batch']);self.assertFalse(restarted['handoffs'])
        self.assertEqual(len(restarted['resume_candidates']),3)
        self.assertIsNone(read_json(assistant_session.handle_file(self.store.home,self.parent))['active'])

    def test_assigned_module_aliases_and_exact_delegate_permissions(self):
        team.assign(self.store,'server/optimizer',self.principal,self.root/'order.json')
        self.assertEqual(dispatch.resolve_modules(self.store,['优化器']),['server/optimizer'])
        self.assertEqual(dispatch.resolve_modules(self.store,['optimizer']),['server/optimizer'])
        batch=self.begin(['优化器']);self.assertEqual(len(batch['handoffs']),1)
        child=batch['handoffs'][0];task=planner.task_status(self.store,child['task']['id'])
        self.assertTrue(dispatch.authorized_delegate(self.store,child['worker'],self.principal,task))
        self.assertFalse(dispatch.authorized_delegate(self.store,child['worker'],'invented-principal',task))
        outside=self.plan['modules']['server/tools']['task']
        with self.assertRaisesRegex(ValueError,'outside its active task scope'):
            planner.lease(self.store,outside,child['worker'])
        with self.assertRaisesRegex(ValueError,'belongs to another'):
            planner.lease(self.store,task['id'],'unassigned-person')
        dispatch.close(self.store,batch['batch'],release=True)
        with self.assertRaisesRegex(ValueError,'outside its active task scope'):
            planner.lease(self.store,task['id'],child['worker'])

    def test_concurrent_dispatch_claims_once_and_existing_workers_are_not_cloned(self):
        batch=self.begin(parallel=2);child=batch['handoffs'][0];handle=self.handle(child)
        planner.lease(self.store,child['task']['id'],child['worker'],action='release',token=handle['active']['token'])
        def advance(_):
            with Store(self.store.home) as connection:return dispatch.next_batch(connection,batch['batch'])
        with ThreadPoolExecutor(max_workers=2) as pool:results=list(pool.map(advance,range(2)))
        issued=[h for result in results for h in result['handoffs']]
        self.assertEqual(len(issued),1)
        self.assertEqual(issued[0]['session'],child['session'])
        self.assertEqual(dispatch.status(self.store,batch['batch'])['principal_active_tasks'],2)

    def test_expired_attempt_reclaims_and_old_read_receipts_are_invalid(self):
        batch=self.begin(['optimizer'],parallel=1);child=batch['handoffs'][0];handle=self.handle(child)
        task=child['task']['id'];asset=self.plan['modules']['server/optimizer']['files'][0]
        read=whole.read_source(self.store,task,child['worker'],handle['active']['token'],asset,1,400)
        with self.store.transaction():self.store.db.execute('UPDATE tasks SET deadline=? WHERE id=?',(time.time()-1,task))
        again=dispatch.next_batch(self.store,batch['batch']);new=again['handoffs'][0]
        self.assertEqual(new['session'],child['session']);self.assertEqual(new['task']['attempt'],2)
        self.assertEqual(new['dispatch'],'new_attempt');self.assertTrue(new['evidence_must_be_reread'])
        refreshed=self.handle(child)
        unit={'id':'mechanism:attempt','kind':'mechanism','title':'Attempt binding','body':'Synthetic read receipt test',
              'source_refs':[read['id']]}
        with self.assertRaisesRegex(ValueError,'not fully read'):
            planner.stage_research_unit(self.store,task,child['worker'],refreshed['active']['token'],unit)

    def test_does_not_steal_another_live_token_or_duplicate_host_agents(self):
        batch=self.begin(['optimizer'],parallel=1);child=batch['handoffs'][0];task=child['task']['id']
        dispatch.attach_agent(self.store,batch['batch'],child['session'],'actual-host-agent-27')
        resumed=dispatch.status(self.store,batch['batch'])['resume_candidates'][0]
        self.assertEqual(resumed['native_agent_id'],'actual-host-agent-27')
        with self.store.transaction():self.store.db.execute('UPDATE tasks SET deadline=? WHERE id=?',(time.time()-1,task))
        other=planner.lease(self.store,task,'other-real-worker')
        result=dispatch.next_batch(self.store,batch['batch']);self.assertFalse(result['handoffs'])
        self.assertEqual(result['children'][0]['state'],'superseded')
        row=self.store.db.execute('SELECT owner,token FROM tasks WHERE id=?',(task,)).fetchone()
        self.assertEqual((row['owner'],row['token']),('other-real-worker',other['token']))

    def test_close_releases_only_owned_leases_and_never_accepts(self):
        batch=self.begin(parallel=2);child_tasks={x['task']['id'] for x in batch['children']}
        other=next(info['task'] for info in self.plan['modules'].values() if info['task'] not in child_tasks)
        parent_lease=planner.lease(self.store,other,self.principal)
        result=dispatch.close(self.store,batch['batch'],release=True)
        self.assertEqual(result['state'],'closed');self.assertEqual(set(result['released_tasks']),child_tasks)
        for task in child_tasks:self.assertEqual(planner.task_status(self.store,task)['status'],'queued')
        self.assertEqual(planner.task_status(self.store,other)['status'],'leased')
        self.assertEqual(self.store.db.execute('SELECT token FROM tasks WHERE id=?',(other,)).fetchone()[0],parent_lease['token'])
        with self.assertRaisesRegex(ValueError,'closed'):dispatch.next_batch(self.store,batch['batch'])

    def test_submission_waits_for_actual_review_and_pending_budget_is_shared(self):
        batch=self.begin(parallel=1);head=self.store.get_meta('knowledge_head');issued=[]
        for _ in range(4):
            self.assertEqual(len(batch['handoffs']),1)
            child=batch['handoffs'][0];handle=self.handle(child);issued.append(child['task']['id'])
            planner.submit(self.store,child['task']['id'],child['worker'],handle['active']['token'],{
                'coverage':[{'question':'What still needs source research?','status':'open',
                             'explanation':'Synthetic protocol submission intentionally awaits real research review','evidence_refs':[]}]})
            # A pending slot cannot silently acquire the next task. A new explicit slot
            # is only possible by closing and restarting the parent batch.
            stopped=dispatch.next_batch(self.store,batch['batch'])
            self.assertFalse(stopped['handoffs']);self.assertEqual(stopped['state'],'awaiting_review')
            dispatch.close(self.store,batch['batch'])
            batch=self.begin(parallel=1)
        self.assertFalse(batch['handoffs']);self.assertEqual(batch['principal_pending_review'],4)
        self.assertEqual(self.store.get_meta('knowledge_head'),head)
        self.assertTrue(all(planner.task_status(self.store,t)['status']=='submitted' for t in issued))

    def test_member_scope_and_stale_snapshot_revoke_delegation(self):
        p=study.current(self.store);p['worker_scope']='server/optimizer'
        with self.store.transaction():self.store.set_meta(p['id'],p)
        self.assertEqual(dispatch.resolve_modules(self.store,['optimizer']),['server/optimizer'])
        with self.assertRaisesRegex(ValueError,'scoped'):dispatch.resolve_modules(self.store,['tools'])
        batch=self.begin(['optimizer'],parallel=1);child=batch['handoffs'][0]
        outside=planner.task_status(self.store,self.plan['modules']['server/tools']['task'])
        self.assertFalse(dispatch.candidate_allowed(self.store,'ordinary-worker',outside))
        task=planner.task_status(self.store,child['task']['id'])
        with self.store.transaction():self.store.set_meta(p['id'],{**p,'snapshot':'changed-snapshot'})
        self.assertFalse(dispatch.candidate_allowed(self.store,child['worker'],task))

    def test_dependencies_use_exact_native_closure_without_broadening_the_module(self):
        optimizer=self.plan['modules']['server/optimizer']['task']
        executor=self.plan['modules']['server/executor']['task']
        with self.store.transaction():
            self.store.db.execute('INSERT INTO task_edges(task,dependency) VALUES(?,?)',(optimizer,executor))
            unrelated=planner.create_task(self.store,snapshot=self.plan['snapshot'],run=self.plan['run'],
                profile=self.plan['profile'],kind='feature_research',
                bundle={'module':'server/executor','plan_id':self.plan['id'],'question':'Independent executor feature'})
        blocked=self.begin(['optimizer'],parallel=1,include_dependencies=False)
        self.assertFalse(blocked['handoffs']);dispatch.close(self.store,blocked['batch'])
        batch=self.begin(['optimizer'],parallel=1)
        self.assertEqual(batch['dependency_modules'],['server/executor'])
        self.assertEqual(batch['handoffs'][0]['task']['id'],executor)
        child=batch['handoffs'][0]
        self.assertFalse(dispatch.candidate_allowed(self.store,child['worker'],planner.task_status(self.store,unrelated)))
        self.assertEqual(dispatch.resolve_modules(self.store,['server']),sorted(self.plan['modules']))

    def test_native_claim_requires_applicable_published_knowledge(self):
        curriculum.ensure(self.store)
        with self.store.transaction():
            task=planner.create_task(self.store,snapshot=self.plan['snapshot'],run=self.plan['run'],
                profile=self.plan['profile'],kind='feature_research',bundle={
                    'plan_id':self.plan['id'],'module':'server/optimizer',
                    'question':'Build on a reviewed prerequisite','requires_knowledge':['fixture:prerequisite']})
        with self.assertRaisesRegex(ValueError,'knowledge prerequisites'):
            planner.lease(self.store,task,'learner')
        accept(self.store,{**self.base_unit,'id':'fixture:prerequisite'})
        self.assertEqual(planner.lease(self.store,task,'learner')['status'],'leased')

    def test_misbound_paths_and_nested_child_batches_are_rejected(self):
        wrong=self.root/'wrong-paths.json'
        wrong.write_text(json.dumps({'source':str(self.root/'source'),'home':str(self.root/'another-home')}),encoding='utf-8')
        with self.assertRaisesRegex(ValueError,'another workspace'):
            dispatch.begin(self.store,self.parent,str(wrong),['optimizer'])
        batch=self.begin(['optimizer'],parallel=1)
        with self.assertRaisesRegex(ValueError,'original parent'):
            dispatch.begin(self.store,batch['children'][0]['session'],None,['optimizer'])


if __name__=='__main__':unittest.main()
