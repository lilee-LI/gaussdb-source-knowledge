# 全仓持续学习计划

快照 `snapshot:53bf0e1006c0c8ed389600202e1a97c6`；配置 `linux-native`；知识 `knowledge:742c722ab8652fa5c3e3b1e36e636058`。

范围：15629 项资产、535 个模块；状态：**incomplete**。目录归属和任务不是已学知识。

配置→全仓盘点→经审阅的机制规划→按模块持续研究→多人回收/反馈→知识审阅→覆盖与使用验收。

## 领域范围

| 领域 | 资产 |
| --- | ---: |
| build / 构建、配置与发布 | 71 |
| session / 启动、连接、会话与调度 | 146 |
| frontend / 语法、分析、绑定与重写 | 120 |
| catalog / 系统目录、DDL与依赖 | 1169 |
| optimizer / 查询优化器 | 246 |
| executor / 执行器与代码生成 | 382 |
| semantics / 类型、函数与过程语言 | 330 |
| transaction / 事务、快照与可见性 | 124 |
| storage / 页面、缓存、访问与索引 | 533 |
| recovery / WAL、恢复、复制与解码 | 217 |
| foundation / 内存、并发、缓存与公共设施 | 252 |
| security / 认证、权限与数据安全 | 103 |
| communication / 节点通信、并行与外部接口 | 179 |
| engines / 专用存储与可选引擎 | 477 |
| client / 客户端库与编程接口 | 633 |
| tools / 工具、安装与运维 | 594 |
| extensions / 扩展、插件与生态 | 1293 |
| observability / 统计、观测与资源治理 | 239 |
| documents / 文档、教程与说明 | 702 |
| tests / 测试、预期与数据资产 | 6846 |
| 待确认领域（已有模块归属） | 973 |

## 模块与持续任务


