# 全仓持续学习计划

快照 `snapshot:e3c7591bc57779ef711950941aa64146`；配置 `declared-build`；知识 `knowledge:9e4ee092006998e86d257dfc0032055f`。

范围：15217 项资产、537 个模块；状态：**incomplete**。目录归属和任务不是已学知识。

配置→全仓盘点→经审阅的机制规划→按模块持续研究→多人回收/反馈→知识审阅→覆盖与使用验收。

## 领域范围

| 领域 | 资产 |
| --- | ---: |
| build / 构建、配置与发布 | 66 |
| session / 启动、连接、会话与调度 | 144 |
| frontend / 语法、分析、绑定与重写 | 110 |
| catalog / 系统目录、DDL与依赖 | 1164 |
| optimizer / 查询优化器 | 246 |
| executor / 执行器与代码生成 | 382 |
| semantics / 类型、函数与过程语言 | 321 |
| transaction / 事务、快照与可见性 | 124 |
| storage / 页面、缓存、访问与索引 | 531 |
| recovery / WAL、恢复、复制与解码 | 208 |
| foundation / 内存、并发、缓存与公共设施 | 208 |
| security / 认证、权限与数据安全 | 102 |
| communication / 节点通信、并行与外部接口 | 179 |
| engines / 专用存储与可选引擎 | 476 |
| client / 客户端库与编程接口 | 587 |
| tools / 工具、安装与运维 | 558 |
| extensions / 扩展、插件与生态 | 1251 |
| observability / 统计、观测与资源治理 | 217 |
| documents / 文档、教程与说明 | 460 |
| tests / 测试、预期与数据资产 | 6925 |
| 待确认领域（已有模块归属） | 958 |

## 模块与持续任务


