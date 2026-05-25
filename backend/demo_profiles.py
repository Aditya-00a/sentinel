"""
8 curated player trajectory profiles, each illustrating a different
behavioral health pattern and intervention scenario.

Unlike traditional report-review demos, these profiles contain multi-session
trajectory data — behavioral health scores over time, showing the arc of a
player's community experience, not just a snapshot.
"""

import random
import time


def _ts(days_ago: int) -> int:
    return int((time.time() - days_ago * 86400) * 1000)


def _session(date: str, time_of_day: str, matches: int, health: float,
             reports_recv: int = 0, honor_recv: int = 0,
             surrender_yes: int = 0, surrender_total: int = 0,
             chat_flags: list[str] | None = None,
             avg_kda: float = 2.5, cs_per_min: float = 7.0,
             champions: list[str] | None = None,
             headshot_pct: float = 0.0, agents: list[str] | None = None):
    return {
        "date": date,
        "time_of_day": time_of_day,
        "matches_played": matches,
        "behavioral_health": round(health, 2),
        "reports_received": reports_recv,
        "honor_received": honor_recv,
        "surrender_votes_yes": surrender_yes,
        "surrender_votes_total": surrender_total,
        "chat_flags": chat_flags or [],
        "avg_kda": avg_kda,
        "cs_per_min": cs_per_min,
        "champions_played": champions or [],
        "headshot_pct": headshot_pct,
        "agents_played": agents or [],
    }


