"""Four-input entry points work offline without compiler or model execution."""
import json
from pathlib import Path
import tempfile
import unittest

from platform_fixture import ROOT
from unified_knowledge import assistant_session as session,project,curriculum,service,study
from unified_knowledge.store import Store


class FourInputWorkflowTests(unittest.TestCase):
    def setUp(self):
        temp=tempfile.TemporaryDirectory();self.addCleanup(temp.cleanup);self.root=Path(temp.name)
        self.source=self.root/'source';module=self.source/'src/gausskernel/optimizer/geqo';module.mkdir(parents=True)
        (module/'main.cpp').write_text('#ifdef FEATURE_A\nint choose(int n) { return n + 1; }\n#endif\n',encoding='utf8')
        (module/'unused.cpp').write_text('int orphan() { return 7; }\n',encoding='utf8')
        (module/'public.h').write_text('int choose(int);\n',encoding='utf8')
        self.manual=self.root/'manual.md';self.manual.write_text('# GEQO\nCandidate feature semantics, not verified behavior.\n',encoding='utf8')
        self.features=self.root/'features.csv';self.features.write_text('id,name,module_hint\nf1,GEQO,server/src/gausskernel/optimizer/geqo\nf2,UNKNOWN_FEATURE,\n',encoding='utf8')
        self.cdb=self.root/'compile_commands.json';self.cdb.write_text(json.dumps([
            {'directory':'/ecs/gauss','file':'src/gausskernel/optimizer/geqo/main.cpp','arguments':['c++','-DFEATURE_A','-I/ecs/gauss/src/include','-c','src/gausskernel/optimizer/geqo/main.cpp']},
            {'directory':'/ecs/gauss','file':'generated.cpp','arguments':['c++','-c','generated.cpp']}]),encoding='utf8')
        self.paths=self.root/'paths.json';self.home=self.root/'workspace'
        self.paths.write_text(json.dumps({'product':'openGauss','product_adapter':'opengauss','source':str(self.source),
            'manual':str(self.manual),'features':str(self.features),'compile_db':str(self.cdb),
            'path_maps':[{'from':'/ecs/gauss','to':str(self.source)}],'home':str(self.home),
            'module_prefixes':['server/src/gausskernel/optimizer/geqo']}),encoding='utf8')
        self.started=self.call('init')
        self.module='server/src/gausskernel/optimizer/geqo'

    def call(self,*args):
        return session.execute(session.parser().parse_args(['--paths',str(self.paths),'--session','current-host',*args]))

    def test_paths_plan_context_and_mcp_preserve_uncompiled_source(self):
        self.assertEqual(self.started['input_summary']['compile_contexts'],2)
        self.assertEqual(self.started['input_summary']['mapped_contexts'],1)
        plan=self.call('plan');self.assertTrue(Path(plan['plan']).is_file())
        self.assertEqual(plan['summary']['cpp_files'],2);self.assertFalse(plan['summary']['unassigned_cpp'])
        with Store(self.home,readonly=True) as store:
            bound=study.current(store);run=store.record('runs',bound['run'])
            self.assertEqual(run['frontend_invocations'],0)
            self.assertEqual(store.db.execute('SELECT count(*) FROM relations').fetchone()[0],0)
            manifest=service.invoke(store,'learning_inputs',{})
            self.assertFalse(manifest['capabilities']['compiler_bindings_verified'])
            contexts=service.invoke(store,'compile_contexts',{'module':self.module,'limit':1})
            self.assertEqual(contexts['total'],1);self.assertIn('FEATURE_A',contexts['items'][0]['defines'])
            self.assertEqual(contexts['compiler_validation'],'not_inferred')
            self.assertNotIn('command',contexts['items'][0])
            items=service.invoke(store,'implementation_items',{'module':self.module})
            self.assertEqual(items['total'],2)
            self.assertTrue(any(r['asset'].endswith('unused.cpp') for r in items['items']))
            pack=service.invoke(store,'get_context',{'task':'operations','module':self.module,'query':'How to observe GEQO?'})
            self.assertEqual(pack['role_context']['status'],'partial')
            names={r['name'] for r in service.tools('query')}
            self.assertNotIn('learning_batch',names);self.assertIn('learning_curriculum',names)
        task=self.call('next','--module',self.module)['task']
        read_plan=self.call('read-plan','--limit','1')
        self.assertEqual(read_plan['task'],task['id']);self.assertEqual(read_plan['receipts_created'],0)

    def test_input_update_new_snapshot_and_refresh_rebind_header(self):
        with Store(self.home,readonly=True) as store:first=curriculum.current(store)['id'];snapshot=study.current(store)['snapshot']
        self.features.write_text(self.features.read_text(encoding='utf8')+'f3,NEW_FEATURE,\n',encoding='utf8')
        result=project.start(project.settings(self.paths),False)
        self.assertEqual(result['input_summary']['feature_rows'],3)
        with Store(self.home,readonly=True) as store:
            self.assertNotEqual(first,curriculum.current(store)['id']);second=study.current(store)['snapshot']
            self.assertNotEqual(snapshot,second)
        (self.source/'src/gausskernel/optimizer/geqo/public.h').write_text('int choose(int, int);\n',encoding='utf8')
        project.start(project.settings(self.paths),True)
        with Store(self.home,readonly=True) as store:self.assertNotEqual(second,study.current(store)['snapshot'])
        with self.assertRaisesRegex(ValueError,'another source snapshot'):self.call('status')

    def test_ecs_handoff_uses_original_commands_and_cli_batch_has_private_handles(self):
        cdb_before=self.cdb.read_bytes();job=self.call('graph-job')
        self.assertTrue(Path(job['script']).is_file());self.assertFalse(job['host_inventory_is_replay_input'])
        self.assertIn('ORIGINAL_COMPILE_DB',Path(job['script']).read_text())
        self.assertEqual(self.cdb.read_bytes(),cdb_before)
        batch=self.call('batch','--module',self.module,'--parallel','2','--no-dependencies')
        self.assertEqual(len(batch['handoffs']),1)
        child=batch['handoffs'][0]
        status=self.call('batch-status','--batch',batch['batch'])
        self.assertFalse(status['model_process_started'])
        result=session.execute(session.parser().parse_args(['--home',str(self.home),'--session',child['session'],'context']))
        self.assertEqual(result['id'],child['task']['id'])
        handle=json.loads((self.home/'assistant-sessions'/child['session']/'handle.json').read_text(encoding='utf8'))
        self.assertNotIn(handle['active']['token'],json.dumps(batch))
        self.call('batch-close','--batch',batch['batch'],'--release')


if __name__=='__main__':unittest.main()
