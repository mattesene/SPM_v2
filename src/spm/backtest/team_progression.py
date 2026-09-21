"""Leakage-safe historical backtest of the SPM same-team draw progression."""
from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass
from datetime import date

from spm.data.models import Match
from spm.data.normalization import canonical_team_name
from spm.data.season import Season
from spm.statistics.engine import SPMEngine, SPMScore


@dataclass(frozen=True, slots=True)
class TeamProgressionObservation:
    date: date
    team: str
    opponent: str
    selected_probability: float
    streak_before: int
    actual_draw: bool
    stake_units: int


@dataclass(frozen=True, slots=True)
class TeamProgressionReport:
    observations: tuple[TeamProgressionObservation, ...]
    teams_selected: int
    series_started: int
    series_completed: int
    draws: int
    non_draws: int
    max_streak: int
    max_stake_units: int
    max_capital_units: int
    busts: int
    profit_units: float | None = None
    total_staked_units: float | None = None
    max_drawdown_units: float | None = None
    draw_odds: float | None = None

    @property
    def bets(self) -> int:
        return len(self.observations)

    @property
    def hit_rate(self) -> float:
        return self.draws / self.bets if self.bets else 0.0

    @property
    def completion_rate(self) -> float:
        return self.series_completed / self.series_started if self.series_started else 0.0

    @property
    def roi(self) -> float | None:
        if self.total_staked_units in (None, 0):
            return None
        return self.profit_units / self.total_staked_units


def _team_and_opponent(match: Match, selected_team: str) -> tuple[str, str]:
    canonical = canonical_team_name(selected_team)
    if canonical_team_name(match.home_team) == canonical:
        return match.home_team, match.away_team
    return match.away_team, match.home_team


def evaluate_odds_sensitivity(
    observations: Iterable[TeamProgressionObservation],
    odds_values: Iterable[float],
) -> dict[float, dict[str, float | None]]:
    """Evaluate fixed-odds economics without rerunning the selection model.

    This is sensitivity analysis, not historical-odds performance: decisions
    and stakes stay unchanged and only the settlement price is varied.
    """
    normalized_odds = tuple(float(odds) for odds in odds_values)
    if any(odds <= 1.0 for odds in normalized_odds):
        raise ValueError("all odds values must be greater than 1.0")

    rows = tuple(observations)
    fixtures: dict[tuple[date, tuple[str, str]], list[TeamProgressionObservation]] = {}
    for row in rows:
        teams = tuple(sorted((canonical_team_name(row.team), canonical_team_name(row.opponent))))
        fixtures.setdefault((row.date, teams), []).append(row)

    ordered_fixtures = [fixtures[key] for key in sorted(fixtures)]
    results: dict[float, dict[str, float | None]] = {}
    for odds in normalized_odds:
        profit = 0.0
        staked = 0.0
        peak = 0.0
        max_drawdown = 0.0
        for fixture in ordered_fixtures:
            fixture_profit = 0.0
            fixture_staked = 0.0
            for row in fixture:
                fixture_staked += row.stake_units
                fixture_profit += (
                    row.stake_units * (odds - 1.0)
                    if row.actual_draw
                    else -row.stake_units
                )
            staked += fixture_staked
            profit += fixture_profit
            peak = max(peak, profit)
            max_drawdown = max(max_drawdown, peak - profit)
        results[odds] = {
            "profit_units": profit,
            "total_staked_units": staked,
            "roi": profit / staked if staked else None,
            "max_drawdown_units": max_drawdown,
        }
    return results

def build_progression_stress(
    observations: Iterable[TeamProgressionObservation],
) -> dict[str, object]:
    """Summarize observed progression depth and capital stress.

    Capital for a single series includes the next doubled stake after each
    non-draw, matching the backtest's committed-capital convention.
    """
    rows = tuple(observations)
    series_capital: dict[str, int] = {}
    observed_max_streak = 0
    observed_max_stake = 0
    observed_max_series_capital = 0
    streak_counts: dict[str, int] = {}
    max_streak_examples: list[dict[str, object]] = []

    for row in rows:
        team = canonical_team_name(row.team)
        if row.streak_before == 0 or team not in series_capital:
            series_capital[team] = row.stake_units

        if not row.actual_draw:
            series_capital[team] += row.stake_units * 2

        observed_max_streak = max(observed_max_streak, row.streak_before)
        observed_max_stake = max(observed_max_stake, row.stake_units)
        observed_max_series_capital = max(
            observed_max_series_capital, series_capital[team]
        )

        key = str(row.streak_before)
        streak_counts[key] = streak_counts.get(key, 0) + 1

        if row.streak_before == observed_max_streak:
            max_streak_examples.append({
                "date": row.date.isoformat(),
                "team": team,
                "opponent": canonical_team_name(row.opponent),
                "streak_before": row.streak_before,
                "stake_units": row.stake_units,
            })

    max_streak_examples = [
        item for item in max_streak_examples
        if item["streak_before"] == observed_max_streak
    ][:20]

    theoretical = {
        str(streak): (2 ** (streak + 1)) - 1
        for streak in range(observed_max_streak + 1)
    }
    return {
        "observed_max_streak": observed_max_streak,
        "observed_max_stake_units": observed_max_stake,
        "observed_max_series_capital_units": observed_max_series_capital,
        "streak_observation_counts": streak_counts,
        "theoretical_capital_by_streak": theoretical,
        "max_streak_examples": max_streak_examples,
    }



