"""Role-specific views of the *same* reviewed knowledge, never inferred facts.

Views refer to delivered units and expose their structured fields. A prose
claim is useful behavior evidence, but cannot manufacture a test oracle,
runtime observation, diagnostic action, or producer/consumer contract.
"""
from .store import canonical, require


ROLES = ('coding', 'test_generation', 'review', 'operations')
PRIORITY = {
    'coding': ('contract', 'mechanism', 'flow', 'claim', 'feature', 'test_obligation', 'requirement', 'observation'),
    'test_generation': ('test_obligation', 'requirement', 'contract', 'claim', 'flow', 'mechanism', 'observation'),
    'review': ('contract', 'flow', 'mechanism', 'test_obligation', 'claim', 'requirement', 'observation'),
    'operations': ('observation', 'mechanism', 'contract', 'flow', 'claim', 'requirement', 'test_obligation'),
}
REQUIRED = {
    'coding': ('behavior', 'conditions', 'implementation_evidence', 'interface_or_state', 'consumers'),
    'test_generation': ('behavior', 'test_oracle', 'test_dimensions', 'implementation_evidence'),
    'review': ('behavior', 'conditions', 'invariants', 'consumers', 'implementation_evidence'),
    'operations': ('conditions', 'observations', 'diagnostic_evidence', 'configuration', 'conditional_actions'),
}
LABELS = {
    'behavior': '实现行为与入口', 'conditions': '适用条件', 'implementation_evidence': '实现证据',
    'interface_or_state': '接口与状态约束', 'consumers': '消费者与影响', 'test_oracle': '测试预期依据',
    'test_dimensions': '输入、状态与边界维度', 'invariants': '评审不变量', 'observations': '症状与观测',
    'diagnostic_evidence': '诊断证据', 'configuration': '配置来源及生效边界', 'conditional_actions': '有条件处理依据',
}
# These are the actual unified-skill-profiles section names. An answered
# structured section can supply its stated view; an open checklist cannot.
TOPIC_SECTIONS = {
    'compatibility': {'inputs_and_binding': ('interface_or_state',), 'conditions_and_branches': ('conditions',),
                      'behavior_and_counterexamples': ('behavior', 'test_dimensions')},
    'memory': {'ownership_and_lifetime': ('interface_or_state', 'invariants'),
               'allocation_and_cleanup': ('interface_or_state',), 'accounting_and_growth': ('observations',)},
    'waits': {'state_lifecycle': ('interface_or_state',), 'timing_and_scope': ('observations',),
              'cancellation_and_observation': ('observations',)},
    'views': {'definition_and_lineage': ('interface_or_state',), 'visibility_and_consistency': ('invariants',),
              'field_semantics': ('observations',)},
    'tools': {'options_and_stages': ('configuration', 'interface_or_state'),
              'consistency_and_dependencies': ('consumers', 'invariants')},
    'decoding': {'transaction_and_snapshot': ('interface_or_state',),
                 'positions_and_confirmation': ('interface_or_state',), 'resources_and_restart': ('invariants',)},
    'guc': {'parameter_definition': ('configuration',), 'precedence_and_effective_time': ('configuration',),
            'consumers_and_observation': ('consumers', 'observations')},
}


def priority(role, kind):
    order = PRIORITY.get(role, PRIORITY['coding'])
    return order.index(kind) if kind in order else len(order)


def rank_bonus(role, unit):
    if role not in ROLES:
        return 0
    # Small tie-breaker: role relevance never turns an unrelated unit into a hit.
    bonus = max(0, 0.35 - priority(role, unit['kind']) * 0.04)
    if role == 'operations' and (unit.get('operations') or set(unit.get('topic_extensions', {})) & {'errors', 'guc', 'waits', 'views', 'tools', 'decoding'}):
        bonus += 0.4
    return bonus


def _bounded(value, maximum=900):
    """Keep a whole structured value, or leave an explicit expansion reference."""
    if len(canonical(value).encode('utf8')) <= maximum:
        return value
    return {'omitted_for_budget': True, 'expand_with': 'reference_knowledge'}


