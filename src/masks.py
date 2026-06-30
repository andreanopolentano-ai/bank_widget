import logging
from pathlib import Path


LOGS_DIR = Path(__file__).resolve().parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

masks_logger = logging.getLogger(__name__)
masks_logger.setLevel(logging.DEBUG)
masks_logger.propagate = False

if not masks_logger.handlers:
    masks_file_handler = logging.FileHandler(
        LOGS_DIR / "masks.log",
        mode="w",
        encoding="utf-8",
    )
    masks_file_formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    masks_file_handler.setFormatter(masks_file_formatter)
    masks_logger.addHandler(masks_file_handler)


def get_mask_card_number(card_number: str) -> str:
    """Возвращает замаскированный номер банковской карты."""
    try:
        clean_card_number = card_number.replace(" ", "")
        masked_card_number = (
            f"{clean_card_number[:4]} {clean_card_number[4:6]}** "
            f"**** {clean_card_number[-4:]}"
        )
        masks_logger.info("Card number was masked successfully")
        return masked_card_number
    except Exception as error:
        masks_logger.error("Error while masking card number: %s", error)
        raise


def get_mask_account(account_number: str) -> str:
    """Возвращает замаскированный номер счета."""
    try:
        masked_account_number = f"**{account_number[-4:]}"
        masks_logger.info("Account number was masked successfully")
        return masked_account_number
    except Exception as error:
        masks_logger.error("Error while masking account number: %s", error)
        raise