def build_progression_stress_breakdown(
    dataset_observations: Iterable[
        tuple[str, Iterable[TeamProgressionObservation]]
    ],
) -> dict[str, object]:
    """Build dataset- and team-scoped progression stress diagnostics.

    Dataset boundaries are preserved so identical team names from different
    leagues/seasons cannot share progression state. Team rows are keyed by
    dataset plus canonical team name.
    """
    dataset_rows: list[dict[str, object]] = []
    team_rows: list[dict[str, object]] = []
    global_streak_counts: dict[str, int] = {}
    global_max_streak = 0
    global_max_stake = 0
    global_max_series_capital = 0

    for dataset, raw_observations in dataset_observations:
        rows = tuple(raw_observations)
        stress = build_progression_stress(rows)
        dataset_rows.append({"dataset": dataset, **stress})

        global_max_streak = max(global_max_streak, int(stress["observed_max_streak"]))
        global_max_stake = max(global_max_stake, int(stress["observed_max_stake_units"]))
        global_max_series_capital = max(
            global_max_series_capital,
            int(stress["observed_max_series_capital_units"]),
        )
        for key, count in stress["streak_observation_counts"].items():
            global_streak_counts[key] = global_streak_counts.get(key, 0) + count

        teams: dict[str, list[TeamProgressionObservation]] = {}
        for row in rows:
            team = canonical_team_name(row.team)
            teams.setdefault(team, []).append(row)
        for team, team_observations in sorted(teams.items()):
            team_stress = build_progression_stress(team_observations)
            team_rows.append({
                "dataset": dataset,
                "team": team,
                **team_stress,
            })

    dataset_rows.sort(
        key=lambda row: (
            -int(row["observed_max_streak"]),
            -int(row["observed_max_series_capital_units"]),
            str(row["dataset"]),
        )
    )
    team_rows.sort(
        key=lambda row: (
            -int(row["observed_max_streak"]),
            -int(row["observed_max_series_capital_units"]),
            str(row["dataset"]),
            str(row["team"]),
        )
    )
    return {
        "observed_max_streak": global_max_streak,
        "observed_max_stake_units": global_max_stake,
        "observed_max_series_capital_units": global_max_series_capital,
        "streak_observation_counts": global_streak_counts,
        "by_dataset": dataset_rows,
        "by_team": team_rows,
    }


def aggregate_odds_sensitivity(
    sensitivity_reports: Iterable[dict[float, dict[str, float | None]]],
) -> dict[float, dict[str, float | None]]:
    """Aggregate fixed-odds sensitivity across independent datasets.

    Profit and stake are additive. Drawdown is kept dataset-scoped by taking
    the largest drawdown observed in any individual dataset; separate leagues
    and seasons are not treated as one chronological bankroll timeline.
    """
    reports = tuple(sensitivity_reports)
    odds_values = sorted({odds for report in reports for odds in report})
    aggregated: dict[float, dict[str, float | None]] = {}
    for odds in odds_values:
        rows = [report[odds] for report in reports if odds in report]
        profit = sum(row["profit_units"] or 0.0 for row in rows)
        staked = sum(row["total_staked_units"] or 0.0 for row in rows)
        drawdowns = [row["max_drawdown_units"] or 0.0 for row in rows]
        aggregated[odds] = {
            "profit_units": profit,
            "total_staked_units": staked,
            "roi": profit / staked if staked else None,
            "max_dataset_drawdown_units": max(drawdowns) if rows else None,
        }
    return aggregated


def aggregate_economic_reports(
    reports: Iterable[TeamProgressionReport],
) -> dict[str, float | int | None]:
    """Aggregate independent dataset economics without inventing one timeline.

    Profit and stake are additive across datasets. Drawdown and peak committed
    capital are *dataset maxima*, because separate leagues/seasons do not share
    a single chronological bankroll timeline in this runner.
    """
    items = tuple(reports)
    priced = [report for report in items if report.profit_units is not None]
    if not priced:
        return {
            "profit_units": None,
            "total_staked_units": None,
            "roi": None,
            "max_dataset_drawdown_units": None,
            "max_dataset_capital_units": None,
        }

    profit = sum(report.profit_units or 0.0 for report in priced)
    staked = sum(report.total_staked_units or 0.0 for report in priced)
    return {
        "profit_units": profit,
        "total_staked_units": staked,
        "roi": profit / staked if staked else None,
        "max_dataset_drawdown_units": max(
            report.max_drawdown_units or 0.0 for report in priced
        ),
        "max_dataset_capital_units": max(
            report.max_capital_units for report in priced
        ),
    }


