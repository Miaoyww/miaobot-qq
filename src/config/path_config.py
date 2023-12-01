from pathlib import Path

BOT_PATH: Path = Path(__file__).parent.parent
DATA_PATH: Path = BOT_PATH / "data"
TEXT_PATH: Path = DATA_PATH / "resource" / "text"
RECORD_PATH: Path = DATA_PATH / "resource" / "record"
