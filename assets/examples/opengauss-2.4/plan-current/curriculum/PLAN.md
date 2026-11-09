# 模块、特性与主干流程学习计划

537模块 / 3668功能工作包候选 / 2380个C++实现文件。

先按模块确认课程，再研究机制与主干；函数、TU和图节点不是学习任务。分组是待核候选，不是已审知识。

| 模块 | 工作包 | C++文件 | 历史特性候选 | 依赖 |
| --- | --- | ---: | --- | --- |
| compile_database/@materials | 模块实现、接口与状态机制 | 0 |  | task:eaa9ef6caf7da7eb03d871cc7e02b015 |
| historical_features/@materials | 模块实现、接口与状态机制 | 0 |  | task:aed7fd9c347265b7b535de5bcd9b4e39 |
| manual/@materials | 模块实现、接口与状态机制 | 0 |  | task:7c348891edec17c5a2cef58e9c22a9fd |
| server/@root | 配置注册与生效 / 分批1 | 0 |  | task:cd9200bf52e8b3473a660d3404b939ed |
| server/@root | 配置注册与生效 / 分批2 | 0 |  | task:cd9200bf52e8b3473a660d3404b939ed |
| server/@root | 配置注册与生效 / 分批3 | 0 |  | task:cd9200bf52e8b3473a660d3404b939ed |
| server/@root | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:cd9200bf52e8b3473a660d3404b939ed |
| server/@root | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:cd9200bf52e8b3473a660d3404b939ed |
| server/@root | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:cd9200bf52e8b3473a660d3404b939ed |
| server/Tools | 模块实现、接口与状态机制 | 0 |  | task:31404a5b71ace431119543e56392f8bc |
| server/Tools | 资源寿命与错误清理 | 0 |  | task:31404a5b71ace431119543e56392f8bc |
| server/build | 配置注册与生效 | 0 |  | task:763edf52f7a79f1560c10398b849b00e |
| server/build | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:763edf52f7a79f1560c10398b849b00e |
| server/build | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:763edf52f7a79f1560c10398b849b00e |
| server/build | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:763edf52f7a79f1560c10398b849b00e |
| server/cmake/src | 模块实现、接口与状态机制 | 0 |  | task:7005de8ccd2977ea4ba8e4ead2064332 |
| server/cmake/src/config-in | 配置注册与生效 | 0 |  | task:08a81bc4ef5104eabf16bbf2fef5ef5f |
| server/config | 配置注册与生效 | 0 |  | task:51fe927d0ae24e0f6d870816bcdec3b4 |
| server/config | 模块实现、接口与状态机制 | 0 |  | task:51fe927d0ae24e0f6d870816bcdec3b4 |
| server/contrib | 模块实现、接口与状态机制 | 0 |  | task:f40c022c379acdd537472cc9319e6c04 |
| server/contrib/adminpack | 模块实现、接口与状态机制 | 1 |  | task:ea2f3b13fd8151789798eaef379798a3 |
| server/contrib/auth_delay | 模块实现、接口与状态机制 | 1 |  | task:3f58f83bdfccae319d103242a04d4900 |
| server/contrib/auto_explain | 模块实现、接口与状态机制 | 1 |  | task:5d7f0632e90566c63d711290ad4a1152 |
| server/contrib/btree_gin | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:29c800229ff81bbeb8ebe1eb28548461 |
| server/contrib/btree_gin | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:29c800229ff81bbeb8ebe1eb28548461 |
| server/contrib/btree_gin | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:29c800229ff81bbeb8ebe1eb28548461 |
| server/contrib/btree_gist | 模块实现、接口与状态机制 / 分批1 | 19 |  | task:ba8b2fdafe780318a3736a21cb0cd8c2 |
| server/contrib/btree_gist | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:ba8b2fdafe780318a3736a21cb0cd8c2 |
| server/contrib/btree_gist/data | 模块实现、接口与状态机制 | 0 |  | task:2bcdddbd0ae743bb968b806afe60c4ec |
| server/contrib/btree_gist/expected | 回归主题：bit | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：bytea | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：cash | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：char | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：cidr | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：date | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：float | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：inet | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：init | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：int | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：interval | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：macaddr | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：not | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：numeric | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：oid | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：text | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：time | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：timestamp | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：timestamptz | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：timetz | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：varbit | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/expected | 回归主题：varchar | 0 |  | task:d6751a23f914ddc1787d9c16f7d8ddf5 |
| server/contrib/btree_gist/sql | 回归主题：bit | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：bytea | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：cash | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：char | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：cidr | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：date | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：float | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：inet | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：init | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：int | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：interval | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：macaddr | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：not | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：numeric | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：oid | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：text | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：time | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：timestamp | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：timestamptz | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：timetz | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：varbit | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/btree_gist/sql | 回归主题：varchar | 0 |  | task:4ac17b482bc498eb7297cdd2e6af833f |
| server/contrib/chkpass | 模块实现、接口与状态机制 | 1 |  | task:ae3a8069b39302fbb16d4d2663817652 |
| server/contrib/citext | 模块实现、接口与状态机制 | 1 |  | task:7254b6048ae74cf3267cbf13817acb9f |
| server/contrib/common_cipher | 模块实现、接口与状态机制 | 6 |  | task:bea38104ad2fc87667b99abac6ef9f3b |
| server/contrib/cube | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:13be1833c911a959a6f5439bcc296d58 |
| server/contrib/cube | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:13be1833c911a959a6f5439bcc296d58 |
| server/contrib/dblink | 模块实现、接口与状态机制 | 1 |  | task:804dddd75291d2e79b88f6df889426d8 |
| server/contrib/dict_int | 模块实现、接口与状态机制 | 1 |  | task:121c44a60d48380bbf38e8a140c4cb51 |
| server/contrib/dict_xsyn | 模块实现、接口与状态机制 | 1 |  | task:866bd132b5ed82c6910b8b7c36a57525 |
| server/contrib/dummy_seclabel | 模块实现、接口与状态机制 | 1 |  | task:51bf8ca2942cda33b6161ec6ef1dfaaa |
| server/contrib/earthdistance | 模块实现、接口与状态机制 | 1 |  | task:45e62ce58016b65cfb91bebe892da094 |
| server/contrib/file_fdw | 模块实现、接口与状态机制 | 1 |  | task:627b1ecdfaaf9e493935afaf356ffd77 |
| server/contrib/fuzzystrmatch | 模块实现、接口与状态机制 | 3 |  | task:cc0057096a78f91040ba705bf2696335 |
| server/contrib/gauss_connector | 模块实现、接口与状态机制 | 2 |  | task:f3b2c4e4e11c7fd08062993d579d1d2d |
| server/contrib/gc_fdw | 模块实现、接口与状态机制 | 3 |  | task:5a8435f50f4073bf19fade82ff22d7f6 |
| server/contrib/gms_assert | 模块实现、接口与状态机制 | 1 |  | task:a927c881fca857a18a02915b3f726634 |
| server/contrib/gms_compress | 模块实现、接口与状态机制 | 1 |  | task:de7f19741c272c74adfed6128436fbbc |
| server/contrib/gms_debug | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:408f3fe95e23e3b5b841ef03c7e9f95e |
| server/contrib/gms_debug | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:408f3fe95e23e3b5b841ef03c7e9f95e |
| server/contrib/gms_i18n | 模块实现、接口与状态机制 | 1 |  | task:19d4d07759f3cefb06e33fadc6ea44e4 |
| server/contrib/gms_inaddr | 模块实现、接口与状态机制 | 1 |  | task:15aec4553a33f2c353ed7accc14da71b |
| server/contrib/gms_lob | 模块实现、接口与状态机制 | 2 |  | task:d795ee25631e35bd936b48398f297900 |
| server/contrib/gms_match | 模块实现、接口与状态机制 | 1 |  | task:0c108d1c8e47ce86f65f2ce518b6e6b5 |
| server/contrib/gms_output | 模块实现、接口与状态机制 | 1 |  | task:7edee1f4278b2408d2c8850cf0793c56 |
| server/contrib/gms_profiler | 模块实现、接口与状态机制 | 1 |  | task:54e8f4a7ef0544d648d2533a3460d17f |
| server/contrib/gms_raw | 模块实现、接口与状态机制 | 1 |  | task:cb0dfbb9c9235e2bbfaf795792e0ea6e |
| server/contrib/gms_sql | 模块实现、接口与状态机制 | 1 |  | task:747c59dbed39a204ab2bbe1ceda9b753 |
| server/contrib/gms_stats | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:14ccb5bbb29e2f7bbe5142bb635838b1 |
| server/contrib/gms_stats | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:14ccb5bbb29e2f7bbe5142bb635838b1 |
| server/contrib/gms_tcp | 模块实现、接口与状态机制 | 1 |  | task:bb307e1b5ca6b0744197a60f1af7735c |
| server/contrib/gms_utility | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:fdd06420fbd0f40bd487e1e3a0cf3ca8 |
| server/contrib/gms_utility | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:fdd06420fbd0f40bd487e1e3a0cf3ca8 |
| server/contrib/gms_xmlgen | 模块实现、接口与状态机制 | 1 |  | task:d9c4af779115c610312853daa3efbfc8 |
| server/contrib/gms_xmlparser | 模块实现、接口与状态机制 | 1 |  | task:70bf9449bcf64d8bb1d412896850473e |
| server/contrib/gs_filedump | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:e32ca5c373166a398adc32e012d96653 |
| server/contrib/gs_filedump | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:e32ca5c373166a398adc32e012d96653 |
| server/contrib/gv_index | 模块实现、接口与状态机制 | 5 |  | task:6cdeb26a2a211306c6fc174982860c4d |
| server/contrib/gv_index | 资源寿命与错误清理 | 0 |  | task:6cdeb26a2a211306c6fc174982860c4d |
| server/contrib/hstore | 模块实现、接口与状态机制 | 6 |  | task:c06ee528f2a1e0cbe357bc9519cbecaa |
| server/contrib/intagg | 模块实现、接口与状态机制 | 0 |  | task:b9fdfeda672e8e657f5eb77dd4caeecf |
| server/contrib/intarray | 模块实现、接口与状态机制 | 6 |  | task:6e379bb3ba9b6114757504d6412e6bc6 |
| server/contrib/isn | 模块实现、接口与状态机制 | 1 |  | task:c86b0045f68fff3e5d48444472884e67 |
| server/contrib/jieba_tokenizer | 配置注册与生效 | 0 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer | 模块实现、接口与状态机制 / 分批7 | 1 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer | 资源寿命与错误清理 | 0 |  | task:eec1e501bc7683811816dc58c108209a |
| server/contrib/jieba_tokenizer/include/cppjieba | 模块实现、接口与状态机制 | 0 |  | task:981664824711f4cf1239b6dc420d305f |
| server/contrib/lo | 模块实现、接口与状态机制 | 1 |  | task:d93c248ca6f82be5e2c768fd3460e5c1 |
| server/contrib/log_fdw | 模块实现、接口与状态机制 | 2 |  | task:aca12277cef1fcedf573cebbd7346eff |
| server/contrib/ltree | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:1ca845bef694ad196e37da2d12b6c8cc |
| server/contrib/ltree | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:1ca845bef694ad196e37da2d12b6c8cc |
| server/contrib/ltree | 模块实现、接口与状态机制 / 分批3 | 3 |  | task:1ca845bef694ad196e37da2d12b6c8cc |
| server/contrib/mppdb_decoding | 模块实现、接口与状态机制 | 1 |  | task:26a0cdde9f865072631c34e83a48753c |
| server/contrib/mysql_fdw | 模块实现、接口与状态机制 | 0 |  | task:3736c9b4e0e0333532d76277c11931b6 |
| server/contrib/ndpplugin | 模块实现、接口与状态机制 | 6 |  | task:4b29f2eecb4b657c4aa22d2f18f3c6a4 |
| server/contrib/nputurbo | 模块实现、接口与状态机制 | 2 |  | task:e41c0d22171677a208b553ac6f805ba6 |
| server/contrib/ogai | 模块实现、接口与状态机制 | 1 |  | task:71191383c157b813db78022c7c0f3b93 |
| server/contrib/oid2name | 模块实现、接口与状态机制 | 1 |  | task:60022dc54ebc2d6b97c1238a7fbf5842 |
| server/contrib/oracle_fdw | 模块实现、接口与状态机制 | 0 |  | task:26e6c15bf19a8dc8edf4e34028aa09ac |
| server/contrib/pagehack | 模块实现、接口与状态机制 | 1 |  | task:ae1a46f425c5f56a105d495332905c71 |
| server/contrib/pageinspect | 模块实现、接口与状态机制 | 5 |  | task:e2bafa1ddd0475ee7b4da9437eb0a1bf |
| server/contrib/passwordcheck | 模块实现、接口与状态机制 | 1 |  | task:0bd2a65300555f6af1471ef857b83df0 |
| server/contrib/pg_archivecleanup | 模块实现、接口与状态机制 | 1 |  | task:d3a6577d341f50c068e3670316bb235d |
| server/contrib/pg_buffercache | 缓存、失效与复用 | 1 |  | task:fd7b0067ea759eeec3da5d4759634993 |
| server/contrib/pg_buffercache | 模块实现、接口与状态机制 | 0 |  | task:fd7b0067ea759eeec3da5d4759634993 |
| server/contrib/pg_check_clog | 模块实现、接口与状态机制 | 1 |  | task:12dade961b5f1c5a70c4cc392cc277f2 |
| server/contrib/pg_check_replslot | 模块实现、接口与状态机制 | 1 |  | task:4fca205c1a2e70e411ce130270d9b387 |
| server/contrib/pg_freespacemap | 模块实现、接口与状态机制 | 1 |  | task:2dcf4ab5f3a5407d80422f9f341a23f1 |
| server/contrib/pg_standby | 模块实现、接口与状态机制 | 1 |  | task:19293ab5784d94b634ac588c50da35df |
| server/contrib/pg_stat_statements | 模块实现、接口与状态机制 | 1 |  | task:63acf91a56d7856411a9634f8eea8bcf |
| server/contrib/pg_test_fsync | 模块实现、接口与状态机制 | 1 |  | task:0b73bff97d9e7751cfa9e9328bd89e1d |
| server/contrib/pg_test_timing | 模块实现、接口与状态机制 | 1 |  | task:57087d9fd17cf34c17bd262aaf0bb94e |
| server/contrib/pg_trgm | 模块实现、接口与状态机制 | 3 |  | task:be706204a99d5f55eb84552bfbddfbfb |
| server/contrib/pg_upgrade_support | 模块实现、接口与状态机制 | 1 |  | task:a6f1051dad0a7bc3ad8b1e273b5aa8e5 |
| server/contrib/pg_xlogdump | 模块实现、接口与状态机制 | 2 |  | task:fd6422dfb52902df80546155fe0fc606 |
| server/contrib/pg_xlogdump | 持久化与恢复 | 1 |  | task:fd6422dfb52902df80546155fe0fc606 |
| server/contrib/pgbench | 模块实现、接口与状态机制 | 1 |  | task:a2faf8c3fc13ff6634c691ea5d675a03 |
| server/contrib/pgcrypto | 模块实现、接口与状态机制 / 分批1 | 7 |  | task:a17ae1725d45d97522f78d89b45a6beb |
| server/contrib/pgcrypto | 模块实现、接口与状态机制 / 分批2 | 18 |  | task:a17ae1725d45d97522f78d89b45a6beb |
| server/contrib/pgcrypto | 模块实现、接口与状态机制 / 分批3 | 10 |  | task:a17ae1725d45d97522f78d89b45a6beb |
| server/contrib/pgcrypto/expected | 回归主题：3des | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：blowfish | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：cast | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：crypt-blowfish | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：crypt-des | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：crypt-md | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：crypt-xdes | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：des | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：hmac-md | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：hmac-sha | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：init | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：md | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-armor | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-compression | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-decrypt | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-encrypt | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-encrypt-disabled | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-info | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-pubkey-decrypt | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-pubkey-disabled | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-pubkey-encrypt | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：pgp-zlib-disabled | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：rijndael | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/expected | 回归主题：sha | 0 |  | task:afaedc5061d701a6825ad95658ff1fbc |
| server/contrib/pgcrypto/sql | 回归主题：3des | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：blowfish | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：cast | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：crypt-blowfish | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：crypt-des | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：crypt-md | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：crypt-xdes | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：des | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：hmac-md | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：hmac-sha | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：init | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：md | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-armor | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-compression | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-decrypt | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-encrypt | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-encrypt-disabled | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-info | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-pubkey-decrypt | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-pubkey-disabled | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-pubkey-encrypt | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：pgp-zlib-disabled | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：rijndael | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgcrypto/sql | 回归主题：sha | 0 |  | task:af7dfe092f6a96e2588482ea8f1f0d8e |
| server/contrib/pgrowlocks | 模块实现、接口与状态机制 | 1 |  | task:5f0bd9ebb6e219606d24473a7c5a71c2 |
| server/contrib/pgstattuple | 模块实现、接口与状态机制 | 2 |  | task:e1e5680f2955f62194afe689502a68f9 |
| server/contrib/postgres_fdw | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:356a16049c9ca66da84b4fcba09c1399 |
| server/contrib/postgres_fdw | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:356a16049c9ca66da84b4fcba09c1399 |
| server/contrib/postgres_fdw | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:356a16049c9ca66da84b4fcba09c1399 |
| server/contrib/postgres_fdw | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:356a16049c9ca66da84b4fcba09c1399 |
| server/contrib/postgres_fdw | 模块实现、接口与状态机制 / 分批5 | 3 |  | task:356a16049c9ca66da84b4fcba09c1399 |
| server/contrib/postgres_fdw | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:356a16049c9ca66da84b4fcba09c1399 |
| server/contrib/postgres_fdw | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:356a16049c9ca66da84b4fcba09c1399 |
| server/contrib/rack_dev | 模块实现、接口与状态机制 | 1 |  | task:8e5a72555ab80f2a7d134f1e0dbe1136 |
| server/contrib/rack_dev | 资源寿命与错误清理 | 2 |  | task:8e5a72555ab80f2a7d134f1e0dbe1136 |
| server/contrib/rack_dev/include | 模块实现、接口与状态机制 | 0 |  | task:4f41aad6104b96ba606ea6762c465e94 |
| server/contrib/rack_dev/include | 资源寿命与错误清理 | 0 |  | task:4f41aad6104b96ba606ea6762c465e94 |
| server/contrib/security_plugin | 模块实现、接口与状态机制 / 分批1 | 7 |  | task:9f8fb3193857dd55f5283044b5747555 |
| server/contrib/security_plugin | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:9f8fb3193857dd55f5283044b5747555 |
| server/contrib/seg | 模块实现、接口与状态机制 | 1 |  | task:531f38369914ca0c88f02b701e8f10a1 |
| server/contrib/sepgsql | 模块实现、接口与状态机制 | 9 |  | task:ef6e2fd99cb566da93d952fe08034ff3 |
| server/contrib/shark | 模块实现、接口与状态机制 / 分批1 | 6 |  | task:236af40bee310be7f8bb1bed2ec49a6c |
| server/contrib/shark | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:236af40bee310be7f8bb1bed2ec49a6c |
| server/contrib/shark/data | 模块实现、接口与状态机制 | 0 |  | task:dfbf3e0efde88488dafc9bce01679a44 |
| server/contrib/shark/expected | 回归主题：alter | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：basetest | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：clustered | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：day | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：dummy | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：functions | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：identity | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：init | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：insert | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：objectproperty | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：proc | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：rand | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：rotate-test-part | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：rotate-test-part2 | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：sbr | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：sharksysfunction | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：table | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：test / 分批1 | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：test / 分批2 | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：test / 分批3 | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：transaction | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 回归主题：use | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/expected | 事务、可见性与结束处理 | 0 |  | task:52325d86b50d3e68c503a3ff6aabac2a |
| server/contrib/shark/input | 模块实现、接口与状态机制 | 0 |  | task:4be7c6f5c8e7eb53772993d62a79d91d |
| server/contrib/shark/output | 模块实现、接口与状态机制 | 0 |  | task:3917620d78a2a31919357b6febf5a3f4 |
| server/contrib/shark/rollback_script | 模块实现、接口与状态机制 | 0 |  | task:c6b70ad75a75219579959cc5e4ad37aa |
| server/contrib/shark/sql | 回归主题：alter | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：basetest | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：clustered | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：day | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：dummy | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：functions | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：identity | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：init | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：insert | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：objectproperty | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：proc | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：rand | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：rotate-test-part | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：rotate-test-part2 | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：sbr | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：sharksysfunction | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：table | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：test | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：transaction | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 回归主题：use | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/sql | 事务、可见性与结束处理 | 0 |  | task:5194f74532107c6faa19ed25678de6e4 |
| server/contrib/shark/src | 模块实现、接口与状态机制 | 2 |  | task:c4b3920b98cf9b43357e97bd87ce54c8 |
| server/contrib/shark/src/backend_parser | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:adce86c6cc8067481af415dba8dfe486 |
| server/contrib/shark/src/backend_parser | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:adce86c6cc8067481af415dba8dfe486 |
| server/contrib/shark/src/pltsql | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:b49b8b9c1d39a7508a7344735aa084ef |
| server/contrib/shark/src/pltsql | 模块实现、接口与状态机制 / 分批2 | 4 |  | task:b49b8b9c1d39a7508a7344735aa084ef |
| server/contrib/shark/upgrade_script | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:fbabab5f1dd1e6e00d5447cc933dbc6e |
| server/contrib/shark/upgrade_script | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:fbabab5f1dd1e6e00d5447cc933dbc6e |
| server/contrib/spi | 模块实现、接口与状态机制 / 分批1 | 4 |  | task:7433c69f0f289cfb700fdf642bebddfa |
| server/contrib/spi | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:7433c69f0f289cfb700fdf642bebddfa |
| server/contrib/sql_decoding | 回归主题：cmakelists | 0 |  | task:09c183c8ecac1a85ba54bff8c19925dc |
| server/contrib/sql_decoding | 回归主题：logical | 0 |  | task:09c183c8ecac1a85ba54bff8c19925dc |
| server/contrib/sql_decoding | 回归主题：sql | 1 |  | task:09c183c8ecac1a85ba54bff8c19925dc |
| server/contrib/sslinfo | 模块实现、接口与状态机制 | 1 |  | task:4ebaf04ecdbcd28303d16cca232db8b2 |
| server/contrib/start-scripts | 模块实现、接口与状态机制 | 0 |  | task:f257a4902667c1cd6f7651b99f379fec |
| server/contrib/tablefunc | 模块实现、接口与状态机制 | 1 |  | task:fb01c4a270b61f72c4c32a5b467175b4 |
| server/contrib/tcn | 模块实现、接口与状态机制 | 1 |  | task:c83ffb5c0079311bba232eea40c5fffc |
| server/contrib/test_decoding | 回归主题：cmakelists | 0 |  | task:1b3d55f344cad67255d9b0068e462e80 |
| server/contrib/test_decoding | 回归主题：logical | 0 |  | task:1b3d55f344cad67255d9b0068e462e80 |
| server/contrib/test_decoding | 回归主题：makefile | 0 |  | task:1b3d55f344cad67255d9b0068e462e80 |
| server/contrib/test_decoding | 回归主题：test | 1 |  | task:1b3d55f344cad67255d9b0068e462e80 |
| server/contrib/test_parser | 回归主题：makefile | 0 |  | task:5d3a4fbecc94061f311cbc056eb546f9 |
| server/contrib/test_parser | 回归主题：test | 1 |  | task:5d3a4fbecc94061f311cbc056eb546f9 |
| server/contrib/tsearch2 | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:652341dc86e56e86b1480dfffcc5cf16 |
| server/contrib/tsearch2 | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:652341dc86e56e86b1480dfffcc5cf16 |
| server/contrib/tsearch2 | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:652341dc86e56e86b1480dfffcc5cf16 |
| server/contrib/tsearch2 | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:652341dc86e56e86b1480dfffcc5cf16 |
| server/contrib/unaccent | 模块实现、接口与状态机制 | 1 |  | task:886c30f569950d455807b8b052a33e0a |
| server/contrib/vacuumlo | 模块实现、接口与状态机制 | 1 |  | task:162dad1794f4cdee58867abf199d97a4 |
| server/contrib/wal2json | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:3362d291128b8bd32426c7e779586967 |
| server/contrib/wal2json | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:3362d291128b8bd32426c7e779586967 |
| server/contrib/wal2json | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:3362d291128b8bd32426c7e779586967 |
| server/contrib/wal2json | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:3362d291128b8bd32426c7e779586967 |
| server/contrib/wal2json | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:3362d291128b8bd32426c7e779586967 |
| server/contrib/wal2json | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:3362d291128b8bd32426c7e779586967 |
| server/contrib/wal2json | 持久化与恢复 | 1 |  | task:3362d291128b8bd32426c7e779586967 |
| server/contrib/xml2 | 模块实现、接口与状态机制 | 2 |  | task:bd83fccfee9c5c1702eb5752bb5cd5ae |
| server/doc | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:0943c9c7af576c2dbc8f1310da32437a |
| server/doc | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:0943c9c7af576c2dbc8f1310da32437a |
| server/doc/src | 模块实现、接口与状态机制 | 0 |  | task:1dadee68ba66b71900c3f30d0dbe40da |
| server/doc/src/sgml | 缓存、失效与复用 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 配置注册与生效 / 分批1 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 配置注册与生效 / 分批2 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 连接路径与连接约束 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批10 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批11 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批12 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批13 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批14 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批15 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批16 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批17 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批18 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批19 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批20 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批21 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批22 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批23 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批24 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批25 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批26 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批27 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批28 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批29 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批30 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批31 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批32 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批33 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批34 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批35 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批36 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批37 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批38 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 模块实现、接口与状态机制 / 分批39 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 计划生成与计划接口 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml | 持久化与恢复 | 0 |  | task:096a93e68a8c3d793d0ce52b95aa9e00 |
| server/doc/src/sgml/ref | 配置注册与生效 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 模块实现、接口与状态机制 / 分批10 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 计划生成与计划接口 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 持久化与恢复 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/doc/src/sgml/ref | 事务、可见性与结束处理 | 0 |  | task:2c1e54aaea87ff459c747c3a69ed1e71 |
| server/docker | 配置注册与生效 | 0 |  | task:f1c161ea990f4420a271da71c073a7a9 |
| server/docker | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:f1c161ea990f4420a271da71c073a7a9 |
| server/docker | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:f1c161ea990f4420a271da71c073a7a9 |
| server/docker | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:f1c161ea990f4420a271da71c073a7a9 |
| server/docker | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:f1c161ea990f4420a271da71c073a7a9 |
| server/docker | 资源寿命与错误清理 | 0 |  | task:f1c161ea990f4420a271da71c073a7a9 |
| server/liteom | 配置注册与生效 | 0 |  | task:ed726d75f1f1835730a4448d5b1c31f8 |
| server/liteom | 模块实现、接口与状态机制 | 0 |  | task:ed726d75f1f1835730a4448d5b1c31f8 |
| server/liteom | 资源寿命与错误清理 | 0 |  | task:ed726d75f1f1835730a4448d5b1c31f8 |
| server/simpleInstall | 模块实现、接口与状态机制 | 0 |  | task:d44e798fa8afd5ce6a88cd56c125aff8 |
| server/src | 模块实现、接口与状态机制 | 0 |  | task:28b450e80890f65a9f3c25ca467ed66d |
| server/src/bin | 模块实现、接口与状态机制 | 0 |  | task:c57fbbad9670b136229b598a2eac9020 |
| server/src/bin/gs_cgroup | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:aea5d3740a03cbe617e566eb2e834871 |
| server/src/bin/gs_cgroup | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:aea5d3740a03cbe617e566eb2e834871 |
| server/src/bin/gs_cgroup | 模块实现、接口与状态机制 / 分批3 | 1 |  | task:aea5d3740a03cbe617e566eb2e834871 |
| server/src/bin/gs_guc | 配置注册与生效 / 分批1 | 1 |  | task:ab1ea3a2ca433f01abc2dffb0ef81dda |
| server/src/bin/gs_guc | 配置注册与生效 / 分批2 | 1 |  | task:ab1ea3a2ca433f01abc2dffb0ef81dda |
| server/src/bin/gs_guc | 配置注册与生效 / 分批3 | 1 |  | task:ab1ea3a2ca433f01abc2dffb0ef81dda |
| server/src/bin/gs_guc | 模块实现、接口与状态机制 | 3 |  | task:ab1ea3a2ca433f01abc2dffb0ef81dda |
| server/src/bin/gs_loader | 模块实现、接口与状态机制 | 1 |  | task:112c91345d5f3f9c6e5dab1e87e9c4c5 |
| server/src/bin/gs_log | 模块实现、接口与状态机制 | 2 |  | task:1b57e36cd9942d0b9e56f1875015afc9 |
| server/src/bin/gs_persist | 模块实现、接口与状态机制 | 3 |  | task:db9f2b6593c8160783b92c9faf234c82 |
| server/src/bin/gs_plan_simulator | 模块实现、接口与状态机制 | 0 |  | task:2ab733311887357e27c0d14774ccfede |
| server/src/bin/gs_plan_simulator | 计划生成与计划接口 | 0 |  | task:2ab733311887357e27c0d14774ccfede |
| server/src/bin/gs_retrieve | 模块实现、接口与状态机制 | 1 |  | task:737dbf396b74641457fc345059a6fec2 |
| server/src/bin/gsqlerr | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:57c12c4bc4180ce0742eb74865fbdb2e |
| server/src/bin/gsqlerr | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:57c12c4bc4180ce0742eb74865fbdb2e |
| server/src/bin/gsqlerr | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:57c12c4bc4180ce0742eb74865fbdb2e |
| server/src/bin/initdb | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:e6c790e66b6d30a0ae1aa1e4c86a0b8a |
| server/src/bin/initdb | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:e6c790e66b6d30a0ae1aa1e4c86a0b8a |
| server/src/bin/initdb | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:e6c790e66b6d30a0ae1aa1e4c86a0b8a |
| server/src/bin/initdb | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:e6c790e66b6d30a0ae1aa1e4c86a0b8a |
| server/src/bin/initdb | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:e6c790e66b6d30a0ae1aa1e4c86a0b8a |
| server/src/bin/libog_query | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:b59dd9da2ae775062286f7681b4adecd |
| server/src/bin/libog_query | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:b59dd9da2ae775062286f7681b4adecd |
| server/src/bin/libog_query | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:b59dd9da2ae775062286f7681b4adecd |
| server/src/bin/libog_query | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:b59dd9da2ae775062286f7681b4adecd |
| server/src/bin/license_checker | 模块实现、接口与状态机制 | 2 |  | task:49b5966870a01d284182b8f684323c5b |
| server/src/bin/pg_basebackup | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:3ce1f63c6716f8932ec1e88966ed1504 |
| server/src/bin/pg_basebackup | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:3ce1f63c6716f8932ec1e88966ed1504 |
| server/src/bin/pg_basebackup | 持久化与恢复 | 1 |  | task:3ce1f63c6716f8932ec1e88966ed1504 |
| server/src/bin/pg_basebackup | 资源寿命与错误清理 | 1 |  | task:3ce1f63c6716f8932ec1e88966ed1504 |
| server/src/bin/pg_config | 配置注册与生效 | 1 |  | task:b6f0e8b374499a113b7367053f66acbb |
| server/src/bin/pg_config | 模块实现、接口与状态机制 | 0 |  | task:b6f0e8b374499a113b7367053f66acbb |
| server/src/bin/pg_controldata | 模块实现、接口与状态机制 | 1 |  | task:a90a194d970c25eda5898c632eb1399c |
| server/src/bin/pg_ctl | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:4b9a5f81c0fd7aa7e5ed898dc982ab82 |
| server/src/bin/pg_ctl | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:4b9a5f81c0fd7aa7e5ed898dc982ab82 |
| server/src/bin/pg_ctl | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:4b9a5f81c0fd7aa7e5ed898dc982ab82 |
| server/src/bin/pg_ctl | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:4b9a5f81c0fd7aa7e5ed898dc982ab82 |
| server/src/bin/pg_ctl | 资源寿命与错误清理 | 1 |  | task:4b9a5f81c0fd7aa7e5ed898dc982ab82 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批1 | 6 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批5 | 2 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_dump | 资源寿命与错误清理 | 1 |  | task:410956962a351d7aca4a69860b2679e7 |
| server/src/bin/pg_probackup | 配置注册与生效 | 2 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup | 模块实现、接口与状态机制 / 分批4 | 5 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup | 模块实现、接口与状态机制 / 分批5 | 12 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup | 模块实现、接口与状态机制 / 分批6 | 5 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup | 模块实现、接口与状态机制 / 分批7 | 6 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup | 持久化与恢复 | 1 |  | task:75d9c263610dd74dd5f54df4d0756aa3 |
| server/src/bin/pg_probackup/oss/include | 模块实现、接口与状态机制 | 0 |  | task:8e57f03fa4ff08ac7e9a3a23192c7c92 |
| server/src/bin/pg_resetxlog | 模块实现、接口与状态机制 | 0 |  | task:d5ea71849af71e92014bd51097de02d6 |
| server/src/bin/pg_resetxlog | 持久化与恢复 | 1 |  | task:d5ea71849af71e92014bd51097de02d6 |
| server/src/bin/pg_rewind | 模块实现、接口与状态机制 / 分批1 | 6 |  | task:ac3ebc0d5a07ca218b9f111f6d96c8a9 |
| server/src/bin/pg_rewind | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:ac3ebc0d5a07ca218b9f111f6d96c8a9 |
| server/src/bin/pg_rewind | 持久化与恢复 | 1 |  | task:ac3ebc0d5a07ca218b9f111f6d96c8a9 |
| server/src/bin/pg_upgrade | 模块实现、接口与状态机制 | 1 |  | task:4b777ac3f5b19450cfc055c31934d3e0 |
| server/src/bin/pgevent | 模块实现、接口与状态机制 | 1 |  | task:1497cca96649ccec1ae4d22fe368ba59 |
| server/src/bin/pgxc_clean | 模块实现、接口与状态机制 | 2 |  | task:84b922bdc6f4c0a1e14de0ac7b6e212c |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批3 | 5 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批10 | 2 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批11 | 2 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/psql | 模块实现、接口与状态机制 / 分批12 | 2 |  | task:c95e9f2adcc0c2eb2a23ecb5430d3b7a |
| server/src/bin/scripts | 缓存、失效与复用 | 0 |  | task:1bae2388f81494cad080dd31f68a95aa |
| server/src/bin/scripts | 模块实现、接口与状态机制 / 分批1 | 7 |  | task:1bae2388f81494cad080dd31f68a95aa |
| server/src/bin/scripts | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:1bae2388f81494cad080dd31f68a95aa |
| server/src/bin/scripts | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:1bae2388f81494cad080dd31f68a95aa |
| server/src/bin/scripts | 计划生成与计划接口 | 1 |  | task:1bae2388f81494cad080dd31f68a95aa |
| server/src/bin/scripts | 资源寿命与错误清理 | 0 |  | task:1bae2388f81494cad080dd31f68a95aa |
| server/src/bin/smb_mgr | 模块实现、接口与状态机制 | 1 |  | task:b1862f64fb4665e78ec9289dca6c72be |
| server/src/common | 模块实现、接口与状态机制 | 0 |  | task:3bff787e5fb7fbbc2918e2278c02bc02 |
| server/src/common/backend | 模块实现、接口与状态机制 | 0 |  | task:a3288e4885a329c01f5ffc6f9f04b938 |
| server/src/common/backend/catalog | 配置注册与生效 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批4 | 2 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批5 | 3 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批7 | 2 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批8 | 3 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批9 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批10 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批11 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批12 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批13 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批14 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批15 | 3 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批16 | 7 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批17 | 7 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批18 | 5 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批19 | 12 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批20 | 3 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/catalog | 模块实现、接口与状态机制 / 分批21 | 1 |  | task:c4fa2c766badf364f2127c5652c21111 |
| server/src/common/backend/client_logic | 缓存、失效与复用 | 1 |  | task:f15b3d3ac2014b7959e1caca84d0dbee |
| server/src/common/backend/client_logic | 模块实现、接口与状态机制 | 2 |  | task:f15b3d3ac2014b7959e1caca84d0dbee |
| server/src/common/backend/lib | 缓存、失效与复用 | 1 |  | task:644e1797796bc3193d5d83a42dcaa50b |
| server/src/common/backend/lib | 模块实现、接口与状态机制 | 9 |  | task:644e1797796bc3193d5d83a42dcaa50b |
| server/src/common/backend/libpq | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:6450d2d3bbefacac91bb727634e02311 |
| server/src/common/backend/libpq | 模块实现、接口与状态机制 / 分批2 | 4 |  | task:6450d2d3bbefacac91bb727634e02311 |
| server/src/common/backend/libpq | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:6450d2d3bbefacac91bb727634e02311 |
| server/src/common/backend/nodes | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:52f15f674b5314ccaa6c4371ab0f9a15 |
| server/src/common/backend/nodes | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:52f15f674b5314ccaa6c4371ab0f9a15 |
| server/src/common/backend/nodes | 模块实现、接口与状态机制 / 分批3 | 3 |  | task:52f15f674b5314ccaa6c4371ab0f9a15 |
| server/src/common/backend/nodes | 模块实现、接口与状态机制 / 分批4 | 2 |  | task:52f15f674b5314ccaa6c4371ab0f9a15 |
| server/src/common/backend/nodes | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:52f15f674b5314ccaa6c4371ab0f9a15 |
| server/src/common/backend/nodes | 模块实现、接口与状态机制 / 分批6 | 3 |  | task:52f15f674b5314ccaa6c4371ab0f9a15 |
| server/src/common/backend/nodes | 模块实现、接口与状态机制 / 分批7 | 1 |  | task:52f15f674b5314ccaa6c4371ab0f9a15 |
| server/src/common/backend/nodes | 模块实现、接口与状态机制 / 分批8 | 2 |  | task:52f15f674b5314ccaa6c4371ab0f9a15 |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批5 | 3 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批7 | 2 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批8 | 3 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批9 | 1 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批10 | 3 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批11 | 3 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批12 | 3 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批13 | 1 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/parser | 模块实现、接口与状态机制 / 分批14 | 2 |  | task:19ab79d26cba4531500f0767ec3e1f8f |
| server/src/common/backend/pgxc_single | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:13df5375f6bf6494d5a2941c7241393a |
| server/src/common/backend/pgxc_single | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:13df5375f6bf6494d5a2941c7241393a |
| server/src/common/backend/pgxc_single | 模块实现、接口与状态机制 / 分批3 | 1 |  | task:13df5375f6bf6494d5a2941c7241393a |
| server/src/common/backend/pgxc_single | 模块实现、接口与状态机制 / 分批4 | 2 |  | task:13df5375f6bf6494d5a2941c7241393a |
| server/src/common/backend/pgxc_single | 模块实现、接口与状态机制 / 分批5 | 2 |  | task:13df5375f6bf6494d5a2941c7241393a |
| server/src/common/backend/port | 模块实现、接口与状态机制 / 分批1 | 10 |  | task:e399fd0cc1f7d5ad9bae1792ab412184 |
| server/src/common/backend/port | 模块实现、接口与状态机制 / 分批2 | 13 |  | task:e399fd0cc1f7d5ad9bae1792ab412184 |
| server/src/common/backend/port | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:e399fd0cc1f7d5ad9bae1792ab412184 |
| server/src/common/backend/port | 资源寿命与错误清理 | 2 |  | task:e399fd0cc1f7d5ad9bae1792ab412184 |
| server/src/common/backend/regex | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:14baf6487b95346014f275707aaef60b |
| server/src/common/backend/regex | 模块实现、接口与状态机制 / 分批2 | 7 |  | task:14baf6487b95346014f275707aaef60b |
| server/src/common/backend/regex | 资源寿命与错误清理 | 1 |  | task:14baf6487b95346014f275707aaef60b |
| server/src/common/backend/snowball | 模块实现、接口与状态机制 / 分批1 | 21 |  | task:79f22a49041d7c63b009d1bd24a44820 |
| server/src/common/backend/snowball | 模块实现、接口与状态机制 / 分批2 | 13 |  | task:79f22a49041d7c63b009d1bd24a44820 |
| server/src/common/backend/snowball | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:79f22a49041d7c63b009d1bd24a44820 |
| server/src/common/backend/tsearch | 代价与基数估算 | 1 |  | task:a04e5d54814c1ea696ba284f4716e94a |
| server/src/common/backend/tsearch | 模块实现、接口与状态机制 / 分批1 | 12 |  | task:a04e5d54814c1ea696ba284f4716e94a |
| server/src/common/backend/tsearch | 模块实现、接口与状态机制 / 分批2 | 5 |  | task:a04e5d54814c1ea696ba284f4716e94a |
| server/src/common/backend/utils | 模块实现、接口与状态机制 | 0 |  | task:4bba3924f5798c9162462ffc2b4b9362 |
| server/src/common/backend/utils/adt | 代价与基数估算 / 分批1 | 3 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 代价与基数估算 / 分批2 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批3 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批4 | 11 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批6 | 2 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批7 | 9 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批8 | 2 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批9 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批10 | 3 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批11 | 7 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批12 | 5 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批13 | 2 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批14 | 4 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批15 | 7 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批16 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批17 | 6 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批18 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批19 | 4 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批20 | 3 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批21 | 2 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批22 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批23 | 4 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批24 | 3 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批25 | 13 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批26 | 2 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批27 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批28 | 4 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 模块实现、接口与状态机制 / 分批29 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 持久化与恢复 | 3 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/adt | 资源寿命与错误清理 | 1 |  | task:58903cf5ed0399f69f322e538f6f47d4 |
| server/src/common/backend/utils/cache | 缓存、失效与复用 / 分批1 | 5 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/cache | 缓存、失效与复用 / 分批2 | 8 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/cache | 缓存、失效与复用 / 分批3 | 4 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/cache | 缓存、失效与复用 / 分批4 | 1 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/cache | 缓存、失效与复用 / 分批5 | 1 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/cache | 缓存、失效与复用 / 分批6 | 1 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/cache | 缓存、失效与复用 / 分批7 | 4 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/cache | 模块实现、接口与状态机制 | 4 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/cache | 计划生成与计划接口 | 1 |  | task:18d24ba36498dafaeba8fd9f47acb6e1 |
| server/src/common/backend/utils/error | 模块实现、接口与状态机制 | 4 |  | task:e168c7623f787d0c09f893206c65d897 |
| server/src/common/backend/utils/error | 资源寿命与错误清理 | 1 |  | task:e168c7623f787d0c09f893206c65d897 |
| server/src/common/backend/utils/fmgr | 模块实现、接口与状态机制 | 3 |  | task:c6750e389814e2eac1be75b1e1a5ecaa |
| server/src/common/backend/utils/gsplsql | 模块实现、接口与状态机制 | 2 |  | task:9d85caa0bb4fe81b26e335c6e560ab6d |
| server/src/common/backend/utils/hash | 模块实现、接口与状态机制 | 2 |  | task:a547f7a39e003d8c0df8558e624ba9a7 |
| server/src/common/backend/utils/init | 模块实现、接口与状态机制 | 3 |  | task:b6af25e0bdb894b5f317861085cd8a72 |
| server/src/common/backend/utils/matrix | 模块实现、接口与状态机制 | 1 |  | task:46b54d3ae4d2947fc3c19bfdf5437111 |
| server/src/common/backend/utils/mb | 模块实现、接口与状态机制 | 9 |  | task:4c80e8593ff7541cb4242e89f868a1f8 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批10 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批11 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批12 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批13 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批14 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批15 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批16 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批17 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批18 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批19 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批20 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批21 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批22 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批23 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批24 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批25 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批26 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批27 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批28 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批29 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批30 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批31 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批32 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批33 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批34 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批35 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批36 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批37 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批38 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/Unicode | 模块实现、接口与状态机制 / 分批39 | 0 |  | task:0a2b38f5cd4a594d51ec0266cfaa4f96 |
| server/src/common/backend/utils/mb/conversion_procs | 模块实现、接口与状态机制 / 分批1 | 10 |  | task:e86db6c95fa076c0605091bcd9723704 |
| server/src/common/backend/utils/mb/conversion_procs | 模块实现、接口与状态机制 / 分批2 | 10 |  | task:e86db6c95fa076c0605091bcd9723704 |
| server/src/common/backend/utils/mb/conversion_procs | 模块实现、接口与状态机制 / 分批3 | 7 |  | task:e86db6c95fa076c0605091bcd9723704 |
| server/src/common/backend/utils/mb/nlssort | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:73f586a514e115cd45c8e6e2c308b3cf |
| server/src/common/backend/utils/mb/nlssort | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:73f586a514e115cd45c8e6e2c308b3cf |
| server/src/common/backend/utils/mb/nlssort | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:73f586a514e115cd45c8e6e2c308b3cf |
| server/src/common/backend/utils/mb/nlssort | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:73f586a514e115cd45c8e6e2c308b3cf |
| server/src/common/backend/utils/misc | 配置注册与生效 / 分批1 | 0 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/misc | 配置注册与生效 / 分批2 | 1 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/misc | 配置注册与生效 / 分批3 | 3 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/misc | 配置注册与生效 / 分批4 | 1 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/misc | 配置注册与生效 / 分批5 | 1 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/misc | 配置注册与生效 / 分批6 | 1 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/misc | 模块实现、接口与状态机制 / 分批1 | 10 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/misc | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/misc | 资源寿命与错误清理 | 1 |  | task:5700438e2b713847543b2e4140d089d8 |
| server/src/common/backend/utils/mmgr | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:9afab589e4dc6f9b2ace1aaa1985be7e |
| server/src/common/backend/utils/mmgr | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:9afab589e4dc6f9b2ace1aaa1985be7e |
| server/src/common/backend/utils/mmgr | 资源寿命与错误清理 | 6 |  | task:9afab589e4dc6f9b2ace1aaa1985be7e |
| server/src/common/backend/utils/mmgr | 事务、可见性与结束处理 | 1 |  | task:9afab589e4dc6f9b2ace1aaa1985be7e |
| server/src/common/backend/utils/resowner | 模块实现、接口与状态机制 | 0 |  | task:8b1d31501ed4cbb842ece2e74d67c399 |
| server/src/common/backend/utils/resowner | 资源寿命与错误清理 | 1 |  | task:8b1d31501ed4cbb842ece2e74d67c399 |
| server/src/common/backend/utils/sort | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:53ffbf0c76fc01104d61e1a2bae6d047 |
| server/src/common/backend/utils/sort | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:53ffbf0c76fc01104d61e1a2bae6d047 |
| server/src/common/backend/utils/time | 模块实现、接口与状态机制 | 2 |  | task:6c0b27bec3740410b0492820ea4ccfe6 |
| server/src/common/interfaces | 模块实现、接口与状态机制 | 0 |  | task:d36929b6b8f0569cc9f3d188edab1b6f |
| server/src/common/interfaces/ecpg | 模块实现、接口与状态机制 | 0 |  | task:0334705bd0695d851ab1f952967f7467 |
| server/src/common/interfaces/ecpg/compatlib | 模块实现、接口与状态机制 | 1 |  | task:704f2028895360df364b51c4bb116d7b |
| server/src/common/interfaces/ecpg/ecpglib | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:4568dcac1f88482a99b4678072d9548b |
| server/src/common/interfaces/ecpg/ecpglib | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:4568dcac1f88482a99b4678072d9548b |
| server/src/common/interfaces/ecpg/ecpglib | 资源寿命与错误清理 | 2 |  | task:4568dcac1f88482a99b4678072d9548b |
| server/src/common/interfaces/ecpg/include | 配置注册与生效 | 0 |  | task:1d452f50b2a4be8152b86ec951aa6c6d |
| server/src/common/interfaces/ecpg/include | 模块实现、接口与状态机制 | 0 |  | task:1d452f50b2a4be8152b86ec951aa6c6d |
| server/src/common/interfaces/ecpg/include | 资源寿命与错误清理 | 0 |  | task:1d452f50b2a4be8152b86ec951aa6c6d |
| server/src/common/interfaces/ecpg/pgtypeslib | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:1e3545400724d6563999f76e84d134b6 |
| server/src/common/interfaces/ecpg/pgtypeslib | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:1e3545400724d6563999f76e84d134b6 |
| server/src/common/interfaces/ecpg/preproc | 模块实现、接口与状态机制 / 分批1 | 7 |  | task:a2974d690e076704d2b182d6cb1a21d9 |
| server/src/common/interfaces/ecpg/preproc | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:a2974d690e076704d2b182d6cb1a21d9 |
| server/src/common/interfaces/ecpg/preproc | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:a2974d690e076704d2b182d6cb1a21d9 |
| server/src/common/interfaces/ecpg/test | 回归主题：ecpg | 0 |  | task:3c6404bddb5fd2b00011b536c4f4136b |
| server/src/common/interfaces/ecpg/test | 回归主题：make | 0 |  | task:3c6404bddb5fd2b00011b536c4f4136b |
| server/src/common/interfaces/ecpg/test | 回归主题：makefile | 0 |  | task:3c6404bddb5fd2b00011b536c4f4136b |
| server/src/common/interfaces/ecpg/test | 回归主题：pg | 1 |  | task:3c6404bddb5fd2b00011b536c4f4136b |
| server/src/common/interfaces/ecpg/test | 回归主题：regress | 0 |  | task:3c6404bddb5fd2b00011b536c4f4136b |
| server/src/common/interfaces/ecpg/test | 回归主题：regression | 0 |  | task:3c6404bddb5fd2b00011b536c4f4136b |
| server/src/common/interfaces/ecpg/test | 回归主题：resultmap | 0 |  | task:3c6404bddb5fd2b00011b536c4f4136b |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：charfuncs | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：dec | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：describe | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：makefile | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：rfmtdate | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：rfmtlong | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：rnull | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：sqlda | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/compat_informix | 回归主题：test | 0 |  | task:b85eaff8d40aec68dc5cf8536a69d1e7 |
| server/src/common/interfaces/ecpg/test/connect | 回归主题：makefile | 0 |  | task:92cd8c0393343f19dd22e065bb2a6b9e |
| server/src/common/interfaces/ecpg/test/connect | 回归主题：readme | 0 |  | task:92cd8c0393343f19dd22e065bb2a6b9e |
| server/src/common/interfaces/ecpg/test/connect | 回归主题：test | 0 |  | task:92cd8c0393343f19dd22e065bb2a6b9e |
| server/src/common/interfaces/ecpg/test/data | 回归主题：fakedata | 0 |  | task:2df64f5e54da629efe6f93058cca54c1 |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：compat / 分批1 | 8 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：compat / 分批2 | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：connect-test | 5 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：connect-test1-mingw | 0 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：pgtypeslib-dt | 2 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：pgtypeslib-nan | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：pgtypeslib-num | 2 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-array | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-autoprep | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-comment | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-cursor | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-define | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-describe | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-init | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-outofscope | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-strings | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-type | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-variable | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：preproc-whenever | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-array | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-binary | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-code | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-copystdout | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-define | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-desc | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-describe | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-dynalloc | 2 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-dyntest | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-execute | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-fetch | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-func | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-indicators | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-insupd | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-oldexec | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-parser | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-quote | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-show | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：sql-sqlda | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：thread-alloc | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：thread-descriptor | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：thread-prep | 1 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/expected | 回归主题：thread-thread | 2 |  | task:00aff72160d1ca29294a925bcb093e6e |
| server/src/common/interfaces/ecpg/test/performance | 回归主题：makefile | 0 |  | task:d8c5c8951cdccbc233d7d2940c3dd43b |
| server/src/common/interfaces/ecpg/test/performance | 回归主题：perftest | 0 |  | task:d8c5c8951cdccbc233d7d2940c3dd43b |
| server/src/common/interfaces/ecpg/test/pgtypeslib | 回归主题：dt | 0 |  | task:bc89db0395ea4af84a4676a4e2c40d75 |
| server/src/common/interfaces/ecpg/test/pgtypeslib | 回归主题：makefile | 0 |  | task:bc89db0395ea4af84a4676a4e2c40d75 |
| server/src/common/interfaces/ecpg/test/pgtypeslib | 回归主题：nan | 0 |  | task:bc89db0395ea4af84a4676a4e2c40d75 |
| server/src/common/interfaces/ecpg/test/pgtypeslib | 回归主题：num | 0 |  | task:bc89db0395ea4af84a4676a4e2c40d75 |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：array | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：autoprep | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：comment | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：cursor | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：define | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：init | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：makefile | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：outofscope | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：strings | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：struct | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：type | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：variable | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/preproc | 回归主题：whenever | 0 |  | task:4300f90987ac0e9535c6ec0ad5010c4e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：array | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：binary | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：code | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：copystdout | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：define | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：desc | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：describe | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：dynalloc | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：dyntest | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：execute | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：fetch | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：func | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：indicators | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：insupd | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：makefile | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：oldexec | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：parser | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：quote | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：show | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/sql | 回归主题：sqlda | 0 |  | task:4ca088369d6d6218c3ede37a2e36686e |
| server/src/common/interfaces/ecpg/test/thread | 回归主题：alloc | 0 |  | task:dc3b6e5d6a1382b0931635c4cd39814a |
| server/src/common/interfaces/ecpg/test/thread | 回归主题：descriptor | 0 |  | task:dc3b6e5d6a1382b0931635c4cd39814a |
| server/src/common/interfaces/ecpg/test/thread | 回归主题：makefile | 0 |  | task:dc3b6e5d6a1382b0931635c4cd39814a |
| server/src/common/interfaces/ecpg/test/thread | 回归主题：prep | 0 |  | task:dc3b6e5d6a1382b0931635c4cd39814a |
| server/src/common/interfaces/ecpg/test/thread | 回归主题：thread | 0 |  | task:dc3b6e5d6a1382b0931635c4cd39814a |
| server/src/common/interfaces/libpq | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:fdc3dba512cc3053f64f371e3456ffd0 |
| server/src/common/interfaces/libpq | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:fdc3dba512cc3053f64f371e3456ffd0 |
| server/src/common/interfaces/libpq | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:fdc3dba512cc3053f64f371e3456ffd0 |
| server/src/common/interfaces/libpq | 模块实现、接口与状态机制 / 分批4 | 4 |  | task:fdc3dba512cc3053f64f371e3456ffd0 |
| server/src/common/interfaces/libpq | 模块实现、接口与状态机制 / 分批5 | 4 |  | task:fdc3dba512cc3053f64f371e3456ffd0 |
| server/src/common/interfaces/libpq/client_logic_cache | 缓存、失效与复用 / 分批1 | 11 |  | task:de6f78c2f77394453ee50631be18891e |
| server/src/common/interfaces/libpq/client_logic_cache | 缓存、失效与复用 / 分批2 | 0 |  | task:de6f78c2f77394453ee50631be18891e |
| server/src/common/interfaces/libpq/client_logic_cache | 模块实现、接口与状态机制 | 8 |  | task:de6f78c2f77394453ee50631be18891e |
| server/src/common/interfaces/libpq/client_logic_common | 模块实现、接口与状态机制 | 7 |  | task:b07e23e9afdd83bee2ac0b3b1b5ad15b |
| server/src/common/interfaces/libpq/client_logic_data_fetcher | 模块实现、接口与状态机制 | 4 |  | task:1b4e8575b27251355886f03e172fe43b |
| server/src/common/interfaces/libpq/client_logic_expressions | 模块实现、接口与状态机制 | 5 |  | task:c4dca1c5344fd74ecfc3bf7850303b60 |
| server/src/common/interfaces/libpq/client_logic_fmt | 模块实现、接口与状态机制 | 11 |  | task:1f0b1d44a4599889fe5ec8d899247b8f |
| server/src/common/interfaces/libpq/client_logic_hooks | 模块实现、接口与状态机制 | 7 |  | task:0ea59d200c35bd2cee288082f2b83b0e |
| server/src/common/interfaces/libpq/client_logic_processor | 模块实现、接口与状态机制 / 分批1 | 13 |  | task:7e1ffe1420a41c3f0f13f8c5e0ddfe0d |
| server/src/common/interfaces/libpq/client_logic_processor | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:7e1ffe1420a41c3f0f13f8c5e0ddfe0d |
| server/src/common/interfaces/libpq/frontend_parser | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:140d8e3fdbd028253712db8e01f65008 |
| server/src/common/interfaces/libpq/frontend_parser | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:140d8e3fdbd028253712db8e01f65008 |
| server/src/common/interfaces/libpq/frontend_parser | 模块实现、接口与状态机制 / 分批3 | 6 |  | task:140d8e3fdbd028253712db8e01f65008 |
| server/src/common/interfaces/libpq/frontend_parser | 资源寿命与错误清理 | 1 |  | task:140d8e3fdbd028253712db8e01f65008 |
| server/src/common/interfaces/libpq/jdbc | 模块实现、接口与状态机制 | 6 |  | task:dfc219b1987a37879cc0f3fe58557115 |
| server/src/common/interfaces/libpq/jdbc | 资源寿命与错误清理 | 1 |  | task:dfc219b1987a37879cc0f3fe58557115 |
| server/src/common/interfaces/libpq/po | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:9b37a156fe2fecddf3cf42b1378a9554 |
| server/src/common/interfaces/libpq/po | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:9b37a156fe2fecddf3cf42b1378a9554 |
| server/src/common/interfaces/libpq/test | 回归主题：expected | 0 |  | task:b88ba48d4bf099cb4d47e02fe78bcbaa |
| server/src/common/interfaces/libpq/test | 回归主题：makefile | 0 |  | task:b88ba48d4bf099cb4d47e02fe78bcbaa |
| server/src/common/interfaces/libpq/test | 回归主题：readme | 0 |  | task:b88ba48d4bf099cb4d47e02fe78bcbaa |
| server/src/common/interfaces/libpq/test | 回归主题：regress | 0 |  | task:b88ba48d4bf099cb4d47e02fe78bcbaa |
| server/src/common/interfaces/libpq/test | 回归主题：uri-regress | 1 |  | task:b88ba48d4bf099cb4d47e02fe78bcbaa |
| server/src/common/pgxc | 模块实现、接口与状态机制 | 1 |  | task:7276e6e2928fede7f4c6721b9b587c6a |
| server/src/common/pl | 模块实现、接口与状态机制 | 0 |  | task:29d5d9d7e7dc64482fb05ae4e0359846 |
| server/src/common/pl/plpgsql | 缓存、失效与复用 | 1 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批5 | 2 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批7 | 2 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批8 | 4 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpgsql | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:8260ce69eb05eb9357e36b731192f02f |
| server/src/common/pl/plpython | 模块实现、接口与状态机制 / 分批1 | 9 |  | task:0bb9d2f4c40215d90e18338598dc884a |
| server/src/common/pl/plpython | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:0bb9d2f4c40215d90e18338598dc884a |
| server/src/common/pl/plpython | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:0bb9d2f4c40215d90e18338598dc884a |
| server/src/common/pl/plpython | 计划生成与计划接口 | 1 |  | task:0bb9d2f4c40215d90e18338598dc884a |
| server/src/common/pl/plpython | 资源寿命与错误清理 | 1 |  | task:0bb9d2f4c40215d90e18338598dc884a |
| server/src/common/pl/plpython | 事务、可见性与结束处理 | 1 |  | task:0bb9d2f4c40215d90e18338598dc884a |
| server/src/common/port | 模块实现、接口与状态机制 / 分批1 | 12 |  | task:e1c1cd745dd84a6a95e7d7acf224883d |
| server/src/common/port | 模块实现、接口与状态机制 / 分批2 | 24 |  | task:e1c1cd745dd84a6a95e7d7acf224883d |
| server/src/common/port | 模块实现、接口与状态机制 / 分批3 | 18 |  | task:e1c1cd745dd84a6a95e7d7acf224883d |
| server/src/common/port | 资源寿命与错误清理 | 4 |  | task:e1c1cd745dd84a6a95e7d7acf224883d |
| server/src/common/template | 模块实现、接口与状态机制 | 0 |  | task:e08195fba5224876e62829739d04ddd6 |
| server/src/common/timezone | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:969d092c432ecdefe1eae22b086e4ce7 |
| server/src/common/timezone | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:969d092c432ecdefe1eae22b086e4ce7 |
| server/src/common/timezone | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:969d092c432ecdefe1eae22b086e4ce7 |
| server/src/common/timezone | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:969d092c432ecdefe1eae22b086e4ce7 |
| server/src/common/timezone | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:969d092c432ecdefe1eae22b086e4ce7 |
| server/src/common/timezone | 模块实现、接口与状态机制 / 分批6 | 5 |  | task:969d092c432ecdefe1eae22b086e4ce7 |
| server/src/common/timezone | 模块实现、接口与状态机制 / 分批7 | 1 |  | task:969d092c432ecdefe1eae22b086e4ce7 |
| server/src/common/tutorial | 模块实现、接口与状态机制 | 3 |  | task:dbf5017b32dec1d7623954bb26fa1648 |
| server/src/gausskernel | 模块实现、接口与状态机制 | 0 |  | task:ea1e22698e0693d6dd89f1f9f88c02c8 |
| server/src/gausskernel/bootstrap | 模块实现、接口与状态机制 | 1 |  | task:10f45d323617b38fab3d8ccd8631edd9 |
| server/src/gausskernel/cbb | 模块实现、接口与状态机制 | 0 |  | task:ad2049569c31215e48ff96c04ec8fb34 |
| server/src/gausskernel/cbb/bbox | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:33402bd80f3711737e14d082b5f28765 |
| server/src/gausskernel/cbb/bbox | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:33402bd80f3711737e14d082b5f28765 |
| server/src/gausskernel/cbb/communication | 模块实现、接口与状态机制 / 分批1 | 7 |  | task:157e9033e6a49de2a0b0f6f6014b77b7 |
| server/src/gausskernel/cbb/communication | 模块实现、接口与状态机制 / 分批2 | 4 |  | task:157e9033e6a49de2a0b0f6f6014b77b7 |
| server/src/gausskernel/cbb/communication | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:157e9033e6a49de2a0b0f6f6014b77b7 |
| server/src/gausskernel/cbb/communication | 模块实现、接口与状态机制 / 分批4 | 6 |  | task:157e9033e6a49de2a0b0f6f6014b77b7 |
| server/src/gausskernel/cbb/communication | 模块实现、接口与状态机制 / 分批5 | 7 |  | task:157e9033e6a49de2a0b0f6f6014b77b7 |
| server/src/gausskernel/cbb/communication | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:157e9033e6a49de2a0b0f6f6014b77b7 |
| server/src/gausskernel/cbb/communication | 资源寿命与错误清理 | 1 |  | task:157e9033e6a49de2a0b0f6f6014b77b7 |
| server/src/gausskernel/cbb/extension | 模块实现、接口与状态机制 | 7 |  | task:092d894302b5bc3f51aaf0c71efd755d |
| server/src/gausskernel/cbb/grpc | 模块实现、接口与状态机制 | 1 |  | task:66974c393dfc81058ee7b03aa966ef11 |
| server/src/gausskernel/cbb/instruments | 模块实现、接口与状态机制 / 分批1 | 8 |  | task:5f140be30f486b5dab1ceb4905d8c75a |
| server/src/gausskernel/cbb/instruments | 模块实现、接口与状态机制 / 分批2 | 6 |  | task:5f140be30f486b5dab1ceb4905d8c75a |
| server/src/gausskernel/cbb/instruments | 模块实现、接口与状态机制 / 分批3 | 7 |  | task:5f140be30f486b5dab1ceb4905d8c75a |
| server/src/gausskernel/cbb/instruments | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:5f140be30f486b5dab1ceb4905d8c75a |
| server/src/gausskernel/cbb/instruments | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:5f140be30f486b5dab1ceb4905d8c75a |
| server/src/gausskernel/cbb/instruments | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:5f140be30f486b5dab1ceb4905d8c75a |
| server/src/gausskernel/cbb/instruments | 计划生成与计划接口 | 1 |  | task:5f140be30f486b5dab1ceb4905d8c75a |
| server/src/gausskernel/cbb/instruments | 事务、可见性与结束处理 | 1 |  | task:5f140be30f486b5dab1ceb4905d8c75a |
| server/src/gausskernel/cbb/utils | 模块实现、接口与状态机制 / 分批1 | 4 |  | task:22c266182bc38e67bf2163be2571a029 |
| server/src/gausskernel/cbb/utils | 模块实现、接口与状态机制 / 分批2 | 9 |  | task:22c266182bc38e67bf2163be2571a029 |
| server/src/gausskernel/cbb/utils | 模块实现、接口与状态机制 / 分批3 | 6 |  | task:22c266182bc38e67bf2163be2571a029 |
| server/src/gausskernel/cbb/workload | 配置注册与生效 | 1 |  | task:0187c43beffcfe375116cd79a90ce43a |
| server/src/gausskernel/cbb/workload | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:0187c43beffcfe375116cd79a90ce43a |
| server/src/gausskernel/cbb/workload | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:0187c43beffcfe375116cd79a90ce43a |
| server/src/gausskernel/cbb/workload | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:0187c43beffcfe375116cd79a90ce43a |
| server/src/gausskernel/cbb/workload | 模块实现、接口与状态机制 / 分批4 | 4 |  | task:0187c43beffcfe375116cd79a90ce43a |
| server/src/gausskernel/cbb/workload | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:0187c43beffcfe375116cd79a90ce43a |
| server/src/gausskernel/cbb/workload | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:0187c43beffcfe375116cd79a90ce43a |
| server/src/gausskernel/cbb/workload | 资源寿命与错误清理 | 1 |  | task:0187c43beffcfe375116cd79a90ce43a |
| server/src/gausskernel/dbmind | 模块实现、接口与状态机制 | 0 |  | task:596bd6ee3b7df607adfdbb990c0c277c |
| server/src/gausskernel/dbmind/db4ai | 缓存、失效与复用 | 1 |  | task:49c6b41d319af4d8073257809a367c21 |
| server/src/gausskernel/dbmind/db4ai | 模块实现、接口与状态机制 / 分批1 | 7 |  | task:49c6b41d319af4d8073257809a367c21 |
| server/src/gausskernel/dbmind/db4ai | 模块实现、接口与状态机制 / 分批2 | 13 |  | task:49c6b41d319af4d8073257809a367c21 |
| server/src/gausskernel/dbmind/db4ai | 模块实现、接口与状态机制 / 分批3 | 6 |  | task:49c6b41d319af4d8073257809a367c21 |
| server/src/gausskernel/dbmind/deepsql | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:3a6942832b8029b6d17d29a4fb6dfdaa |
| server/src/gausskernel/dbmind/deepsql | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:3a6942832b8029b6d17d29a4fb6dfdaa |
| server/src/gausskernel/dbmind/deepsql | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:3a6942832b8029b6d17d29a4fb6dfdaa |
| server/src/gausskernel/dbmind/deepsql | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:3a6942832b8029b6d17d29a4fb6dfdaa |
| server/src/gausskernel/dbmind/kernel | 模块实现、接口与状态机制 | 2 |  | task:13b09074bb3ef03af399c002f16f55de |
| server/src/gausskernel/ddes | 模块实现、接口与状态机制 / 分批1 | 8 |  | task:2aedc780c8911e50e5aab2e54a464260 |
| server/src/gausskernel/ddes | 模块实现、接口与状态机制 / 分批2 | 5 |  | task:2aedc780c8911e50e5aab2e54a464260 |
| server/src/gausskernel/ddes | 持久化与恢复 | 1 |  | task:2aedc780c8911e50e5aab2e54a464260 |
| server/src/gausskernel/optimizer | 模块实现、接口与状态机制 | 0 |  | task:260dee874b98cf9219cb2e70869eb331 |
| server/src/gausskernel/optimizer/aioptimizer | 代价与基数估算 | 1 |  | task:a1d1de8af7f2eb8470756a5828961d86 |
| server/src/gausskernel/optimizer/aioptimizer | 模块实现、接口与状态机制 | 1 |  | task:a1d1de8af7f2eb8470756a5828961d86 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批3 | 3 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批5 | 4 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批7 | 3 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批8 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批9 | 7 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批10 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批11 | 3 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批12 | 2 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批13 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批14 | 4 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批15 | 5 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批16 | 5 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批17 | 5 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批18 | 3 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批19 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批20 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批21 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批22 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批23 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批24 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批25 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批26 | 1 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批27 | 3 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/commands | 模块实现、接口与状态机制 / 分批28 | 2 |  | task:cdf1d76e007d8cb35aa44bc69d339ee1 |
| server/src/gausskernel/optimizer/gplanmgr | 模块实现、接口与状态机制 | 0 | feature:fa46b45bdacd74a66bfa655f416a0b48 | task:3625ae2ac2a87a5d85a54371b74b43d7 |
| server/src/gausskernel/optimizer/gplanmgr | 计划生成与计划接口 | 1 | feature:fa46b45bdacd74a66bfa655f416a0b48 | task:3625ae2ac2a87a5d85a54371b74b43d7 |
| server/src/gausskernel/optimizer/path | 代价与基数估算 / 分批1 | 1 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/path | 代价与基数估算 / 分批2 | 1 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/path | 代价与基数估算 / 分批3 | 1 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/path | 连接路径与连接约束 | 2 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/path | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/path | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/path | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/path | 模块实现、接口与状态机制 / 分批4 | 3 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/path | 计划生成与计划接口 | 1 |  | task:5435074259297480bf2df8e37c1283eb |
| server/src/gausskernel/optimizer/plan | 连接路径与连接约束 | 1 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/plan | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/plan | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/plan | 计划生成与计划接口 / 分批1 | 1 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/plan | 计划生成与计划接口 / 分批2 | 4 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/plan | 计划生成与计划接口 / 分批3 | 1 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/plan | 计划生成与计划接口 / 分批4 | 4 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/plan | 计划生成与计划接口 / 分批5 | 2 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/plan | 持久化与恢复 | 1 |  | task:ec9b6288b0d720c916b83e54d19b2fa0 |
| server/src/gausskernel/optimizer/prep | 连接路径与连接约束 / 分批1 | 1 |  | task:d1f0a1a25fb70fe9d4a213626603e96c |
| server/src/gausskernel/optimizer/prep | 连接路径与连接约束 / 分批2 | 1 |  | task:d1f0a1a25fb70fe9d4a213626603e96c |
| server/src/gausskernel/optimizer/prep | 模块实现、接口与状态机制 | 4 |  | task:d1f0a1a25fb70fe9d4a213626603e96c |
| server/src/gausskernel/optimizer/rewrite | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:f726f03d50e5c1fa7f35e5032d712342 |
| server/src/gausskernel/optimizer/rewrite | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:f726f03d50e5c1fa7f35e5032d712342 |
| server/src/gausskernel/optimizer/rewrite | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:f726f03d50e5c1fa7f35e5032d712342 |
| server/src/gausskernel/optimizer/sqladvisor | 回归主题：cmakelists | 0 |  | task:e1a9052cae32060ea3727497b43702f9 |
| server/src/gausskernel/optimizer/sqladvisor | 回归主题：makefile | 0 |  | task:e1a9052cae32060ea3727497b43702f9 |
| server/src/gausskernel/optimizer/sqladvisor | 回归主题：sqladvisor / 分批1 | 3 |  | task:e1a9052cae32060ea3727497b43702f9 |
| server/src/gausskernel/optimizer/sqladvisor | 回归主题：sqladvisor / 分批2 | 1 |  | task:e1a9052cae32060ea3727497b43702f9 |
| server/src/gausskernel/optimizer/sqlpatch | 回归主题：cmakelists | 0 | feature:4af6e617b84d8878b7e7ebbfbbd47396 | task:3692398393e3d9dfbb38cb057a266aec |
| server/src/gausskernel/optimizer/sqlpatch | 回归主题：makefile | 0 | feature:4af6e617b84d8878b7e7ebbfbbd47396 | task:3692398393e3d9dfbb38cb057a266aec |
| server/src/gausskernel/optimizer/sqlpatch | 回归主题：sqlpatch | 1 | feature:4af6e617b84d8878b7e7ebbfbbd47396 | task:3692398393e3d9dfbb38cb057a266aec |
| server/src/gausskernel/optimizer/statistics | 模块实现、接口与状态机制 | 1 |  | task:e678a3f39487b4cf8f608adca85d3897 |
| server/src/gausskernel/optimizer/util | 连接路径与连接约束 | 2 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 模块实现、接口与状态机制 / 分批4 | 4 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 模块实现、接口与状态机制 / 分批6 | 2 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 模块实现、接口与状态机制 / 分批7 | 3 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 模块实现、接口与状态机制 / 分批8 | 5 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/optimizer/util | 计划生成与计划接口 | 5 |  | task:17b3768ea59871dbc9edb21e1c1a5e11 |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/po | 模块实现、接口与状态机制 / 分批10 | 0 |  | task:4f791d5b4f8e8b5bff1e912e452bec9f |
| server/src/gausskernel/process | 模块实现、接口与状态机制 | 0 |  | task:9d31eab76c98d85cda77002cb52eb0a5 |
| server/src/gausskernel/process/datasource | 模块实现、接口与状态机制 | 1 |  | task:74607e20be3f4303cf74e16c8dc4126b |
| server/src/gausskernel/process/globalplancache | 模块实现、接口与状态机制 | 0 |  | task:7306fa540ef3d53a0ca4a266a154005c |
| server/src/gausskernel/process/globalplancache | 计划生成与计划接口 | 4 |  | task:7306fa540ef3d53a0ca4a266a154005c |
| server/src/gausskernel/process/job | 模块实现、接口与状态机制 | 4 |  | task:2ec7d7e82aedd2bfa3fede5be8822dd5 |
| server/src/gausskernel/process/main | 模块实现、接口与状态机制 | 1 |  | task:27946a0815b25ee948001a91527e7f4d |
| server/src/gausskernel/process/postmaster | 模块实现、接口与状态机制 / 分批1 | 4 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 模块实现、接口与状态机制 / 分批2 | 7 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 模块实现、接口与状态机制 / 分批3 | 6 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 模块实现、接口与状态机制 / 分批4 | 3 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 模块实现、接口与状态机制 / 分批7 | 1 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 模块实现、接口与状态机制 / 分批8 | 5 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 持久化与恢复 | 2 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/postmaster | 资源寿命与错误清理 | 2 |  | task:b399eca6ef5125860e87743fd8ff014b |
| server/src/gausskernel/process/stream | 代价与基数估算 | 1 |  | task:aedb44591f82f376027c9910ccc53b23 |
| server/src/gausskernel/process/stream | 模块实现、接口与状态机制 / 分批1 | 4 |  | task:aedb44591f82f376027c9910ccc53b23 |
| server/src/gausskernel/process/stream | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:aedb44591f82f376027c9910ccc53b23 |
| server/src/gausskernel/process/tcop | 模块实现、接口与状态机制 / 分批1 | 4 |  | task:a71cb2926f825b2ec1aa5dc199fd6e13 |
| server/src/gausskernel/process/tcop | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:a71cb2926f825b2ec1aa5dc199fd6e13 |
| server/src/gausskernel/process/tcop | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:a71cb2926f825b2ec1aa5dc199fd6e13 |
| server/src/gausskernel/process/tcop | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:a71cb2926f825b2ec1aa5dc199fd6e13 |
| server/src/gausskernel/process/threadpool | 配置注册与生效 | 1 |  | task:819a1ff1fa3abc3852a7ec14b1b81532 |
| server/src/gausskernel/process/threadpool | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:819a1ff1fa3abc3852a7ec14b1b81532 |
| server/src/gausskernel/process/threadpool | 模块实现、接口与状态机制 / 分批2 | 7 |  | task:819a1ff1fa3abc3852a7ec14b1b81532 |
| server/src/gausskernel/runtime | 模块实现、接口与状态机制 | 0 |  | task:dfaaa1bbf03b4937e636848b7ace9009 |
| server/src/gausskernel/runtime/codegen | 连接路径与连接约束 | 1 |  | task:bcb97f2f697c72407bdd1bcf90954c66 |
| server/src/gausskernel/runtime/codegen | 模块实现、接口与状态机制 / 分批1 | 6 |  | task:bcb97f2f697c72407bdd1bcf90954c66 |
| server/src/gausskernel/runtime/codegen | 模块实现、接口与状态机制 / 分批2 | 7 |  | task:bcb97f2f697c72407bdd1bcf90954c66 |
| server/src/gausskernel/runtime/codegen | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:bcb97f2f697c72407bdd1bcf90954c66 |
| server/src/gausskernel/runtime/codegen | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:bcb97f2f697c72407bdd1bcf90954c66 |
| server/src/gausskernel/runtime/codegen | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:bcb97f2f697c72407bdd1bcf90954c66 |
| server/src/gausskernel/runtime/codegen | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:bcb97f2f697c72407bdd1bcf90954c66 |
| server/src/gausskernel/runtime/codegen | 模块实现、接口与状态机制 / 分批7 | 1 |  | task:bcb97f2f697c72407bdd1bcf90954c66 |
| server/src/gausskernel/runtime/executor | 连接路径与连接约束 | 2 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批6 | 4 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批7 | 1 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批8 | 1 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批9 | 2 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批10 | 2 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批11 | 11 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批12 | 4 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批13 | 3 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批14 | 1 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批15 | 7 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批16 | 15 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批17 | 7 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 模块实现、接口与状态机制 / 分批18 | 3 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 计划生成与计划接口 | 1 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/executor | 资源寿命与错误清理 | 1 |  | task:5e1d48de3f9675f9cd53b87a1737ee99 |
| server/src/gausskernel/runtime/opfusion | 模块实现、接口与状态机制 / 分批1 | 12 |  | task:23ef6579be6b79e06cd2bb558e8649c4 |
| server/src/gausskernel/runtime/opfusion | 模块实现、接口与状态机制 / 分批2 | 6 |  | task:23ef6579be6b79e06cd2bb558e8649c4 |
| server/src/gausskernel/runtime/vecexecutor | 缓存、失效与复用 | 1 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 连接路径与连接约束 / 分批1 | 2 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 连接路径与连接约束 / 分批2 | 2 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 模块实现、接口与状态机制 / 分批1 | 4 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 模块实现、接口与状态机制 / 分批2 | 10 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 模块实现、接口与状态机制 / 分批3 | 6 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 模块实现、接口与状态机制 / 分批4 | 15 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 模块实现、接口与状态机制 / 分批5 | 6 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 模块实现、接口与状态机制 / 分批6 | 9 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 模块实现、接口与状态机制 / 分批7 | 3 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/runtime/vecexecutor | 计划生成与计划接口 | 1 |  | task:f5f8cd5b1941d991b57337bad422a865 |
| server/src/gausskernel/security | 模块实现、接口与状态机制 / 分批1 | 10 |  | task:ec00c2369029adbc5155f52a9963cefb |
| server/src/gausskernel/security | 模块实现、接口与状态机制 / 分批2 | 18 |  | task:ec00c2369029adbc5155f52a9963cefb |
| server/src/gausskernel/security | 模块实现、接口与状态机制 / 分批3 | 13 |  | task:ec00c2369029adbc5155f52a9963cefb |
| server/src/gausskernel/security | 资源寿命与错误清理 | 1 |  | task:ec00c2369029adbc5155f52a9963cefb |
| server/src/gausskernel/storage | 模块实现、接口与状态机制 | 0 |  | task:132c57bea1350e2b078e7b505fec7f6b |
| server/src/gausskernel/storage/access | 模块实现、接口与状态机制 | 0 |  | task:19e7bc93dcbe3708149db169234413cf |
| server/src/gausskernel/storage/access/archive | 模块实现、接口与状态机制 | 2 |  | task:5af0137771151c40d09107f4a5f6a2d7 |
| server/src/gausskernel/storage/access/bloom | 代价与基数估算 | 1 |  | task:da18c705b47774fbb0eef788aea3a609 |
| server/src/gausskernel/storage/access/bloom | 模块实现、接口与状态机制 | 4 |  | task:da18c705b47774fbb0eef788aea3a609 |
| server/src/gausskernel/storage/access/cbtree | 模块实现、接口与状态机制 | 1 |  | task:529c6795599b763692473c9742007978 |
| server/src/gausskernel/storage/access/common | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:758e09c6fca28eac27ad93b4b0885139 |
| server/src/gausskernel/storage/access/common | 模块实现、接口与状态机制 / 分批2 | 6 |  | task:758e09c6fca28eac27ad93b4b0885139 |
| server/src/gausskernel/storage/access/datavec | 模块实现、接口与状态机制 / 分批1 | 11 |  | task:06b88c61e2a84c49e4c120fb2b2900cc |
| server/src/gausskernel/storage/access/datavec | 模块实现、接口与状态机制 / 分批2 | 8 |  | task:06b88c61e2a84c49e4c120fb2b2900cc |
| server/src/gausskernel/storage/access/datavec | 模块实现、接口与状态机制 / 分批3 | 6 |  | task:06b88c61e2a84c49e4c120fb2b2900cc |
| server/src/gausskernel/storage/access/datavec | 模块实现、接口与状态机制 / 分批4 | 14 |  | task:06b88c61e2a84c49e4c120fb2b2900cc |
| server/src/gausskernel/storage/access/datavec | 模块实现、接口与状态机制 / 分批5 | 10 |  | task:06b88c61e2a84c49e4c120fb2b2900cc |
| server/src/gausskernel/storage/access/datavec | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:06b88c61e2a84c49e4c120fb2b2900cc |
| server/src/gausskernel/storage/access/gin | 模块实现、接口与状态机制 / 分批1 | 6 |  | task:d0cd8057a23a5673b07e4efa7cd38ae2 |
| server/src/gausskernel/storage/access/gin | 模块实现、接口与状态机制 / 分批2 | 7 |  | task:d0cd8057a23a5673b07e4efa7cd38ae2 |
| server/src/gausskernel/storage/access/gin | 持久化与恢复 | 1 |  | task:d0cd8057a23a5673b07e4efa7cd38ae2 |
| server/src/gausskernel/storage/access/gist | 模块实现、接口与状态机制 / 分批1 | 6 |  | task:be49b6c2fbf82242cb3a6ad0c7e17557 |
| server/src/gausskernel/storage/access/gist | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:be49b6c2fbf82242cb3a6ad0c7e17557 |
| server/src/gausskernel/storage/access/gist | 持久化与恢复 | 1 |  | task:be49b6c2fbf82242cb3a6ad0c7e17557 |
| server/src/gausskernel/storage/access/hash | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:9c9f645282ba4d44d7b9ba28cfdd05ae |
| server/src/gausskernel/storage/access/hash | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:9c9f645282ba4d44d7b9ba28cfdd05ae |
| server/src/gausskernel/storage/access/hash | 持久化与恢复 | 1 |  | task:9c9f645282ba4d44d7b9ba28cfdd05ae |
| server/src/gausskernel/storage/access/hbstore | 模块实现、接口与状态机制 | 2 |  | task:92c4f0a487de9a2bfbce7bc5dc81a36e |
| server/src/gausskernel/storage/access/heap | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:f6eafeb50485beb6beae4e03ed24ec27 |
| server/src/gausskernel/storage/access/heap | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:f6eafeb50485beb6beae4e03ed24ec27 |
| server/src/gausskernel/storage/access/heap | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:f6eafeb50485beb6beae4e03ed24ec27 |
| server/src/gausskernel/storage/access/heap | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:f6eafeb50485beb6beae4e03ed24ec27 |
| server/src/gausskernel/storage/access/heap | 事务、可见性与结束处理 | 2 |  | task:f6eafeb50485beb6beae4e03ed24ec27 |
| server/src/gausskernel/storage/access/index | 模块实现、接口与状态机制 | 2 |  | task:8ccbfd80f84662b1e75195bb57c2e32b |
| server/src/gausskernel/storage/access/nbtree | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:03cfeb633334dff7d2648405b9e3a378 |
| server/src/gausskernel/storage/access/nbtree | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:03cfeb633334dff7d2648405b9e3a378 |
| server/src/gausskernel/storage/access/nbtree | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:03cfeb633334dff7d2648405b9e3a378 |
| server/src/gausskernel/storage/access/nbtree | 模块实现、接口与状态机制 / 分批4 | 2 |  | task:03cfeb633334dff7d2648405b9e3a378 |
| server/src/gausskernel/storage/access/nbtree | 持久化与恢复 | 1 |  | task:03cfeb633334dff7d2648405b9e3a378 |
| server/src/gausskernel/storage/access/obs | 模块实现、接口与状态机制 | 1 |  | task:7f6ec1f3f611ea697545265c8371f873 |
| server/src/gausskernel/storage/access/psort | 模块实现、接口与状态机制 | 1 |  | task:6a53831561110fb33a3e368b809d9b9d |
| server/src/gausskernel/storage/access/redo | 模块实现、接口与状态机制 | 7 |  | task:615d223bed59ee38762b915ebc0406be |
| server/src/gausskernel/storage/access/redo | 持久化与恢复 / 分批1 | 10 |  | task:615d223bed59ee38762b915ebc0406be |
| server/src/gausskernel/storage/access/redo | 持久化与恢复 / 分批2 | 12 |  | task:615d223bed59ee38762b915ebc0406be |
| server/src/gausskernel/storage/access/redo | 持久化与恢复 / 分批3 | 2 |  | task:615d223bed59ee38762b915ebc0406be |
| server/src/gausskernel/storage/access/redo | 事务、可见性与结束处理 | 2 |  | task:615d223bed59ee38762b915ebc0406be |
| server/src/gausskernel/storage/access/rmgrdesc | 模块实现、接口与状态机制 | 22 |  | task:b64831d2dea7b8e5c00aa9c78086c56e |
| server/src/gausskernel/storage/access/rmgrdesc | 持久化与恢复 | 1 |  | task:b64831d2dea7b8e5c00aa9c78086c56e |
| server/src/gausskernel/storage/access/rmgrdesc | 事务、可见性与结束处理 | 2 |  | task:b64831d2dea7b8e5c00aa9c78086c56e |
| server/src/gausskernel/storage/access/spgist | 模块实现、接口与状态机制 | 8 |  | task:7cec6825afd5cd5dfe1690da5de1a4f0 |
| server/src/gausskernel/storage/access/spgist | 持久化与恢复 | 1 |  | task:7cec6825afd5cd5dfe1690da5de1a4f0 |
| server/src/gausskernel/storage/access/table | 模块实现、接口与状态机制 | 1 |  | task:d30077b0d3ede8733e49ab37b0da44e6 |
| server/src/gausskernel/storage/access/transam | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 模块实现、接口与状态机制 / 分批2 | 6 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 模块实现、接口与状态机制 / 分批3 | 3 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 模块实现、接口与状态机制 / 分批4 | 6 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 模块实现、接口与状态机制 / 分批5 | 5 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 模块实现、接口与状态机制 / 分批6 | 4 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 持久化与恢复 / 分批1 | 2 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 持久化与恢复 / 分批2 | 8 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 持久化与恢复 / 分批3 | 3 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 持久化与恢复 / 分批4 | 7 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 持久化与恢复 / 分批5 | 1 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 持久化与恢复 / 分批6 | 3 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 持久化与恢复 / 分批7 | 1 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 资源寿命与错误清理 | 1 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 事务、可见性与结束处理 / 分批1 | 1 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/transam | 事务、可见性与结束处理 / 分批2 | 1 |  | task:ed44d2bb705465daf8841ea622f20295 |
| server/src/gausskernel/storage/access/ubtree | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:a053644ea70821afd658ff061b5953de |
| server/src/gausskernel/storage/access/ubtree | 模块实现、接口与状态机制 / 分批2 | 6 |  | task:a053644ea70821afd658ff061b5953de |
| server/src/gausskernel/storage/access/ubtree | 模块实现、接口与状态机制 / 分批3 | 1 |  | task:a053644ea70821afd658ff061b5953de |
| server/src/gausskernel/storage/access/ubtree | 持久化与恢复 | 1 |  | task:a053644ea70821afd658ff061b5953de |
| server/src/gausskernel/storage/access/ubtreepcr | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:ecbb02f9fdc9f8d427dbaf428bf0f8fd |
| server/src/gausskernel/storage/access/ubtreepcr | 模块实现、接口与状态机制 / 分批2 | 6 |  | task:ecbb02f9fdc9f8d427dbaf428bf0f8fd |
| server/src/gausskernel/storage/access/ustore | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:620f841dbe60af7cb9735cae75ebfee6 |
| server/src/gausskernel/storage/access/ustore | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:620f841dbe60af7cb9735cae75ebfee6 |
| server/src/gausskernel/storage/access/ustore | 模块实现、接口与状态机制 / 分批3 | 7 |  | task:620f841dbe60af7cb9735cae75ebfee6 |
| server/src/gausskernel/storage/access/ustore | 模块实现、接口与状态机制 / 分批4 | 5 |  | task:620f841dbe60af7cb9735cae75ebfee6 |
| server/src/gausskernel/storage/access/ustore | 模块实现、接口与状态机制 / 分批5 | 5 |  | task:620f841dbe60af7cb9735cae75ebfee6 |
| server/src/gausskernel/storage/access/ustore | 持久化与恢复 | 3 |  | task:620f841dbe60af7cb9735cae75ebfee6 |
| server/src/gausskernel/storage/access/ustore | 事务、可见性与结束处理 | 1 |  | task:620f841dbe60af7cb9735cae75ebfee6 |
| server/src/gausskernel/storage/buffer | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:2a204582396ab87ecdc4d05d9009cabe |
| server/src/gausskernel/storage/buffer | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:2a204582396ab87ecdc4d05d9009cabe |
| server/src/gausskernel/storage/buffer | 模块实现、接口与状态机制 / 分批3 | 3 |  | task:2a204582396ab87ecdc4d05d9009cabe |
| server/src/gausskernel/storage/bulkload | 模块实现、接口与状态机制 | 5 |  | task:138c7b7ce6e4630fde5969894c70d220 |
| server/src/gausskernel/storage/bulkload | 资源寿命与错误清理 | 1 |  | task:138c7b7ce6e4630fde5969894c70d220 |
| server/src/gausskernel/storage/cmgr | 缓存、失效与复用 | 1 |  | task:416bc7b7fe1ee999a626cbb5f1aadfeb |
| server/src/gausskernel/storage/cmgr | 模块实现、接口与状态机制 | 0 |  | task:416bc7b7fe1ee999a626cbb5f1aadfeb |
| server/src/gausskernel/storage/cstore | 缓存、失效与复用 | 1 |  | task:0279f3d86cd84723309498d28aae75c4 |
| server/src/gausskernel/storage/cstore | 模块实现、接口与状态机制 / 分批1 | 5 |  | task:0279f3d86cd84723309498d28aae75c4 |
| server/src/gausskernel/storage/cstore | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:0279f3d86cd84723309498d28aae75c4 |
| server/src/gausskernel/storage/cstore | 模块实现、接口与状态机制 / 分批3 | 4 |  | task:0279f3d86cd84723309498d28aae75c4 |
| server/src/gausskernel/storage/cstore | 模块实现、接口与状态机制 / 分批4 | 5 |  | task:0279f3d86cd84723309498d28aae75c4 |
| server/src/gausskernel/storage/cstore | 资源寿命与错误清理 | 1 |  | task:0279f3d86cd84723309498d28aae75c4 |
| server/src/gausskernel/storage/dorado_operation | 模块实现、接口与状态机制 | 1 |  | task:a90098665b3dec7a1de15f6bcbebdbfc |
| server/src/gausskernel/storage/dss | 模块实现、接口与状态机制 | 3 |  | task:f86c9696e691ef17515eafdb4b93c3f0 |
| server/src/gausskernel/storage/file | 模块实现、接口与状态机制 | 7 |  | task:5e80a11809646f1ac8b8a8dff3347188 |
| server/src/gausskernel/storage/freespace | 模块实现、接口与状态机制 | 3 |  | task:38b7ee22ea3a31f01eab5e45b2fffda0 |
| server/src/gausskernel/storage/gs_uwal | 模块实现、接口与状态机制 | 0 |  | task:cdd882a4ac9268c56964b0e7293c2156 |
| server/src/gausskernel/storage/gs_uwal | 持久化与恢复 | 2 |  | task:cdd882a4ac9268c56964b0e7293c2156 |
| server/src/gausskernel/storage/htap | 缓存、失效与复用 | 2 |  | task:4da12a061507e25bd62f70d7638ff86c |
| server/src/gausskernel/storage/htap | 模块实现、接口与状态机制 | 7 |  | task:4da12a061507e25bd62f70d7638ff86c |
| server/src/gausskernel/storage/htap | 资源寿命与错误清理 | 2 |  | task:4da12a061507e25bd62f70d7638ff86c |
| server/src/gausskernel/storage/ipc | 缓存、失效与复用 | 2 |  | task:21a70c0d28c564575f275d3339458906 |
| server/src/gausskernel/storage/ipc | 模块实现、接口与状态机制 / 分批1 | 4 |  | task:21a70c0d28c564575f275d3339458906 |
| server/src/gausskernel/storage/ipc | 模块实现、接口与状态机制 / 分批2 | 3 |  | task:21a70c0d28c564575f275d3339458906 |
| server/src/gausskernel/storage/ipc | 模块实现、接口与状态机制 / 分批3 | 1 |  | task:21a70c0d28c564575f275d3339458906 |
| server/src/gausskernel/storage/ipc | 资源寿命与错误清理 | 1 |  | task:21a70c0d28c564575f275d3339458906 |
| server/src/gausskernel/storage/large_object | 模块实现、接口与状态机制 | 1 |  | task:a3dec08dd8dd75006f2f077664658dfc |
| server/src/gausskernel/storage/lmgr | 模块实现、接口与状态机制 / 分批1 | 2 |  | task:265874d26a243e9eee3fc05528bc7e3b |
| server/src/gausskernel/storage/lmgr | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:265874d26a243e9eee3fc05528bc7e3b |
| server/src/gausskernel/storage/lmgr | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:265874d26a243e9eee3fc05528bc7e3b |
| server/src/gausskernel/storage/lmgr | 模块实现、接口与状态机制 / 分批4 | 1 |  | task:265874d26a243e9eee3fc05528bc7e3b |
| server/src/gausskernel/storage/lmgr | 模块实现、接口与状态机制 / 分批5 | 3 |  | task:265874d26a243e9eee3fc05528bc7e3b |
| server/src/gausskernel/storage/matrix_mem | 模块实现、接口与状态机制 | 0 |  | task:b9cd1e875947bc79519de181699966b1 |
| server/src/gausskernel/storage/matrix_mem | 资源寿命与错误清理 | 1 |  | task:b9cd1e875947bc79519de181699966b1 |
| server/src/gausskernel/storage/mot | 模块实现、接口与状态机制 | 0 |  | task:d8b877ee6e871e658c583bcf529b037c |
| server/src/gausskernel/storage/mot/core | 模块实现、接口与状态机制 | 0 |  | task:3094800aa64eaa035b920c6717d6eb2b |
| server/src/gausskernel/storage/mot/core/concurrency_control | 模块实现、接口与状态机制 | 1 |  | task:456b0fe0a60cbe190326219b6d310757 |
| server/src/gausskernel/storage/mot/core/infra | 模块实现、接口与状态机制 | 1 |  | task:7b92040dffd7ec5111a6fb866582be23 |
| server/src/gausskernel/storage/mot/core/infra/config | 配置注册与生效 / 分批1 | 11 |  | task:58b54120058103100341fe721bf53096 |
| server/src/gausskernel/storage/mot/core/infra/config | 配置注册与生效 / 分批2 | 4 |  | task:58b54120058103100341fe721bf53096 |
| server/src/gausskernel/storage/mot/core/infra/config | 模块实现、接口与状态机制 | 1 |  | task:58b54120058103100341fe721bf53096 |
| server/src/gausskernel/storage/mot/core/infra/containers | 模块实现、接口与状态机制 | 2 |  | task:3e99c4ff0d291610255bbc7caf46e005 |
| server/src/gausskernel/storage/mot/core/infra/stats | 代价与基数估算 | 4 |  | task:b39c992bb0ca65293d92798a7c139199 |
| server/src/gausskernel/storage/mot/core/infra/stats | 模块实现、接口与状态机制 | 6 |  | task:b39c992bb0ca65293d92798a7c139199 |
| server/src/gausskernel/storage/mot/core/infra/stats | 资源寿命与错误清理 | 1 |  | task:b39c992bb0ca65293d92798a7c139199 |
| server/src/gausskernel/storage/mot/core/infra/synchronization | 模块实现、接口与状态机制 | 4 |  | task:d38d0005cc97422a8dc010f84c9ab6fa |
| server/src/gausskernel/storage/mot/core/memory | 代价与基数估算 | 1 |  | task:5d0e722ff8f7f8bad8ae1e76911c9d6e |
| server/src/gausskernel/storage/mot/core/memory | 模块实现、接口与状态机制 / 分批1 | 9 |  | task:5d0e722ff8f7f8bad8ae1e76911c9d6e |
| server/src/gausskernel/storage/mot/core/memory | 模块实现、接口与状态机制 / 分批2 | 9 |  | task:5d0e722ff8f7f8bad8ae1e76911c9d6e |
| server/src/gausskernel/storage/mot/core/memory | 模块实现、接口与状态机制 / 分批3 | 8 |  | task:5d0e722ff8f7f8bad8ae1e76911c9d6e |
| server/src/gausskernel/storage/mot/core/memory | 模块实现、接口与状态机制 / 分批4 | 4 |  | task:5d0e722ff8f7f8bad8ae1e76911c9d6e |
| server/src/gausskernel/storage/mot/core/storage | 模块实现、接口与状态机制 / 分批1 | 6 |  | task:1d61d42f5b4d5eb4c6f481db9b454c38 |
| server/src/gausskernel/storage/mot/core/storage | 模块实现、接口与状态机制 / 分批2 | 9 |  | task:1d61d42f5b4d5eb4c6f481db9b454c38 |
| server/src/gausskernel/storage/mot/core/system | 配置注册与生效 | 1 |  | task:fd181eae8fd49aa65ab99d1c056b27df |
| server/src/gausskernel/storage/mot/core/system | 模块实现、接口与状态机制 | 2 |  | task:fd181eae8fd49aa65ab99d1c056b27df |
| server/src/gausskernel/storage/mot/core/system | 资源寿命与错误清理 | 1 |  | task:fd181eae8fd49aa65ab99d1c056b27df |
| server/src/gausskernel/storage/mot/core/system/checkpoint | 模块实现、接口与状态机制 | 4 |  | task:9bcb6ff06fb51537f14a82ea026c6d15 |
| server/src/gausskernel/storage/mot/core/system/common | 模块实现、接口与状态机制 | 7 |  | task:3f6d294de2d7a7677a2b38bb2b220195 |
| server/src/gausskernel/storage/mot/core/system/recovery | 模块实现、接口与状态机制 | 4 |  | task:b0ef3c8bef0c424aad6ef7e9570d4410 |
| server/src/gausskernel/storage/mot/core/system/recovery | 持久化与恢复 | 7 |  | task:b0ef3c8bef0c424aad6ef7e9570d4410 |
| server/src/gausskernel/storage/mot/core/system/statistics | 代价与基数估算 | 4 |  | task:765f8cd9423efe8598fae133f091cdbd |
| server/src/gausskernel/storage/mot/core/system/statistics | 模块实现、接口与状态机制 | 0 |  | task:765f8cd9423efe8598fae133f091cdbd |
| server/src/gausskernel/storage/mot/core/system/transaction | 模块实现、接口与状态机制 | 5 |  | task:44569df7c18b1b2b5d13818f06b17878 |
| server/src/gausskernel/storage/mot/core/system/transaction_logger | 代价与基数估算 | 2 |  | task:cc80a4ef1e3b104b82b24edd67ccafa0 |
| server/src/gausskernel/storage/mot/core/system/transaction_logger | 模块实现、接口与状态机制 | 5 |  | task:cc80a4ef1e3b104b82b24edd67ccafa0 |
| server/src/gausskernel/storage/mot/core/system/transaction_logger | 持久化与恢复 | 7 |  | task:cc80a4ef1e3b104b82b24edd67ccafa0 |
| server/src/gausskernel/storage/mot/core/utils | 模块实现、接口与状态机制 | 6 |  | task:4235d49cbef0f29f4598f19a4e99995d |
| server/src/gausskernel/storage/mot/fdw_adapter | 配置注册与生效 | 0 |  | task:0ba6a5d52306ded71c08792c2cad9d39 |
| server/src/gausskernel/storage/mot/fdw_adapter | 模块实现、接口与状态机制 / 分批1 | 3 |  | task:0ba6a5d52306ded71c08792c2cad9d39 |
| server/src/gausskernel/storage/mot/fdw_adapter | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:0ba6a5d52306ded71c08792c2cad9d39 |
| server/src/gausskernel/storage/mot/fdw_adapter | 持久化与恢复 | 1 |  | task:0ba6a5d52306ded71c08792c2cad9d39 |
| server/src/gausskernel/storage/mot/fdw_adapter | 资源寿命与错误清理 | 1 |  | task:0ba6a5d52306ded71c08792c2cad9d39 |
| server/src/gausskernel/storage/mot/fdw_adapter | 事务、可见性与结束处理 | 1 |  | task:0ba6a5d52306ded71c08792c2cad9d39 |
| server/src/gausskernel/storage/mot/jit_exec | 代价与基数估算 | 1 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批1 | 1 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批2 | 2 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批4 | 2 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批5 | 1 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批6 | 1 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批7 | 1 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批8 | 3 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 模块实现、接口与状态机制 / 分批9 | 2 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 计划生成与计划接口 / 分批1 | 2 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/mot/jit_exec | 计划生成与计划接口 / 分批2 | 2 |  | task:a22826263356d9a67e68ed66bf9c6ea7 |
| server/src/gausskernel/storage/nvm | 模块实现、接口与状态机制 | 2 |  | task:200906e181a76606c8a1227bfa6690b7 |
| server/src/gausskernel/storage/page | 模块实现、接口与状态机制 | 6 |  | task:cc99b71ffba5dc8c9407ed956d080ded |
| server/src/gausskernel/storage/page | 持久化与恢复 | 1 |  | task:cc99b71ffba5dc8c9407ed956d080ded |
| server/src/gausskernel/storage/remote | 模块实现、接口与状态机制 | 2 |  | task:edfd8c456b768215810835caf91bdee3 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批1 | 4 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批2 | 4 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批3 | 9 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批4 | 5 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批5 | 5 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批6 | 5 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批7 | 2 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批8 | 4 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批9 | 3 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 模块实现、接口与状态机制 / 分批10 | 1 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 持久化与恢复 / 分批1 | 5 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 持久化与恢复 / 分批2 | 2 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/replication | 持久化与恢复 / 分批3 | 1 |  | task:e15e431caf1349475901b247ebd659e6 |
| server/src/gausskernel/storage/roach | 模块实现、接口与状态机制 | 0 |  | task:7666c0f9dcf74ba3c5b2b9634c4f6d9c |
| server/src/gausskernel/storage/smgr | 模块实现、接口与状态机制 / 分批1 | 6 |  | task:0bb9b066b59d7ac20e7d35d547fbc289 |
| server/src/gausskernel/storage/smgr | 模块实现、接口与状态机制 / 分批2 | 7 |  | task:0bb9b066b59d7ac20e7d35d547fbc289 |
| server/src/gausskernel/storage/smgr | 模块实现、接口与状态机制 / 分批3 | 2 |  | task:0bb9b066b59d7ac20e7d35d547fbc289 |
| server/src/gausskernel/storage/smgr | 模块实现、接口与状态机制 / 分批4 | 3 |  | task:0bb9b066b59d7ac20e7d35d547fbc289 |
| server/src/gausskernel/storage/smgr | 持久化与恢复 | 2 |  | task:0bb9b066b59d7ac20e7d35d547fbc289 |
| server/src/gausskernel/storage/sync | 模块实现、接口与状态机制 | 1 |  | task:84e4265d8eb01adcf3948be242ce2c8b |
| server/src/gausskernel/storage/tcap | 模块实现、接口与状态机制 | 4 |  | task:629ac8bc4ca02c02f6231fef650f73f3 |
| server/src/gausskernel/storage/test | 回归主题：cmakelists | 0 |  | task:9d5d484767fcfe1de35706ea0f5269cd |
| server/src/gausskernel/storage/test | 回归主题：utesteventutil | 1 |  | task:9d5d484767fcfe1de35706ea0f5269cd |
| server/src/gausskernel/storage/xlog_share_storage | 模块实现、接口与状态机制 | 0 |  | task:b918070f669260a68d7341bf52f6a123 |
| server/src/gausskernel/storage/xlog_share_storage | 持久化与恢复 | 1 |  | task:b918070f669260a68d7341bf52f6a123 |
| server/src/include | 配置注册与生效 | 0 |  | task:2364aca01f75d0980ae8cc3fff0771e7 |
| server/src/include | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:2364aca01f75d0980ae8cc3fff0771e7 |
| server/src/include | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:2364aca01f75d0980ae8cc3fff0771e7 |
| server/src/include | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:2364aca01f75d0980ae8cc3fff0771e7 |
| server/src/include | 资源寿命与错误清理 | 0 |  | task:2364aca01f75d0980ae8cc3fff0771e7 |
| server/src/include/access | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:9a6b5efebac887a88ee88108bae16ccb |
| server/src/include/access | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:9a6b5efebac887a88ee88108bae16ccb |
| server/src/include/access | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:9a6b5efebac887a88ee88108bae16ccb |
| server/src/include/access | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:9a6b5efebac887a88ee88108bae16ccb |
| server/src/include/access | 持久化与恢复 | 0 |  | task:9a6b5efebac887a88ee88108bae16ccb |
| server/src/include/access | 资源寿命与错误清理 | 0 |  | task:9a6b5efebac887a88ee88108bae16ccb |
| server/src/include/access | 事务、可见性与结束处理 | 0 |  | task:9a6b5efebac887a88ee88108bae16ccb |
| server/src/include/access/archive | 模块实现、接口与状态机制 | 0 |  | task:1fcd42c64e8226f253a2553fe211037d |
| server/src/include/access/datavec | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:3015773e808c69ea5034d403a8df8154 |
| server/src/include/access/datavec | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:3015773e808c69ea5034d403a8df8154 |
| server/src/include/access/extreme_rto | 模块实现、接口与状态机制 | 0 |  | task:82712e703e6844bb393f9bfe74310deb |
| server/src/include/access/extreme_rto | 持久化与恢复 | 0 |  | task:82712e703e6844bb393f9bfe74310deb |
| server/src/include/access/htap | 缓存、失效与复用 | 0 |  | task:bc8252a694e9867be9231ff9f6d5192f |
| server/src/include/access/htap | 模块实现、接口与状态机制 | 0 |  | task:bc8252a694e9867be9231ff9f6d5192f |
| server/src/include/access/htap | 资源寿命与错误清理 | 0 |  | task:bc8252a694e9867be9231ff9f6d5192f |
| server/src/include/access/obs | 模块实现、接口与状态机制 | 0 |  | task:a0e27bd35e2c9bd597acc7d74b4f83d0 |
| server/src/include/access/ondemand_extreme_rto | 模块实现、接口与状态机制 | 0 |  | task:cc542e6035dea7ed1ac2338f3fe8894f |
| server/src/include/access/ondemand_extreme_rto | 持久化与恢复 | 0 |  | task:cc542e6035dea7ed1ac2338f3fe8894f |
| server/src/include/access/parallel_recovery | 模块实现、接口与状态机制 | 0 |  | task:5df0ea86a1a7fd32dec686adae369829 |
| server/src/include/access/parallel_recovery | 持久化与恢复 | 0 |  | task:5df0ea86a1a7fd32dec686adae369829 |
| server/src/include/access/ustore | 模块实现、接口与状态机制 | 0 |  | task:d8a048f90bf06c2879baefead86413be |
| server/src/include/access/ustore | 持久化与恢复 | 0 |  | task:d8a048f90bf06c2879baefead86413be |
| server/src/include/access/ustore | 事务、可见性与结束处理 | 0 |  | task:d8a048f90bf06c2879baefead86413be |
| server/src/include/alarm | 配置注册与生效 | 0 |  | task:5a514e1b40c6c5e93b73ea66b22798ca |
| server/src/include/alarm | 模块实现、接口与状态机制 | 0 |  | task:5a514e1b40c6c5e93b73ea66b22798ca |
| server/src/include/bin | 资源寿命与错误清理 | 0 |  | task:82f2b3b1902ee8c0527621a10a74e7b9 |
| server/src/include/bootstrap | 模块实现、接口与状态机制 | 0 |  | task:70dd22ca1d537028d74bba99af2f05c0 |
| server/src/include/bulkload | 模块实现、接口与状态机制 | 0 |  | task:fd6042066360dfa07bba081f7d4760ac |
| server/src/include/bulkload | 资源寿命与错误清理 | 0 |  | task:fd6042066360dfa07bba081f7d4760ac |
| server/src/include/catalog | 配置注册与生效 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 持久化与恢复 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 资源寿命与错误清理 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog | 事务、可见性与结束处理 | 0 |  | task:8599b18915581fbb6c57fab4da31cfe9 |
| server/src/include/catalog/upgrade_sql/check_upgrade | 模块实现、接口与状态机制 | 0 |  | task:826c37073aff94c2f2560b06465fe802 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_maindb | 模块实现、接口与状态机制 / 分批10 | 0 |  | task:9ba624eddfaa0269408f7450c1e80f68 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/rollback_catalog_otherdb | 模块实现、接口与状态机制 / 分批10 | 0 |  | task:88f94481e5767536e1332e858d971da6 |
| server/src/include/catalog/upgrade_sql/set_guc | 配置注册与生效 | 0 |  | task:5a6468f60f624dce8ef2bda5dd696de5 |
| server/src/include/catalog/upgrade_sql/set_guc | 模块实现、接口与状态机制 | 0 |  | task:5a6468f60f624dce8ef2bda5dd696de5 |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批10 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批11 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批12 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批13 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_maindb | 模块实现、接口与状态机制 / 分批14 | 0 |  | task:e8b4d74a3f84426af252adee06e1525c |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批7 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批8 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批9 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批10 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批11 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批12 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批13 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/catalog/upgrade_sql/upgrade_catalog_otherdb | 模块实现、接口与状态机制 / 分批14 | 0 |  | task:01cf6fd81fb00b9bcdbebbbaa549d74f |
| server/src/include/client_logic | 缓存、失效与复用 | 0 |  | task:f3336e27180a3310ec8116f5c1971d4f |
| server/src/include/client_logic | 模块实现、接口与状态机制 | 0 |  | task:f3336e27180a3310ec8116f5c1971d4f |
| server/src/include/cm | 模块实现、接口与状态机制 | 0 |  | task:164ac2d568077b8e65de97e419c7ad55 |
| server/src/include/cm | 资源寿命与错误清理 | 0 |  | task:164ac2d568077b8e65de97e419c7ad55 |
| server/src/include/codegen | 连接路径与连接约束 | 0 |  | task:6c481d58cc62e7ddb05d0152356d3e56 |
| server/src/include/codegen | 模块实现、接口与状态机制 | 0 |  | task:6c481d58cc62e7ddb05d0152356d3e56 |
| server/src/include/commands | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:437f1824b30ac0fb917c503f3ff90aca |
| server/src/include/commands | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:437f1824b30ac0fb917c503f3ff90aca |
| server/src/include/common | 模块实现、接口与状态机制 | 0 |  | task:bbf44ef1583b7549afaa6df04dfb28b1 |
| server/src/include/common | 资源寿命与错误清理 | 0 |  | task:bbf44ef1583b7549afaa6df04dfb28b1 |
| server/src/include/common/build_query | 模块实现、接口与状态机制 | 0 |  | task:487106ac62b50488b37be9e619653696 |
| server/src/include/common/config | 配置注册与生效 | 0 |  | task:ec7dacb42dcea77a91fdb4115d76ae3b |
| server/src/include/communication | 模块实现、接口与状态机制 | 0 |  | task:74b41b2cfe5c3e0ba5046210a0cff0c8 |
| server/src/include/datasource | 模块实现、接口与状态机制 | 0 |  | task:ebb75e6a92e2b8cc5ca8dd05a57161ef |
| server/src/include/datatype | 模块实现、接口与状态机制 | 0 |  | task:2c3d862a5a1fd10511e8f9b5cf2d2bc6 |
| server/src/include/db4ai | 模块实现、接口与状态机制 | 0 |  | task:5b80b6d7e6076616247bb363a8593980 |
| server/src/include/dbmind | 模块实现、接口与状态机制 | 0 |  | task:0dd8b468a1925acd0406b8e6c4859c63 |
| server/src/include/ddes | 模块实现、接口与状态机制 | 0 |  | task:9439cd9abd6b0990841c25dc05df1854 |
| server/src/include/ddes | 持久化与恢复 | 0 |  | task:9439cd9abd6b0990841c25dc05df1854 |
| server/src/include/ddes | 资源寿命与错误清理 | 0 |  | task:9439cd9abd6b0990841c25dc05df1854 |
| server/src/include/distributelayer | 模块实现、接口与状态机制 | 0 |  | task:d1e774068e0046283415a2eda0ef7b31 |
| server/src/include/executor | 连接路径与连接约束 | 0 |  | task:3e9105f9a2ec2fcb1265460177fb8e96 |
| server/src/include/executor | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:3e9105f9a2ec2fcb1265460177fb8e96 |
| server/src/include/executor | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:3e9105f9a2ec2fcb1265460177fb8e96 |
| server/src/include/executor | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:3e9105f9a2ec2fcb1265460177fb8e96 |
| server/src/include/executor | 计划生成与计划接口 | 0 |  | task:3e9105f9a2ec2fcb1265460177fb8e96 |
| server/src/include/executor | 资源寿命与错误清理 | 0 |  | task:3e9105f9a2ec2fcb1265460177fb8e96 |
| server/src/include/fmgr | 模块实现、接口与状态机制 | 0 |  | task:52c6bb046cd9f65ef232ab1eb67209fb |
| server/src/include/foreign | 模块实现、接口与状态机制 | 0 |  | task:0f354208e27de6ab6e8cebebbf9dcb33 |
| server/src/include/gs_ledger | 模块实现、接口与状态机制 | 0 |  | task:58596ebb454d5fe9562a870b8bf8d173 |
| server/src/include/gs_policy | 模块实现、接口与状态机制 | 0 |  | task:366382ca5674fcc82570f242489bd969 |
| server/src/include/gs_policy | 资源寿命与错误清理 | 0 |  | task:366382ca5674fcc82570f242489bd969 |
| server/src/include/gs_register | 模块实现、接口与状态机制 | 0 |  | task:a89bd0f777d1c6a6b7fab42a645ddb1f |
| server/src/include/gssignal | 模块实现、接口与状态机制 | 0 |  | task:69612ae32fa7a6c7da2a5b5b0eeb156b |
| server/src/include/gstrace | 模块实现、接口与状态机制 | 0 |  | task:5ef769f763dac315b24857a15b2bf50f |
| server/src/include/gtm | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:bcb7d6a31ab79ddaa330a6f58bf2a2b2 |
| server/src/include/gtm | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:bcb7d6a31ab79ddaa330a6f58bf2a2b2 |
| server/src/include/gtm | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:bcb7d6a31ab79ddaa330a6f58bf2a2b2 |
| server/src/include/gtm | 资源寿命与错误清理 | 0 |  | task:bcb7d6a31ab79ddaa330a6f58bf2a2b2 |
| server/src/include/hotpatch | 模块实现、接口与状态机制 | 0 |  | task:40be448870dfc4be7c0adacbbe23faaa |
| server/src/include/instruments | 模块实现、接口与状态机制 | 0 |  | task:0df23d60a41afc336c5e14b8f2b0822e |
| server/src/include/instruments | 事务、可见性与结束处理 | 0 |  | task:0df23d60a41afc336c5e14b8f2b0822e |
| server/src/include/iprange | 模块实现、接口与状态机制 | 0 |  | task:2617f05c1155ac564751d8b4ce6f10c7 |
| server/src/include/job | 模块实现、接口与状态机制 | 0 |  | task:1ce87980d30a044c3cda63185ae20fab |
| server/src/include/job | 资源寿命与错误清理 | 0 |  | task:1ce87980d30a044c3cda63185ae20fab |
| server/src/include/keymgr | 模块实现、接口与状态机制 | 0 |  | task:00d7f2250035965c54eea581fba8ee2a |
| server/src/include/keymgr | 资源寿命与错误清理 | 0 |  | task:00d7f2250035965c54eea581fba8ee2a |
| server/src/include/knl | 配置注册与生效 | 0 |  | task:7663f298af74a085b57250dd23a56e89 |
| server/src/include/knl | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:7663f298af74a085b57250dd23a56e89 |
| server/src/include/knl | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:7663f298af74a085b57250dd23a56e89 |
| server/src/include/knl | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:7663f298af74a085b57250dd23a56e89 |
| server/src/include/knl | 资源寿命与错误清理 | 0 |  | task:7663f298af74a085b57250dd23a56e89 |
| server/src/include/lib | 缓存、失效与复用 | 0 |  | task:dd1e52e14a7404f1f20c4fa8618de569 |
| server/src/include/lib | 模块实现、接口与状态机制 | 0 |  | task:dd1e52e14a7404f1f20c4fa8618de569 |
| server/src/include/libcomm | 模块实现、接口与状态机制 | 0 |  | task:9cbc39c38ee85073ed6d52177e69278b |
| server/src/include/libpq | 配置注册与生效 | 0 |  | task:1fce23c61bb40b355a44f64330eb26c1 |
| server/src/include/libpq | 模块实现、接口与状态机制 | 0 |  | task:1fce23c61bb40b355a44f64330eb26c1 |
| server/src/include/lite | 资源寿命与错误清理 | 0 |  | task:e6fc9b4cd29f2493715a80e46455c99f |
| server/src/include/mb | 模块实现、接口与状态机制 | 0 |  | task:7955249c2dfa40a945ee25a9662d92b8 |
| server/src/include/nodes | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:2edfca40dfa808763c1f01678ecf4df6 |
| server/src/include/nodes | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:2edfca40dfa808763c1f01678ecf4df6 |
| server/src/include/nodes | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:2edfca40dfa808763c1f01678ecf4df6 |
| server/src/include/nodes | 计划生成与计划接口 | 0 |  | task:2edfca40dfa808763c1f01678ecf4df6 |
| server/src/include/nodes | 资源寿命与错误清理 | 0 |  | task:2edfca40dfa808763c1f01678ecf4df6 |
| server/src/include/opfusion | 模块实现、接口与状态机制 | 0 |  | task:ce6c0526593cd2d3eb9204982e8d7099 |
| server/src/include/optimizer | 代价与基数估算 | 0 |  | task:df5d53f521bd301d90e95720ae85fd3f |
| server/src/include/optimizer | 连接路径与连接约束 | 0 |  | task:df5d53f521bd301d90e95720ae85fd3f |
| server/src/include/optimizer | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:df5d53f521bd301d90e95720ae85fd3f |
| server/src/include/optimizer | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:df5d53f521bd301d90e95720ae85fd3f |
| server/src/include/optimizer | 计划生成与计划接口 | 0 |  | task:df5d53f521bd301d90e95720ae85fd3f |
| server/src/include/parser | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:8012109989190111d981298790f33272 |
| server/src/include/parser | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:8012109989190111d981298790f33272 |
| server/src/include/pgxc | 模块实现、接口与状态机制 | 0 |  | task:9a34cda02a3a81b101cda650b433ce89 |
| server/src/include/pgxc | 事务、可见性与结束处理 | 0 |  | task:9a34cda02a3a81b101cda650b433ce89 |
| server/src/include/port | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:80fcb37aead8696071e94ea470ef8524 |
| server/src/include/port | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:80fcb37aead8696071e94ea470ef8524 |
| server/src/include/portability | 模块实现、接口与状态机制 | 0 |  | task:829bbcfbf5a844b00edfbffb30d71440 |
| server/src/include/postmaster | 模块实现、接口与状态机制 | 0 |  | task:9c7168edd1ae598317f7d70adaf1f8cd |
| server/src/include/postmaster | 持久化与恢复 | 0 |  | task:9c7168edd1ae598317f7d70adaf1f8cd |
| server/src/include/postmaster | 资源寿命与错误清理 | 0 |  | task:9c7168edd1ae598317f7d70adaf1f8cd |
| server/src/include/query_anomaly | 模块实现、接口与状态机制 | 0 |  | task:f83055f27a90c29f6264f7a41d8aefc1 |
| server/src/include/regex | 模块实现、接口与状态机制 | 0 |  | task:3526048e110d9c2bf14400269b5e1ac4 |
| server/src/include/replication | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:4b1103e3b45bcd0bc0f28f41df78c90c |
| server/src/include/replication | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:4b1103e3b45bcd0bc0f28f41df78c90c |
| server/src/include/replication | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:4b1103e3b45bcd0bc0f28f41df78c90c |
| server/src/include/replication | 持久化与恢复 | 0 |  | task:4b1103e3b45bcd0bc0f28f41df78c90c |
| server/src/include/rewrite | 模块实现、接口与状态机制 | 0 |  | task:74e802798509489b202b487a335daf6a |
| server/src/include/service | 模块实现、接口与状态机制 | 0 |  | task:09ab8d8777220f8150a2a9be81501338 |
| server/src/include/snowball | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:345fc22c20e19e96961362f0003f5c97 |
| server/src/include/snowball | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:345fc22c20e19e96961362f0003f5c97 |
| server/src/include/ssl | 模块实现、接口与状态机制 | 0 |  | task:5271c72d46dc4e035925ccd648256b03 |
| server/src/include/storage | 缓存、失效与复用 | 0 |  | task:85a6254d10ff26bbb49e45acff31b06e |
| server/src/include/storage | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:85a6254d10ff26bbb49e45acff31b06e |
| server/src/include/storage | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:85a6254d10ff26bbb49e45acff31b06e |
| server/src/include/storage | 资源寿命与错误清理 | 0 |  | task:85a6254d10ff26bbb49e45acff31b06e |
| server/src/include/storage/buf | 模块实现、接口与状态机制 | 0 |  | task:601c45af9bbc0cbec7db0c547702667b |
| server/src/include/storage/cfs | 模块实现、接口与状态机制 | 0 |  | task:ba93a6d1c8810ae635b9e5e61e7794de |
| server/src/include/storage/cstore | 模块实现、接口与状态机制 | 0 |  | task:95738a7634f26f46a7de2babeeefd103 |
| server/src/include/storage/cstore | 资源寿命与错误清理 | 0 |  | task:95738a7634f26f46a7de2babeeefd103 |
| server/src/include/storage/dorado_operation | 模块实现、接口与状态机制 | 0 |  | task:0aabb561406b88fb4db3a9e0019bee2f |
| server/src/include/storage/dss | 模块实现、接口与状态机制 | 0 |  | task:65ee504f9043e7525cc7eb14049085c3 |
| server/src/include/storage/file | 模块实现、接口与状态机制 | 0 |  | task:6c732a207a3440b8b83a318e0f05a777 |
| server/src/include/storage/gs_uwal | 持久化与恢复 | 0 |  | task:ae0cf2660a66d23215ebf3db30d1ead2 |
| server/src/include/storage/item | 模块实现、接口与状态机制 | 0 |  | task:d71404b592233b7a91f0e5b790e159ae |
| server/src/include/storage/lock | 模块实现、接口与状态机制 | 0 |  | task:d9d18db3cada17f772033cb63120c213 |
| server/src/include/storage/mot | 模块实现、接口与状态机制 | 0 |  | task:6c1dc7cc07ef854266947a29273b94b6 |
| server/src/include/storage/mot | 持久化与恢复 | 0 |  | task:6c1dc7cc07ef854266947a29273b94b6 |
| server/src/include/storage/nvm | 模块实现、接口与状态机制 | 0 |  | task:abfe7712a2d33c9f601ad39caca29d72 |
| server/src/include/storage/smgr | 模块实现、接口与状态机制 | 0 |  | task:81bed2338e3afa5e36dd7b55af283d0a |
| server/src/include/storage/xlog_share_storage | 持久化与恢复 | 0 |  | task:ece41aebbb837825b87b0d8b9e07cec9 |
| server/src/include/streaming | 缓存、失效与复用 | 0 |  | task:f004dfb56a92727431c714dda86eac3c |
| server/src/include/streaming | 模块实现、接口与状态机制 | 0 |  | task:f004dfb56a92727431c714dda86eac3c |
| server/src/include/streaming | 计划生成与计划接口 | 0 |  | task:f004dfb56a92727431c714dda86eac3c |
| server/src/include/tcop | 模块实现、接口与状态机制 | 0 |  | task:374671c5b6a34688c2a42bbbc6e4e07b |
| server/src/include/tde_key_management | 模块实现、接口与状态机制 | 0 |  | task:2e7614ece8c6bfbace145d3977a4292b |
| server/src/include/threadpool | 模块实现、接口与状态机制 | 0 |  | task:fb4182b77b55b280402311a59313c13e |
| server/src/include/tsearch | 缓存、失效与复用 | 0 |  | task:5284fab68a6ab4ed9b997da38ee98b23 |
| server/src/include/tsearch | 模块实现、接口与状态机制 | 0 |  | task:5284fab68a6ab4ed9b997da38ee98b23 |
| server/src/include/utils | 缓存、失效与复用 / 分批1 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 缓存、失效与复用 / 分批2 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 配置注册与生效 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 代价与基数估算 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 模块实现、接口与状态机制 / 分批4 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 模块实现、接口与状态机制 / 分批5 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 模块实现、接口与状态机制 / 分批6 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 计划生成与计划接口 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 资源寿命与错误清理 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/utils | 事务、可见性与结束处理 | 0 |  | task:8edb0857fe638a76185109c616dd4463 |
| server/src/include/vecexecutor | 连接路径与连接约束 | 0 |  | task:601bdb2660bd677034f9e235fbde89b7 |
| server/src/include/vecexecutor | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:601bdb2660bd677034f9e235fbde89b7 |
| server/src/include/vecexecutor | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:601bdb2660bd677034f9e235fbde89b7 |
| server/src/include/vecexecutor | 计划生成与计划接口 | 0 |  | task:601bdb2660bd677034f9e235fbde89b7 |
| server/src/include/vectorsonic | 连接路径与连接约束 | 0 |  | task:fe9589a14102b66e9ae65504ec12cdab |
| server/src/include/vectorsonic | 模块实现、接口与状态机制 | 0 |  | task:fe9589a14102b66e9ae65504ec12cdab |
| server/src/include/workload | 模块实现、接口与状态机制 | 0 |  | task:71644c69a02afe64c907694a0698d274 |
| server/src/include/workload | 资源寿命与错误清理 | 0 |  | task:71644c69a02afe64c907694a0698d274 |
| server/src/lib | 模块实现、接口与状态机制 | 0 |  | task:6c5351b05210acf32f0efdee21ad04e8 |
| server/src/lib/alarm | 模块实现、接口与状态机制 | 2 |  | task:f0018b6e0ec31f3aefc2c330a67c6d32 |
| server/src/lib/build_query | 模块实现、接口与状态机制 | 1 |  | task:19639e519d3c6da43cd5d5fac95d5772 |
| server/src/lib/cm_common | 模块实现、接口与状态机制 | 5 |  | task:6c2f652a9de5e7f101f831cac58e6de7 |
| server/src/lib/cm_common | 资源寿命与错误清理 | 1 |  | task:6c2f652a9de5e7f101f831cac58e6de7 |
| server/src/lib/cm_communication | 模块实现、接口与状态机制 | 10 |  | task:077b7f0739760f6e61405445f168d0c7 |
| server/src/lib/config | 配置注册与生效 | 1 |  | task:e8605b77b642d5f6cf884fdcd9c92925 |
| server/src/lib/config | 模块实现、接口与状态机制 | 0 |  | task:e8605b77b642d5f6cf884fdcd9c92925 |
| server/src/lib/elog | 模块实现、接口与状态机制 | 0 |  | task:dbe557353d13f581da6097bbd9f9169e |
| server/src/lib/elog | 资源寿命与错误清理 | 1 |  | task:dbe557353d13f581da6097bbd9f9169e |
| server/src/lib/gstrace | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:79cbdf83cf46ce5396be5504f7a8a6e1 |
| server/src/lib/gstrace | 模块实现、接口与状态机制 / 分批2 | 1 |  | task:79cbdf83cf46ce5396be5504f7a8a6e1 |
| server/src/lib/gstrace/common | 模块实现、接口与状态机制 | 1 |  | task:3a57b57bf161bc7d4aa5a0dc7961d0b8 |
| server/src/lib/hotpatch | 模块实现、接口与状态机制 | 1 |  | task:31d6916b8a98d52fef6831598cdfa593 |
| server/src/lib/page_compression | 模块实现、接口与状态机制 | 1 |  | task:5698da18a7c03e13c44578419598936b |
| server/src/lib/pgcommon | 模块实现、接口与状态机制 | 0 |  | task:f9fb69bec6b2fe493dcd7bc5432122fb |
| server/src/lib/pgcommon | 资源寿命与错误清理 | 1 |  | task:f9fb69bec6b2fe493dcd7bc5432122fb |
| server/src/makefiles | 模块实现、接口与状态机制 | 0 |  | task:5c122355c4569c0a11d68bb1487c1f61 |
| server/src/test | 回归主题：cmakelists | 0 |  | task:aed0b632831bc7abbcaee1facbd98110 |
| server/src/test | 回归主题：makefile | 0 |  | task:aed0b632831bc7abbcaee1facbd98110 |
| server/src/test/examples | 回归主题：makefile | 0 |  | task:2dbd4e35d3f0f0a8e91024462ad28ef6 |
| server/src/test/examples | 回归主题：testlibpq | 4 |  | task:2dbd4e35d3f0f0a8e91024462ad28ef6 |
| server/src/test/examples | 回归主题：testlo | 2 |  | task:2dbd4e35d3f0f0a8e91024462ad28ef6 |
| server/src/test/grayscale_upgrade | 回归主题：upgradecheck | 0 |  | task:b291b9b952da1cf32e968bed460abb1d |
| server/src/test/ha | 持久化与恢复 | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：deploy | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：gnumakefile | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：ha | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：makefile | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：paxos | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：pgxc | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：pubsub | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：run | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：standby | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：tools | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha | 回归主题：util | 0 |  | task:69e463a84a9de5ff15d80a77719d351a |
| server/src/test/ha/data | 回归主题：cstore | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：customer0 | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：data / 分批1 | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：data / 分批2 | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：extension | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：gin | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：lineitem | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：parallel | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：sequence | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：smartmatch | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：sql | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：user / 分批1 | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 回归主题：user / 分批2 | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/data | 事务、可见性与结束处理 | 0 |  | task:6c680005d7c0ca738399b25c952ca0ef |
| server/src/test/ha/results | 回归主题：.gitignore | 0 |  | task:84f49b67e2a685fce73201fba67683a6 |
| server/src/test/ha/results | 回归主题：readme | 0 |  | task:84f49b67e2a685fce73201fba67683a6 |
| server/src/test/ha/script | 配置注册与生效 | 0 |  | task:9bb1254a9e2b76fdd399351dd5eaefe5 |
| server/src/test/ha/script | 回归主题：01.log | 0 |  | task:9bb1254a9e2b76fdd399351dd5eaefe5 |
| server/src/test/ha/script | 回归主题：02.cleanenv | 0 |  | task:9bb1254a9e2b76fdd399351dd5eaefe5 |
| server/src/test/ha/script | 回归主题：03.get | 0 |  | task:9bb1254a9e2b76fdd399351dd5eaefe5 |
| server/src/test/ha/script | 回归主题：private | 0 |  | task:9bb1254a9e2b76fdd399351dd5eaefe5 |
| server/src/test/ha/script | 回归主题：remote | 0 |  | task:9bb1254a9e2b76fdd399351dd5eaefe5 |
| server/src/test/ha/testcase/cascade | 持久化与恢复 | 0 |  | task:995e56b0a56ce2e43366c13bc080aec9 |
| server/src/test/ha/testcase/cascade | 回归主题：clean | 0 |  | task:995e56b0a56ce2e43366c13bc080aec9 |
| server/src/test/ha/testcase/cascade | 回归主题：failover | 0 |  | task:995e56b0a56ce2e43366c13bc080aec9 |
| server/src/test/ha/testcase/cascade | 回归主题：inc | 0 |  | task:995e56b0a56ce2e43366c13bc080aec9 |
| server/src/test/ha/testcase/cascade | 回归主题：switchover | 0 |  | task:995e56b0a56ce2e43366c13bc080aec9 |
| server/src/test/ha/testcase/catchup_single | 回归主题：full | 0 |  | task:b9d2416876c07df8a38db313d4ea1e07 |
| server/src/test/ha/testcase/catchup_single | 回归主题：incremental | 0 |  | task:b9d2416876c07df8a38db313d4ea1e07 |
| server/src/test/ha/testcase/catchup_single | 回归主题：switchover | 0 |  | task:b9d2416876c07df8a38db313d4ea1e07 |
| server/src/test/ha/testcase/data_replication_single | 持久化与恢复 | 0 |  | task:b44b88d6f3543412267cfb6019cd8f6a |
| server/src/test/ha/testcase/data_replication_single | 回归主题：datareplica | 0 |  | task:b44b88d6f3543412267cfb6019cd8f6a |
| server/src/test/ha/testcase/data_replication_single | 回归主题：kill | 0 |  | task:b44b88d6f3543412267cfb6019cd8f6a |
| server/src/test/ha/testcase/data_replication_single | 回归主题：switchover | 0 |  | task:b44b88d6f3543412267cfb6019cd8f6a |
| server/src/test/ha/testcase/dataqueue_single | 回归主题：dataqueue | 0 |  | task:7e6611d436092f0c4ca1cecafa7e0c2f |
| server/src/test/ha/testcase/decode_single | 回归主题：logical | 0 |  | task:a58927330ada29e5f80d944695064185 |
| server/src/test/ha/testcase/dms_reform | 回归主题：ss | 0 |  | task:91438ec43d22048d3b503a9c29d8b446 |
| server/src/test/ha/testcase/exrtostandbyread | 回归主题：single | 0 |  | task:329f476eff77b49699ec4ec213afc025 |
| server/src/test/ha/testcase/exrtostandbyread | 回归主题：start | 0 |  | task:329f476eff77b49699ec4ec213afc025 |
| server/src/test/ha/testcase/llt_single | 持久化与恢复 | 0 |  | task:dae658aa364b306db650bded32cd32d9 |
| server/src/test/ha/testcase/llt_single | 回归主题：disable | 0 |  | task:dae658aa364b306db650bded32cd32d9 |
| server/src/test/ha/testcase/llt_single | 回归主题：sequence | 0 |  | task:dae658aa364b306db650bded32cd32d9 |
| server/src/test/ha/testcase/llt_single | 回归主题：sql | 0 |  | task:dae658aa364b306db650bded32cd32d9 |
| server/src/test/ha/testcase/llt_single | 回归主题：temp | 0 |  | task:dae658aa364b306db650bded32cd32d9 |
| server/src/test/ha/testcase/llt_single | 回归主题：text | 0 |  | task:dae658aa364b306db650bded32cd32d9 |
| server/src/test/ha/testcase/llt_single | 回归主题：validate | 0 |  | task:dae658aa364b306db650bded32cd32d9 |
| server/src/test/ha/testcase/multi_standby_single | 持久化与恢复 | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：auto | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：consistency | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：failover | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：hash | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：inc | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：log | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：most | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：params | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：quorum | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：standby | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：switchover | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single | 回归主题：sync | 0 |  | task:beda268508324941ed7629be5b0ede14 |
| server/src/test/ha/testcase/multi_standby_single_archive | 回归主题：archive | 0 |  | task:481787d21a9a18a3b195596aa0340fe5 |
| server/src/test/ha/testcase/multi_standby_single_shared_storage | 持久化与恢复 | 0 |  | task:48d8ff1eb10409b14071343e71be9204 |
| server/src/test/ha/testcase/multi_standby_single_shared_storage | 回归主题：cluster | 0 |  | task:48d8ff1eb10409b14071343e71be9204 |
| server/src/test/ha/testcase/multi_standby_single_shared_storage | 回归主题：failover | 0 |  | task:48d8ff1eb10409b14071343e71be9204 |
| server/src/test/ha/testcase/multi_standby_single_shared_storage | 回归主题：inc | 0 |  | task:48d8ff1eb10409b14071343e71be9204 |
| server/src/test/ha/testcase/multi_standby_single_shared_storage | 回归主题：standby | 0 |  | task:48d8ff1eb10409b14071343e71be9204 |
| server/src/test/ha/testcase/multi_standby_single_shared_storage | 回归主题：switchover | 0 |  | task:48d8ff1eb10409b14071343e71be9204 |
| server/src/test/ha/testcase/multi_uwal | 回归主题：simple | 0 |  | task:91cf90f6fc3babb9202a8479c069f47d |
| server/src/test/ha/testcase/multi_uwal | 回归主题：switchover | 0 |  | task:91cf90f6fc3babb9202a8479c069f47d |
| server/src/test/ha/testcase/paxos_single | 回归主题：changerole | 0 |  | task:e039885258e54f2fffadafd0e71c5195 |
| server/src/test/ha/testcase/paxos_single | 回归主题：kill | 0 |  | task:e039885258e54f2fffadafd0e71c5195 |
| server/src/test/ha/testcase/paxos_single | 回归主题：remove | 0 |  | task:e039885258e54f2fffadafd0e71c5195 |
| server/src/test/ha/testcase/paxos_single | 回归主题：set | 0 |  | task:e039885258e54f2fffadafd0e71c5195 |
| server/src/test/ha/testcase/paxos_single | 回归主题：switchover | 0 |  | task:e039885258e54f2fffadafd0e71c5195 |
| server/src/test/ha/testcase/pg_rewind_single | 回归主题：buildquery | 0 |  | task:f56249abeddfbdf4b3f0af7c82ebcb4b |
| server/src/test/ha/testcase/pg_rewind_single | 回归主题：enhance | 0 |  | task:f56249abeddfbdf4b3f0af7c82ebcb4b |
| server/src/test/ha/testcase/pg_rewind_single | 回归主题：failover | 0 |  | task:f56249abeddfbdf4b3f0af7c82ebcb4b |
| server/src/test/ha/testcase/pg_rewind_single | 回归主题：gs | 0 |  | task:f56249abeddfbdf4b3f0af7c82ebcb4b |
| server/src/test/ha/testcase/pg_rewind_single | 回归主题：rewind | 0 |  | task:f56249abeddfbdf4b3f0af7c82ebcb4b |
| server/src/test/ha/testcase/secondary_single | 回归主题：copy | 0 |  | task:23a1157d5c6949df1c6bf856c2d30dd3 |
| server/src/test/ha/testcase/secondary_single | 回归主题：dummy | 0 |  | task:23a1157d5c6949df1c6bf856c2d30dd3 |
| server/src/test/ha/testcase/secondary_single | 回归主题：dummystandby | 0 |  | task:23a1157d5c6949df1c6bf856c2d30dd3 |
| server/src/test/ha/testcase/secondary_single | 回归主题：failover | 0 |  | task:23a1157d5c6949df1c6bf856c2d30dd3 |
| server/src/test/ha/testcase/secondary_single | 回归主题：kill | 0 |  | task:23a1157d5c6949df1c6bf856c2d30dd3 |
| server/src/test/ha/testcase/secondary_single | 回归主题：standby | 0 |  | task:23a1157d5c6949df1c6bf856c2d30dd3 |
| server/src/test/ha/testcase/slot_single | 回归主题：replication | 0 |  | task:5fe8defe25212e416cc422e40aefc3a4 |
| server/src/test/ha/testcase/streaming | 回归主题：build | 0 |  | task:7892dc2e14d77d2c4fdc06c253c238f3 |
| server/src/test/ha/testcase/streaming | 回归主题：failover | 0 |  | task:7892dc2e14d77d2c4fdc06c253c238f3 |
| server/src/test/ha/testcase/streaming | 回归主题：majority | 0 |  | task:7892dc2e14d77d2c4fdc06c253c238f3 |
| server/src/test/ha/testcase/streaming | 回归主题：reconnect | 0 |  | task:7892dc2e14d77d2c4fdc06c253c238f3 |
| server/src/test/ha/testcase/streaming | 回归主题：repair | 0 |  | task:7892dc2e14d77d2c4fdc06c253c238f3 |
| server/src/test/ha/testcase/streaming | 回归主题：set | 0 |  | task:7892dc2e14d77d2c4fdc06c253c238f3 |
| server/src/test/ipv6 | 回归主题：check | 0 |  | task:2b09dc1a490dd4e8dfeeef1f8f3905bd |
| server/src/test/ipv6 | 回归主题：create | 0 |  | task:2b09dc1a490dd4e8dfeeef1f8f3905bd |
| server/src/test/ipv6 | 回归主题：gnumakefile | 0 |  | task:2b09dc1a490dd4e8dfeeef1f8f3905bd |
| server/src/test/ipv6 | 回归主题：ipv6 | 0 |  | task:2b09dc1a490dd4e8dfeeef1f8f3905bd |
| server/src/test/ipv6 | 回归主题：ipv6test | 0 |  | task:2b09dc1a490dd4e8dfeeef1f8f3905bd |
| server/src/test/ipv6 | 回归主题：makefile | 0 |  | task:2b09dc1a490dd4e8dfeeef1f8f3905bd |
| server/src/test/isolation | 计划生成与计划接口 | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：classroom-scheduling | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：cmakelists | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：drop-index-concurrently | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：fk-contention | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：fk-deadlock | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：fk-deadlock2 | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：index-only-scan | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：isolation | 1 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：isolationtester | 1 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：makefile | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：multiple-row-versions | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：partial-index | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：pgstat | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：prepared-transactions / 分批1 | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：prepared-transactions / 分批2 | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：project-manager | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：readme | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：receipt-report | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：referential-integrity | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：ri-trigger | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：simple-write-skew | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：specparse | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：specscanner | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：temporal-range-integrity | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：total-cash | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/isolation | 回归主题：two-ids | 0 |  | task:5d483298acec5df7f71bdec74ac223dc |
| server/src/test/locale | 回归主题：de-ctype | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：gr-ctype | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：koi8-ctype | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：makefile | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：readme | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：runall | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：sort-test | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-ctype | 1 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-char.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-select.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-sort | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-text.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-upper-char.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-upper-text.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-upper-varchar.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-upper.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de-varchar.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-de.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-gr-char.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-gr-select.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-gr-sort | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-gr-text.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-gr-varchar.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-gr.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-koi8-char.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-koi8-select.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-koi8-sort | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-koi8-text.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-koi8-varchar.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/locale | 回归主题：test-koi8.sql | 0 |  | task:9419294a9beca96d81f822f0e4275cf2 |
| server/src/test/mb | 回归主题：big | 0 |  | task:9da9ceb5745dafe945bf0ac51318cb94 |
| server/src/test/mb | 回归主题：euc | 0 |  | task:9da9ceb5745dafe945bf0ac51318cb94 |
| server/src/test/mb | 回归主题：mbregress | 0 |  | task:9da9ceb5745dafe945bf0ac51318cb94 |
| server/src/test/mb | 回归主题：mule | 0 |  | task:9da9ceb5745dafe945bf0ac51318cb94 |
| server/src/test/mb | 回归主题：readme | 0 |  | task:9da9ceb5745dafe945bf0ac51318cb94 |
| server/src/test/mb | 回归主题：sjis | 0 |  | task:9da9ceb5745dafe945bf0ac51318cb94 |
| server/src/test/mb | 回归主题：utf | 0 |  | task:9da9ceb5745dafe945bf0ac51318cb94 |
| server/src/test/modules | 配置注册与生效 | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：alter | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：comment | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：create | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：defprivs | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：makefile | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：matviews | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：opfamily | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：readme | 0 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/modules | 回归主题：test | 1 |  | task:692e80d90ec5e87b34284d6d74870566 |
| server/src/test/mutil_ip | 回归主题：check | 0 |  | task:cfa3216a2d74458150d5f0bde6de2737 |
| server/src/test/mutil_ip | 回归主题：create | 0 |  | task:cfa3216a2d74458150d5f0bde6de2737 |
| server/src/test/mutil_ip | 回归主题：expected | 0 |  | task:cfa3216a2d74458150d5f0bde6de2737 |
| server/src/test/mutil_ip | 回归主题：makefile | 0 |  | task:cfa3216a2d74458150d5f0bde6de2737 |
| server/src/test/mutil_ip | 回归主题：mutilip | 0 |  | task:cfa3216a2d74458150d5f0bde6de2737 |
| server/src/test/mutil_ip | 回归主题：mutilip.in | 0 |  | task:cfa3216a2d74458150d5f0bde6de2737 |
| server/src/test/mutil_ip | 回归主题：testlibpq | 2 |  | task:cfa3216a2d74458150d5f0bde6de2737 |
| server/src/test/performance | 回归主题：connection | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：crtsimple | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：crtsimpleidx | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：drpsimple | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：inssimple / 分批1 | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：inssimple / 分批2 | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：orbsimple | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：pgsql | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：runtests | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：slcsimple / 分批1 | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：slcsimple / 分批2 | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：start-pgsql | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/performance | 回归主题：vacuum | 0 |  | task:bd78342af8238f84bf052a57ff5e8109 |
| server/src/test/regress | 计划生成与计划接口 | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 持久化与恢复 | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：.gitignore | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：addnode | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：caseownerlist | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：ce | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：check | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：cmakelists | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：delete | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：gnumakefile | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：gs | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：gsql | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：make | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：makefile | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：parallel / 分批1 | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：parallel / 分批2 | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：pg / 分批1 | 1 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：pg / 分批2 | 1 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：query | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：regress | 1 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：resultmap | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：security | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：serial | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：single | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：smartmatch | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress | 回归主题：wlm | 0 |  | task:e9c16ae8781bf4558762dea26b9d54a8 |
| server/src/test/regress/data | 连接路径与连接约束 / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批4 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批5 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批6 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批7 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批8 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批9 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 连接路径与连接约束 / 分批10 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 计划生成与计划接口 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 持久化与恢复 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 资源寿命与错误清理 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：abalone | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：add&drop | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：agg | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：anomaly / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：anomaly / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：anomaly / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：array | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：audit | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：autoanalyze | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：bayesnet | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：bitmapops | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：book | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：call | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：catalog / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：catalog / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：catalog / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：ce | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：cmpr / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：cmpr / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：cmpr / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：colcmpr / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：colcmpr / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：colcmpr / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：compress | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：constrf | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：constro | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：copy | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：create | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：cs | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：cstore / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：cstore / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：customer / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：customer / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：data / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：data / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：dept | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：desc | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：ecoli | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：emp | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：etl / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：etl / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：exchange | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：exclude | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：f | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：f1t | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：ft | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：full | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：fvt | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gcc | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gcm | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gin / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gin / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gs / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gs / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gs / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gs / 分批4 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gs / 分批5 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gs / 分批6 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：gs / 分批7 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：hash | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：hashagg | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：hdfs | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：houses | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：hw / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：hw / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：hw / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：ignore | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：insert / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：insert / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：inventory | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：item / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：item / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：item / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：jsonb | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：lineitem / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：lineitem / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：load | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：moons | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：onek | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：oorder | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：oorder1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：oorder2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：partition | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：person | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：pgbench | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：postgresql-2018-01-17 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：priority | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：promotion | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：quality | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：rain | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：real | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：rect | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：redis / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：redis / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：redis / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：roughcheck / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：roughcheck / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：row | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：ship | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：sort / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：sort / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：sqlldr | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：store | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：streets | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：stud | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：student | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：supplier | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：t1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：tablespace | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：tbl | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：tenk | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：test / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：test / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：test / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：test / 分批4 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：test / 分批5 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：test / 分批6 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：time | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：tmp / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：tmp / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：tpch | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：ts | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：tsearch | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：ustore | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vec / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vec / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vec / 分批3 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vec / 分批4 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vecctor / 分批1 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vecctor / 分批2 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vfloat4 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vfloat8 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vint4 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：vint8 | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：web | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data | 回归主题：whitebox | 0 |  | task:9266c823c2391bb24210365f32d89f5e |
| server/src/test/regress/data/datanode1 | 缓存、失效与复用 / 分批1 | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 缓存、失效与复用 / 分批2 | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 资源寿命与错误清理 | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：copy | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：datetime | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：escape | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：header | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：header1m | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：in | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：insert | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：lineitem / 分批1 | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：lineitem / 分批2 | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：load | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：nation | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：noescaping | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：null | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：overload | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：smartcare | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：str | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：test | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/datanode1 | 回归主题：utf | 0 |  | task:eb9436609b9252b05ff67179223a2328 |
| server/src/test/regress/data/pgbench | 回归主题：pgbench / 分批1 | 0 |  | task:6d809d24cd07ba669bcf5ab36605bcd3 |
| server/src/test/regress/data/pgbench | 回归主题：pgbench / 分批2 | 0 |  | task:6d809d24cd07ba669bcf5ab36605bcd3 |
| server/src/test/regress/data/upgrade | 回归主题：12345 | 0 |  | task:4b7a1d7fdc757d5e79aeb0b59152c9fa |
| server/src/test/regress/data/upgrade | 回归主题：16386 | 0 |  | task:4b7a1d7fdc757d5e79aeb0b59152c9fa |
| server/src/test/regress/data/upgrade | 回归主题：regression | 0 |  | task:4b7a1d7fdc757d5e79aeb0b59152c9fa |
| server/src/test/regress/expected | 缓存、失效与复用 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 配置注册与生效 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 代价与基数估算 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批6 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批7 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批8 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批9 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批10 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批11 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批12 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批13 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批14 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批15 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批16 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批17 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批18 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批19 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 连接路径与连接约束 / 分批20 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 计划生成与计划接口 / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 计划生成与计划接口 / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 计划生成与计划接口 / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 计划生成与计划接口 / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 计划生成与计划接口 / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 持久化与恢复 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 资源寿命与错误清理 / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 资源寿命与错误清理 / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：abstime | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：accept | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：advisory | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：agg | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：aggregate | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：aggregates / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：aggregates / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ai | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：alarm | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：alter / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：alter / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：alter / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：alter / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：alter / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：am | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：amheap / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：amheap / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：analytic | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：analyze | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：array | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：arrayinterface | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：arrays | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：auto | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：autocommit | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：autonomous | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：b | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：backtrace | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：base | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：batchpreparedstatementsbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：batchsimplequerybin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：batchstatamentbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：bit | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：bloom | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：bm25 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：boolean | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：box | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：bpchar | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：btree | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：bypass | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：case | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：cast | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ce | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ceil | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：cgin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：char | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：charset / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：charset / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：checksum | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：chr | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：circle | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：cluster | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：col | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：collate | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：collate.linux.utf | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：combocid | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：comment | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：comments | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：composite | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：compress | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：conversion | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：copy | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：copy2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：copyselect | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：count | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：create / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：create / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：create / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：createfunctionbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：createtablewithpreparestatamentbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：cstore | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：cte | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：cursor | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：databasemetadatagetcolumnsbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：date | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：datefunc | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：declare | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：decode / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：decode / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：deferrable | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：delete | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：dependency | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：dependent | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：describe | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：deserialize | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：detail | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：disable | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：disconnectedrsbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：diskann | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：display | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：distinct | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：dml | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：domain | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：double | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：drop | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：duplicate | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：early | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：enable | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：encode | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：encrypt | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：enum | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：equivalence | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：euc | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：event | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：exec | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：execcleartuple | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：execcopyslottuple | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：execfetchslottuple | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：execstoretuple | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：explain | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：expr | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：extendstat | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：extra | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：extract | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：fenced | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：fetch | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：first | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：float | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：float4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：float4-exp-three-digits | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：float8 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：float8-exp-three-digits-win | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：float8-small-is-zero | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：forall | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：force | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：foreign / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：foreign / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：func | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：function | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：functional | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：functionsinoutparambin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：functionsinoutparambinarymodebin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：functionsinoutparamsbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：functionsmetadatabin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：functionsoutparambin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：functionsreturnvaluesbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gb | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gen | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：generated | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：geometry | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：get | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：global | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gms | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：goto | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gpi / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gpi / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gs | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gsc | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：gtt | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：handlingbadsqlbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hash | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hashfilter | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：heap / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：heap / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hll | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hnsw | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：huge | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批6 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批7 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批8 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批9 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批10 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批11 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批12 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批13 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批14 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批15 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批16 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批17 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批18 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批19 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批20 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批21 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批22 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批23 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批24 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批25 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批26 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批27 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批28 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批29 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批30 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hw / 分批31 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：hybrid | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：icbc | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ignore | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：index | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：inet | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：inherit | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：inherits | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：inlineview | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：inplace | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：insert | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：int | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：int8-exp-three-digits | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：interval | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：invisible | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：iud | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：json | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：jsonb | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：jsonpath | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：keep | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：keywords | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：large | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：leaky | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：limit | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：llt | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：llvm / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：llvm / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：llvm / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：llvm / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：llvm / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：lock | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：locktag | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：long | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：lseg | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：macaddr | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：magic | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：matview | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：median | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：merge / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：merge / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：merge / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：min | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：money | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：mule | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：multi | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：multithreadclientlogicbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：mysql / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：mysql / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：name | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：namespace | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：nested | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：nls | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：nlssort | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：node | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：normal | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：not | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：null | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：nullemptystringbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：numeric / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：numeric / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：numeric / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：numerology | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：object | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：obsscaninfo | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：oid | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：on | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：online | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：opr | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：optimizing | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：orderby | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：out | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：outfuncs | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：package | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：parallel | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：parametermetadatatestbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：parse | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：partition / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：partition / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：path | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pbe | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pg | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pgfincore | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pgstat | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：physical | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pl | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pldeveloper | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pljson | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：plpgsql / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：plpgsql / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：plpgsql / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：plpgsql / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：plpgsql / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：plpgsql / 分批6 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：plpython | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pmk | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：point | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：polygon | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：polymorphism | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：portals | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：post | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pre | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：prefixkey | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：prepare | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatamentintbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatamentnumericbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatamentstringbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatamentvarcharbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatamentwithhardcodedvaluesbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatementdeleteresultsetbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatementinsertresultsetbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatementuniquebin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatementupdateresultsetbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preparestatementviewbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：preread | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：pri | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：privileges / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：privileges / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：procedure | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：psql | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：query | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：random | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rangefuncs | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rangetypes | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rawlike | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：readline | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：record | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：recursive / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：recursive / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：reduce | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：regex | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：regex.linux.utf | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：reindex | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：reltime | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rename | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：replace | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：replaceinto | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：replica | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：replication | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：resolve | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：resultsetfetchbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：resultsetfetchnoclbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：resultsetmetadatatestbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：returning | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rollback | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：row | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rowlevelsecurity | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rowtypes | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rule | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：rules | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sanity | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：security | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：seg | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：segment / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：segment / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：segment / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：select / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：select / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：select / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：select / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：select / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：select / 分批6 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：select / 分批7 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：seqscan | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sequence | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：set | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：setop | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：setrefs | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：show | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：shutdown | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：simplequerybin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：simplesort | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批6 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批7 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批8 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批9 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批10 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批11 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批12 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批13 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批14 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批15 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批16 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批17 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批18 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：single / 分批19 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：skew / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：skew / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：skew / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：skew / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：skew / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：skiplocked | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：slot | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：smp | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sortgroup | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：split | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sql | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sqlbypass | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sqlcode | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sqlllt | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sqlpatch | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ss | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：stable | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：statistic | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：stats | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：stmtbatchclientlogicbin | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：string | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：strings | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sublink | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：subselect | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：substr | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：subtype | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sw / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sw / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sync | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：synchronous | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：synonym | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：sytcomp | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：table | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tableam | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tableof | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tablesample | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tabletype | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：temp | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：test / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：test / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：test / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：test / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：test / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：test / 分批6 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：text | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：threadpool | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：time | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：timeout | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：timestamp | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：timetz | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tinterval | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：to | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：toomanyparams | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tpch / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tpch / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tpch / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tpch / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tpch11 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tpchcol / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tpchcol / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tpchcol / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：transactions | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：triggers / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：triggers / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：trunc | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：truncate | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ts | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tsdb | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tsdicts | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tsearch | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：tstypes | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：txid | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：type | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：typed | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：union | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：unique | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：unsupported | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：updatable | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：update | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：uppercase | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：upsert / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：upsert / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ustore / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ustore / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：ustore / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：uuid | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vacuum | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：varchar | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批6 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批7 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批8 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批9 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批10 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批11 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批12 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批13 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批14 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批15 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vec / 分批16 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：vector | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：view | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：wait | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：window | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：with | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：without | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：workload | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xc / 分批1 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xc / 分批2 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xc / 分批3 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xc / 分批4 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xc / 分批5 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xc / 分批6 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xc / 分批7 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xml | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xmlmap | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 回归主题：xmltype | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected | 事务、可见性与结束处理 | 0 |  | task:a1502b3fe769e64a2b6f5bffe815bf50 |
| server/src/test/regress/expected/d_format_test | 连接路径与连接约束 | 0 |  | task:1f58acfc3feda3a12c59d2bc57dc98a5 |
| server/src/test/regress/expected/d_format_test | 回归主题：apply | 0 |  | task:1f58acfc3feda3a12c59d2bc57dc98a5 |
| server/src/test/regress/expected/d_format_test | 回归主题：charset | 0 |  | task:1f58acfc3feda3a12c59d2bc57dc98a5 |
| server/src/test/regress/expected/ignore | 缓存、失效与复用 | 0 |  | task:dde644ba55bf3fa8aac4a2c792a6b11b |
| server/src/test/regress/expected/ignore | 回归主题：ignore | 0 |  | task:dde644ba55bf3fa8aac4a2c792a6b11b |
| server/src/test/regress/expected/mot | 连接路径与连接约束 | 0 |  | task:f6b427a992b29ccaeb5415a48118b4bb |
| server/src/test/regress/expected/mot | 回归主题：disable | 0 |  | task:f6b427a992b29ccaeb5415a48118b4bb |
| server/src/test/regress/expected/mot | 回归主题：enable | 0 |  | task:f6b427a992b29ccaeb5415a48118b4bb |
| server/src/test/regress/expected/mot | 回归主题：single / 分批1 | 0 |  | task:f6b427a992b29ccaeb5415a48118b4bb |
| server/src/test/regress/expected/mot | 回归主题：single / 分批2 | 0 |  | task:f6b427a992b29ccaeb5415a48118b4bb |
| server/src/test/regress/expected/mot | 回归主题：single / 分批3 | 0 |  | task:f6b427a992b29ccaeb5415a48118b4bb |
| server/src/test/regress/expected/mot | 回归主题：without | 0 |  | task:f6b427a992b29ccaeb5415a48118b4bb |
| server/src/test/regress/expected/plpgsql | 回归主题：plpgsql | 0 |  | task:80b4b22a3649a47c4963528d27e05455 |
| server/src/test/regress/expected/plpgsql_depend | 回归主题：plpgsql / 分批1 | 0 |  | task:c8a45442964ca060924d62a8690104d4 |
| server/src/test/regress/expected/plpgsql_depend | 回归主题：plpgsql / 分批2 | 0 |  | task:c8a45442964ca060924d62a8690104d4 |
| server/src/test/regress/expected/plpgsql_depend | 回归主题：plpgsql / 分批3 | 0 |  | task:c8a45442964ca060924d62a8690104d4 |
| server/src/test/regress/expected/plpgsql_depend | 回归主题：plpgsql / 分批4 | 0 |  | task:c8a45442964ca060924d62a8690104d4 |
| server/src/test/regress/expected/row_compression | 回归主题：alter | 0 |  | task:b8e4d651131c4f810a1afb5b5878d9a8 |
| server/src/test/regress/expected/row_compression | 回归主题：normal | 0 |  | task:b8e4d651131c4f810a1afb5b5878d9a8 |
| server/src/test/regress/expected/row_compression | 回归主题：pg | 0 |  | task:b8e4d651131c4f810a1afb5b5878d9a8 |
| server/src/test/regress/expected/row_compression | 回归主题：row | 0 |  | task:b8e4d651131c4f810a1afb5b5878d9a8 |
| server/src/test/regress/expected/row_compression | 回归主题：unsupported | 0 |  | task:b8e4d651131c4f810a1afb5b5878d9a8 |
| server/src/test/regress/expected/sqlldr | 回归主题：load | 0 |  | task:725a81457a5099a7cb817d990c178433 |
| server/src/test/regress/expected/ss_r | 回归主题：gsc | 0 |  | task:69fc54ac93e9412610a6c4bae8226a07 |
| server/src/test/regress/expected/ss_r | 回归主题：pg | 0 |  | task:69fc54ac93e9412610a6c4bae8226a07 |
| server/src/test/regress/expected/ss_r | 回归主题：replace | 0 |  | task:69fc54ac93e9412610a6c4bae8226a07 |
| server/src/test/regress/expected/ss_r | 回归主题：segment | 0 |  | task:69fc54ac93e9412610a6c4bae8226a07 |
| server/src/test/regress/expected/ss_r | 回归主题：ss | 0 |  | task:69fc54ac93e9412610a6c4bae8226a07 |
| server/src/test/regress/expected/ss_r | 回归主题：trunc | 0 |  | task:69fc54ac93e9412610a6c4bae8226a07 |
| server/src/test/regress/expected/ss_wr | 回归主题：gsc | 0 |  | task:604b2ba4e455986af77cb7d0c25f7fd6 |
| server/src/test/regress/expected/ss_wr | 回归主题：pg | 0 |  | task:604b2ba4e455986af77cb7d0c25f7fd6 |
| server/src/test/regress/expected/ss_wr | 回归主题：replace | 0 |  | task:604b2ba4e455986af77cb7d0c25f7fd6 |
| server/src/test/regress/expected/ss_wr | 回归主题：segment | 0 |  | task:604b2ba4e455986af77cb7d0c25f7fd6 |
| server/src/test/regress/expected/ss_wr | 回归主题：ss | 0 |  | task:604b2ba4e455986af77cb7d0c25f7fd6 |
| server/src/test/regress/expected/ss_wr | 回归主题：trunc | 0 |  | task:604b2ba4e455986af77cb7d0c25f7fd6 |
| server/src/test/regress/input | 缓存、失效与复用 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 配置注册与生效 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 代价与基数估算 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 连接路径与连接约束 / 分批1 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 连接路径与连接约束 / 分批2 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 连接路径与连接约束 / 分批3 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 连接路径与连接约束 / 分批4 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 计划生成与计划接口 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 持久化与恢复 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 资源寿命与错误清理 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：accept | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：add | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：aioptimizer | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：alter | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：analyse | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：anomaly | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：any | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：autoanalyze | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：backup | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：bitmapops | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：bulkload | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：bypass | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：cgin | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：charset | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：cluster | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：cmpr / 分批1 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：cmpr / 分批2 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：comment | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：component | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：compress / 分批1 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：compress / 分批2 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：constraints | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：copy | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：create | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：cstore / 分批1 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：cstore / 分批2 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：csv | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：cursor | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：data | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：db4ai / 分批1 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：db4ai / 分批2 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：db4ai / 分批3 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：delete | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：directory | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：dump | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：dw | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：enum | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：event | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：explain | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：fdw | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：forbid | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gaussdb | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gin | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gs | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gsbasebackup | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gsc | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gsdump | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gsloader | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gsql | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gsqlerr | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gstrace | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：gtt | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：holdable | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：hw / 分批1 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：hw / 分批2 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：hw / 分批3 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：hw / 分批4 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：hw / 分批5 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：hw / 分批6 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：initdb | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：insert | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：instr | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：iud | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：largeobject | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：lateral | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：ledger | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：libcomm | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：matview | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：misc | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：multi | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：mysql | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：nested | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：not | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：parallel | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：partition | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：performance | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：pg | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：pldebugger | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：plpgsql | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：predefined | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：prevent | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：pri | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：procedure | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：process | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：psql | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：public | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：publication | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：quality | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：related | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：remotetype | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：retry | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：rlstm | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：row | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：security | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：segment | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：select | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：set | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：single | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：slow | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：smp | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：sort | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：sp | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：sqlpatch | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：srf | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：ss | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：subscription | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：tablespace | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：temp | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：test / 分批1 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：test / 分批2 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：test / 分批3 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：test / 分批4 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：tidrangescan | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：timecapsule / 分批1 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：timecapsule / 分批2 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：tpchrush | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：trigger | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：ts | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：udf | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：unify | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：user | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：ustore | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：vec | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：view | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：xc | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 回归主题：xml | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input | 事务、可见性与结束处理 | 0 |  | task:bc57eff180b0027117d9187dbe57ab71 |
| server/src/test/regress/input/mot | 回归主题：single | 0 |  | task:0fea1d082b9f0a07c66794b93da2c5b2 |
| server/src/test/regress/input/row_compression | 回归主题：row | 0 |  | task:f9519e415894e455db97679506407519 |
| server/src/test/regress/input/row_compression | 回归主题：twophase | 0 |  | task:f9519e415894e455db97679506407519 |
| server/src/test/regress/input/sqlldr | 回归主题：gs | 0 |  | task:797d15b48d5a6f1dff2ccaedc313d933 |
| server/src/test/regress/input/sqlldr | 回归主题：load | 0 |  | task:797d15b48d5a6f1dff2ccaedc313d933 |
| server/src/test/regress/jar | 配置注册与生效 | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：basic | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：bcprov-ext-jdk15on | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：commons-codec-1. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：commons-collections-3.2. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：commons-io-2. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：commons-lang-2. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：commons-logging-1. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：dim | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：dom4j-1.6. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：factor | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：factor.cfg | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：fastjson-1.2. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：geoip | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：geoip-api-1.2. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：global | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：gt-geojson-14. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：guava-19. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：hive-exec-0.7. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：huawei | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：ipip | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：jackson-annotations-2.3. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：jackson-core-2.5. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：jackson-databind-2.3. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：json-lib-2.4-jdk | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：log4j-1.2. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：maxmind-db-1.0. | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：mcc | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jar | 回归主题：workey | 0 |  | task:7c43ed3b21ba4dfe8fa35488025b9325 |
| server/src/test/regress/jdbc_ce_test | 回归主题：clientencryptioncreatetest | 0 |  | task:164e72abd0cf14b3b3e37108b0a828a9 |
| server/src/test/regress/jdbc_ce_test | 回归主题：clientencryptionfetchsizetest | 0 |  | task:164e72abd0cf14b3b3e37108b0a828a9 |
| server/src/test/regress/jdbc_ce_test | 回归主题：clientencryptionmulsql | 0 |  | task:164e72abd0cf14b3b3e37108b0a828a9 |
| server/src/test/regress/jdbc_ce_test | 回归主题：clientencryptionpreparetest | 0 |  | task:164e72abd0cf14b3b3e37108b0a828a9 |
| server/src/test/regress/jdbc_ce_test | 回归主题：clientencryptionselecttest | 0 |  | task:164e72abd0cf14b3b3e37108b0a828a9 |
| server/src/test/regress/jdbc_ce_test | 回归主题：clientencryptiontransactiontest | 0 |  | task:164e72abd0cf14b3b3e37108b0a828a9 |
| server/src/test/regress/jdbc_ce_test | 回归主题：clientencryptiontriggertest | 0 |  | task:164e72abd0cf14b3b3e37108b0a828a9 |
| server/src/test/regress/jdbc_ce_test | 回归主题：utiltool | 0 |  | task:164e72abd0cf14b3b3e37108b0a828a9 |
| server/src/test/regress/jdbc_client | 缓存、失效与复用 | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 资源寿命与错误清理 | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：.gitignore | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：batchpreparedstatementsbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：batchsimplequerybin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：batchstatamentbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：binutils | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：cmakelists | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：commandtype | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：createfunctionbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：createtablewithpreparestatamentbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：databaseconnection4test | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：databasemetadatagetcolumnsbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：dbutils | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：disconnectedrsbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：functionsinoutparambin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：functionsinoutparambinarymodebin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：functionsinoutparamsbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：functionsmetadatabin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：functionsoutparambin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：functionsreturnvaluesbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：handlingbadsqlbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：ibinarytest | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：iinputfileparser | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：inputfileparser | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：jdbcclient | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：jdbcclientwrapper4test | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：makefile | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：manifest | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：metadtautils | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：multithreadclientlogicbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：nullemptystringbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：outfilewriter | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：parametermetadatatestbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatamentintbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatamentnumericbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatamentstringbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatamentvarcharbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatamentwithhardcodedvaluesbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatementdeleteresultsetbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatementinsertresultsetbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatementuniquebin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatementupdateresultsetbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：preparestatementviewbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：resultsetfetchbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：resultsetfetchnoclbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：resultsetmetadatatestbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：simplequerybin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：sqlcommand | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：stmtbatchclientlogicbin | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：stringutils | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client | 回归主题：testleak | 0 |  | task:3c9ec5e541314bd1c3699218dce3b92f |
| server/src/test/regress/jdbc_client_lib | 回归主题：gsjdbc | 0 |  | task:a9f622c94facc2dec22305a245b927b6 |
| server/src/test/regress/jdbc_test | 回归主题：bypasspbe | 0 |  | task:3de17ad86260f4b2d051d90fa97fc755 |
| server/src/test/regress/jdbc_test | 回归主题：gsjdbc | 0 |  | task:3de17ad86260f4b2d051d90fa97fc755 |
| server/src/test/regress/jdbc_test | 回归主题：insertrightreftest | 0 |  | task:3de17ad86260f4b2d051d90fa97fc755 |
| server/src/test/regress/jdbc_test | 回归主题：multisimplequery | 0 |  | task:3de17ad86260f4b2d051d90fa97fc755 |
| server/src/test/regress/krbclient | 配置注册与生效 | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：.gitignore | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：compile | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：gss-client | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：hadoop | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：k5srvutil | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：kadmin | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：kdestroy | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：kinit | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：klist | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：kpasswd | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：ksu | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：kswitch | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：ktutil | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：kvno | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：sclient | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：security | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：sim | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/krbclient | 回归主题：uuclient | 0 |  | task:8b18917b29e67f84601582b035c12061 |
| server/src/test/regress/obstools | 回归主题：makefile | 0 |  | task:60b44eb3a3771c25caeec7f0fc328ca6 |
| server/src/test/regress/obstools | 回归主题：obs | 0 |  | task:60b44eb3a3771c25caeec7f0fc328ca6 |
| server/src/test/regress/obstools | 回归主题：obstool | 0 |  | task:60b44eb3a3771c25caeec7f0fc328ca6 |
| server/src/test/regress/output | 缓存、失效与复用 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 配置注册与生效 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 代价与基数估算 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批3 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批4 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批5 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批6 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批7 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批8 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批9 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 连接路径与连接约束 / 分批10 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 计划生成与计划接口 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 持久化与恢复 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 资源寿命与错误清理 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：accept | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：add | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：aioptimizer | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：alter | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：analyse | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：anomaly | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：any | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：area | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：autoanalyze | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：backup | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：binary | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：bitmapops | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：bulkload | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：bypass | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cgin | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：charset | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cluster | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cmpr / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cmpr / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：comment | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：component | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：compress | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：compress01 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：constraints | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：copy | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：create | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cstore / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cstore / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cstore / 分批3 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cstore / 分批4 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：csv | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：cursor | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：data | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：db4ai | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：ddl | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：delete | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：dfs | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：directory | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：dump | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：dw | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：enum | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：event | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：explain | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：fdw | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：forbid | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gaussdb | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gin | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gs | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gsbasebackup | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gsc | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gsdump | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gsloader | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gsql | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gsqlerr | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gstrace | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：gtt | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：holdable | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批3 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批4 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批5 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批6 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批7 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批8 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批9 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批10 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批11 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批12 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批13 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批14 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批15 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：hw / 分批16 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：initdb | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：insert | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：instr | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：iud | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：largeobject | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：lateral / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：lateral / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：ledger | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：libcomm | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：matview | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：misc | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：multi | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：mysql | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：nested | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：not | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：parallel | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：partition | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：performance | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：pg | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：pldebugger | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：plpgsql | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：predefined | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：prevent | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：pri | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：procedure | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：process | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：psql | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：public | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：publication | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：quality | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：related | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：remotetype | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：replication | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：retry | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：rewrite | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：rlstm | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：row | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：security | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：segment | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：select | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：set | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：single | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：slow | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：smp | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：sort | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：sp | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：spill | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：sqlpatch | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：srf | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：subscription | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：tablespace | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：temp | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：test / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：test / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：test / 分批3 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：test / 分批4 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：test / 分批5 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：tidrangescan | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：timecapsule / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：timecapsule / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：toast | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：tpchrush | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：trigger | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：ts | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：udf | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：unify | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：user | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：ustore / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：ustore / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：vec / 分批1 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：vec / 分批2 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：vec / 分批3 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：view | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：xc | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 回归主题：xml | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output | 事务、可见性与结束处理 | 0 |  | task:3af1255e3882e07214c8831d0f7dee65 |
| server/src/test/regress/output/mot | 回归主题：single | 0 |  | task:7c26b31b1aa94e2366db677503af3245 |
| server/src/test/regress/output/row_compression | 回归主题：row | 0 |  | task:90b1ba9ad4efc4b0f85199ab2a1cd01d |
| server/src/test/regress/output/row_compression | 回归主题：twophase | 0 |  | task:90b1ba9ad4efc4b0f85199ab2a1cd01d |
| server/src/test/regress/output/sqlldr | 回归主题：gs | 0 |  | task:555a985f3f0b66756bdc70d0d178d436 |
| server/src/test/regress/output/sqlldr | 回归主题：load | 0 |  | task:555a985f3f0b66756bdc70d0d178d436 |
| server/src/test/regress/s3bin | 回归主题：s | 0 |  | task:79cf4cf4d18a8d891a29e31e22055056 |
| server/src/test/regress/s3bin | 回归主题：s3 | 0 |  | task:79cf4cf4d18a8d891a29e31e22055056 |
| server/src/test/regress/script | 缓存、失效与复用 | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/script | 配置注册与生效 | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/script | 回归主题：auto | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/script | 回归主题：automated-test | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/script | 回归主题：check | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/script | 回归主题：find | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/script | 回归主题：gs | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/script | 回归主题：init | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/script | 回归主题：opengaussops | 0 |  | task:3dcd48fa1313257c5586f232f280ca86 |
| server/src/test/regress/security_scripts | 回归主题：post | 0 |  | task:79a7941c883ffcb980b61632303e62de |
| server/src/test/regress/security_scripts | 回归主题：prepare | 0 |  | task:79a7941c883ffcb980b61632303e62de |
| server/src/test/regress/security_scripts | 回归主题：syslog | 0 |  | task:79a7941c883ffcb980b61632303e62de |
| server/src/test/regress/snapshots_test | 回归主题：06 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：07 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：08 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：09 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：10 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：11 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：12 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：13 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：14 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：exectestharness | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：setuptestharness | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：teardowntestharness | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：test | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 回归主题：xx | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/snapshots_test | 事务、可见性与结束处理 | 0 |  | task:6b4396be1f73fa6aa27a2a120ca9545d |
| server/src/test/regress/sql | 缓存、失效与复用 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 配置注册与生效 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 代价与基数估算 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 连接路径与连接约束 / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 连接路径与连接约束 / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 连接路径与连接约束 / 分批3 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 计划生成与计划接口 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 持久化与恢复 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 资源寿命与错误清理 / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 资源寿命与错误清理 / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：abstime | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：accept | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：advisory | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：agg | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：aggregate | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：aggregates | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：ai | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：alarm | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：alter / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：alter / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：alter / 分批3 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：am | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：amheap | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：analytic | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：analyze | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：array | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：arrayinterface | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：arrays | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：auto | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：autocommit | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：autonomous | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：b | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：backtrace | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：base | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：binary | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：bit | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：bloom | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：bm25 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：boolean | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：box | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：bpchar | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：btree | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：bypass | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：case | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：cast | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：ceil | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：cgin | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：char | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：charset | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：checksum | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：chr | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：circle | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：cluster | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：col | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：collate | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：collate.linux.utf | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：combocid | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：comment | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：comments | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：composite | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：compress | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：conversion | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：copy | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：copy2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：copyselect | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：count | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：create / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：create / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：cstore | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：cte | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：cursor | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：date | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：datefunc | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：ddl | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：declare | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：decode | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：deferrable | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：delete | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：dependency | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：dependent | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：describe | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：deserialize | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：detail | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：disable | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：diskann | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：display | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：distinct | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：dml | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：domain | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：double | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：drop | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：duplicate | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：early | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：enable | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：encode | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：encrypt | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：enum | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：equivalence | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：euc | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：event | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：exec | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：explain | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：expr | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：extendstat | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：extra | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：extract | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：fenced | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：fetch | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：first | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：float | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：forall | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：force | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：foreign | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：func | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：function | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：functional | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：gb | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：gen | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：generated | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：geometry | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：get | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：gin | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：global | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：gms | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：goto | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：gpi | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：gs | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：gsc | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：gtt | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hash | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hashfilter | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：heap | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hll | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hnsw | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：huge | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批3 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批4 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批5 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批6 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批7 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批8 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批9 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批10 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批11 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批12 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hw / 分批13 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：hybrid | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：icbc | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：ignore | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：index | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：inet | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：inherits | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：inlineview | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：inplace | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：insert | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：int | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：interval | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：invisible | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：iud | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：json | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：jsonb | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：jsonpath | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：keep | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：keywords | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：large | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：leaky | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：limit | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：llt | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：llvm | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：lock | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：locktag | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：long | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：lseg | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：macaddr | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：magic | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：matview | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：median | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：merge / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：merge / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：min | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：money | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：mule | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：multi | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：mysql | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：name | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：namespace | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：nested | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：nls | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：nlssort | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：node | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：normal | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：not | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：null | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：numeric / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：numeric / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：numeric / 分批3 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：numerology | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：object | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：obsscaninfo | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：oid | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：on | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：online | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：opr | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：optimizing | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：orderby | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：out | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：outfuncs | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：package | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：parallel | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：parse | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：partition | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：path | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pbe | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pg | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pgfincore | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pgstat | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：physical | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pl | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pldeveloper | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pljson | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：plpgsql / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：plpgsql / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：plpgsql / 分批3 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：plpython | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pmk | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：point | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：polygon | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：polymorphism | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：portals | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：post | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：postgis | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：prefixkey | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：prepare | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：preread | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：pri | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：privileges | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：procedure | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：psql | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：query | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：random | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rangefuncs | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rangetypes | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rawlike | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：readline | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：record | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：recursive | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：reduce | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：regex | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：regex.linux.utf | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：reindex | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：reltime | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rename | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：replace | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：replaceinto | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：replica | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：replication | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：resolve | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：returning | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rewrite | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rollback | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：row | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rowlevelsecurity | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rowtypes | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rule | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：rules | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sanity | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：security | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：seg | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：segment | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：select | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：seqscan | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sequence | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：set | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：setop | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：setrefs | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：show | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：shutdown | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：simplesort | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：single / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：single / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：single / 分批3 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：single / 分批4 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：single / 分批5 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：single / 分批6 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：single / 分批7 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：single / 分批8 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：skew | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：skiplocked | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：slot | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：smp | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sortgroup | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：spill | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：split | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sql | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sqlbypass | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sqlcode | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sqlllt | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sqlpatch | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：srf | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：ss | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：stable | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：statistic | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：stats | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：string | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：strings | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sublink | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：subselect | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：substr | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：subtype | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sw | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sync | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：synchronous | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：synonym | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：sytcomp | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：table | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tableam | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tableof | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tablesample | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tabletype | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：temp | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：test / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：test / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：test / 分批3 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：text | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：threadpool | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：time | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：timeout | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：timestamp | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：timetz | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tinterval | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：to | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：toast | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：toomanyparams | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tpch / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tpch / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tpch11 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tpchcol | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：transactions | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：triggers | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：trunc | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：truncate | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：ts | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tsdb | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tsdicts | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tsearch | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：tstypes | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：txid | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：type | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：typed | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：union | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：unique | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：unsupported | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：updatable | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：update | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：uppercase | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：upsert | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：ustore / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：ustore / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：uuid | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：vacuum | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：varchar | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：vec / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：vec / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：vec / 分批3 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：vec / 分批4 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：vector | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：verify | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：view | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：wait | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：window | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：with | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：without | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：workload | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：xc / 分批1 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：xc / 分批2 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：xml | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：xmlmap | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 回归主题：xmltype | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql | 事务、可见性与结束处理 | 0 |  | task:d9697e262ffbab18842621b9ddd05803 |
| server/src/test/regress/sql/d_format_test | 连接路径与连接约束 | 0 |  | task:c6ede59a0d5a6d66920f33498afae2ee |
| server/src/test/regress/sql/d_format_test | 回归主题：apply | 0 |  | task:c6ede59a0d5a6d66920f33498afae2ee |
| server/src/test/regress/sql/d_format_test | 回归主题：charset | 0 |  | task:c6ede59a0d5a6d66920f33498afae2ee |
| server/src/test/regress/sql/gs_basebackup | 回归主题：compress | 0 |  | task:329a3d949a458b6c4eba1f4864c9989a |
| server/src/test/regress/sql/gs_basebackup | 回归主题：mot | 0 |  | task:329a3d949a458b6c4eba1f4864c9989a |
| server/src/test/regress/sql/gs_basebackup | 回归主题：tablespace | 0 |  | task:329a3d949a458b6c4eba1f4864c9989a |
| server/src/test/regress/sql/ignore | 缓存、失效与复用 | 0 |  | task:123ed5950ce0f6acfd3455910741b52a |
| server/src/test/regress/sql/ignore | 回归主题：ignore | 0 |  | task:123ed5950ce0f6acfd3455910741b52a |
| server/src/test/regress/sql/mot | 连接路径与连接约束 | 0 |  | task:832077c7672e1e05c5a023729aba57ab |
| server/src/test/regress/sql/mot | 回归主题：enable | 0 |  | task:832077c7672e1e05c5a023729aba57ab |
| server/src/test/regress/sql/mot | 回归主题：single / 分批1 | 0 |  | task:832077c7672e1e05c5a023729aba57ab |
| server/src/test/regress/sql/mot | 回归主题：single / 分批2 | 0 |  | task:832077c7672e1e05c5a023729aba57ab |
| server/src/test/regress/sql/mot | 回归主题：single / 分批3 | 0 |  | task:832077c7672e1e05c5a023729aba57ab |
| server/src/test/regress/sql/mot | 回归主题：without | 0 |  | task:832077c7672e1e05c5a023729aba57ab |
| server/src/test/regress/sql/plpgsql | 回归主题：plpgsql | 0 |  | task:f96ad58399d0fb107e30778d7b0746a5 |
| server/src/test/regress/sql/plpgsql_depend | 回归主题：plpgsql / 分批1 | 0 |  | task:7e9cc87ffd9fa3711aaa7f63ed6de0cf |
| server/src/test/regress/sql/plpgsql_depend | 回归主题：plpgsql / 分批2 | 0 |  | task:7e9cc87ffd9fa3711aaa7f63ed6de0cf |
| server/src/test/regress/sql/row_compression | 回归主题：alter | 0 |  | task:b0f855533f75efd613c277f149d41996 |
| server/src/test/regress/sql/row_compression | 回归主题：normal | 0 |  | task:b0f855533f75efd613c277f149d41996 |
| server/src/test/regress/sql/row_compression | 回归主题：pg | 0 |  | task:b0f855533f75efd613c277f149d41996 |
| server/src/test/regress/sql/row_compression | 回归主题：row | 0 |  | task:b0f855533f75efd613c277f149d41996 |
| server/src/test/regress/sql/row_compression | 回归主题：unsupported | 0 |  | task:b0f855533f75efd613c277f149d41996 |
| server/src/test/regress/sql/sqlldr | 回归主题：load | 0 |  | task:d53e7c0eed91d94deae9c3c860802056 |
| server/src/test/regress/sql/ss_r | 回归主题：gsc | 0 |  | task:28770f405bb192bc4d9a74da2a87b662 |
| server/src/test/regress/sql/ss_r | 回归主题：replace | 0 |  | task:28770f405bb192bc4d9a74da2a87b662 |
| server/src/test/regress/sql/ss_r | 回归主题：segment | 0 |  | task:28770f405bb192bc4d9a74da2a87b662 |
| server/src/test/regress/sql/ss_r | 回归主题：ss | 0 |  | task:28770f405bb192bc4d9a74da2a87b662 |
| server/src/test/regress/sql/ss_r | 回归主题：trunc | 0 |  | task:28770f405bb192bc4d9a74da2a87b662 |
| server/src/test/regress/sql/ss_wr | 回归主题：gsc | 0 |  | task:a6b7ba26d9c12b4bb865e4aac427655d |
| server/src/test/regress/sql/ss_wr | 回归主题：replace | 0 |  | task:a6b7ba26d9c12b4bb865e4aac427655d |
| server/src/test/regress/sql/ss_wr | 回归主题：segment | 0 |  | task:a6b7ba26d9c12b4bb865e4aac427655d |
| server/src/test/regress/sql/ss_wr | 回归主题：ss | 0 |  | task:a6b7ba26d9c12b4bb865e4aac427655d |
| server/src/test/regress/sql/ss_wr | 回归主题：trunc | 0 |  | task:a6b7ba26d9c12b4bb865e4aac427655d |
| server/src/test/regress/sslcert | 回归主题：client | 0 |  | task:565ce06212f23049a24eceb4864b6896 |
| server/src/test/regress/sslcert | 回归主题：server | 0 |  | task:565ce06212f23049a24eceb4864b6896 |
| server/src/test/regress/sslcert_withpwd | 回归主题：client | 0 |  | task:fac2fd2b5c9c181b4cd45a05f48d18e2 |
| server/src/test/regress/sslcert_withpwd | 回归主题：server | 0 |  | task:fac2fd2b5c9c181b4cd45a05f48d18e2 |
| server/src/test/regress/stub | 回归主题：cmakelists | 0 |  | task:48465af91e32cd179c316e60cdaac28b |
| server/src/test/regress/stub | 回归主题：makefile | 0 |  | task:48465af91e32cd179c316e60cdaac28b |
| server/src/test/regress/stub | 回归主题：roach | 1 |  | task:48465af91e32cd179c316e60cdaac28b |
| server/src/test/regress/wastebin/expected | 缓存、失效与复用 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 连接路径与连接约束 / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 连接路径与连接约束 / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 连接路径与连接约束 / 分批3 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 连接路径与连接约束 / 分批4 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 计划生成与计划接口 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 资源寿命与错误清理 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：active | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：add | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：advance | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：at | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：cbm | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：ce / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：ce / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：ce / 分批3 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：ce / 分批4 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：ce / 分批5 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：ce / 分批6 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：check | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：cn | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：concat | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：create | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dbe | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批3 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批4 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批5 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批6 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批7 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批8 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批9 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批10 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批11 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批12 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批13 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批14 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：dfs / 分批15 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：drop | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：hash | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：hdfs | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：hll | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：horology | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：hs | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：hw / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：hw / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：hw / 分批3 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：hw / 分批4 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：inherit | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：insert / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：insert / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：instr | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：javaudf | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：limit | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：llt | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：merge | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：nodegroup / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：nodegroup / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：nodegroup / 分批3 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：nodegroup / 分批4 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：nodegroup / 分批5 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：not | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：others | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：plpgsql | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：post | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：postgis / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：postgis / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：postgis / 分批3 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：pre | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：redis | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：shipping / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：shipping / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：single / 分批1 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：single / 分批2 | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：timestamptz | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：workload | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/expected | 回归主题：xc | 0 |  | task:81fed5a1d851caf8528df3cefb2442a4 |
| server/src/test/regress/wastebin/input | 缓存、失效与复用 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 配置注册与生效 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 连接路径与连接约束 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 计划生成与计划接口 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 持久化与恢复 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 资源寿命与错误清理 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：addnode | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：analyze | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：bulkload | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：ca | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：ce | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：cleannode | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：create | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：dfs / 分批1 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：dfs / 分批2 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：dfs / 分批3 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：dfs / 分批4 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：do | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：drop | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：dummy | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：enum | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：fdw | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：global | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：gs | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：hdfs | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：holdable | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：hotpatch | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：hw | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：informational | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：inner | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：javaudf | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：license | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：obs / 分批1 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：obs / 分批2 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：obs / 分批3 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：online | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：orc / 分批1 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：orc / 分批2 | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：parquet | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：pre | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：redis | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：security | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：shipping | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：single | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：vec | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/input | 回归主题：wlm | 0 |  | task:49f8eaa0db2770b9633c2e369c49fde4 |
| server/src/test/regress/wastebin/output | 缓存、失效与复用 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 配置注册与生效 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 连接路径与连接约束 / 分批1 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 连接路径与连接约束 / 分批2 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 计划生成与计划接口 / 分批1 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 计划生成与计划接口 / 分批2 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 计划生成与计划接口 / 分批3 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 持久化与恢复 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 资源寿命与错误清理 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：addnode | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：analyze | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：bulkload / 分批1 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：bulkload / 分批2 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：ca | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：ce | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：cleannode | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：create | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批1 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批2 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批3 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批4 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批5 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批6 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批7 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批8 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批9 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dfs / 分批10 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：directory | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：do | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：dummy | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：enum | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：fdw | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：global | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：gs | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：hdfs | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：holdable | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：hotpatch | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：hw | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：informational | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：inner | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：javaudf | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：license | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批1 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批2 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批3 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批4 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批5 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批6 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批7 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批8 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批9 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批10 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批11 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批12 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批13 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：obs / 分批14 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：online | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：orc / 分批1 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：orc / 分批2 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：orc / 分批3 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：orc / 分批4 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：orc / 分批5 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：orc / 分批6 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：parquet / 分批1 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：parquet / 分批2 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：parquet / 分批3 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：parquet / 分批4 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：parquet / 分批5 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：pre | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：redis | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：security | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：shipping | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：single | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：vec / 分批1 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：vec / 分批2 | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/output | 回归主题：wlm | 0 |  | task:50c9ed913a391d784360b56370ab074d |
| server/src/test/regress/wastebin/sql | 缓存、失效与复用 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 连接路径与连接约束 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 计划生成与计划接口 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 资源寿命与错误清理 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：active | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：add | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：advance | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：area | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：at | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：cbm | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：ce / 分批1 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：ce / 分批2 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：ce / 分批3 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：ce / 分批4 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：ce / 分批5 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：ce / 分批6 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：check | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：cn | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：concat | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：create | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：dbe | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：dfs / 分批1 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：dfs / 分批2 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：dfs / 分批3 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：drop | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：gpi | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：hash | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：hdfs | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：hll | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：horology | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：hs | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：hw / 分批1 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：hw / 分批2 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：inherit | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：insert | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：instr | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：javaudf | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：limit | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：llt | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：merge | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：nodegroup / 分批1 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：nodegroup / 分批2 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：not | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：others | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：plpgsql | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：post | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：postgis | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：pre | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：redis / 分批1 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：redis / 分批2 | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：shipping | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：single | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：timestamptz | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：workload | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/regress/wastebin/sql | 回归主题：xc | 0 |  | task:96657139e5427463f981c0debd656cb6 |
| server/src/test/ss | 配置注册与生效 | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 持久化与恢复 | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 回归主题：build | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 回归主题：cm | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 回归主题：common | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 回归主题：conf | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 回归主题：deploy | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 回归主题：ha | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 回归主题：ss | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/ss | 回归主题：standby | 0 |  | task:9a624a24b7bf62a6d771d3637e6e5190 |
| server/src/test/subscription | 回归主题：cmakelists | 0 |  | task:945abc782606f69143f5d0dae4f15991 |
| server/src/test/subscription | 回归主题：env | 0 |  | task:945abc782606f69143f5d0dae4f15991 |
| server/src/test/subscription | 回归主题：gnumakefile | 0 |  | task:945abc782606f69143f5d0dae4f15991 |
| server/src/test/subscription | 回归主题：makefile | 0 |  | task:945abc782606f69143f5d0dae4f15991 |
| server/src/test/subscription | 回归主题：pubsub | 0 |  | task:945abc782606f69143f5d0dae4f15991 |
| server/src/test/subscription | 回归主题：run | 0 |  | task:945abc782606f69143f5d0dae4f15991 |
| server/src/test/subscription | 回归主题：schedule | 0 |  | task:945abc782606f69143f5d0dae4f15991 |
| server/src/test/subscription/testcase | 持久化与恢复 | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：binary | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：bugs | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：constraints | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：create | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：ddl / 分批1 | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：ddl / 分批2 | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：ddl / 分批3 | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：ddl / 分批4 | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：diff | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：disable | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：dump | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：encoding | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：generated | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：matviews | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：pub | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：rep | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：rewrite | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：skiplsn | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：sync | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/subscription/testcase | 回归主题：types | 0 |  | task:3a0e1aaf4a7270c01555ea1ca694f760 |
| server/src/test/thread | 回归主题：makefile | 0 |  | task:e5729e7afc6868870cf7ed854f2c3a88 |
| server/src/test/thread | 回归主题：readme | 0 |  | task:e5729e7afc6868870cf7ed854f2c3a88 |
| server/src/test/thread | 回归主题：thread | 1 |  | task:e5729e7afc6868870cf7ed854f2c3a88 |
| server/src/test/ut | 回归主题：cmakelists | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：coordinates | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：direct | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：ecoli | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：gd | 1 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：kmeans | 1 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：makefile | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：mock | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：moons | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：patients | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：pca | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：pg | 1 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：rain | 0 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：readers | 1 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：svm | 1 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：ut | 2 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut | 回归主题：xgboost | 1 |  | task:1140780d6a9c2488150a9445192b3a29 |
| server/src/test/ut/include | 回归主题：gunit | 0 |  | task:596cee167606fe4aaa9b2ab80aee2d17 |
| server/src/test/whitebox | 回归主题：knl | 1 |  | task:58cac957b08abad776291888195ad9f0 |
| server/src/test/whitebox | 回归主题：makefile | 0 |  | task:58cac957b08abad776291888195ad9f0 |
| server/src/tools | 模块实现、接口与状态机制 | 0 |  | task:b32edfc7f7ca543b858a367d0ac8b49f |
| server/src/tools | 资源寿命与错误清理 | 0 |  | task:b32edfc7f7ca543b858a367d0ac8b49f |
| server/src/tools/backend | 模块实现、接口与状态机制 / 分批1 | 0 |  | task:b901379dd3fe0361326412e8d455080a |
| server/src/tools/backend | 模块实现、接口与状态机制 / 分批2 | 0 |  | task:b901379dd3fe0361326412e8d455080a |
| server/src/tools/backend | 模块实现、接口与状态机制 / 分批3 | 0 |  | task:b901379dd3fe0361326412e8d455080a |
| server/src/tools/editors | 模块实现、接口与状态机制 | 0 |  | task:4fb3e75e9e1cbba537783b635e264691 |
| server/src/tools/entab | 模块实现、接口与状态机制 | 2 |  | task:22eb3561305fc52910d13cd9e3743092 |
| server/src/tools/findoidjoins | 连接路径与连接约束 | 1 |  | task:8f40bfe76bf917bc7183e977e3870b39 |
| server/src/tools/findoidjoins | 模块实现、接口与状态机制 | 0 |  | task:8f40bfe76bf917bc7183e977e3870b39 |
| server/src/tools/ifaddrs | 模块实现、接口与状态机制 | 1 |  | task:822b38951ca26ef016bc88eb915d7ad8 |
| server/src/tools/make_diff | 模块实现、接口与状态机制 | 0 |  | task:ca0374eb56907839a8902912a6644ae7 |
| server/src/tools/msvc | 配置注册与生效 | 0 |  | task:3dadf7cee0faa83fb2828e3e67b9e1a3 |
| server/src/tools/msvc | 模块实现、接口与状态机制 | 0 |  | task:3dadf7cee0faa83fb2828e3e67b9e1a3 |
| server/src/tools/pginclude | 模块实现、接口与状态机制 | 0 |  | task:64a96597be73aacf30d3afa5d41aa0ef |
| server/src/tools/pgindent | 模块实现、接口与状态机制 | 0 |  | task:8403b8f8013c4b5fa0e39497a305fce2 |
| server/src/gausskernel/optimizer/geqo | 总体入口、代价评估与构建 | 待核 | feature:9de1d11c1df26047a9d7a49ec7caa95c | task:38ad7ecb51cadb0091359cbb5c53b76a |
| server/src/gausskernel/optimizer/geqo | 种群、选择、随机与复制 | 待核 | feature:9de1d11c1df26047a9d7a49ec7caa95c | task:38ad7ecb51cadb0091359cbb5c53b76a |
| server/src/gausskernel/optimizer/geqo | 交叉、变异、重组与调试辅助 | 待核 | feature:9de1d11c1df26047a9d7a49ec7caa95c | task:38ad7ecb51cadb0091359cbb5c53b76a |

