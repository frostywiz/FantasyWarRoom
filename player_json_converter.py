import argparse
import json

INPUT_JSON = "nfl2026.json"
OUTPUT_JSON = "sleeper_player_map_fantasy_2026.json"

ALLOWED = {"QB", "RB", "WR", "TE", "K", "DEF"}
PREF = ["QB", "RB", "WR", "TE", "K", "DEF"]

def safe_join_name(full_name, first_name, last_name):
    if full_name and str(full_name).strip():
        return str(full_name).strip()
    parts = []
    if first_name:
        parts.append(str(first_name).strip())
    if last_name:
        parts.append(str(last_name).strip())
    return " ".join(parts).strip()

def pick_primary(fps_list):
    for p in PREF:
        if p in fps_list:
            return p
    return fps_list[0] if fps_list else ""

def normalize_team(p):
    return p.get("team") or p.get("team_abbr") or ""

def as_str(v):
    return "" if v is None else str(v)

def convert_players(input_json, output_json):
    with open(input_json, "r", encoding="utf-8") as f:
        data = json.load(f)

    rows = []
    for player_id, p in data.items():
        if not isinstance(p, dict):
            continue

        # Prefer fantasy_positions for relevance + multi-position support
        fps_raw = p.get("fantasy_positions") or []
        fps_allowed = [pos for pos in fps_raw if pos in ALLOWED]

        # Fallback: some entries might be missing fantasy_positions
        pos = p.get("position") or ""
        is_relevant = bool(fps_allowed) or (pos in ALLOWED)

        if not is_relevant:
            continue

        # Use allowed fantasy positions if present; else fallback to NFL position
        fantasy_positions_out = fps_allowed if fps_allowed else ([pos] if pos in ALLOWED else [])

        # Build final fantasy positions set/list
        if fps_allowed:
            fantasy_positions = sorted(set(fps_allowed), key=lambda x: PREF.index(x) if x in PREF else 999)
        else:
            fantasy_positions = [pos]

        primary_pos = pick_primary(fantasy_positions)
        full_name = safe_join_name(p.get("full_name"), p.get("first_name"), p.get("last_name"))

        rows.append({
            "player_id": as_str(player_id),
            "full_name": full_name,
            "position": primary_pos,
            "fantasy_positions": fantasy_positions,

            # identity / lookup helpers
            "team": normalize_team(p),
            "active": p.get("active", ""),
            "status": p.get("status", ""),

            # useful external ids (optional but handy)
            "espn_id": as_str(p.get("espn_id")),
            "yahoo_id": as_str(p.get("yahoo_id")),
            "rotowire_id": as_str(p.get("rotowire_id")),
            "rotoworld_id": as_str(p.get("rotoworld_id")),
            "fantasy_data_id": as_str(p.get("fantasy_data_id")),
            "gsis_id": as_str(p.get("gsis_id")),

            # injury fields you listed
            "injury_status": as_str(p.get("injury_status")),
            "injury_body_part": as_str(p.get("injury_body_part")),
            "injury_start_date": as_str(p.get("injury_start_date")),
            "injury_notes": as_str(p.get("injury_notes")),

            # depth chart fields (often null, but included)
            "depth_chart_position": as_str(p.get("depth_chart_position")),
            "depth_chart_order": as_str(p.get("depth_chart_order")),

            # misc keys you showed
            "number": as_str(p.get("number")),
            "years_exp": as_str(p.get("years_exp")),
            "college": as_str(p.get("college")),
            "search_full_name": as_str(p.get("search_full_name")),
            "search_last_name": as_str(p.get("search_last_name")),
            "news_updated": as_str(p.get("news_updated")),
        })

    # Sort so lookups are consistent (IDs are strings; this keeps NE/DEF etc at top unless filtered out)
    rows.sort(key=lambda r: r["player_id"])

    with open(output_json, "w", encoding="utf-8") as f:
        json.dump(rows, f, ensure_ascii=False, indent=2)

    print(f"Wrote {len(rows)} fantasy-relevant rows -> {output_json}")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert Sleeper player JSON into agent-friendly JSON."
    )
    parser.add_argument(
        "--input",
        default=INPUT_JSON,
        help="Input JSON file (default: %(default)s)",
    )
    parser.add_argument(
        "--output",
        default=OUTPUT_JSON,
        help="Output JSON file (default: %(default)s)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    convert_players(args.input, args.output)