| 模块 | 资产 | 盘点审阅 | 资产状态 | 源码知识闭合 |
| --- | ---: | --- | --- | --- |
| server/@root | 25 | False | {"unreviewed":25} | False |
| server/Tools | 3 | False | {"unreviewed":3} | False |
| server/build | 25 | False | {"unreviewed":25} | False |
| server/cc_build | 3 | False | {"unreviewed":3} | False |
| server/cmake/src | 4 | False | {"unreviewed":4} | False |
| server/cmake/src/config-in | 5 | False | {"unreviewed":5} | False |
| server/config | 17 | False | {"unreviewed":17} | False |
| server/contrib | 5 | False | {"unreviewed":5} | False |
| server/contrib/adminpack | 4 | False | {"unreviewed":4} | False |
| server/contrib/auth_delay | 2 | False | {"unreviewed":2} | False |
| server/contrib/auto_explain | 2 | False | {"unreviewed":2} | False |
| server/contrib/btree_gin | 53 | False | {"unreviewed":53} | False |
| server/contrib/btree_gist | 27 | False | {"unreviewed":27} | False |
| server/contrib/btree_gist/data | 19 | False | {"unreviewed":19} | False |
| server/contrib/btree_gist/expected | 28 | False | {"unreviewed":28} | False |
| server/contrib/btree_gist/sql | 25 | False | {"unreviewed":25} | False |
| server/contrib/chkpass | 5 | False | {"unreviewed":5} | False |
| server/contrib/citext | 8 | False | {"unreviewed":8} | False |
| server/contrib/common_cipher | 13 | False | {"unreviewed":13} | False |
| server/contrib/cube | 15 | False | {"unreviewed":15} | False |
| server/contrib/dblink | 15 | False | {"unreviewed":15} | False |
| server/contrib/dict_int | 7 | False | {"unreviewed":7} | False |
| server/contrib/dict_xsyn | 8 | False | {"unreviewed":8} | False |
| server/contrib/dummy_seclabel | 3 | False | {"unreviewed":3} | False |
| server/contrib/earthdistance | 7 | False | {"unreviewed":7} | False |
| server/contrib/file_fdw | 11 | False | {"unreviewed":11} | False |
| server/contrib/fuzzystrmatch | 7 | False | {"unreviewed":7} | False |
| server/contrib/gauss_connector | 2 | False | {"unreviewed":2} | False |
| server/contrib/gc_fdw | 8 | False | {"unreviewed":8} | False |
| server/contrib/gms_assert | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_compress | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_debug | 31 | False | {"unreviewed":31} | False |
| server/contrib/gms_i18n | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_inaddr | 10 | False | {"unreviewed":10} | False |
| server/contrib/gms_lob | 13 | False | {"unreviewed":13} | False |
| server/contrib/gms_match | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_output | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_profiler | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_raw | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_sql | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_stats | 11 | False | {"unreviewed":11} | False |
| server/contrib/gms_tcp | 17 | False | {"unreviewed":17} | False |
| server/contrib/gms_utility | 10 | False | {"unreviewed":10} | False |
| server/contrib/gms_xmlgen | 9 | False | {"unreviewed":9} | False |
| server/contrib/gms_xmlparser | 9 | False | {"unreviewed":9} | False |
| server/contrib/gs_filedump | 14 | False | {"unreviewed":14} | False |
| server/contrib/gv_index | 23 | False | {"unreviewed":23} | False |
| server/contrib/hstore | 18 | False | {"unreviewed":18} | False |
| server/contrib/intagg | 4 | False | {"unreviewed":4} | False |
| server/contrib/intarray | 16 | False | {"unreviewed":16} | False |
| server/contrib/isn | 11 | False | {"unreviewed":11} | False |
| server/contrib/jieba_tokenizer | 29 | False | {"unreviewed":29} | False |
| server/contrib/jieba_tokenizer/include/cppjieba | 16 | False | {"unreviewed":16} | False |
| server/contrib/lo | 6 | False | {"unreviewed":6} | False |
| server/contrib/log_fdw | 9 | False | {"unreviewed":9} | False |
| server/contrib/ltree | 20 | False | {"unreviewed":20} | False |
| server/contrib/mppdb_decoding | 5 | False | {"unreviewed":5} | False |
| server/contrib/mysql_fdw | 1 | False | {"unreviewed":1} | False |
| server/contrib/ndpplugin | 22 | False | {"unreviewed":22} | False |
| server/contrib/nputurbo | 5 | False | {"unreviewed":5} | False |
| server/contrib/ogai | 5 | False | {"unreviewed":5} | False |
| server/contrib/oid2name | 2 | False | {"unreviewed":2} | False |
| server/contrib/oracle_fdw | 1 | False | {"unreviewed":1} | False |
| server/contrib/pagehack | 4 | False | {"unreviewed":4} | False |
| server/contrib/pageinspect | 9 | False | {"unreviewed":9} | False |
| server/contrib/passwordcheck | 2 | False | {"unreviewed":2} | False |
| server/contrib/pg_archivecleanup | 2 | False | {"unreviewed":2} | False |
| server/contrib/pg_buffercache | 5 | False | {"unreviewed":5} | False |
| server/contrib/pg_check_clog | 2 | False | {"unreviewed":2} | False |
| server/contrib/pg_check_replslot | 2 | False | {"unreviewed":2} | False |
| server/contrib/pg_freespacemap | 5 | False | {"unreviewed":5} | False |
| server/contrib/pg_standby | 2 | False | {"unreviewed":2} | False |
| server/contrib/pg_stat_statements | 7 | False | {"unreviewed":7} | False |
| server/contrib/pg_test_fsync | 2 | False | {"unreviewed":2} | False |
| server/contrib/pg_test_timing | 2 | False | {"unreviewed":2} | False |
| server/contrib/pg_trgm | 11 | False | {"unreviewed":11} | False |
| server/contrib/pg_upgrade_support | 3 | False | {"unreviewed":3} | False |
| server/contrib/pg_xlogdump | 36 | False | {"unreviewed":36} | False |
| server/contrib/pgbench | 2 | False | {"unreviewed":2} | False |
| server/contrib/pgcrypto | 52 | False | {"unreviewed":52} | False |
| server/contrib/pgcrypto/expected | 25 | False | {"unreviewed":25} | False |
| server/contrib/pgcrypto/sql | 25 | False | {"unreviewed":25} | False |
| server/contrib/pgrowlocks | 5 | False | {"unreviewed":5} | False |
| server/contrib/pgstattuple | 8 | False | {"unreviewed":8} | False |
| server/contrib/postgres_fdw | 18 | False | {"unreviewed":18} | False |
| server/contrib/rack_dev | 7 | False | {"unreviewed":7} | False |
| server/contrib/rack_dev/include | 3 | False | {"unreviewed":3} | False |
| server/contrib/security_plugin | 24 | False | {"unreviewed":24} | False |
| server/contrib/seg | 14 | False | {"unreviewed":14} | False |
| server/contrib/sepgsql | 23 | False | {"unreviewed":23} | False |
| server/contrib/shark | 20 | False | {"unreviewed":20} | False |
| server/contrib/shark/data | 1 | False | {"unreviewed":1} | False |
| server/contrib/shark/expected | 40 | False | {"unreviewed":40} | False |
| server/contrib/shark/input | 7 | False | {"unreviewed":7} | False |
| server/contrib/shark/output | 7 | False | {"unreviewed":7} | False |
| server/contrib/shark/rollback_script | 3 | False | {"unreviewed":3} | False |
| server/contrib/shark/sql | 40 | False | {"unreviewed":40} | False |
| server/contrib/shark/src | 2 | False | {"unreviewed":2} | False |
| server/contrib/shark/src/backend_parser | 24 | False | {"unreviewed":24} | False |
| server/contrib/shark/src/pltsql | 11 | False | {"unreviewed":11} | False |
| server/contrib/shark/upgrade_script | 3 | False | {"unreviewed":3} | False |
| server/contrib/spi | 27 | False | {"unreviewed":27} | False |
| server/contrib/sql_decoding | 4 | False | {"unreviewed":4} | False |
| server/contrib/sslinfo | 5 | False | {"unreviewed":5} | False |
| server/contrib/start-scripts | 6 | False | {"unreviewed":6} | False |
| server/contrib/tablefunc | 11 | False | {"unreviewed":11} | False |
| server/contrib/tcn | 4 | False | {"unreviewed":4} | False |
| server/contrib/test_decoding | 5 | False | {"unreviewed":5} | False |
| server/contrib/test_parser | 7 | False | {"unreviewed":7} | False |
| server/contrib/tsearch2 | 9 | False | {"unreviewed":9} | False |
| server/contrib/unaccent | 8 | False | {"unreviewed":8} | False |
| server/contrib/vacuumlo | 2 | False | {"unreviewed":2} | False |
| server/contrib/wal2json | 57 | False | {"unreviewed":57} | False |
| server/contrib/xml2 | 9 | False | {"unreviewed":9} | False |
| server/doc | 7 | False | {"unreviewed":7} | False |
| server/doc/src | 1 | False | {"unreviewed":1} | False |
| server/doc/src/sgml | 180 | False | {"unreviewed":180} | False |
| server/doc/src/sgml/ref | 490 | False | {"unreviewed":490} | False |
| server/docker | 21 | False | {"unreviewed":21} | False |
| server/liteom | 7 | False | {"unreviewed":7} | False |
| server/simpleInstall | 4 | False | {"unreviewed":4} | False |
| server/src | 12 | False | {"unreviewed":12} | False |
| server/src/bin | 2 | False | {"unreviewed":2} | False |
| server/src/bin/gs_cgroup | 10 | False | {"unreviewed":10} | False |
| server/src/bin/gs_guc | 10 | False | {"unreviewed":10} | False |
| server/src/bin/gs_loader | 4 | False | {"unreviewed":4} | False |
| server/src/bin/gs_log | 6 | False | {"unreviewed":6} | False |
| server/src/bin/gs_persist | 6 | False | {"unreviewed":6} | False |
| server/src/bin/gs_plan_simulator | 10 | False | {"unreviewed":10} | False |
| server/src/bin/gs_retrieve | 7 | False | {"unreviewed":7} | False |
| server/src/bin/gsqlerr | 12 | False | {"unreviewed":12} | False |
| server/src/bin/initdb | 27 | False | {"unreviewed":27} | False |
| server/src/bin/libog_query | 6 | False | {"unreviewed":6} | False |
| server/src/bin/license_checker | 5 | False | {"unreviewed":5} | False |
| server/src/bin/pg_basebackup | 24 | False | {"unreviewed":24} | False |
| server/src/bin/pg_config | 22 | False | {"unreviewed":22} | False |
| server/src/bin/pg_controldata | 18 | False | {"unreviewed":18} | False |
| server/src/bin/pg_ctl | 30 | False | {"unreviewed":30} | False |
| server/src/bin/pg_dump | 44 | False | {"unreviewed":44} | False |
| server/src/bin/pg_probackup | 76 | False | {"unreviewed":76} | False |
| server/src/bin/pg_probackup/oss/include | 6 | False | {"unreviewed":6} | False |
| server/src/bin/pg_resetxlog | 19 | False | {"unreviewed":19} | False |
| server/src/bin/pg_rewind | 17 | False | {"unreviewed":17} | False |
| server/src/bin/pg_upgrade | 3 | False | {"unreviewed":3} | False |
| server/src/bin/pgevent | 7 | False | {"unreviewed":7} | False |
| server/src/bin/pgxc_clean | 6 | False | {"unreviewed":6} | False |
| server/src/bin/psql | 58 | False | {"unreviewed":58} | False |
| server/src/bin/scripts | 38 | False | {"unreviewed":38} | False |
| server/src/bin/smb_mgr | 4 | False | {"unreviewed":4} | False |
| server/src/common | 2 | False | {"unreviewed":2} | False |
| server/src/common/backend | 2 | False | {"unreviewed":2} | False |
| server/src/common/backend/catalog | 73 | False | {"unreviewed":73} | False |
| server/src/common/backend/client_logic | 6 | False | {"unreviewed":6} | False |
| server/src/common/backend/lib | 12 | False | {"unreviewed":12} | False |
| server/src/common/backend/libpq | 20 | False | {"unreviewed":20} | False |
| server/src/common/backend/nodes | 17 | False | {"unreviewed":17} | False |
| server/src/common/backend/parser | 38 | False | {"unreviewed":38} | False |
| server/src/common/backend/pgxc_single | 24 | False | {"unreviewed":24} | False |
| server/src/common/backend/port | 59 | False | {"unreviewed":59} | False |
| server/src/common/backend/regex | 18 | False | {"unreviewed":18} | False |
| server/src/common/backend/snowball | 53 | False | {"unreviewed":53} | False |
| server/src/common/backend/tsearch | 29 | False | {"unreviewed":29} | False |
| server/src/common/backend/utils | 12 | False | {"unreviewed":12} | False |
| server/src/common/backend/utils/adt | 125 | False | {"unreviewed":125} | False |
| server/src/common/backend/utils/cache | 31 | False | {"unreviewed":31} | False |
| server/src/common/backend/utils/error | 7 | False | {"unreviewed":7} | False |
| server/src/common/backend/utils/fmgr | 6 | False | {"unreviewed":6} | False |
| server/src/common/backend/utils/gsplsql | 4 | False | {"unreviewed":4} | False |
| server/src/common/backend/utils/hash | 4 | False | {"unreviewed":4} | False |
| server/src/common/backend/utils/init | 5 | False | {"unreviewed":5} | False |
| server/src/common/backend/utils/matrix | 3 | False | {"unreviewed":3} | False |
| server/src/common/backend/utils/mb | 12 | False | {"unreviewed":12} | False |
| server/src/common/backend/utils/mb/Unicode | 100 | False | {"unreviewed":100} | False |
| server/src/common/backend/utils/mb/conversion_procs | 61 | False | {"unreviewed":61} | False |
| server/src/common/backend/utils/mb/nlssort | 4 | False | {"unreviewed":4} | False |
| server/src/common/backend/utils/misc | 30 | False | {"unreviewed":30} | False |
| server/src/common/backend/utils/mmgr | 17 | False | {"unreviewed":17} | False |
| server/src/common/backend/utils/resowner | 4 | False | {"unreviewed":4} | False |
| server/src/common/backend/utils/sort | 9 | False | {"unreviewed":9} | False |
| server/src/common/backend/utils/time | 4 | False | {"unreviewed":4} | False |
| server/src/common/interfaces | 2 | False | {"unreviewed":2} | False |
| server/src/common/interfaces/ecpg | 3 | False | {"unreviewed":3} | False |
| server/src/common/interfaces/ecpg/compatlib | 4 | False | {"unreviewed":4} | False |
| server/src/common/interfaces/ecpg/ecpglib | 31 | False | {"unreviewed":31} | False |
| server/src/common/interfaces/ecpg/include | 20 | False | {"unreviewed":20} | False |
| server/src/common/interfaces/ecpg/pgtypeslib | 12 | False | {"unreviewed":12} | False |
| server/src/common/interfaces/ecpg/preproc | 37 | False | {"unreviewed":37} | False |
| server/src/common/interfaces/ecpg/test | 9 | False | {"unreviewed":9} | False |
| server/src/common/interfaces/ecpg/test/compat_informix | 10 | False | {"unreviewed":10} | False |
| server/src/common/interfaces/ecpg/test/connect | 7 | False | {"unreviewed":7} | False |
| server/src/common/interfaces/ecpg/test/data | 1 | False | {"unreviewed":1} | False |
| server/src/common/interfaces/ecpg/test/expected | 176 | False | {"unreviewed":176} | False |
| server/src/common/interfaces/ecpg/test/performance | 2 | False | {"unreviewed":2} | False |
| server/src/common/interfaces/ecpg/test/pgtypeslib | 6 | False | {"unreviewed":6} | False |
| server/src/common/interfaces/ecpg/test/preproc | 14 | False | {"unreviewed":14} | False |
| server/src/common/interfaces/ecpg/test/sql | 21 | False | {"unreviewed":21} | False |
| server/src/common/interfaces/ecpg/test/thread | 6 | False | {"unreviewed":6} | False |
| server/src/common/interfaces/libpq | 50 | False | {"unreviewed":50} | False |
| server/src/common/interfaces/libpq/client_logic_cache | 46 | False | {"unreviewed":46} | False |
| server/src/common/interfaces/libpq/client_logic_common | 14 | False | {"unreviewed":14} | False |
| server/src/common/interfaces/libpq/client_logic_data_fetcher | 10 | False | {"unreviewed":10} | False |
| server/src/common/interfaces/libpq/client_logic_expressions | 12 | False | {"unreviewed":12} | False |
| server/src/common/interfaces/libpq/client_logic_fmt | 24 | False | {"unreviewed":24} | False |
| server/src/common/interfaces/libpq/client_logic_hooks | 18 | False | {"unreviewed":18} | False |
| server/src/common/interfaces/libpq/client_logic_processor | 31 | False | {"unreviewed":31} | False |
| server/src/common/interfaces/libpq/frontend_parser | 23 | False | {"unreviewed":23} | False |
| server/src/common/interfaces/libpq/jdbc | 17 | False | {"unreviewed":17} | False |
| server/src/common/interfaces/libpq/libpq_ce | 9 | False | {"unreviewed":9} | False |
| server/src/common/interfaces/libpq/po | 12 | False | {"unreviewed":12} | False |
| server/src/common/interfaces/libpq/test | 6 | False | {"unreviewed":6} | False |
| server/src/common/pgxc | 8 | False | {"unreviewed":8} | False |
| server/src/common/pl | 2 | False | {"unreviewed":2} | False |
| server/src/common/pl/plpgsql | 39 | False | {"unreviewed":39} | False |
| server/src/common/pl/plpython | 47 | False | {"unreviewed":47} | False |
| server/src/common/port | 66 | False | {"unreviewed":66} | False |
| server/src/common/port/port_srv | 34 | False | {"unreviewed":34} | False |
| server/src/common/template | 14 | False | {"unreviewed":14} | False |
| server/src/common/timezone | 45 | False | {"unreviewed":45} | False |
| server/src/common/tutorial | 10 | False | {"unreviewed":10} | False |
| server/src/gausskernel | 5 | False | {"unreviewed":5} | False |
| server/src/gausskernel/bootstrap | 7 | False | {"unreviewed":7} | False |
| server/src/gausskernel/cbb | 2 | False | {"unreviewed":2} | False |
| server/src/gausskernel/cbb/bbox | 31 | False | {"unreviewed":31} | False |
| server/src/gausskernel/cbb/communication | 62 | False | {"unreviewed":62} | False |
| server/src/gausskernel/cbb/extension | 18 | False | {"unreviewed":18} | False |
| server/src/gausskernel/cbb/grpc | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/cbb/instruments | 58 | False | {"unreviewed":58} | False |
| server/src/gausskernel/cbb/utils | 39 | False | {"unreviewed":39} | False |
| server/src/gausskernel/cbb/workload | 18 | False | {"unreviewed":18} | False |
| server/src/gausskernel/dbmind | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/dbmind/db4ai | 51 | False | {"unreviewed":51} | False |
| server/src/gausskernel/dbmind/deepsql | 24 | False | {"unreviewed":24} | False |
| server/src/gausskernel/dbmind/kernel | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/ddes | 21 | False | {"unreviewed":21} | False |
| server/src/gausskernel/optimizer | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/optimizer/aioptimizer | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/optimizer/commands | 72 | False | {"unreviewed":72} | False |
| server/src/gausskernel/optimizer/geqo | 17 | False | {"unreviewed":17} | False |
| server/src/gausskernel/optimizer/gplanmgr | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/optimizer/path | 15 | False | {"unreviewed":15} | False |
| server/src/gausskernel/optimizer/plan | 21 | False | {"unreviewed":21} | False |
| server/src/gausskernel/optimizer/prep | 8 | False | {"unreviewed":8} | False |
| server/src/gausskernel/optimizer/rewrite | 8 | False | {"unreviewed":8} | False |
| server/src/gausskernel/optimizer/sqladvisor | 6 | False | {"unreviewed":6} | False |
| server/src/gausskernel/optimizer/sqlpatch | 3 | True | {"deferred":2,"partial":1} | False |
| server/src/gausskernel/optimizer/statistics | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/optimizer/util | 34 | False | {"unreviewed":34} | False |
| server/src/gausskernel/po | 10 | False | {"unreviewed":10} | False |
| server/src/gausskernel/process | 2 | False | {"unreviewed":2} | False |
| server/src/gausskernel/process/datasource | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/process/globalplancache | 6 | False | {"unreviewed":6} | False |
| server/src/gausskernel/process/job | 6 | False | {"unreviewed":6} | False |
| server/src/gausskernel/process/main | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/process/postmaster | 35 | False | {"unreviewed":35} | False |
| server/src/gausskernel/process/stream | 9 | False | {"unreviewed":9} | False |
| server/src/gausskernel/process/tcop | 10 | False | {"unreviewed":10} | False |
| server/src/gausskernel/process/threadpool | 13 | False | {"unreviewed":13} | False |
| server/src/gausskernel/runtime | 2 | False | {"unreviewed":2} | False |
| server/src/gausskernel/runtime/codegen | 29 | False | {"unreviewed":29} | False |
| server/src/gausskernel/runtime/executor | 82 | False | {"unreviewed":82} | False |
| server/src/gausskernel/runtime/opfusion | 20 | False | {"unreviewed":20} | False |
| server/src/gausskernel/runtime/vecexecutor | 74 | False | {"unreviewed":74} | False |
| server/src/gausskernel/security | 57 | False | {"unreviewed":57} | False |
| server/src/gausskernel/storage | 2 | False | {"unreviewed":2} | False |
| server/src/gausskernel/storage/access | 2 | False | {"unreviewed":2} | False |
| server/src/gausskernel/storage/access/archive | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/storage/access/bloom | 7 | False | {"unreviewed":7} | False |
| server/src/gausskernel/storage/access/cbtree | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/access/common | 13 | False | {"unreviewed":13} | False |
| server/src/gausskernel/storage/access/datavec | 54 | False | {"unreviewed":54} | False |
| server/src/gausskernel/storage/access/gin | 17 | False | {"unreviewed":17} | False |
| server/src/gausskernel/storage/access/gist | 13 | False | {"unreviewed":13} | False |
| server/src/gausskernel/storage/access/hash | 12 | False | {"unreviewed":12} | False |
| server/src/gausskernel/storage/access/hbstore | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/storage/access/heap | 12 | False | {"unreviewed":12} | False |
| server/src/gausskernel/storage/access/index | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/storage/access/nbtree | 13 | False | {"unreviewed":13} | False |
| server/src/gausskernel/storage/access/obs | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/access/psort | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/access/redo | 37 | False | {"unreviewed":37} | False |
| server/src/gausskernel/storage/access/rmgrdesc | 27 | False | {"unreviewed":27} | False |
| server/src/gausskernel/storage/access/spgist | 12 | False | {"unreviewed":12} | False |
| server/src/gausskernel/storage/access/table | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/access/transam | 67 | False | {"unreviewed":67} | False |
| server/src/gausskernel/storage/access/ubtree | 13 | False | {"unreviewed":13} | False |
| server/src/gausskernel/storage/access/ubtreepcr | 11 | False | {"unreviewed":11} | False |
| server/src/gausskernel/storage/access/ustore | 28 | False | {"unreviewed":28} | False |
| server/src/gausskernel/storage/buffer | 9 | False | {"unreviewed":9} | False |
| server/src/gausskernel/storage/bulkload | 10 | False | {"unreviewed":10} | False |
| server/src/gausskernel/storage/cmgr | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/cstore | 23 | False | {"unreviewed":23} | False |
| server/src/gausskernel/storage/dorado_operation | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/dss | 5 | False | {"unreviewed":5} | False |
| server/src/gausskernel/storage/file | 9 | False | {"unreviewed":9} | False |
| server/src/gausskernel/storage/freespace | 6 | False | {"unreviewed":6} | False |
| server/src/gausskernel/storage/gs_uwal | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/storage/htap | 13 | False | {"unreviewed":13} | False |
| server/src/gausskernel/storage/ipc | 13 | False | {"unreviewed":13} | False |
| server/src/gausskernel/storage/large_object | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/lmgr | 18 | False | {"unreviewed":18} | False |
| server/src/gausskernel/storage/matrix_mem | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/mot | 2 | False | {"unreviewed":2} | False |
| server/src/gausskernel/storage/mot/core | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/storage/mot/core/concurrency_control | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/mot/core/infra | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/storage/mot/core/infra/config | 37 | False | {"unreviewed":37} | False |
| server/src/gausskernel/storage/mot/core/infra/containers | 11 | False | {"unreviewed":11} | False |
| server/src/gausskernel/storage/mot/core/infra/stats | 25 | False | {"unreviewed":25} | False |
| server/src/gausskernel/storage/mot/core/infra/synchronization | 12 | False | {"unreviewed":12} | False |
| server/src/gausskernel/storage/mot/core/memory | 67 | False | {"unreviewed":67} | False |
| server/src/gausskernel/storage/mot/core/storage | 45 | False | {"unreviewed":45} | False |
| server/src/gausskernel/storage/mot/core/system | 10 | False | {"unreviewed":10} | False |
| server/src/gausskernel/storage/mot/core/system/checkpoint | 9 | False | {"unreviewed":9} | False |
| server/src/gausskernel/storage/mot/core/system/common | 16 | False | {"unreviewed":16} | False |
| server/src/gausskernel/storage/mot/core/system/recovery | 27 | False | {"unreviewed":27} | False |
| server/src/gausskernel/storage/mot/core/system/statistics | 9 | False | {"unreviewed":9} | False |
| server/src/gausskernel/storage/mot/core/system/transaction | 14 | False | {"unreviewed":14} | False |
| server/src/gausskernel/storage/mot/core/system/transaction_logger | 34 | False | {"unreviewed":34} | False |
| server/src/gausskernel/storage/mot/core/utils | 17 | False | {"unreviewed":17} | False |
| server/src/gausskernel/storage/mot/fdw_adapter | 18 | False | {"unreviewed":18} | False |
| server/src/gausskernel/storage/mot/jit_exec | 44 | False | {"unreviewed":44} | False |
| server/src/gausskernel/storage/nvm | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/storage/page | 10 | False | {"unreviewed":10} | False |
| server/src/gausskernel/storage/remote | 4 | False | {"unreviewed":4} | False |
| server/src/gausskernel/storage/replication | 74 | False | {"unreviewed":74} | False |
| server/src/gausskernel/storage/roach | 1 | False | {"unreviewed":1} | False |
| server/src/gausskernel/storage/smgr | 27 | False | {"unreviewed":27} | False |
| server/src/gausskernel/storage/sync | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/tcap | 6 | False | {"unreviewed":6} | False |
| server/src/gausskernel/storage/test | 2 | False | {"unreviewed":2} | False |
| server/src/gausskernel/storage/xlog_share_storage | 4 | False | {"unreviewed":4} | False |
| server/src/include | 45 | False | {"unreviewed":45} | False |
| server/src/include/access | 87 | False | {"unreviewed":87} | False |
| server/src/include/access/archive | 2 | False | {"unreviewed":2} | False |
| server/src/include/access/datavec | 34 | False | {"unreviewed":34} | False |
| server/src/include/access/extreme_rto | 14 | False | {"unreviewed":14} | False |
| server/src/include/access/htap | 10 | False | {"unreviewed":10} | False |
| server/src/include/access/obs | 1 | False | {"unreviewed":1} | False |
| server/src/include/access/ondemand_extreme_rto | 9 | False | {"unreviewed":9} | False |
| server/src/include/access/parallel_recovery | 6 | False | {"unreviewed":6} | False |
| server/src/include/access/ustore | 27 | False | {"unreviewed":27} | False |
| server/src/include/alarm | 10 | False | {"unreviewed":10} | False |
| server/src/include/bin | 1 | False | {"unreviewed":1} | False |
| server/src/include/bootstrap | 1 | False | {"unreviewed":1} | False |
| server/src/include/bulkload | 7 | False | {"unreviewed":7} | False |
| server/src/include/catalog | 155 | False | {"unreviewed":155} | False |
| server/src/include/catalog/upgrade_sql/check_upgrade | 1 | False | {"unreviewed":1} | False |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 219 | False | {"unreviewed":219} | False |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 217 | False | {"unreviewed":217} | False |
| server/src/include/catalog/upgrade_sql/set_guc | 3 | False | {"unreviewed":3} | False |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 223 | False | {"unreviewed":223} | False |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 221 | False | {"unreviewed":221} | False |
| server/src/include/client_logic | 5 | False | {"unreviewed":5} | False |
| server/src/include/cm | 20 | False | {"unreviewed":20} | False |
| server/src/include/codegen | 10 | False | {"unreviewed":10} | False |
| server/src/include/commands | 48 | False | {"unreviewed":48} | False |
| server/src/include/common | 2 | False | {"unreviewed":2} | False |
| server/src/include/common/build_query | 1 | False | {"unreviewed":1} | False |
| server/src/include/common/config | 1 | False | {"unreviewed":1} | False |
| server/src/include/communication | 4 | False | {"unreviewed":4} | False |
| server/src/include/datasource | 1 | False | {"unreviewed":1} | False |
| server/src/include/datatype | 1 | False | {"unreviewed":1} | False |
| server/src/include/db4ai | 21 | False | {"unreviewed":21} | False |
| server/src/include/dbmind | 1 | False | {"unreviewed":1} | False |
| server/src/include/ddes | 18 | False | {"unreviewed":18} | False |
| server/src/include/distributelayer | 6 | False | {"unreviewed":6} | False |
| server/src/include/executor | 68 | False | {"unreviewed":68} | False |
| server/src/include/fmgr | 2 | False | {"unreviewed":2} | False |
| server/src/include/foreign | 5 | False | {"unreviewed":5} | False |
| server/src/include/gs_ledger | 5 | False | {"unreviewed":5} | False |
| server/src/include/gs_policy | 10 | False | {"unreviewed":10} | False |
| server/src/include/gs_register | 1 | False | {"unreviewed":1} | False |
| server/src/include/gssignal | 1 | False | {"unreviewed":1} | False |
| server/src/include/gstrace | 25 | False | {"unreviewed":25} | False |
| server/src/include/gtm | 54 | False | {"unreviewed":54} | False |
| server/src/include/hotpatch | 4 | False | {"unreviewed":4} | False |
| server/src/include/instruments | 23 | False | {"unreviewed":23} | False |
| server/src/include/iprange | 1 | False | {"unreviewed":1} | False |
| server/src/include/job | 3 | False | {"unreviewed":3} | False |
| server/src/include/keymgr | 25 | False | {"unreviewed":25} | False |
| server/src/include/knl | 21 | False | {"unreviewed":21} | False |
| server/src/include/lib | 13 | False | {"unreviewed":13} | False |
| server/src/include/libcomm | 1 | False | {"unreviewed":1} | False |
| server/src/include/libpq | 19 | False | {"unreviewed":19} | False |
| server/src/include/lite | 1 | False | {"unreviewed":1} | False |
| server/src/include/mb | 1 | False | {"unreviewed":1} | False |
| server/src/include/nodes | 21 | False | {"unreviewed":21} | False |
| server/src/include/opfusion | 18 | False | {"unreviewed":18} | False |
| server/src/include/optimizer | 57 | False | {"unreviewed":57} | False |
| server/src/include/parser | 29 | False | {"unreviewed":29} | False |
| server/src/include/pgxc | 24 | False | {"unreviewed":24} | False |
| server/src/include/port | 32 | False | {"unreviewed":32} | False |
| server/src/include/portability | 1 | False | {"unreviewed":1} | False |
| server/src/include/postmaster | 25 | False | {"unreviewed":25} | False |
| server/src/include/query_anomaly | 2 | False | {"unreviewed":2} | False |
| server/src/include/regex | 5 | False | {"unreviewed":5} | False |
| server/src/include/replication | 59 | False | {"unreviewed":59} | False |
| server/src/include/rewrite | 7 | False | {"unreviewed":7} | False |
| server/src/include/service | 1 | False | {"unreviewed":1} | False |
| server/src/include/snowball | 34 | False | {"unreviewed":34} | False |
| server/src/include/ssl | 5 | False | {"unreviewed":5} | False |
| server/src/include/storage | 52 | False | {"unreviewed":52} | False |
| server/src/include/storage/buf | 7 | False | {"unreviewed":7} | False |
| server/src/include/storage/cfs | 6 | False | {"unreviewed":6} | False |
| server/src/include/storage/cstore | 3 | False | {"unreviewed":3} | False |
| server/src/include/storage/dorado_operation | 1 | False | {"unreviewed":1} | False |
| server/src/include/storage/dss | 4 | False | {"unreviewed":4} | False |
| server/src/include/storage/file | 2 | False | {"unreviewed":2} | False |
| server/src/include/storage/gs_uwal | 3 | False | {"unreviewed":3} | False |
| server/src/include/storage/item | 3 | False | {"unreviewed":3} | False |
| server/src/include/storage/lock | 6 | False | {"unreviewed":6} | False |
| server/src/include/storage/mot | 4 | False | {"unreviewed":4} | False |
| server/src/include/storage/nvm | 1 | False | {"unreviewed":1} | False |
| server/src/include/storage/smgr | 8 | False | {"unreviewed":8} | False |
| server/src/include/storage/xlog_share_storage | 1 | False | {"unreviewed":1} | False |
| server/src/include/streaming | 5 | False | {"unreviewed":5} | False |
| server/src/include/tcop | 10 | False | {"unreviewed":10} | False |
| server/src/include/tde_key_management | 6 | False | {"unreviewed":6} | False |
| server/src/include/threadpool | 8 | False | {"unreviewed":8} | False |
| server/src/include/tsearch | 10 | False | {"unreviewed":10} | False |
| server/src/include/utils | 171 | False | {"unreviewed":171} | False |
| server/src/include/vecexecutor | 47 | False | {"unreviewed":47} | False |
| server/src/include/vectorsonic | 11 | False | {"unreviewed":11} | False |
| server/src/include/workload | 14 | False | {"unreviewed":14} | False |
| server/src/lib | 2 | False | {"unreviewed":2} | False |
| server/src/lib/alarm | 5 | False | {"unreviewed":5} | False |
| server/src/lib/build_query | 3 | False | {"unreviewed":3} | False |
| server/src/lib/cm_common | 11 | False | {"unreviewed":11} | False |
| server/src/lib/cm_communication | 16 | False | {"unreviewed":16} | False |
| server/src/lib/config | 3 | False | {"unreviewed":3} | False |
| server/src/lib/elog | 3 | False | {"unreviewed":3} | False |
| server/src/lib/gstrace | 26 | False | {"unreviewed":26} | False |
| server/src/lib/gstrace/common | 2 | False | {"unreviewed":2} | False |
| server/src/lib/hotpatch | 4 | False | {"unreviewed":4} | False |
| server/src/lib/page_compression | 13 | False | {"unreviewed":13} | False |
| server/src/lib/pgcommon | 3 | False | {"unreviewed":3} | False |
| server/src/makefiles | 16 | False | {"unreviewed":16} | False |
| server/src/test | 2 | False | {"unreviewed":2} | False |
| server/src/test/examples | 9 | False | {"unreviewed":9} | False |
| server/src/test/grayscale_upgrade | 1 | False | {"unreviewed":1} | False |
| server/src/test/ha | 58 | False | {"unreviewed":58} | False |
| server/src/test/ha/data | 18 | False | {"unreviewed":18} | False |
| server/src/test/ha/results | 11 | False | {"unreviewed":11} | False |
| server/src/test/ha/script | 7 | False | {"unreviewed":7} | False |
| server/src/test/ha/testcase/cascade | 11 | False | {"unreviewed":11} | False |
| server/src/test/ha/testcase/catchup_single | 3 | False | {"unreviewed":3} | False |
| server/src/test/ha/testcase/data_replication_single | 17 | False | {"unreviewed":17} | False |
| server/src/test/ha/testcase/dataqueue_single | 3 | False | {"unreviewed":3} | False |
| server/src/test/ha/testcase/decode_single | 1 | False | {"unreviewed":1} | False |
| server/src/test/ha/testcase/dms_reform | 3 | False | {"unreviewed":3} | False |
| server/src/test/ha/testcase/exrtostandbyread | 3 | False | {"unreviewed":3} | False |
| server/src/test/ha/testcase/llt_single | 8 | False | {"unreviewed":8} | False |
| server/src/test/ha/testcase/multi_standby_single | 28 | False | {"unreviewed":28} | False |
| server/src/test/ha/testcase/multi_standby_single_archive | 1 | False | {"unreviewed":1} | False |
| server/src/test/ha/testcase/multi_standby_single_shared_storage | 8 | False | {"unreviewed":8} | False |
| server/src/test/ha/testcase/multi_uwal | 2 | False | {"unreviewed":2} | False |
| server/src/test/ha/testcase/paxos_single | 5 | False | {"unreviewed":5} | False |
| server/src/test/ha/testcase/pg_rewind_single | 11 | False | {"unreviewed":11} | False |
| server/src/test/ha/testcase/secondary_single | 12 | False | {"unreviewed":12} | False |
| server/src/test/ha/testcase/slot_single | 1 | False | {"unreviewed":1} | False |
| server/src/test/ha/testcase/streaming | 6 | False | {"unreviewed":6} | False |
| server/src/test/ipv6 | 6 | False | {"unreviewed":6} | False |
| server/src/test/isolation | 51 | False | {"unreviewed":51} | False |
| server/src/test/locale | 55 | False | {"unreviewed":55} | False |
| server/src/test/mb | 18 | False | {"unreviewed":18} | False |
| server/src/test/modules | 52 | False | {"unreviewed":52} | False |
| server/src/test/mutil_ip | 14 | False | {"unreviewed":14} | False |
| server/src/test/performance | 13 | False | {"unreviewed":13} | False |
| server/src/test/regress | 80 | False | {"unreviewed":80} | False |
| server/src/test/regress/data | 278 | False | {"unreviewed":278} | False |
| server/src/test/regress/data/datanode1 | 41 | False | {"unreviewed":41} | False |
| server/src/test/regress/data/upgrade | 4 | False | {"unreviewed":4} | False |
| server/src/test/regress/expected | 1625 | False | {"unreviewed":1625} | False |
| server/src/test/regress/expected/d_format_test | 3 | False | {"unreviewed":3} | False |
| server/src/test/regress/expected/ignore | 5 | False | {"unreviewed":5} | False |
| server/src/test/regress/expected/mot | 57 | False | {"unreviewed":57} | False |
| server/src/test/regress/expected/plpgsql | 4 | False | {"unreviewed":4} | False |
| server/src/test/regress/expected/plpgsql_depend | 5 | False | {"unreviewed":5} | False |
| server/src/test/regress/expected/row_compression | 6 | False | {"unreviewed":6} | False |
| server/src/test/regress/expected/sqlldr | 1 | False | {"unreviewed":1} | False |
| server/src/test/regress/expected/ss_r | 13 | False | {"unreviewed":13} | False |
| server/src/test/regress/expected/ss_wr | 13 | False | {"unreviewed":13} | False |
| server/src/test/regress/input | 510 | False | {"unreviewed":510} | False |
| server/src/test/regress/input/mot | 2 | False | {"unreviewed":2} | False |
| server/src/test/regress/input/row_compression | 2 | False | {"unreviewed":2} | False |
| server/src/test/regress/input/sqlldr | 8 | False | {"unreviewed":8} | False |
| server/src/test/regress/jar | 11 | False | {"unreviewed":11} | False |
| server/src/test/regress/jdbc_ce_test | 8 | False | {"unreviewed":8} | False |
| server/src/test/regress/jdbc_client | 52 | False | {"unreviewed":52} | False |
| server/src/test/regress/jdbc_test | 3 | False | {"unreviewed":3} | False |
| server/src/test/regress/krbclient | 7 | False | {"unreviewed":7} | False |
| server/src/test/regress/obstools | 3 | False | {"unreviewed":3} | False |
| server/src/test/regress/output | 545 | False | {"unreviewed":545} | False |
| server/src/test/regress/output/mot | 2 | False | {"unreviewed":2} | False |
| server/src/test/regress/output/row_compression | 2 | False | {"unreviewed":2} | False |
| server/src/test/regress/output/sqlldr | 8 | False | {"unreviewed":8} | False |
| server/src/test/regress/s3bin | 1 | False | {"unreviewed":1} | False |
| server/src/test/regress/script | 11 | False | {"unreviewed":11} | False |
| server/src/test/regress/security_scripts | 4 | False | {"unreviewed":4} | False |
| server/src/test/regress/snapshots_test | 21 | False | {"unreviewed":21} | False |
| server/src/test/regress/sql | 1461 | False | {"unreviewed":1461} | False |
| server/src/test/regress/sql/d_format_test | 3 | False | {"unreviewed":3} | False |
| server/src/test/regress/sql/gs_basebackup | 6 | False | {"unreviewed":6} | False |
| server/src/test/regress/sql/ignore | 5 | False | {"unreviewed":5} | False |
| server/src/test/regress/sql/mot | 56 | False | {"unreviewed":56} | False |
| server/src/test/regress/sql/plpgsql | 4 | False | {"unreviewed":4} | False |
| server/src/test/regress/sql/plpgsql_depend | 5 | False | {"unreviewed":5} | False |
| server/src/test/regress/sql/row_compression | 6 | False | {"unreviewed":6} | False |
| server/src/test/regress/sql/sqlldr | 1 | False | {"unreviewed":1} | False |
| server/src/test/regress/sql/ss_r | 11 | False | {"unreviewed":11} | False |
| server/src/test/regress/sql/ss_wr | 10 | False | {"unreviewed":10} | False |
| server/src/test/regress/sslcert | 2 | False | {"unreviewed":2} | False |
| server/src/test/regress/sslcert_withpwd | 2 | False | {"unreviewed":2} | False |
| server/src/test/regress/stub | 5 | False | {"unreviewed":5} | False |
| server/src/test/regress/wastebin/expected | 333 | False | {"unreviewed":333} | False |
| server/src/test/regress/wastebin/input | 337 | False | {"unreviewed":337} | False |
| server/src/test/regress/wastebin/output | 332 | False | {"unreviewed":332} | False |
| server/src/test/regress/wastebin/sql | 360 | False | {"unreviewed":360} | False |
| server/src/test/ss | 12 | False | {"unreviewed":12} | False |
| server/src/test/subscription | 7 | False | {"unreviewed":7} | False |
| server/src/test/subscription/testcase | 80 | False | {"unreviewed":80} | False |
| server/src/test/thread | 3 | False | {"unreviewed":3} | False |
| server/src/test/ut | 27 | False | {"unreviewed":27} | False |
| server/src/test/ut/include | 1 | False | {"unreviewed":1} | False |
| server/src/test/whitebox | 2 | False | {"unreviewed":2} | False |
| server/src/tools | 22 | False | {"unreviewed":22} | False |
| server/src/tools/backend | 4 | False | {"unreviewed":4} | False |
| server/src/tools/editors | 2 | False | {"unreviewed":2} | False |
| server/src/tools/entab | 4 | False | {"unreviewed":4} | False |
| server/src/tools/findoidjoins | 4 | False | {"unreviewed":4} | False |
| server/src/tools/ifaddrs | 3 | False | {"unreviewed":3} | False |
| server/src/tools/make_diff | 4 | False | {"unreviewed":4} | False |
| server/src/tools/msvc | 25 | False | {"unreviewed":25} | False |
| server/src/tools/pginclude | 7 | False | {"unreviewed":7} | False |
| server/src/tools/pgindent | 7 | False | {"unreviewed":7} | False |

