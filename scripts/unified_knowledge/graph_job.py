"""Concrete ECS producer handoff using this repository's existing compiler engine."""
import json
from pathlib import Path

from .store import atomic_write,require


def prepare(store,spec=None):
    manifest=store.get_meta('learning_inputs',{})
    cdb=manifest.get('inputs',{}).get('compile_db')
    require(cdb,'Configure the original compile_db and run start before preparing an ECS graph job')
    root=Path(__file__).resolve().parents[2]
    folder=store.home/'graph-job'
    script='''#!/bin/sh
set -eu
if [ "$#" -lt 5 ]; then
  echo "Usage: sh run-graph.sh ENGINE SOURCE ORIGINAL_COMPILE_DB WORK OUTPUT [JOBS]" >&2
  exit 2
fi
engine=$1
source=$2
cdb=$3
work=$4
output=$5
jobs=${6:-4}
exec sh "$engine/ecs.sh" build --source "$source" --compile-db "$cdb" --work "$work" --output "$output" --jobs "$jobs" --facts calls --frontend auto
'''
    atomic_write(folder/'run-graph.sh',script)
    metadata={'schema':'ecs-graph-job/v1','source_snapshot':store.get_meta('snapshot_head'),
              'original_compile_database':cdb,'producer':'ecs.sh build','frontend':'auto','facts':'calls',
              'host_inventory_is_replay_input':False,'graph_storage':'reference','compiler_execution':'not_started',
              'note':'Run on the actual Linux build host with its compiler, generated headers, macro variants and dependencies. Use the original CDB, never compile_commands.inventory.json.'}
    atomic_write(folder/'job.json',json.dumps(metadata,ensure_ascii=False,indent=2)+'\n')
    return {**metadata,'script':str(folder/'run-graph.sh'),'metadata':str(folder/'job.json'),
            'engine_to_copy':str(root),'example':'sh run-graph.sh /opt/gaussdb-source-knowledge /data/GaussDB /data/compile_commands.json /data/graph-work /data/graph-handoff 8',
            'return_files':['graph-handoff/knowledge.sqlite3','graph-handoff/run.json','graph-handoff/blobs (if present)'],
            'windows_next':'Copy the sealed handoff and matching source to Windows; set index_db to handoff/knowledge.sqlite3, graph_storage=reference, then start --refresh. This rebinds a new learning snapshot; earlier knowledge keeps its original evidence/version.'}