def run_team_progression_backtest(
    matches: Iterable[Match],
    *,
    min_history: int = 5,
    top_n: int = 5,
    engine: SPMEngine | None = None,
    draw_odds: float | None = None,
) -> TeamProgressionReport:
    """Replay live team-first selection and same-team draw progression chronologically.

    Every date is scored only from matches strictly before that date. New
    progressions use the top ``top_n`` distinct teams whose own historical
    sample reaches ``min_history``; an active team is then followed at its
    next fixture even if it falls out of the daily top N.

    Capital is measured as the cumulative stake already committed to all open
    progressions. If both selected teams meet in the same fixture, both
    progressions settle from that single match outcome and each real stake is
    included in the economic result.

    If ``draw_odds`` is supplied, the report also calculates actual staking
    economics: cumulative net profit, total amount staked, ROI and maximum
    drawdown. Drawdown is updated once per fixture, so two progressions
    settling on the same match cannot create an artificial intra-fixture peak.
    No synthetic odds are assumed when it is omitted.
    """
    if min_history < 1 or top_n < 1:
        raise ValueError("min_history and top_n must be positive")
    if draw_odds is not None and draw_odds <= 1.0:
        raise ValueError("draw_odds must be greater than 1.0")

    ordered = sorted(matches, key=lambda m: (m.date, m.home_team, m.away_team))
    predictor = engine or SPMEngine()
    history: list[Match] = []
    active_stake: dict[str, int] = {}
    active_streak: dict[str, int] = {}
    active_probability: dict[str, float] = {}
    active_capital: dict[str, int] = {}
    observations: list[TeamProgressionObservation] = []
    teams_seen: set[str] = set()
    series_started = series_completed = draws = non_draws = 0
    max_streak = max_stake = max_capital = busts = 0
    profit_units = 0.0
    total_staked_units = 0.0
    peak_profit = 0.0
    max_drawdown = 0.0

    index = 0
    while index < len(ordered):
        current_date = ordered[index].date
        day_matches: list[Match] = []
        while index < len(ordered) and ordered[index].date == current_date:
            day_matches.append(ordered[index])
            index += 1

        season = Season(history)
        ready_teams = {
            canonical_team_name(team)
            for match in day_matches
            for team in (match.home_team, match.away_team)
            if season.team_stats(team).matches >= min_history
        }
        eligible_fixtures = [
            m for m in day_matches
            if canonical_team_name(m.home_team) in ready_teams
            or canonical_team_name(m.away_team) in ready_teams
        ]
        scored = predictor.rank(
            history,
            [(m.home_team, m.away_team) for m in eligible_fixtures],
            current_date,
            eligible_teams=ready_teams,
        )
        selected: dict[str, SPMScore] = {}
        for score in scored:
            team = canonical_team_name(score.selected_team)
            if team in selected:
                continue
            selected[team] = score
            if len(selected) >= top_n:
                break

        # Active progressions take precedence over a new daily selection.
        for match in day_matches:
            participants = {
                canonical_team_name(match.home_team),
                canonical_team_name(match.away_team),
            }
            active_today = participants.intersection(active_stake)
            new_today = participants.intersection(selected).difference(active_stake)
            teams_for_day = active_today | new_today

            for team in sorted(teams_for_day):
                if team not in active_stake:
                    score = selected[team]
                    active_stake[team] = 1
                    active_streak[team] = 0
                    active_probability[team] = float(score.team_probability)
                    active_capital[team] = 1
                    series_started += 1
                    teams_seen.add(team)

            if teams_for_day:
                max_capital = max(max_capital, sum(active_capital.values()))

            fixture_profit = 0.0
            fixture_staked = 0.0
            for team in sorted(teams_for_day):
                team_name, opponent = _team_and_opponent(match, team)
                stake = active_stake[team]
                streak = active_streak[team]
                is_draw = match.is_draw
                observations.append(TeamProgressionObservation(
                    current_date,
                    team_name,
                    opponent,
                    active_probability[team],
                    streak,
                    is_draw,
                    stake,
                ))
                max_stake = max(max_stake, stake)
                max_streak = max(max_streak, streak)
                if draw_odds is not None:
                    fixture_staked += stake
                    fixture_profit += stake * (draw_odds - 1.0) if is_draw else -stake
                if is_draw:
                    draws += 1
                    series_completed += 1
                    active_stake.pop(team, None)
                    active_streak.pop(team, None)
                    active_probability.pop(team, None)
                    active_capital.pop(team, None)
                else:
                    non_draws += 1
                    next_stake = stake * 2
                    active_stake[team] = next_stake
                    active_streak[team] = streak + 1
                    active_capital[team] += next_stake
                    max_capital = max(max_capital, sum(active_capital.values()))

            if draw_odds is not None and teams_for_day:
                total_staked_units += fixture_staked
                profit_units += fixture_profit
                peak_profit = max(peak_profit, profit_units)
                max_drawdown = max(max_drawdown, peak_profit - profit_units)

        history.extend(day_matches)

    return TeamProgressionReport(
        tuple(observations), len(teams_seen), series_started, series_completed,
        draws, non_draws, max_streak, max_stake, max_capital, busts,
        profit_units if draw_odds is not None else None,
        total_staked_units if draw_odds is not None else None,
        max_drawdown if draw_odds is not None else None,
        draw_odds,
    )