## 公共机制与跨域工作包

| ID | 标题 | 主责模块 | 状态 |
| --- | --- | --- | --- |
| B01 | 内存与资源寿命 | server/src/common/backend/utils/mmgr | queued / located |
| B02 | 错误、异常与断言 | server/src/common/backend/utils/error | queued / located |
| B03 | GUC与会话生效边界 | server/src/common/backend/utils/misc | queued / located |
| B04 | 并发与等待协议 | server/src/gausskernel/storage/lmgr | queued / located |
| B05 | 事务与可见性 | server/src/gausskernel/storage/access/transam | queued / located |
| B06 | 持久化与恢复 | server/src/gausskernel/storage/access/transam | queued / located |
| B07 | 系统目录与缓存 | server/src/common/backend/utils/cache | queued / located |
| B08 | 公共数据与SQL语义 | server/src/common/backend/nodes | queued / located |
| B09 | 构建、角色与接口 | server/cmake/src | queued / located |
| B10 | 观测与字段血缘 | server/src/gausskernel/cbb/instruments | queued / located |
| X01 | 查询主链 | server/src/gausskernel/process/tcop | queued / located |
| X02 | DML与事务 | server/src/gausskernel/runtime/executor | queued / located |
| X03 | DDL与缓存失效 | server/src/gausskernel/optimizer/commands | queued / located |
| X04 | 索引读写与属性 | server/src/gausskernel/optimizer/path | queued / located |
| X05 | 算子资源与取消 | server/src/gausskernel/runtime/executor | queued / located |
| X06 | 等待与事务终止 | server/src/gausskernel/storage/lmgr | queued / located |
| X07 | WAL到恢复 | server/src/gausskernel/storage/access/transam | queued / located |
| X08 | 备份、复制与角色 | server/src/gausskernel/storage/replication | queued / located |
| X09 | 解码与插件消费 | server/src/gausskernel/storage/replication | queued / located |
| X10 | 客户端与会话 | server/src/common/interfaces/libpq | queued / located |
| X11 | 工具与内核接口 | server/src/bin/pg_dump | queued / located |
| X12 | 可选引擎与扩展接入 | server/src/gausskernel/storage/mot/core/concurrency_control | queued / located |

