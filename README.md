# Player Converter JSON for Custom GPT

This repository converts Sleeper player JSON into a model-friendly JSON output so agents can read the data without parsing CSV.

## Usage

1. Export player data from the Sleeper API and save it into the repository as `nfl<year>.json`.
2. Run the converter:

```bash
python player_json_converter.py
```

3. By default, the script reads `nfl2026.json` and writes `sleeper_player_map_fantasy_2026.json`.

### Optional arguments

```bash
python player_json_converter.py --input nfl.json --output sleeper_player_map_fantasy.json
```

## Output

- The output is a JSON array of fantasy-relevant players.
- `fantasy_positions` is stored as a JSON list for easier agent interpretation.

## License

This project is licensed under the MIT License. See `LICENSE` for details.
