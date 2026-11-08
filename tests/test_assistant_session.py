"""Current-conversation adapter: real native state/evidence, synthetic text only."""
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

from platform_fixture import ROOT
from unified_knowledge import assistant_session as current, planner
from unified_knowledge.store import Store
import install_claude_skill


class CurrentAssistantTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.source=self.root/'source';folder=self.source/'src/gausskernel/optimizer';folder.mkdir(parents=True)
        (folder/'cost.cpp').write_text('int adjust_cost(int cost) {\n    return cost + 1;\n}\n',encoding='utf8')
        self.manual=self.root/'manual';self.manual.mkdir()
        (self.manual/'cost.md').write_text('# Optimizer cost\nThe synthetic cost routine adds one, excluding overflow.\n使用范围：合成样本。\n',encoding='utf8')
        self.home=self.root/'home'
        result=self.call('init','--source',str(self.source),'--manual',str(self.manual),'--home',str(self.home),fresh=True)
        self.paths=result['paths'];self.module=self.call('modules','--query','优化器')['items'][0]['module']
        self.asset='server/src/gausskernel/optimizer/cost.cpp'

    def call(self,*args,sid='author',fresh=False):
        argv=['--session',sid]+([] if fresh else ['--paths',self.paths])+list(args)
        return current.execute(current.parser().parse_args(argv))

    def write(self,name,value):
        path=self.root/name;path.write_text(json.dumps(value),encoding='utf8');return str(path)

    def claim_read(self):
        task=self.call('next','--module',self.module)['task']
        ref=self.call('read','--asset',self.asset,'--start','1','--lines','200')['id']
        return task,ref

    def unit(self,ref):
        return {'id':'claim:fixture:cost','kind':'claim','title':'Synthetic cost increments by one',
                'statement':'The fixture returns cost + 1.', 'body':'Frozen synthetic source only. Development must preserve the increment. '
                'Tests should check a representable input and overflow exclusion; no database was run.',
                'conditions':['int addition remains representable'],'counterexamples':['INT_MAX is outside this claim'],
                'source_refs':[ref],'symbol_refs':[],'knowledge_refs':[]}

    def submit_knowledge(self):
        task,ref=self.claim_read();unit=self.unit(ref)
        self.call('unit','--input',self.write('unit.json',unit))
        self.call('progress','--input',self.write('progress.json',{'inventory_complete':True,'assets':[
            {'asset':self.asset,'disposition':'studied','reason':'Full three-line synthetic source read and explained',
             'evidence_refs':[ref],'unit_ids':[unit['id']]}]}))
        result=self.call('submit','--input',self.write('coverage.json',[{'question':'How does the fixture change cost?',
            'status':'answered','explanation':'The entire synthetic function was read; signed overflow excluded','evidence_refs':[ref]}]))
        return task,result

    def test_source_manual_init_plan_and_safe_current_session(self):
        plan=self.call('plan');self.assertTrue(Path(plan['plan']).is_file())
        docs=self.call('materials');self.assertEqual(docs['total'],1)
        self.assertEqual(docs['items'][0]['kind'],'document')
        with self.assertRaisesRegex(ValueError,'1..200'):self.call('modules','--offset','-1')
        with self.assertRaisesRegex(ValueError,'separate|分开'):
            self.call('init','--source',str(self.source),'--home',str(self.source/'output'),fresh=True)
        # Same logical session may be safely initialized again without replacing its handle.
        self.call('init');claimed=self.call('next','--module',self.module)
        self.assertTrue(claimed['task']['capabilities']['source_only'])
        self.assertFalse(claimed['task']['capabilities']['compiler_graph'])
        resumed=self.call('next','--module',self.module);self.assertEqual(resumed['state'],'resumed')
        self.assertEqual(resumed['task']['attempt'],claimed['task']['attempt'])
        self.assertNotIn('"token"',json.dumps(claimed))
        self.assertFalse(self.call('symbols','--query','adjust_cost')['available'])
        self.assertEqual(self.call('assets')['total'],1)
        doc_ref=self.call('read','--asset',docs['items'][0]['asset'])['id']
        self.assertTrue(doc_ref.startswith('evidence:'))
        raw=subprocess.check_output([sys.executable,str(ROOT/'scripts/claude_session.py'),'--paths',self.paths,
            '--session','author','read','--asset',docs['items'][0]['asset']],cwd=ROOT,
            env={**os.environ,'PYTHONIOENCODING':'cp1252'})
        self.assertIn('使用范围',json.loads(raw.decode('utf-8'))['text'])

    def test_search_is_not_read_and_source_only_cannot_forge_compiler_facts(self):
        self.call('next','--module',self.module)
        hit=self.call('search','--query','return cost')['matches'][0]
        with self.assertRaisesRegex(ValueError,'not fully read'):
            self.call('unit','--input',self.write('unread.json',self.unit(hit['evidence'])))
        ref=self.call('read','--asset',self.asset)['id']
        for extra in ({'symbol_refs':['invented-symbol']},{'kind':'contract'},
                      {'kind':'flow','steps':[{'kind':'call','symbol':'fake','target':'fake'}]}):
            with self.subTest(extra=extra):
                with self.assertRaisesRegex(ValueError,'no compiler symbol'):
                    self.call('unit','--input',self.write('bad.json',{**self.unit(ref),**extra}))
        good=self.call('unit','--input',self.write('good.json',self.unit(ref)))
        self.assertEqual(good['semantic_approval'],'not_granted')
        self.assertEqual(self.call('drafts')['items'][0]['unit_hash'],good['unit_hash'])

    def test_actual_two_reviews_wiki_and_three_consumer_queries(self):
        task,result=self.submit_knowledge()
        self.assertEqual(result['status'],'submitted');self.assertEqual(self.call('next')['state'],'awaiting_review')
        with self.assertRaisesRegex(ValueError,'已审入库'):self.call('wiki')
        preview=self.call('review');self.assertEqual(preview['stage'],'research')
        self.assertEqual(preview['review_mode'],'self_reviewed')
        with self.assertRaisesRegex(ValueError,'--self-review'):
            self.call('review','--accept',preview['digest'],'--notes','A same-session actual source check')
        proposed=self.call('review','--accept',preview['digest'],'--notes','Synthetic source, inputs and excluded overflow checked','--self-review')
        self.assertEqual(proposed['stage'],'knowledge');self.assertNotEqual(preview['digest'],proposed['digest'])
        with self.assertRaisesRegex(ValueError,'changed'):
            self.call('review','--accept',preview['digest'],'--notes','Stale digest must fail','--self-review')
        accepted=self.call('review','--accept',proposed['digest'],'--notes','Exact proposed unit and evidence checked','--self-review')
        self.assertEqual(accepted['status'],'knowledge_accepted');self.assertFalse(accepted['human_expert_review'])
        wiki=self.call('wiki');self.assertTrue(Path(wiki['wiki']).is_file());self.assertTrue(Path(wiki['markdown']).is_file())
        for role in ('coding','test_generation','review'):
            found=self.call('ask','--role',role,'--question','Synthetic cost increments by one')
            self.assertIn('claim:fixture:cost',json.dumps(found))
        with Store(self.home) as store:
            self.assertEqual(store.units()['claim:fixture:cost']['review']['mode'],'self_reviewed')

    def test_expiry_new_attempt_rereads_and_cannot_steal_another_live_token(self):
        task,ref=self.claim_read();tid=task['id']
        with Store(self.home) as store:
            store.db.execute('UPDATE tasks SET deadline=? WHERE id=?',(time.time()-1,tid));store.db.commit()
        reclaimed=self.call('next');self.assertEqual(reclaimed['state'],'reclaimed')
        self.assertEqual(reclaimed['task']['attempt'],task['attempt']+1)
        with self.assertRaisesRegex(ValueError,'not fully read'):
            self.call('unit','--input',self.write('old-evidence.json',self.unit(ref)))
        self.call('read','--asset',self.asset)
        self.call('unit','--input',self.write('fresh-evidence.json',self.unit(ref)))
        with Store(self.home) as store:
            store.db.execute('UPDATE tasks SET deadline=? WHERE id=?',(time.time()-1,tid));store.db.commit()
            planner.lease(store,tid,'someone-else',seconds=14400)
        with self.assertRaisesRegex(ValueError,'cannot reclaim another lease'):self.call('next')

    def test_planning_only_uses_native_progress_review_and_bounded_mechanisms(self):
        task,ref=self.claim_read()
        report={'inventory_complete':True,'assets':[{'asset':self.asset,'disposition':'deferred','reason':'Inventory only; mechanism awaits follow-up',
                'evidence_refs':[ref],'unit_ids':[]}], 'proposals':[{'id':'cost-boundary','title':'Cost update boundary',
                'question':'Which inputs preserve the increment?', 'owner_module':self.module,'reason':'One bounded mechanism, not per function',
                'evidence':[{'asset':self.asset,'start':1,'end':3}]}]}
        self.call('progress','--input',self.write('planning.json',report))
        finished=self.call('submit','--input',self.write('coverage.json',[{'question':'What next?', 'status':'answered',
            'explanation':'Frozen synthetic function supports a bounded follow-up','evidence_refs':[ref]}]))
        self.assertEqual(finished['units'],0)
        self.call('init',sid='other-review-session')
        preview=self.call('review','--task',task['id'],sid='other-review-session')
        self.assertEqual(preview['review_mode'],'independent_review');self.assertFalse(preview['human_expert_review'])
        accepted=self.call('review','--task',task['id'],'--accept',preview['digest'],'--notes','Actually checked synthetic source and proposal',sid='other-review-session')
        self.assertEqual(accepted['status'],'planning_accepted')
        nxt=self.call('next','--module',self.module);self.assertEqual(nxt['state'],'claimed')
        self.assertNotEqual(nxt['task']['id'],task['id'])
        with Store(self.home) as store:
            self.assertFalse(store.get_meta('knowledge_head'))

    def test_loader_installer_is_idempotent_and_preserves_unrelated_settings(self):
        target=self.root/'isolated-claude/skills';unrelated=target.parent/'settings.json'
        unrelated.parent.mkdir(parents=True);unrelated.write_text('{"model":"leave-config-alone"}',encoding='utf8')
        first=install_claude_skill.install(target);self.assertEqual(first,install_claude_skill.install(target))
        skill=Path(first['skill']);text=skill.read_text(encoding='utf8')
        self.assertIn(ROOT.as_posix(),text);self.assertIn('${CLAUDE_SESSION_ID}',text)
        self.assertNotIn('context: fork',text);self.assertEqual(unrelated.read_text(encoding='utf8'),'{"model":"leave-config-alone"}')
        skill.write_text('another preexisting skill',encoding='utf8')
        with self.assertRaisesRegex(ValueError,'existing skill differs'):install_claude_skill.install(target)
        self.assertEqual(skill.read_text(encoding='utf8'),'another preexisting skill')


if __name__=='__main__':unittest.main()