## 主干流程与公共机制

- B01 内存与资源寿命：server/src/common/backend/utils/mmgr、server/src/common/backend/utils/resowner、server/src/include/gtm、server/src/include/utils；任务 `task:7b8dfaafcba1f04932e3fa5759c306a7`
- B02 错误、异常与断言：server/src/common/backend/utils/error、server/src/include/bin、server/src/include/cm；任务 `task:3e4332cff542910b72d9e42690a4d3ca`
- B03 GUC与会话生效边界：server/src/common/backend/utils/misc、server/src/include/knl、server/src/include/utils；任务 `task:28f32bdb0efc8a4f9e0d3e71ff434489`
- B04 并发与等待协议：server/src/gausskernel/storage/ipc、server/src/gausskernel/storage/lmgr；任务 `task:260dc4a160d537e57dd7c187d25a96e2`
- B05 事务与可见性：server/src/common/backend/utils/time、server/src/gausskernel/storage/access/transam；任务 `task:58622faa48080f656325bc01f3116f48`
- B06 持久化与恢复：server/src/gausskernel/storage/access/redo、server/src/gausskernel/storage/access/transam；任务 `task:1c7571d75cc3fd7ffb80d6a530cbb82a`
- B07 系统目录与缓存：server/src/common/backend/catalog、server/src/common/backend/utils/cache；任务 `task:09356525981f2da00934e2c0a5246e01`
- B08 公共数据与SQL语义：server/src/common/backend/nodes、server/src/common/backend/utils/fmgr、server/src/include/datatype；任务 `task:29cf648b7dc49eafb7b572d1279efa7c`
- B09 构建、角色与接口：server/@root、server/cmake/src、server/contrib；任务 `task:3aba1d888922f0fc5860b5964480fe9e`
- B10 观测与字段血缘：server/contrib/pgstattuple、server/src/gausskernel/cbb/instruments；任务 `task:ca94a38e2f4601f3892e261052a77e8f`
- X01 查询主链：server/src/gausskernel/optimizer/plan、server/src/gausskernel/process/tcop、server/src/gausskernel/runtime/executor；任务 `task:4618c1c5cdc6aa06d4d0928e019eaa92`
- X02 DML与事务：server/src/gausskernel/runtime/executor、server/src/gausskernel/storage/access/heap、server/src/gausskernel/storage/access/transam；任务 `task:187c113b12bd7d4c7dfbe90562d0bbef`
- X03 DDL与缓存失效：server/src/common/backend/utils/cache、server/src/gausskernel/optimizer/commands；任务 `task:cbf338de12911036e83ca4c0f990387d`
- X04 索引读写与属性：server/src/gausskernel/optimizer/path、server/src/gausskernel/storage/access/index、server/src/gausskernel/storage/access/nbtree；任务 `task:3851e4489e878e756a2f19a0cae99638`
- X05 算子资源与取消：server/src/common/backend/utils/sort、server/src/gausskernel/runtime/executor；任务 `task:e6034a301549365a6128c2b593634400`
- X06 等待与事务终止：server/src/gausskernel/process/tcop、server/src/gausskernel/storage/lmgr；任务 `task:8d21b9bca3e9d5917b00cfd98665aa29`
- X07 WAL到恢复：server/src/gausskernel/storage/access/redo、server/src/gausskernel/storage/access/transam；任务 `task:ddf3c4edaefbd1996dbe38f9fed0202d`
- X08 备份、复制与角色：server/src/bin/pg_basebackup、server/src/gausskernel/storage/replication；任务 `task:5211d02851f6444bb7caa4fd7f67b9de`
- X09 解码与插件消费：server/contrib/mppdb_decoding、server/contrib/test_decoding、server/src/gausskernel/storage/replication；任务 `task:8babd777260ee0203c3ac1ba1458dd1c`
- X10 客户端与会话：server/src/common/backend/libpq、server/src/common/interfaces/libpq、server/src/common/interfaces/libpq/client_logic_cache；任务 `task:aa2f0b6ed66adb4922e2f88bd2419b0a`
- X11 工具与内核接口：server/src/bin/gs_loader、server/src/bin/pg_dump、server/src/bin/pg_probackup；任务 `task:983fe3a16f866227bd7d7c49a87cfb93`
- X12 可选引擎与扩展接入：server/contrib/adminpack、server/contrib/auth_delay、server/src/gausskernel/storage/cstore、server/src/gausskernel/storage/mot/core/concurrency_control；任务 `task:40c1c18f977140aee1209f93d8217562`

## 覆盖与输入状态

```json
{
  "schema": "curriculum-status/v1",
  "id": "curriculum:3f0bb2eb169c70af57516f8d847faf5c",
  "revision": "c3cb55852e744858e193f51a4c229b4f32e59ad80a36a3a0d0f782a1dc0f5ba6",
  "module": null,
  "modules": 537,
  "packages": 3668,
  "cpp_files": 2380,
  "unassigned_cpp": [],
  "unassigned_assets": [],
  "historical_feature_states": {
    "mapped": 1,
    "not_located": 3
  },
  "unresolved_feature_rows": 3,
  "implementation": {
    "enabled": true,
    "cpp_files": 2380,
    "cpp_files_explained": 0,
    "cpp_files_closed": 0,
    "items": 13845,
    "states": {
      "unreviewed": 13826,
      "open": 15,
      "explained_with_gaps": 4
    },
    "unclosed_items": 13845,
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
    ],
    "meaning": "evidence-backed region explanations; actual semantic review still required"
  },
  "mainline_tasks": 22,
  "planning_status": "candidate_plan_not_semantic_completion",
  "database_execution": "not_run"
}
```
