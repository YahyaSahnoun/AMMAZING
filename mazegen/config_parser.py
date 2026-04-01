from typing import Any


def parse_config(path: str) -> dict[str, Any]:
    config = {}

    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if "=" not in line:
                raise ValueError("Invalid config line")

            key, value = line.split("=", 1)
            config[key.strip().upper()] = value.strip()

    required_keys = ["WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE",
                     "PERFECT"]
    for k in required_keys:
        if k not in config:
            raise ValueError(f"Missing key in config: {k}")

    # Convert width and height
    width = int(config["WIDTH"])
    height = int(config["HEIGHT"])
    if width <= 0 or height <= 0:
        raise ValueError("WIDTH and HEIGHT must be positive integers")
    if width > 100 or height > 100:
        raise ValueError("Configs are too big (>100), "
                         "retry with small values :)")

    # Convert entry and exit
    try:
        entry = tuple(map(int, config["ENTRY"].split(",")))
        exit_ = tuple(map(int, config["EXIT"].split(",")))
        if len(entry) != 2 or len(exit_) != 2:
            raise ValueError
    except Exception:
        raise ValueError("ENTRY and EXIT must be in format x,y with integers")

    for name, coord in [("ENTRY", entry), ("EXIT", exit_)]:
        x, y = coord
        if x < 0 or y < 0:
            raise ValueError(f"{name} coordinates cannot be negative: {coord}")
        if not (0 <= x < width) or not (0 <= y < height):
            raise ValueError(f"{name} {coord} is out of bounds for grid "
                             f"{width}x{height}")

    if entry == exit_:
        raise ValueError("Config Error: ENTRY = EXIT!!")

    # PERFECT flag
    perfect_raw = config["PERFECT"].strip().lower()
    if perfect_raw not in {"true", "false"}:
        raise ValueError("PERFECT must be True or False")

    # Optional seed
    seed: int | None = None
    seed_value = config.get("SEED")
    if seed_value:
        seed = int(seed_value)

    return {
        "width": width,
        "height": height,
        "entry": entry,
        "exit": exit_,
        "output": config["OUTPUT_FILE"],
        "perfect": perfect_raw == "true",
        "seed": seed
    }