| 模块 | 资产 | 盘点审阅 | 资产状态 | 源码知识闭合 |
| --- | ---: | --- | --- | --- |
| compile_database/@materials | 1 | False | {"unreviewed":1} | False |
| historical_features/@materials | 1 | False | {"unreviewed":1} | False |
| manual/@materials | 1 | False | {"unreviewed":1} | False |
| server/@root | 22 | False | {"unreviewed":22} | False |
| server/Tools | 3 | False | {"unreviewed":3} | False |
| server/build | 23 | False | {"unreviewed":23} | False |
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
| server/contrib/gms_tcp | 18 | False | {"unreviewed":18} | False |
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
| server/contrib/pagehack | 3 | False | {"unreviewed":3} | False |
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
| server/contrib/pg_xlogdump | 6 | False | {"unreviewed":6} | False |
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
| server/contrib/shark | 17 | False | {"unreviewed":17} | False |
| server/contrib/shark/data | 1 | False | {"unreviewed":1} | False |
| server/contrib/shark/expected | 40 | False | {"unreviewed":40} | False |
| server/contrib/shark/input | 7 | False | {"unreviewed":7} | False |
| server/contrib/shark/output | 7 | False | {"unreviewed":7} | False |
| server/contrib/shark/rollback_script | 3 | False | {"unreviewed":3} | False |
| server/contrib/shark/sql | 40 | False | {"unreviewed":40} | False |
| server/contrib/shark/src | 2 | False | {"unreviewed":2} | False |
| server/contrib/shark/src/backend_parser | 17 | False | {"unreviewed":17} | False |
| server/contrib/shark/src/pltsql | 8 | False | {"unreviewed":8} | False |
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
| server/doc | 10 | False | {"unreviewed":10} | False |
| server/doc/src | 1 | False | {"unreviewed":1} | False |
| server/doc/src/sgml | 180 | False | {"unreviewed":180} | False |
| server/doc/src/sgml/ref | 246 | False | {"unreviewed":246} | False |
| server/docker | 23 | False | {"unreviewed":23} | False |
| server/liteom | 7 | False | {"unreviewed":7} | False |
| server/simpleInstall | 4 | False | {"unreviewed":4} | False |
| server/src | 12 | False | {"unreviewed":12} | False |
| server/src/bin | 2 | False | {"unreviewed":2} | False |
| server/src/bin/gs_cgroup | 8 | False | {"unreviewed":8} | False |
| server/src/bin/gs_guc | 10 | False | {"unreviewed":10} | False |
| server/src/bin/gs_loader | 4 | False | {"unreviewed":4} | False |
| server/src/bin/gs_log | 6 | False | {"unreviewed":6} | False |
| server/src/bin/gs_persist | 6 | False | {"unreviewed":6} | False |
| server/src/bin/gs_plan_simulator | 10 | False | {"unreviewed":10} | False |
| server/src/bin/gs_retrieve | 4 | False | {"unreviewed":4} | False |
| server/src/bin/gsqlerr | 6 | False | {"unreviewed":6} | False |
| server/src/bin/initdb | 23 | False | {"unreviewed":23} | False |
| server/src/bin/libog_query | 8 | False | {"unreviewed":8} | False |
| server/src/bin/license_checker | 5 | False | {"unreviewed":5} | False |
| server/src/bin/pg_basebackup | 22 | False | {"unreviewed":22} | False |
| server/src/bin/pg_config | 22 | False | {"unreviewed":22} | False |
| server/src/bin/pg_controldata | 17 | False | {"unreviewed":17} | False |
| server/src/bin/pg_ctl | 26 | False | {"unreviewed":26} | False |
| server/src/bin/pg_dump | 43 | False | {"unreviewed":43} | False |
| server/src/bin/pg_probackup | 66 | False | {"unreviewed":66} | False |
| server/src/bin/pg_probackup/oss/include | 6 | False | {"unreviewed":6} | False |
| server/src/bin/pg_resetxlog | 18 | False | {"unreviewed":18} | False |
| server/src/bin/pg_rewind | 17 | False | {"unreviewed":17} | False |
| server/src/bin/pg_upgrade | 3 | False | {"unreviewed":3} | False |
| server/src/bin/pgevent | 7 | False | {"unreviewed":7} | False |
| server/src/bin/pgxc_clean | 6 | False | {"unreviewed":6} | False |
| server/src/bin/psql | 52 | False | {"unreviewed":52} | False |
| server/src/bin/scripts | 38 | False | {"unreviewed":38} | False |
| server/src/bin/smb_mgr | 3 | False | {"unreviewed":3} | False |
| server/src/common | 2 | False | {"unreviewed":2} | False |
| server/src/common/backend | 2 | False | {"unreviewed":2} | False |
| server/src/common/backend/catalog | 69 | False | {"unreviewed":69} | False |
| server/src/common/backend/client_logic | 5 | False | {"unreviewed":5} | False |
| server/src/common/backend/lib | 12 | False | {"unreviewed":12} | False |
| server/src/common/backend/libpq | 20 | False | {"unreviewed":20} | False |
| server/src/common/backend/nodes | 17 | False | {"unreviewed":17} | False |
| server/src/common/backend/parser | 31 | False | {"unreviewed":31} | False |
| server/src/common/backend/pgxc_single | 24 | False | {"unreviewed":24} | False |
| server/src/common/backend/port | 54 | False | {"unreviewed":54} | False |
| server/src/common/backend/regex | 18 | False | {"unreviewed":18} | False |
| server/src/common/backend/snowball | 53 | False | {"unreviewed":53} | False |
| server/src/common/backend/tsearch | 29 | False | {"unreviewed":29} | False |
| server/src/common/backend/utils | 7 | False | {"unreviewed":7} | False |
| server/src/common/backend/utils/adt | 121 | False | {"unreviewed":121} | False |
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
| server/src/common/backend/utils/misc | 29 | False | {"unreviewed":29} | False |
| server/src/common/backend/utils/mmgr | 17 | False | {"unreviewed":17} | False |
| server/src/common/backend/utils/resowner | 4 | False | {"unreviewed":4} | False |
| server/src/common/backend/utils/sort | 9 | False | {"unreviewed":9} | False |
| server/src/common/backend/utils/time | 4 | False | {"unreviewed":4} | False |
| server/src/common/interfaces | 2 | False | {"unreviewed":2} | False |
| server/src/common/interfaces/ecpg | 3 | False | {"unreviewed":3} | False |
| server/src/common/interfaces/ecpg/compatlib | 4 | False | {"unreviewed":4} | False |
| server/src/common/interfaces/ecpg/ecpglib | 27 | False | {"unreviewed":27} | False |
| server/src/common/interfaces/ecpg/include | 20 | False | {"unreviewed":20} | False |
| server/src/common/interfaces/ecpg/pgtypeslib | 11 | False | {"unreviewed":11} | False |
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
| server/src/common/interfaces/libpq | 28 | False | {"unreviewed":28} | False |
| server/src/common/interfaces/libpq/client_logic_cache | 46 | False | {"unreviewed":46} | False |
| server/src/common/interfaces/libpq/client_logic_common | 14 | False | {"unreviewed":14} | False |
| server/src/common/interfaces/libpq/client_logic_data_fetcher | 10 | False | {"unreviewed":10} | False |
| server/src/common/interfaces/libpq/client_logic_expressions | 12 | False | {"unreviewed":12} | False |
| server/src/common/interfaces/libpq/client_logic_fmt | 24 | False | {"unreviewed":24} | False |
| server/src/common/interfaces/libpq/client_logic_hooks | 18 | False | {"unreviewed":18} | False |
| server/src/common/interfaces/libpq/client_logic_processor | 31 | False | {"unreviewed":31} | False |
| server/src/common/interfaces/libpq/frontend_parser | 13 | False | {"unreviewed":13} | False |
| server/src/common/interfaces/libpq/jdbc | 17 | False | {"unreviewed":17} | False |
| server/src/common/interfaces/libpq/po | 12 | False | {"unreviewed":12} | False |
| server/src/common/interfaces/libpq/test | 6 | False | {"unreviewed":6} | False |
| server/src/common/pgxc | 8 | False | {"unreviewed":8} | False |
| server/src/common/pl | 2 | False | {"unreviewed":2} | False |
| server/src/common/pl/plpgsql | 34 | False | {"unreviewed":34} | False |
| server/src/common/pl/plpython | 47 | False | {"unreviewed":47} | False |
| server/src/common/port | 65 | False | {"unreviewed":65} | False |
| server/src/common/template | 14 | False | {"unreviewed":14} | False |
| server/src/common/timezone | 45 | False | {"unreviewed":45} | False |
| server/src/common/tutorial | 10 | False | {"unreviewed":10} | False |
| server/src/gausskernel | 5 | False | {"unreviewed":5} | False |
| server/src/gausskernel/bootstrap | 5 | False | {"unreviewed":5} | False |
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
| server/src/gausskernel/optimizer/geqo | 17 | True | {"deferred":13,"studied":4} | False |
| server/src/gausskernel/optimizer/gplanmgr | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/optimizer/path | 15 | False | {"unreviewed":15} | False |
| server/src/gausskernel/optimizer/plan | 21 | False | {"unreviewed":21} | False |
| server/src/gausskernel/optimizer/prep | 8 | False | {"unreviewed":8} | False |
| server/src/gausskernel/optimizer/rewrite | 8 | False | {"unreviewed":8} | False |
| server/src/gausskernel/optimizer/sqladvisor | 6 | False | {"unreviewed":6} | False |
| server/src/gausskernel/optimizer/sqlpatch | 3 | False | {"unreviewed":3} | False |
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
| server/src/gausskernel/runtime/codegen | 31 | False | {"unreviewed":31} | False |
| server/src/gausskernel/runtime/executor | 80 | False | {"unreviewed":80} | False |
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
| server/src/gausskernel/storage/lmgr | 16 | False | {"unreviewed":16} | False |
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
| server/src/gausskernel/storage/replication | 67 | False | {"unreviewed":67} | False |
| server/src/gausskernel/storage/roach | 1 | False | {"unreviewed":1} | False |
| server/src/gausskernel/storage/smgr | 27 | False | {"unreviewed":27} | False |
| server/src/gausskernel/storage/sync | 3 | False | {"unreviewed":3} | False |
| server/src/gausskernel/storage/tcap | 6 | False | {"unreviewed":6} | False |
| server/src/gausskernel/storage/test | 2 | False | {"unreviewed":2} | False |
| server/src/gausskernel/storage/xlog_share_storage | 3 | False | {"unreviewed":3} | False |
| server/src/include | 43 | False | {"unreviewed":43} | False |
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
| server/src/include/catalog | 154 | False | {"unreviewed":154} | False |
| server/src/include/catalog/upgrade_sql/check_upgrade | 1 | False | {"unreviewed":1} | False |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 219 | False | {"unreviewed":219} | False |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 217 | False | {"unreviewed":217} | False |
| server/src/include/catalog/upgrade_sql/set_guc | 3 | False | {"unreviewed":3} | False |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 223 | False | {"unreviewed":223} | False |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 221 | False | {"unreviewed":221} | False |
| server/src/include/client_logic | 5 | False | {"unreviewed":5} | False |
| server/src/include/cm | 19 | False | {"unreviewed":19} | False |
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
| server/src/include/gstrace | 3 | False | {"unreviewed":3} | False |
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
| server/src/include/parser | 26 | False | {"unreviewed":26} | False |
| server/src/include/pgxc | 24 | False | {"unreviewed":24} | False |
| server/src/include/port | 32 | False | {"unreviewed":32} | False |
| server/src/include/portability | 1 | False | {"unreviewed":1} | False |
| server/src/include/postmaster | 25 | False | {"unreviewed":25} | False |
| server/src/include/query_anomaly | 2 | False | {"unreviewed":2} | False |
| server/src/include/regex | 5 | False | {"unreviewed":5} | False |
| server/src/include/replication | 57 | False | {"unreviewed":57} | False |
| server/src/include/rewrite | 7 | False | {"unreviewed":7} | False |
| server/src/include/service | 1 | False | {"unreviewed":1} | False |
| server/src/include/snowball | 34 | False | {"unreviewed":34} | False |
| server/src/include/ssl | 5 | False | {"unreviewed":5} | False |
| server/src/include/storage | 51 | False | {"unreviewed":51} | False |
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
| server/src/include/utils | 168 | False | {"unreviewed":168} | False |
| server/src/include/vecexecutor | 47 | False | {"unreviewed":47} | False |
| server/src/include/vectorsonic | 11 | False | {"unreviewed":11} | False |
| server/src/include/workload | 14 | False | {"unreviewed":14} | False |
| server/src/lib | 2 | False | {"unreviewed":2} | False |
| server/src/lib/alarm | 5 | False | {"unreviewed":5} | False |
| server/src/lib/build_query | 3 | False | {"unreviewed":3} | False |
| server/src/lib/cm_common | 10 | False | {"unreviewed":10} | False |
| server/src/lib/cm_communication | 16 | False | {"unreviewed":16} | False |
| server/src/lib/config | 3 | False | {"unreviewed":3} | False |
| server/src/lib/elog | 3 | False | {"unreviewed":3} | False |
| server/src/lib/gstrace | 26 | False | {"unreviewed":26} | False |
| server/src/lib/gstrace/common | 2 | False | {"unreviewed":2} | False |
| server/src/lib/hotpatch | 4 | False | {"unreviewed":4} | False |
| server/src/lib/page_compression | 6 | False | {"unreviewed":6} | False |
| server/src/lib/pgcommon | 3 | False | {"unreviewed":3} | False |
| server/src/makefiles | 16 | False | {"unreviewed":16} | False |
| server/src/test | 2 | False | {"unreviewed":2} | False |
| server/src/test/examples | 9 | False | {"unreviewed":9} | False |
| server/src/test/grayscale_upgrade | 1 | False | {"unreviewed":1} | False |
| server/src/test/ha | 58 | False | {"unreviewed":58} | False |
| server/src/test/ha/data | 20 | False | {"unreviewed":20} | False |
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
| server/src/test/isolation | 49 | False | {"unreviewed":49} | False |
| server/src/test/locale | 55 | False | {"unreviewed":55} | False |
| server/src/test/mb | 18 | False | {"unreviewed":18} | False |
| server/src/test/modules | 52 | False | {"unreviewed":52} | False |
| server/src/test/mutil_ip | 14 | False | {"unreviewed":14} | False |
| server/src/test/performance | 13 | False | {"unreviewed":13} | False |
| server/src/test/regress | 81 | False | {"unreviewed":81} | False |
| server/src/test/regress/data | 282 | False | {"unreviewed":282} | False |
| server/src/test/regress/data/datanode1 | 57 | False | {"unreviewed":57} | False |
| server/src/test/regress/data/pgbench | 2 | False | {"unreviewed":2} | False |
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
| server/src/test/regress/jar | 33 | False | {"unreviewed":33} | False |
| server/src/test/regress/jdbc_ce_test | 16 | False | {"unreviewed":16} | False |
| server/src/test/regress/jdbc_client | 52 | False | {"unreviewed":52} | False |
| server/src/test/regress/jdbc_client_lib | 1 | False | {"unreviewed":1} | False |
| server/src/test/regress/jdbc_test | 7 | False | {"unreviewed":7} | False |
| server/src/test/regress/krbclient | 20 | False | {"unreviewed":20} | False |
| server/src/test/regress/obstools | 4 | False | {"unreviewed":4} | False |
| server/src/test/regress/output | 545 | False | {"unreviewed":545} | False |
| server/src/test/regress/output/mot | 2 | False | {"unreviewed":2} | False |
| server/src/test/regress/output/row_compression | 2 | False | {"unreviewed":2} | False |
| server/src/test/regress/output/sqlldr | 8 | False | {"unreviewed":8} | False |
| server/src/test/regress/s3bin | 2 | False | {"unreviewed":2} | False |
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
| server/src/tools/backend | 5 | False | {"unreviewed":5} | False |
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
    "count": 15205,
    "examples": [
      "compile_database/compile_commands.json",
      "historical_features/historical-features.csv",
      "manual/connection-settings.html",
      "server/.clang-format",
      "server/.gitattributes",
      "server/.gitignore",
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
      "server/aclocal.m4"
    ]
  },
  {
    "kind": "module_closure",
    "count": 537,
    "examples": [
      "compile_database/@materials",
      "historical_features/@materials",
      "manual/@materials",
      "server/@root",
      "server/Tools",
      "server/build",
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
      "server/contrib/citext"
    ]
  },
  {
    "kind": "candidate_disposition",
    "count": 3373,
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
    "task": "task:7b8dfaafcba1f04932e3fa5759c306a7"
  },
  {
    "kind": "program_item",
    "id": "B02",
    "task": "task:3e4332cff542910b72d9e42690a4d3ca"
  },
  {
    "kind": "program_item",
    "id": "B03",
    "task": "task:28f32bdb0efc8a4f9e0d3e71ff434489"
  },
  {
    "kind": "program_item",
    "id": "B04",
    "task": "task:260dc4a160d537e57dd7c187d25a96e2"
  },
  {
    "kind": "program_item",
    "id": "B05",
    "task": "task:58622faa48080f656325bc01f3116f48"
  },
  {
    "kind": "program_item",
    "id": "B06",
    "task": "task:1c7571d75cc3fd7ffb80d6a530cbb82a"
  },
  {
    "kind": "program_item",
    "id": "B07",
    "task": "task:09356525981f2da00934e2c0a5246e01"
  },
  {
    "kind": "program_item",
    "id": "B08",
    "task": "task:29cf648b7dc49eafb7b572d1279efa7c"
  },
  {
    "kind": "program_item",
    "id": "B09",
    "task": "task:3aba1d888922f0fc5860b5964480fe9e"
  },
  {
    "kind": "program_item",
    "id": "B10",
    "task": "task:ca94a38e2f4601f3892e261052a77e8f"
  },
  {
    "kind": "program_item",
    "id": "X01",
    "task": "task:4618c1c5cdc6aa06d4d0928e019eaa92"
  },
  {
    "kind": "program_item",
    "id": "X02",
    "task": "task:187c113b12bd7d4c7dfbe90562d0bbef"
  },
  {
    "kind": "program_item",
    "id": "X03",
    "task": "task:cbf338de12911036e83ca4c0f990387d"
  },
  {
    "kind": "program_item",
    "id": "X04",
    "task": "task:3851e4489e878e756a2f19a0cae99638"
  },
  {
    "kind": "program_item",
    "id": "X05",
    "task": "task:e6034a301549365a6128c2b593634400"
  },
  {
    "kind": "program_item",
    "id": "X06",
    "task": "task:8d21b9bca3e9d5917b00cfd98665aa29"
  },
  {
    "kind": "program_item",
    "id": "X07",
    "task": "task:ddf3c4edaefbd1996dbe38f9fed0202d"
  },
  {
    "kind": "program_item",
    "id": "X08",
    "task": "task:5211d02851f6444bb7caa4fd7f67b9de"
  },
  {
    "kind": "program_item",
    "id": "X09",
    "task": "task:8babd777260ee0203c3ac1ba1458dd1c"
  },
  {
    "kind": "program_item",
    "id": "X10",
    "task": "task:aa2f0b6ed66adb4922e2f88bd2419b0a"
  },
  {
    "kind": "program_item",
    "id": "X11",
    "task": "task:983fe3a16f866227bd7d7c49a87cfb93"
  },
  {
    "kind": "program_item",
    "id": "X12",
    "task": "task:40c1c18f977140aee1209f93d8217562"
  },
  {
    "kind": "open_gap",
    "task": "task:38ad7ecb51cadb0091359cbb5c53b76a",
    "question": "15 个 GEQO .cpp 实际对应哪些编译上下文，构建时启用哪些宏？"
  },
  {
    "kind": "open_gap",
    "task": "task:38ad7ecb51cadb0091359cbb5c53b76a",
    "question": "实际选中的交叉算子宏是哪一个？"
  },
  {
    "kind": "open_gap",
    "task": "task:38ad7ecb51cadb0091359cbb5c53b76a",
    "question": "GEQO 是否有对应产品手册页及其承诺？"
  },
  {
    "kind": "open_gap",
    "task": "task:38ad7ecb51cadb0091359cbb5c53b76a",
    "question": "历史特性 feature:9de1d11c1df26047a9d7a49ec7caa95c 的边界与映射？"
  },
  {
    "kind": "open_gap",
    "task": "task:38ad7ecb51cadb0091359cbb5c53b76a",
    "question": "geqo*.h 头文件中的结构、常量与默认宏如何定义？"
  },
  {
    "kind": "open_gap",
    "task": "task:38ad7ecb51cadb0091359cbb5c53b76a",
    "question": "geqo() 由谁、在什么条件下被调用？"
  },
  {
    "kind": "open_gap",
    "task": "task:38ad7ecb51cadb0091359cbb5c53b76a",
    "question": "19 个实现区间是否已解释？"
  },
  {
    "kind": "open_gap",
    "task": "task:38ad7ecb51cadb0091359cbb5c53b76a",
    "question": "运行时行为（GA 结果质量、随机可复现、代价一致性）是否有验证？"
  },
  {
    "kind": "open_gap",
    "task": "task:7f712073125865f96800648d0fe0c71f",
    "question": "提供的 openGauss 手册样本中是否有 GEQO 机制、参数或行为承诺的专门页面？"
  },
  {
    "kind": "open_gap",
    "task": "task:7f712073125865f96800648d0fe0c71f",
    "question": "GEQO 相关 GUC（如 geqo、geqo_threshold、geqo_pool_size 等）在完整产品手册中的公开说明、默认值和生效范围是什么？"
  },
  {
    "kind": "open_gap",
    "task": "task:35aef36cac90b6845209cacc1800dd6b",
    "question": "构建时实际启用哪个交叉宏？GEQO 的 15 个 .cpp 是否绑定到具体编译命令？"
  },
  {
    "kind": "open_gap",
    "task": "task:35aef36cac90b6845209cacc1800dd6b",
    "question": "上层 ${MACRO_OPTIONS} / Makefile.global 是否注入交叉宏？"
  },
  {
    "kind": "open_gap",
    "task": "task:35aef36cac90b6845209cacc1800dd6b",
    "question": "是否有可用的调用图？"
  },
  {
    "kind": "open_gap",
    "task": "task:35aef36cac90b6845209cacc1800dd6b",
    "question": "GEQO 其余头文件的定义与默认值是否已核对？"
  },
  {
    "kind": "open_gap",
    "task": "task:d6cc25c69595225e7c89328b2d02f61a",
    "question": "19 个 CPP 实现区间是否已解释？"
  },
  {
    "kind": "open_gap",
    "task": "task:35aef36cac90b6845209cacc1800dd6b",
    "question": "运行时行为（GA 结果、可复现性、代价一致性）是否有验证？"
  },
  {
    "kind": "open_gap",
    "task": "task:35aef36cac90b6845209cacc1800dd6b",
    "question": "构建时实际启用哪个交叉宏（TU 级验证）？"
  },
  {
    "kind": "open_gap",
    "task": "task:0d79087056f64b0310de1bba1a2e754a",
    "question": "server/src/gausskernel/optimizer 之外是否还存在 geqo() 的调用方、重载或函数指针间接调用？"
  },
  {
    "kind": "open_gap",
    "task": "task:0d79087056f64b0310de1bba1a2e754a",
    "question": "非断言构建下 gimme_tree 对 root->join_rel_level 是否有检查或需要恢复？"
  },
  {
    "kind": "open_gap",
    "task": "task:0d79087056f64b0310de1bba1a2e754a",
    "question": "全局计划缓存如何比较/复用 env_signature2 与 Geqo 字段（匹配与失效语义）？"
  },
  {
    "kind": "open_gap",
    "task": "task:0d79087056f64b0310de1bba1a2e754a",
    "question": "geqo_eval.cpp 第 201-296 行（merge_clump/desirable_join 等）的行为与边界是什么？"
  },
  {
    "kind": "open_gap",
    "task": "task:0d79087056f64b0310de1bba1a2e754a",
    "question": "声明构建中 ERX/PMX/CX/PX/OX1/OX2 实际启用哪个交叉算子？"
  },
  {
    "kind": "open_gap",
    "task": "task:0d79087056f64b0310de1bba1a2e754a",
    "question": "server/src/gausskernel/optimizer 之外是否还有 geqo() 的其他调用方/重载/间接调用？"
  },
  {
    "kind": "open_gap",
    "task": "task:0d79087056f64b0310de1bba1a2e754a",
    "question": "geqo_eval 结束时 join_rel_level 及其他 PlannerInfo 字段是否完全恢复？"
  },
  {
    "kind": "open_gap",
    "task": "task:0d79087056f64b0310de1bba1a2e754a",
    "question": "全局计划缓存如何比较/复用 env_signature2 与 GEQO 字段（匹配与失效语义）？"
  },
  {
    "kind": "open_gap",
    "task": "task:032d0d5241da7140e82902d156baa664",
    "question": "完整 openGauss 2.4.0 产品手册（含 GUC 参考/优化器配置章节）是否对 GEQO 参数作出承诺，并与源码行为冲突？"
  },
  {
    "kind": "open_gap",
    "task": "task:032d0d5241da7140e82902d156baa664",
    "question": "GEQO 相关 GUC（enable_geqo、geqo_threshold、Geqo_pool_size 等）的实际生效默认值、取值范围和运行时行为是否与（未来接入的）手册一致？"
  },
  {
    "kind": "open_gap",
    "task": "task:009cab4158543cec0040563d357f6bcc",
    "question": "历史特性清单与产品全量特性之间的覆盖关系是否闭合？"
  },
  {
    "kind": "open_gap",
    "task": "task:009cab4158543cec0040563d357f6bcc",
    "question": "GEQO 之外的选择/交叉/变异算子（PMX/CX/PX/OX1/OX2、geqo_mutation）是否还有独立特性行需要映射？"
  },
  {
    "kind": "open_gap",
    "task": "task:009cab4158543cec0040563d357f6bcc",
    "question": "该 GEQO 特性映射是否经过编译产物或运行时验证？"
  },
  {
    "kind": "open_gap",
    "task": "task:d6cc25c69595225e7c89328b2d02f61a",
    "question": "19 个 CPP 实现区间待 3 个机制包解释"
  },
  {
    "kind": "open_gap",
    "task": "task:d6cc25c69595225e7c89328b2d02f61a",
    "question": "模块知识尚未完成"
  },
  {
    "kind": "open_gap",
    "task": "task:d6cc25c69595225e7c89328b2d02f61a",
    "question": "GEQO 模块知识是否完成？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "GEQO 入口分支与 geqo_eval 状态恢复在运行时是否按源码发生？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "实际编译单元启用了 ERX 还是其他交叉宏，是否定义 GEQO_DEBUG？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "同一批 GEQO GUC 进入全局计划缓存环境后，缓存如何比较、失效与复用？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "geqo_eval 125-296（gimme_tree/merge_clump/desirable_join）与 geqo_main 100-199 的遗传算法主循环行为？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "geqo_selection 对 Geqo_selection_bias 的具体消费与 geqo.h 宏值是否需要重新核对？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "产品手册是否对七个 GEQO GUC 的默认值、范围与生效范围有公开承诺？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "入口分支、GUC 校验与状态恢复是否在运行时验证？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "计划缓存如何比较与失效 GEQO 环境，GPCEnv 结构如何定义？"
  },
  {
    "kind": "open_gap",
    "task": "task:ec88ed9b634b348d00cb08e2da7a97aa",
    "question": "模块剩余 3 个课程机制包与未读区间是否已解释？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "list_truncate 返回的 List 头分配在哪个内存上下文，是否会在随后的 MemoryContextDelete(GEQO) 后使 root->join_rel_list 悬挂？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "实际编译产物是否只走 ERX，是否启用 GEQO_DEBUG？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "CMake 与 Makefile 两条构建路径在产品构建中的实际采用关系，以及 add_static_objtarget/Makefile.global/common.mk 的具体语义？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "make_join_rel/set_cheapest/have_relevant_joinclause/have_join_order_restriction 的实现是否严格满足 gimme_tree 假设（append-only、NULL 表示非法、笛卡尔积可强制合并）？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "random_init_pool 是否逐染色体调用 geqo_eval、sort_pool 的排序方向与 spread_chroma 的替换规则？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "调用方 allpaths.cpp 的入口条件与 root->initial_rels 写入是否仍与本快照一致？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "产品手册是否对 GEQO GUC 默认值、范围与生效范围有公开承诺？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "初始种群如何生成、池如何排序并替换最差个体？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "调用方（optimizer/path、planner）在什么条件下选择 geqo()，交叉模块状态契约是什么？"
  },
  {
    "kind": "open_gap",
    "task": "task:a6c811ed9c46511c25278df5638e5a38",
    "question": "产品手册对 GEQO GUC/算法是否有承诺，是否构成文码冲突？"
  },
  {
    "kind": "implementation_explanation",
    "count": 13845,
    "examples": [
      {
        "item": "implementation:58da9eeab41b0aa7e6af9829dd45435a",
        "asset": "server/contrib/adminpack/adminpack.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:b2b4b42c9f39ba9b26f54ce71d8334c6",
        "asset": "server/contrib/adminpack/adminpack.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:e923cdfa483f4696149e356f4a90802c",
        "asset": "server/contrib/auth_delay/auth_delay.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:f57c9858596b152eaacffbfc7a145d9e",
        "asset": "server/contrib/auto_explain/auto_explain.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:14d339d788cbd9b71cb5dd997d921391",
        "asset": "server/contrib/auto_explain/auto_explain.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:fe01e0b0c4b7e8522e28aadfc1f6b8e1",
        "asset": "server/contrib/btree_gin/btree_gin.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:a219c13d6a5409ecb80c6c01211d17da",
        "asset": "server/contrib/btree_gin/btree_gin.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:4810e47e5437ae94c0f5b8528b964107",
        "asset": "server/contrib/btree_gist/btree_bit.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:7a6330302fe0cbca6d8045918749c43a",
        "asset": "server/contrib/btree_gist/btree_bytea.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:7d05d473389ecbce116b6aa1d0a4ad18",
        "asset": "server/contrib/btree_gist/btree_cash.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:1c21e050a1dee7a4160e3ec30669de74",
        "asset": "server/contrib/btree_gist/btree_date.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:81a7c0095725e725cde51e9400454c29",
        "asset": "server/contrib/btree_gist/btree_date.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:29114ae48feb7e00e033723c70ff096e",
        "asset": "server/contrib/btree_gist/btree_float4.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:61310a8d571132e7f94cc550d507835b",
        "asset": "server/contrib/btree_gist/btree_float8.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:889a1010b26bf4336943cde432ca278c",
        "asset": "server/contrib/btree_gist/btree_gist.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:e60b75036c9a9758132da5c735ad473d",
        "asset": "server/contrib/btree_gist/btree_inet.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:09d5b724579feed2988d453901fa336f",
        "asset": "server/contrib/btree_gist/btree_int2.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:1611e0f0898c6af1c1eb36f70b0b09d3",
        "asset": "server/contrib/btree_gist/btree_int4.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:97ca2c600f690353b78a3887a1609512",
        "asset": "server/contrib/btree_gist/btree_int8.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:eafda0bfcee1b02d15ff219e3353be2f",
        "asset": "server/contrib/btree_gist/btree_interval.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:26173ee8768cbd50493d4cde03856e12",
        "asset": "server/contrib/btree_gist/btree_interval.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:e85f7b444fdab8be52bdee4641a717dc",
        "asset": "server/contrib/btree_gist/btree_macaddr.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:75007ce8aed746b601e60c5ff21f620b",
        "asset": "server/contrib/btree_gist/btree_numeric.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:d6b968a07a2942f57ef54031221a8695",
        "asset": "server/contrib/btree_gist/btree_oid.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:2ea1cb981b79d25d7deb10fd36ee01cb",
        "asset": "server/contrib/btree_gist/btree_text.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:3c9343dcc77cbe134d384f80fa0c6f81",
        "asset": "server/contrib/btree_gist/btree_time.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:ff147694bc59f7590d3216f43857838f",
        "asset": "server/contrib/btree_gist/btree_time.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:a9cb997b5af5d6a459dce01431a4325f",
        "asset": "server/contrib/btree_gist/btree_ts.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:1082b91adcc15c4c5d05ca4a96c63859",
        "asset": "server/contrib/btree_gist/btree_ts.cpp",
        "state": "unreviewed"
      },
      {
        "item": "implementation:9706ff82cfc6bc7258eae1b4cd83eec8",
        "asset": "server/contrib/btree_gist/btree_utils_num.cpp",
        "state": "unreviewed"
      }
    ]
  },
  {
    "kind": "historical_feature_mapping",
    "count": 3,
    "examples": [
      {
        "feature_id": "feature:4af6e617b84d8878b7e7ebbfbbd47396",
        "name": "SQL PATCH",
        "state": "not_located"
      },
      {
        "feature_id": "feature:fa46b45bdacd74a66bfa655f416a0b48",
        "name": "计划缓存",
        "state": "not_located"
      },
      {
        "feature_id": "feature:63d78250c3c73314307731e3912a42c2",
        "name": "VALIDATION_ONLY_UNLOCATED_FEATURE",
        "state": "not_located"
      }
    ]
  },
  {
    "kind": "consumer_use_cases",
    "count": 2020,
    "examples": [
      [
        "historical_features/@materials",
        "coding"
      ],
      [
        "historical_features/@materials",
        "operations"
      ],
      [
        "historical_features/@materials",
        "review"
      ],
      [
        "historical_features/@materials",
        "test_generation"
      ],
      [
        "manual/@materials",
        "coding"
      ],
      [
        "manual/@materials",
        "operations"
      ],
      [
        "manual/@materials",
        "review"
      ],
      [
        "manual/@materials",
        "test_generation"
      ],
      [
        "server/@root",
        "coding"
      ],
      [
        "server/@root",
        "operations"
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
        "operations"
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
        "operations"
      ],
      [
        "server/build",
        "review"
      ],
      [
        "server/build",
        "test_generation"
      ]
    ]
  }
]
```

使用 `next` 获取就绪任务，`run` 连接已有Claude按预算执行；提交后由实际审阅者review，`advance`推进下一批。`coverage`不隐藏阻断项，不自动批准知识。