def _sections(unit, evidence_kinds):
    sections = {}
    def add(name, field, value):
        if value not in (None, [], {}, ''):
            sections.setdefault(name, []).append({'unit': unit['id'], 'field': field, 'value': _bounded(value)})
    kind = unit['kind']
    if kind in {'claim', 'mechanism', 'contract', 'requirement', 'flow', 'feature', 'observation'} and (unit.get('statement') or unit.get('body')):
        # Body already lives in the normal ContextPack; references avoid repetition.
        add('behavior', 'statement' if unit.get('statement') else 'body', unit.get('statement') or {'read_from': 'delivered_unit.body'})
    add('conditions', 'conditions', unit.get('conditions'))
    implementation_refs = [ref for ref in unit.get('source_refs', []) if evidence_kinds.get(ref) == 'source']
    add('implementation_evidence', 'source_refs', implementation_refs)
    if kind == 'contract':
        add('interface_or_state', 'requires/ensures', {k: unit[k] for k in ('requires', 'ensures') if unit.get(k)})
        add('invariants', 'invariants', unit.get('invariants'))
        add('consumers', 'producers/consumers', {k: unit[k] for k in ('producers', 'consumers') if unit.get(k)})
    if kind == 'flow':
        add('interface_or_state', 'steps', unit.get('steps'))
    if kind == 'test_obligation':
        add('test_oracle', 'expected_from', unit.get('expected_from'))
        add('test_dimensions', 'conditions', unit.get('conditions'))
        add('test_dimensions', 'cases', unit.get('cases'))
    add('test_dimensions', 'counterexamples', unit.get('counterexamples'))
    for field in ('state', 'state_transitions', 'resource_lifecycle', 'interfaces'):
        add('interface_or_state', field, unit.get(field))
    if kind!='contract' and implementation_refs:
        # Text/source-backed consumers remain useful without compiler symbols.
        # This does not upgrade them to a compiler-bound contract/call edge.
        for field in ('consumers','affected_modules'):
            add('consumers',field,unit.get(field))
    add('invariants', 'invariants', unit.get('invariants'))
    for link in unit.get('knowledge_refs', []):
        if link.get('relation') in {'CONSUMES', 'PRODUCES', 'DEPENDS_ON', 'AFFECTS'}:
            add('consumers', 'knowledge_refs', link)
    ops = unit.get('operations', {})
    if isinstance(ops, dict):
        for concept, fields in {
            'observations': ('symptoms', 'observations', 'metrics'),
            'diagnostic_evidence': ('diagnostics', 'evidence', 'queries'),
            'configuration': ('configuration', 'parameters', 'activation'),
            'conditional_actions': ('actions', 'remedies', 'recovery'),
        }.items():
            for field in fields:
                add(concept, 'operations.' + field, ops.get(field))
    if kind == 'observation':
        add('observations', 'observation', unit.get('observation') or {'read_from': 'delivered_unit.body'})
    for topic, extension in unit.get('topic_extensions', {}).items():
        if not isinstance(extension, dict):
            continue
        details = extension.get('details', {})
        if not isinstance(details, dict):
            continue
        answered = {row.get('check') for row in extension.get('coverage', [])
                    if isinstance(row, dict) and row.get('status') == 'answered'}
        for key, value in details.items():
            if key not in answered:
                continue
            field = 'topic_extensions.' + topic + '.details.' + key
            for concept in TOPIC_SECTIONS.get(topic, {}).get(key, ()):
                add(concept, field, value)
            # Diagnosis/action sections can contain one side only. Preserve the
            # actual named subfields instead of inventing the other half from
            # a combined checklist heading.
            stack = [(field, value)]
            while stack:
                path, part = stack.pop()
                if isinstance(part, list):
                    stack.extend((path + '[' + str(i) + ']', item) for i, item in enumerate(part))
                elif isinstance(part, dict):
                    for name, item in part.items():
                        subfield = path + '.' + name
                        for concept, keys in {
                            'observations': {'symptoms', 'observations', 'metrics'},
                            'diagnostic_evidence': {'diagnostics', 'queries', 'evidence_collection', 'collection'},
                            'configuration': {'configuration', 'parameters', 'activation'},
                            'conditional_actions': {'actions', 'remedies', 'recovery', 'conditional_actions'},
                        }.items():
                            if name in keys:
                                add(concept, subfield, item)
                        stack.append((subfield, item))
    return sections


def compose(pack, units, role, *, evidence_kinds=None):
    """Build a compact view only from units actually delivered in ``pack``."""
    require(role in ROLES, 'Unknown context role')
    evidence_kinds = evidence_kinds or {}
    visible = {r['id']: r for key in ('constraints', 'paths', 'test_obligations') for r in pack.get(key, [])}
    delivered = {uid for uid in visible if units.get(uid) is not None}
    sections = {}
    truncated = False
    for uid in sorted(delivered, key=lambda uid: (priority(role, units[uid]['kind']), uid)):
        unit = {**units[uid], 'body': visible[uid].get('body', '')}
        for concept, rows in _sections(unit, evidence_kinds).items():
            if concept not in REQUIRED[role]:
                continue
            chosen = sections.setdefault(concept, [])
            for row in rows:
                if isinstance(row['value'], dict) and row['value'].get('omitted_for_budget'):
                    truncated = True
                    continue
                if row not in chosen and len(chosen) < 4:
                    chosen.append(row)
                elif row not in chosen:
                    truncated = True
    missing = [name for name in REQUIRED[role] if not sections.get(name)]
    return {'schema': 'role-context/v1', 'role': role,
            'required': list(REQUIRED[role]), 'sections': sections,
            'missing_required': missing,
            'missing_explanations': [{'requirement': name, 'meaning': LABELS[name],
                                      'next': 'Research or retrieve cited knowledge.'}
                                     for name in missing],
            'status': 'partial' if missing or truncated else 'complete',
            'truncated': truncated, 'knowledge_ids': sorted(delivered),
            'runtime_validation': 'not_run'}
