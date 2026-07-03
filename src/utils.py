import json
import logging
from pathlib import Path
from typing import Any


LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

utils_logger = logging.getLogger(__name__)
utils_logger.setLevel(logging.DEBUG)
utils_logger.propagate = False

if not utils_logger.handlers:
    utils_file_handler = logging.FileHandler(
        LOGS_DIR / "utils.log",
        mode="w",
        encoding="utf-8",
    )
    utils_file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    utils_file_handler.setFormatter(utils_file_formatter)
    utils_logger.addHandler(utils_file_handler)


def load_transactions_from_json(file_path: str) -> list[dict[str, Any]]:
    """Возвращает список транзакций из JSON-файла."""
    path = Path(file_path)

    utils_logger.debug("Start reading JSON file: %s", file_path)

    try:
        with path.open(encoding="utf-8") as file:
            transactions = json.load(file)
    except FileNotFoundError as error:
        utils_logger.error("JSON file was not found: %s", error)
        return []
    except json.JSONDecodeError as error:
        utils_logger.error("JSON file decoding error: %s", error)
        return []

    if not isinstance(transactions, list):
        utils_logger.error("JSON file does not contain a list: %s", file_path)
        return []

    utils_logger.info(
        "JSON file was loaded successfully. Transactions count: %s",
        len(transactions),
    )

    return transactions
