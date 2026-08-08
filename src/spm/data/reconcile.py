"""Reconcile records from multiple providers without duplicating matches."""
from collections import defaultdict
from dataclasses import replace

from .normalized import MatchRecord


def reconcile(records: list[MatchRecord]) -> list[MatchRecord]:
    """Merge records sharing the same normalized fixture identity.

    Completed scores win over missing scores; conflicting completed scores are
    rejected instead of silently selecting one provider. Provenance is merged.
    """
    groups: dict[tuple, list[MatchRecord]] = defaultdict(list)
    for record in records:
        groups[record.identity_key].append(record)

    result: list[MatchRecord] = []
    for key, group in groups.items():
        completed = {(r.home_goals, r.away_goals) for r in group if r.completed}
        if len(completed) > 1:
            raise ValueError(f"Conflicting scores for {key}: {sorted(completed)}")
        scored = next(iter(completed), (None, None))
        base = max(group, key=lambda r: (r.completed, r.source_count))
        provenance = []
        seen = set()
        for record in group:
            for source in record.provenance:
                identity = (source.source, source.source_id)
                if identity not in seen:
                    seen.add(identity)
                    provenance.append(source)
        result.append(replace(base, home_goals=scored[0], away_goals=scored[1], provenance=tuple(provenance)))
    return sorted(result, key=lambda r: (r.date, r.canonical_home_team, r.canonical_away_team))