DEMO_PROFILES = {
    "steady-decline": {
        "id": "steady-decline",
        "name": "Steady Decline",
        "description": "3-week progressive tilt. KDA dropping, chat flags rising, champion pool narrowing.",
        "expected_decision": "MONITOR",
        "game": "lol",
        "riot_id": "FadingVet#NA1",
        "region": "americas",
        "platform": "na1",
        "account": {
            "puuid": "demo-decline-puuid",
            "gameName": "FadingVet",
            "tagLine": "NA1",
            "summonerLevel": 312,
        },
        "rank": {"tier": "PLATINUM", "rank": "II", "leaguePoints": 45, "wins": 280, "losses": 270},
        "account_age_days": 1200,
        "sessions": [
            _session("2026-05-03", "evening",  3, 0.88, 0, 2, 0, 0, [], 3.8, 7.5, ["Garen", "Darius", "Sett"]),
            _session("2026-05-05", "evening",  4, 0.85, 0, 1, 0, 1, [], 3.5, 7.2, ["Garen", "Darius"]),
            _session("2026-05-07", "evening",  3, 0.82, 0, 1, 0, 0, [], 3.2, 7.0, ["Garen", "Darius"]),
            _session("2026-05-09", "night",    5, 0.74, 1, 0, 1, 2, ["team diff"], 2.6, 6.5, ["Garen"]),
            _session("2026-05-11", "evening",  3, 0.70, 1, 0, 1, 1, [], 2.4, 6.3, ["Garen"]),
            _session("2026-05-13", "night",    6, 0.62, 2, 0, 2, 3, ["ff15", "jg diff"], 2.0, 5.8, ["Garen"]),
            _session("2026-05-15", "night",    4, 0.55, 1, 0, 2, 2, ["open mid"], 1.8, 5.5, ["Garen"]),
            _session("2026-05-17", "night",    5, 0.48, 2, 0, 3, 3, ["trash team", "ff"], 1.5, 5.0, ["Garen"]),
            _session("2026-05-19", "night",    7, 0.40, 3, 0, 4, 4, ["report jg", "team diff", "uninstall"], 1.2, 4.5, ["Garen"]),
            _session("2026-05-21", "night",    4, 0.35, 2, 0, 3, 3, ["im done", "ff15"], 1.0, 4.2, ["Garen"]),
        ],
        "trajectory": {
            "direction": "declining",
            "velocity": 0.055,
            "current_health": 0.35,
            "predicted_health_3_sessions": 0.18,
            "baseline_health": 0.86,
            "tilt_trigger": "Consecutive ranked losses triggering progressive tilt",
        },
        "intervention_history": [],
        "report_count": 12,
        "honor_level": 2,
    },

    "promo-tilt": {
        "id": "promo-tilt",
        "name": "Promo Tilt",
        "description": "Diamond player. Stable normally, spirals hard after failed promos.",
        "expected_decision": "NUDGE",
        "game": "lol",
        "riot_id": "AlmostDia#TILT",
        "region": "americas",
        "platform": "na1",
        "account": {
            "puuid": "demo-promo-puuid",
            "gameName": "AlmostDia",
            "tagLine": "TILT",
            "summonerLevel": 245,
        },
        "rank": {"tier": "PLATINUM", "rank": "I", "leaguePoints": 85, "wins": 220, "losses": 210},
        "account_age_days": 900,
        "sessions": [
            _session("2026-05-05", "afternoon", 3, 0.90, 0, 3, 0, 0, [], 4.2, 8.0, ["Ahri", "Syndra", "Orianna"]),
            _session("2026-05-07", "afternoon", 2, 0.92, 0, 2, 0, 0, [], 4.5, 8.2, ["Ahri", "Syndra"]),
            _session("2026-05-09", "afternoon", 3, 0.88, 0, 2, 0, 0, [], 4.0, 7.8, ["Ahri", "Syndra", "Viktor"]),
            _session("2026-05-11", "afternoon", 2, 0.91, 0, 3, 0, 0, [], 4.8, 8.5, ["Ahri"]),
            # Promo series begins
            _session("2026-05-13", "evening",   5, 0.85, 0, 1, 0, 1, [], 3.5, 7.5, ["Ahri", "Syndra"]),
            # Promo failed — game 5 loss
            _session("2026-05-13", "night",     3, 0.45, 2, 0, 2, 2, ["ff", "team gap", "boosted"], 1.2, 5.0, ["Ahri"]),
            _session("2026-05-14", "night",     5, 0.32, 3, 0, 3, 3, ["dog team", "ff15", "open", "report bot"], 0.8, 4.0, ["Ahri"]),
            _session("2026-05-15", "afternoon", 2, 0.55, 0, 0, 0, 1, [], 2.5, 6.5, ["Ahri"]),
            _session("2026-05-17", "afternoon", 3, 0.68, 0, 1, 0, 0, [], 3.2, 7.0, ["Ahri", "Syndra"]),
            _session("2026-05-19", "afternoon", 2, 0.78, 0, 2, 0, 0, [], 3.8, 7.5, ["Ahri", "Syndra"]),
        ],
        "trajectory": {
            "direction": "recovering",
            "velocity": 0.03,
            "current_health": 0.78,
            "predicted_health_3_sessions": 0.85,
            "baseline_health": 0.90,
            "tilt_trigger": "Failed Diamond promos (2-3 in game 5)",
        },
        "intervention_history": [],
        "report_count": 5,
        "honor_level": 3,
    },

    "night-tilter": {
        "id": "night-tilter",
        "name": "Night Tilter",
        "description": "Fine during daytime. Toxic in late-night sessions. Time-of-day pattern.",
        "expected_decision": "ADJUST",
        "game": "valorant",
        "riot_id": "NightOwl#LATE",
        "region": "americas",
        "platform": "na1",
        "account": {
            "puuid": "demo-night-puuid",
            "gameName": "NightOwl",
            "tagLine": "LATE",
            "summonerLevel": 1,
        },
        "rank": {"tier": "DIAMOND", "rank": "II", "leaguePoints": 55, "wins": 180, "losses": 170},
        "account_age_days": 600,
        "sessions": [
            _session("2026-05-04", "afternoon", 3, 0.88, 0, 2, 0, 0, [], headshot_pct=0.28, agents=["Jett", "Reyna"]),
            _session("2026-05-04", "night",     4, 0.42, 2, 0, 0, 0, ["trash", "uninstall"], headshot_pct=0.18, agents=["Jett"]),
            _session("2026-05-06", "morning",   2, 0.90, 0, 2, 0, 0, [], headshot_pct=0.30, agents=["Jett", "Sage"]),
            _session("2026-05-07", "night",     5, 0.38, 3, 0, 0, 0, ["bot lobby", "report sage", "im carrying"], headshot_pct=0.15, agents=["Jett"]),
            _session("2026-05-09", "afternoon", 3, 0.85, 0, 1, 0, 0, [], headshot_pct=0.27, agents=["Jett", "Reyna"]),
            _session("2026-05-10", "night",     6, 0.35, 4, 0, 0, 0, ["dog team", "diff", "ff", "report"], headshot_pct=0.14, agents=["Jett"]),
            _session("2026-05-12", "afternoon", 2, 0.87, 0, 2, 0, 0, [], headshot_pct=0.29, agents=["Jett", "Omen"]),
            _session("2026-05-13", "night",     4, 0.40, 2, 0, 0, 0, ["trash", "gg go next"], headshot_pct=0.16, agents=["Jett"]),
            _session("2026-05-15", "morning",   3, 0.89, 0, 3, 0, 0, [], headshot_pct=0.31, agents=["Jett", "Reyna"]),
            _session("2026-05-16", "night",     5, 0.33, 3, 0, 0, 0, ["report team", "braindead", "ff"], headshot_pct=0.13, agents=["Jett"]),
        ],
        "trajectory": {
            "direction": "stable",
            "velocity": 0.0,
            "current_health": 0.60,
            "predicted_health_3_sessions": 0.58,
            "baseline_health": 0.88,
            "tilt_trigger": "Late-night play sessions (after 11 PM) consistently correlate with behavioral decline",
        },
        "intervention_history": [],
        "report_count": 14,
        "honor_level": 2,
    },

    "duo-dependent": {
        "id": "duo-dependent",
        "name": "Duo Dependent",
        "description": "Great teammate when duo'd. Progressively toxic when solo.",
        "expected_decision": "NUDGE",
        "game": "lol",
        "riot_id": "SoloBad#DUO",
        "region": "americas",
        "platform": "na1",
        "account": {
            "puuid": "demo-duo-puuid",
            "gameName": "SoloBad",
            "tagLine": "DUO",
            "summonerLevel": 178,
        },
        "rank": {"tier": "GOLD", "rank": "I", "leaguePoints": 60, "wins": 190, "losses": 185},
        "account_age_days": 800,
        "sessions": [
            _session("2026-05-03", "evening",  3, 0.92, 0, 3, 0, 0, [], 4.0, 7.5, ["Jinx", "Caitlyn"]),  # duo
            _session("2026-05-05", "evening",  4, 0.52, 2, 0, 1, 2, ["supp diff", "no peel"], 1.8, 6.0, ["Jinx"]),  # solo
            _session("2026-05-07", "evening",  3, 0.90, 0, 2, 0, 0, [], 3.8, 7.2, ["Jinx", "Caitlyn"]),  # duo
            _session("2026-05-09", "evening",  5, 0.48, 3, 0, 2, 3, ["report supp", "0 vision", "afk farm"], 1.5, 5.8, ["Jinx"]),  # solo
            _session("2026-05-11", "evening",  2, 0.93, 0, 3, 0, 0, [], 4.2, 7.8, ["Jinx", "Caitlyn"]),  # duo
            _session("2026-05-13", "evening",  4, 0.45, 2, 0, 2, 2, ["trash supp", "im done", "open bot"], 1.2, 5.5, ["Jinx"]),  # solo
            _session("2026-05-15", "evening",  3, 0.91, 0, 3, 0, 0, [], 3.9, 7.4, ["Jinx", "Caitlyn"]),  # duo
            _session("2026-05-17", "evening",  5, 0.42, 3, 0, 3, 3, ["never peel", "supp gap", "ff15"], 1.3, 5.2, ["Jinx"]),  # solo
            _session("2026-05-19", "evening",  2, 0.94, 0, 2, 0, 0, [], 4.5, 8.0, ["Jinx", "Caitlyn"]),  # duo
            _session("2026-05-21", "evening",  4, 0.40, 3, 0, 2, 3, ["worst supp ever", "ff", "report"], 1.1, 5.0, ["Jinx"]),  # solo
        ],
        "trajectory": {
            "direction": "stable",
            "velocity": 0.0,
            "current_health": 0.65,
            "predicted_health_3_sessions": 0.62,
            "baseline_health": 0.92,
            "tilt_trigger": "Solo queue without regular duo partner triggers support-lane frustration spiral",
        },
        "duo_sessions": [0, 2, 4, 6, 8],
        "solo_sessions": [1, 3, 5, 7, 9],
        "intervention_history": [],
        "report_count": 13,
        "honor_level": 2,
    },

    "comeback-kid": {
        "id": "comeback-kid",
        "name": "Comeback Kid",
        "description": "Was declining. Received cooldown nudge. Behavior recovered. Intervention success.",
        "expected_decision": "NO_ACTION",
        "game": "valorant",
        "riot_id": "Reformed#GG",
        "region": "americas",
        "platform": "na1",
        "account": {
            "puuid": "demo-comeback-puuid",
            "gameName": "Reformed",
            "tagLine": "GG",
            "summonerLevel": 1,
        },
        "rank": {"tier": "PLATINUM", "rank": "III", "leaguePoints": 40, "wins": 150, "losses": 145},
        "account_age_days": 500,
        "sessions": [
            _session("2026-04-28", "evening", 3, 0.80, 0, 1, 0, 0, [], headshot_pct=0.26, agents=["Omen", "Sage"]),
            _session("2026-04-30", "evening", 4, 0.65, 1, 0, 0, 0, ["diff"], headshot_pct=0.22, agents=["Omen"]),
            _session("2026-05-02", "night",   5, 0.45, 2, 0, 0, 0, ["trash", "ff"], headshot_pct=0.18, agents=["Omen"]),
            _session("2026-05-04", "night",   6, 0.30, 4, 0, 0, 0, ["report", "dog team", "im done", "afk"], headshot_pct=0.14, agents=["Omen"]),
            # ← Intervention: cooldown suggestion + "take a break" nudge
            _session("2026-05-06", "afternoon", 0, 1.0, 0, 0, 0, 0, []),  # Didn't play — took the break
            _session("2026-05-08", "afternoon", 2, 0.60, 0, 1, 0, 0, [], headshot_pct=0.24, agents=["Omen", "Sage"]),
            _session("2026-05-10", "evening",   3, 0.72, 0, 2, 0, 0, [], headshot_pct=0.26, agents=["Omen", "Sage"]),
            _session("2026-05-12", "evening",   3, 0.80, 0, 2, 0, 0, [], headshot_pct=0.27, agents=["Omen", "Sage", "Killjoy"]),
            _session("2026-05-14", "evening",   2, 0.85, 0, 3, 0, 0, [], headshot_pct=0.28, agents=["Omen", "Sage"]),
            _session("2026-05-16", "evening",   3, 0.88, 0, 3, 0, 0, [], headshot_pct=0.29, agents=["Omen", "Sage", "Killjoy"]),
        ],
        "trajectory": {
            "direction": "recovering",
            "velocity": -0.04,
            "current_health": 0.88,
            "predicted_health_3_sessions": 0.90,
            "baseline_health": 0.82,
            "tilt_trigger": "Loss streak resolved after cooldown intervention",
        },
        "intervention_history": [
            {"date": "2026-05-05", "type": "NUDGE", "action": "Cooldown suggestion after 4-game loss streak",
             "outcome": "Player took 2-day break, behavior recovered to baseline within 1 week"},
        ],
        "report_count": 7,
        "honor_level": 3,
    },

    "false-alarm": {
        "id": "false-alarm",
        "name": "False Alarm",
        "description": "Stats look like decline. Actually just learning a new role. Context exonerates.",
        "expected_decision": "NO_ACTION",
        "game": "lol",
        "riot_id": "NewRole#MID",
        "region": "europe",
        "platform": "euw1",
        "account": {
            "puuid": "demo-false-puuid",
            "gameName": "NewRole",
            "tagLine": "MID",
            "summonerLevel": 267,
        },
        "rank": {"tier": "DIAMOND", "rank": "III", "leaguePoints": 20, "wins": 300, "losses": 290},
        "account_age_days": 1400,
        "sessions": [
            _session("2026-05-01", "afternoon", 3, 0.90, 0, 2, 0, 0, [], 4.5, 8.5, ["Syndra", "Orianna", "Viktor"]),
            _session("2026-05-03", "afternoon", 3, 0.88, 0, 2, 0, 0, [], 4.2, 8.2, ["Syndra", "Orianna"]),
            # Role swap begins — mid to jungle
            _session("2026-05-05", "afternoon", 3, 0.72, 1, 0, 0, 1, [], 1.8, 4.5, ["Viego", "Lee Sin"]),
            _session("2026-05-07", "afternoon", 4, 0.65, 1, 0, 0, 1, [], 1.5, 4.0, ["Viego", "Lee Sin", "Graves"]),
            _session("2026-05-09", "afternoon", 3, 0.60, 1, 0, 0, 0, [], 1.6, 4.2, ["Viego", "Graves"]),
            _session("2026-05-11", "afternoon", 3, 0.62, 0, 1, 0, 0, [], 2.0, 4.8, ["Viego", "Graves"]),
            _session("2026-05-13", "afternoon", 4, 0.68, 0, 1, 0, 0, [], 2.5, 5.2, ["Viego", "Graves"]),
            _session("2026-05-15", "afternoon", 3, 0.72, 0, 1, 0, 0, [], 2.8, 5.5, ["Viego", "Graves", "Lee Sin"]),
            _session("2026-05-17", "afternoon", 3, 0.78, 0, 2, 0, 0, [], 3.0, 5.8, ["Viego", "Graves"]),
            _session("2026-05-19", "afternoon", 2, 0.82, 0, 2, 0, 0, [], 3.2, 6.0, ["Viego", "Graves"]),
        ],
        "trajectory": {
            "direction": "recovering",
            "velocity": -0.02,
            "current_health": 0.82,
            "predicted_health_3_sessions": 0.86,
            "baseline_health": 0.89,
            "tilt_trigger": "No tilt detected — performance dip consistent with role swap learning curve",
        },
        "role_swap_detected": {"from": "MID", "to": "JUNGLE", "started": "2026-05-05"},
        "intervention_history": [],
        "report_count": 3,
        "honor_level": 4,
    },

    "slow-burn": {
        "id": "slow-burn",
        "name": "Slow Burn Griefing",
        "description": "Never triggers chat detection. Subtly suboptimal play over 50+ games. Pattern clear in aggregate.",
        "expected_decision": "MONITOR",
        "game": "lol",
        "riot_id": "Subtle#INT",
        "region": "americas",
        "platform": "na1",
        "account": {
            "puuid": "demo-slowburn-puuid",
            "gameName": "Subtle",
            "tagLine": "INT",
            "summonerLevel": 195,
        },
        "rank": {"tier": "GOLD", "rank": "III", "leaguePoints": 15, "wins": 160, "losses": 175},
        "account_age_days": 700,
        "sessions": [
            _session("2026-05-01", "evening", 4, 0.70, 0, 0, 0, 0, [], 1.8, 5.5, ["Singed", "Teemo"]),
            _session("2026-05-03", "evening", 3, 0.68, 0, 0, 0, 0, [], 1.6, 5.2, ["Singed"]),
            _session("2026-05-05", "evening", 5, 0.65, 1, 0, 0, 1, [], 1.4, 4.8, ["Singed", "Nunu"]),
            _session("2026-05-07", "evening", 3, 0.62, 0, 0, 1, 1, [], 1.5, 5.0, ["Singed"]),
            _session("2026-05-09", "evening", 4, 0.58, 1, 0, 0, 0, [], 1.3, 4.5, ["Singed", "Yuumi"]),
            _session("2026-05-11", "evening", 3, 0.55, 1, 0, 1, 1, [], 1.2, 4.2, ["Singed"]),
            _session("2026-05-13", "evening", 5, 0.52, 1, 0, 0, 0, [], 1.1, 4.0, ["Nunu", "Singed"]),
            _session("2026-05-15", "evening", 4, 0.48, 1, 0, 1, 2, [], 1.0, 3.8, ["Singed"]),
            _session("2026-05-17", "evening", 3, 0.45, 1, 0, 1, 1, [], 0.9, 3.5, ["Singed"]),
            _session("2026-05-19", "evening", 4, 0.42, 2, 0, 2, 2, [], 0.8, 3.2, ["Singed"]),
        ],
        "trajectory": {
            "direction": "declining",
            "velocity": 0.03,
            "current_health": 0.42,
            "predicted_health_3_sessions": 0.33,
            "baseline_health": 0.72,
            "tilt_trigger": "No single trigger — consistent, gradual performance decline without chat toxicity. Possible soft-inting pattern.",
        },
        "unusual_builds_detected": True,
        "chat_toxicity_score": 0.05,
        "gameplay_toxicity_score": 0.65,
        "intervention_history": [],
        "report_count": 8,
        "honor_level": 2,
    },

    "cascade-spiral": {
        "id": "cascade-spiral",
        "name": "Cascade Spiral",
        "description": "One bad game with an AFK triggered 72 hours of escalating toxicity.",
        "expected_decision": "ESCALATE",
        "game": "valorant",
        "riot_id": "Spiraling#HELP",
        "region": "americas",
        "platform": "na1",
        "account": {
            "puuid": "demo-cascade-puuid",
            "gameName": "Spiraling",
            "tagLine": "HELP",
            "summonerLevel": 1,
        },
        "rank": {"tier": "ASCENDANT", "rank": "I", "leaguePoints": 120, "wins": 200, "losses": 190},
        "account_age_days": 400,
        "sessions": [
            _session("2026-05-14", "evening",   2, 0.92, 0, 3, 0, 0, [], headshot_pct=0.30, agents=["Sova", "Fade"]),
            _session("2026-05-15", "evening",   3, 0.90, 0, 2, 0, 0, [], headshot_pct=0.28, agents=["Sova", "Fade"]),
            # Trigger: teammate AFKs in ranked, causes loss
            _session("2026-05-16", "evening",   4, 0.55, 2, 0, 0, 0, ["afk team", "report sage", "4v5 every game"], headshot_pct=0.20, agents=["Sova"]),
            _session("2026-05-16", "night",     5, 0.30, 4, 0, 0, 0, ["dog players", "hardstuck", "diff", "report", "im throwing"], headshot_pct=0.12, agents=["Sova"]),
            _session("2026-05-17", "morning",   3, 0.22, 3, 0, 0, 0, ["trolling", "ff", "im done with this game"], headshot_pct=0.10, agents=["Sova"]),
            _session("2026-05-17", "evening",   6, 0.15, 5, 0, 0, 0, ["report all", "kys", "uninstall", "worst team", "throwing"], headshot_pct=0.08, agents=["Sova"]),
            _session("2026-05-18", "afternoon", 4, 0.12, 4, 0, 0, 0, ["gg open", "ff", "report", "dog lobby"], headshot_pct=0.09, agents=["Sova"]),
            _session("2026-05-18", "night",     5, 0.08, 5, 0, 0, 0, ["kill yourselves", "worst game", "trolling every game", "report"], headshot_pct=0.07, agents=["Sova"]),
            _session("2026-05-19", "morning",   3, 0.10, 3, 0, 0, 0, ["im done", "ff", "report team"], headshot_pct=0.08, agents=["Sova"]),
            _session("2026-05-19", "evening",   4, 0.05, 4, 0, 0, 0, ["kys", "uninstall", "worst players", "im intentionally throwing"], headshot_pct=0.06, agents=["Sova"]),
        ],
        "trajectory": {
            "direction": "spiraling",
            "velocity": 0.12,
            "current_health": 0.05,
            "predicted_health_3_sessions": 0.00,
            "baseline_health": 0.91,
            "tilt_trigger": "AFK teammate in ranked game triggered a 72-hour cascade spiral with rapidly escalating severity",
        },
        "intervention_history": [],
        "report_count": 30,
        "honor_level": 1,
    },
}


def get_demo_profiles_summary() -> list[dict]:
    return [
        {
            "id": p["id"],
            "name": p["name"],
            "description": p["description"],
            "expected_decision": p["expected_decision"],
            "game": p["game"],
            "riot_id": p["riot_id"],
        }
        for p in DEMO_PROFILES.values()
    ]


def get_demo_profile(profile_id: str) -> dict | None:
    return DEMO_PROFILES.get(profile_id)