## 当前验收缺口

```json
[
  {
    "kind": "asset_coverage",
    "count": 15629,
    "examples": [
      "server/.clang-format",
      "server/.gitattributes",
      "server/.gitignore",
      "server/.mcp.json",
      "server/CLAUDE.md",
      "server/CMakeLists.txt",
      "server/CONTRIBUTING.md",
      "server/COPYRIGHT",
      "server/GNUmakefile.in",
      "server/GNUmakefile.in_for_llt",
      "server/License",
      "server/Makefile",
      "server/README.en.md",
      "server/README.md",
      "server/Third_Party_Open_Source_Software_Notice",
      "server/Tools/memory_check/asan_report.pl",
      "server/Tools/memory_check/memleak_ignore",
      "server/Tools/memory_check/setup_memchk.sh",
      "server/aclocal.m4",
      "server/build.sh"
    ]
  },
  {
    "kind": "module_closure",
    "count": 535,
    "examples": [
      "server/@root",
      "server/Tools",
      "server/build",
      "server/cc_build",
      "server/cmake/src",
      "server/cmake/src/config-in",
      "server/config",
      "server/contrib",
      "server/contrib/adminpack",
      "server/contrib/auth_delay",
      "server/contrib/auto_explain",
      "server/contrib/btree_gin",
      "server/contrib/btree_gist",
      "server/contrib/btree_gist/data",
      "server/contrib/btree_gist/expected",
      "server/contrib/btree_gist/sql",
      "server/contrib/chkpass",
      "server/contrib/citext",
      "server/contrib/common_cipher",
      "server/contrib/cube"
    ]
  },
  {
    "kind": "candidate_disposition",
    "count": 3372,
    "examples": [
      "candidate:001689bb07ebf3b8f2f02e8b75a3f328",
      "candidate:001c99afe07a6affd24bab9b10fb86c7",
      "candidate:0022ac02cfae5988066a270e8bc97cdb",
      "candidate:0042e7705209e3699618752b55770766",
      "candidate:005d7ae424021d432667f59c65a1edaf",
      "candidate:006e9834fd0500337a5cb928c278bd3d",
      "candidate:0076fed0d9c67a63bc55ed67ba783e97",
      "candidate:007f70af5a6694defcf1f3cd8aac4872",
      "candidate:00bf4f5e72fe9a047ec8365ba5a08866",
      "candidate:00dc300f1e6050e19fb250e8dba62462",
      "candidate:00e5afb5c5bfc805560276e9178a8aa7",
      "candidate:00e80e9f8fd4eaae6e20eb0b72f0c1df",
      "candidate:00ff58dad36824c429061f29306f6b7e",
      "candidate:01041485126762076531db90860edf86",
      "candidate:0107ec60364df13bf97adfbbb6136583",
      "candidate:0116dba4e6519e027e8bda77fa5e887d",
      "candidate:0118bee8fb7cc0617bdee9b7b1a6cecc",
      "candidate:011a8d8ff1a963abf61e8c17caa76e63",
      "candidate:012aaae6048a6df5a44d5419a3e336b0",
      "candidate:0136180a5ccce2ae4904521179bb2b63"
    ]
  },
  {
    "kind": "program_item",
    "id": "B01",
    "task": "task:b718c9be5dab2a7efe82cad5b6f707bd"
  },
  {
    "kind": "program_item",
    "id": "B02",
    "task": "task:d4a534934c387cefdf1f7271f2155a94"
  },
  {
    "kind": "program_item",
    "id": "B03",
    "task": "task:60f71007b4397f005fb59c6bc347f4b8"
  },
  {
    "kind": "program_item",
    "id": "B04",
    "task": "task:f2b22149c12aa99b25407bc49fe11656"
  },
  {
    "kind": "program_item",
    "id": "B05",
    "task": "task:56c4306db030fe5fe529f96df953bc33"
  },
  {
    "kind": "program_item",
    "id": "B06",
    "task": "task:8dc21a757015ba4f31a8657900141b48"
  },
  {
    "kind": "program_item",
    "id": "B07",
    "task": "task:f7423714ece11a71e54ec132bb6be49b"
  },
  {
    "kind": "program_item",
    "id": "B08",
    "task": "task:51fefd970157a01b784fed1231f10be8"
  },
  {
    "kind": "program_item",
    "id": "B09",
    "task": "task:129688a24e5c4e42bde36174656ed93d"
  },
  {
    "kind": "program_item",
    "id": "B10",
    "task": "task:0c261d636cf3b0487cdfd30914ca22cb"
  },
  {
    "kind": "program_item",
    "id": "X01",
    "task": "task:e560406dfaeec1e874025a3b2c077fc1"
  },
  {
    "kind": "program_item",
    "id": "X02",
    "task": "task:1b58f53ed457268723e87a939704ea26"
  },
  {
    "kind": "program_item",
    "id": "X03",
    "task": "task:4d1f85f257218da9d25b1bbc3436b6d2"
  },
  {
    "kind": "program_item",
    "id": "X04",
    "task": "task:18dcbab4d6fe1e2a322190e59875691a"
  },
  {
    "kind": "program_item",
    "id": "X05",
    "task": "task:872506366ef1a0c66e880bd2d152f6e0"
  },
  {
    "kind": "program_item",
    "id": "X06",
    "task": "task:6994c6c942b42e894225dbf593e98f4b"
  },
  {
    "kind": "program_item",
    "id": "X07",
    "task": "task:e6455d7c03f6d3b5bb3ac4ec1db85d59"
  },
  {
    "kind": "program_item",
    "id": "X08",
    "task": "task:d18ca067aa78223b953d43f0befd038b"
  },
  {
    "kind": "program_item",
    "id": "X09",
    "task": "task:7e543ec3c50f008081ac8e08d35d33f9"
  },
  {
    "kind": "program_item",
    "id": "X10",
    "task": "task:1ddf32a383ba622e8d56998d5adf7882"
  },
  {
    "kind": "program_item",
    "id": "X11",
    "task": "task:924dbce393e92afb3ebae62d89d6239c"
  },
  {
    "kind": "program_item",
    "id": "X12",
    "task": "task:77259776fb3c5592dad6b05d62c4a2c3"
  },
  {
    "kind": "one_sided_contract",
    "unit": "contract:sql-patch-plan-cache-invalidation",
    "producer_modules": [
      "server/src/gausskernel/optimizer/sqlpatch"
    ],
    "consumer_modules": [
      "server/src/common/backend/utils/cache"
    ]
  },
  {
    "kind": "one_sided_contract",
    "unit": "contract:sql-patch-plan-cache-invalidation",
    "producer_modules": [
      "server/src/gausskernel/optimizer/sqlpatch"
    ],
    "consumer_modules": [
      "server/src/gausskernel/process/globalplancache"
    ]
  },
  {
    "kind": "open_gap",
    "task": "task:f467990d2a69a09688fec89746d523e9",
    "question": "sql_patch_sequence_id 的写者、递增时机与提交/回滚语义是什么？"
  },
  {
    "kind": "open_gap",
    "task": "task:f467990d2a69a09688fec89746d523e9",
    "question": "g_instance.cost_cxt.sql_patch_sequence_id 的写者、递增时机与提交/回滚语义是什么？"
  },
  {
    "kind": "open_gap",
    "task": "task:f467990d2a69a09688fec89746d523e9",
    "question": "CMake 静态目标 gausskernel_optimizer_sqlpatch 与 Makefile OBJS=sqlpatch.o 如何接入最终可执行文件，-DOBS_SERVER 是否改变本模块编译路径？"
  },
  {
    "kind": "open_gap",
    "task": "task:f467990d2a69a09688fec89746d523e9",
    "question": "SQL 可调用入口（dbe_sql_util 包装、gs_sql_patch catalog 定义）与权限模型的注册点在哪里？"
  },
  {
    "kind": "open_gap",
    "task": "task:f467990d2a69a09688fec89746d523e9",
    "question": "create/enable/drop 在 ereport(ERROR) 时 relation/tuple 如何释放，GetPatchTuple 无元组时 heap_copytuple(NULL) 的契约是什么？"
  },
  {
    "kind": "open_gap",
    "task": "task:f467990d2a69a09688fec89746d523e9",
    "question": "只读事务下 RevalidateGplanBySqlPatch 绕过序号快速返回后，是否每次 RevalidateCachedQuery 都扫描 gs_sql_patch，其性能与并发可见性边界是什么？"
  },
  {
    "kind": "open_gap",
    "task": "task:a7e9df7d9bbff1d5470d5401e991ff9b",
    "question": "非 SPI 的 GlobalPlanCache::CheckRecreateCachePlan 调用方及 hasGetLock 释放契约？"
  },
  {
    "kind": "open_gap",
    "task": "task:a7e9df7d9bbff1d5470d5401e991ff9b",
    "question": "SQL_PATCH_VERSION_NUM 数值与 workingVersionNum 设置路径？"
  },
  {
    "kind": "open_gap",
    "task": "task:a7e9df7d9bbff1d5470d5401e991ff9b",
    "question": "CopyCachedPlan+ShareInit 后 RevalidateCachedQuery 是否不提前返回？"
  },
  {
    "kind": "open_gap",
    "task": "task:a7e9df7d9bbff1d5470d5401e991ff9b",
    "question": "AbortTransaction 是否有未读到的旗标清理？"
  },
  {
    "kind": "consumer_use_cases",
    "count": 1518,
    "examples": [
      [
        "server/@root",
        "coding"
      ],
      [
        "server/@root",
        "review"
      ],
      [
        "server/@root",
        "test_generation"
      ],
      [
        "server/Tools",
        "coding"
      ],
      [
        "server/Tools",
        "review"
      ],
      [
        "server/Tools",
        "test_generation"
      ],
      [
        "server/build",
        "coding"
      ],
      [
        "server/build",
        "review"
      ],
      [
        "server/build",
        "test_generation"
      ],
      [
        "server/cc_build",
        "coding"
      ],
      [
        "server/cc_build",
        "review"
      ],
      [
        "server/cc_build",
        "test_generation"
      ],
      [
        "server/cmake/src",
        "coding"
      ],
      [
        "server/cmake/src",
        "review"
      ],
      [
        "server/cmake/src",
        "test_generation"
      ],
      [
        "server/cmake/src/config-in",
        "coding"
      ],
      [
        "server/cmake/src/config-in",
        "review"
      ],
      [
        "server/cmake/src/config-in",
        "test_generation"
      ],
      [
        "server/config",
        "coding"
      ],
      [
        "server/config",
        "review"
      ]
    ]
  }
]
```

使用 `next` 获取就绪任务，`run` 连接已有Claude按预算执行；提交后由实际审阅者review，`advance`推进下一批。`coverage`不隐藏阻断项，不自动批准知识。
