import datetime
import logging
import shutil
from pathlib import Path

LOGGER = logging.getLogger(__name__)


def init_logger(log_file="msms.log"):
    """Configure file logging and return the log file path."""
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        filename=log_path,
        filemode="a",
        force=True,
    )
    LOGGER.info("MSMS logging started.")
    return log_path


def backup_data(data_path="data/msms.json", backup_dir="data/backups"):
    """Create a uniquely named backup of the JSON data file."""
    source = Path(data_path)
    destination_directory = Path(backup_dir)

    if not source.is_file():
        LOGGER.error("Backup failed because %s does not exist.", source)
        return False

    try:
        destination_directory.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S-%f")
        destination = destination_directory / f"msms_backup_{timestamp}.json"
        shutil.copy2(source, destination)
    except OSError as error:
        LOGGER.error("Failed to create backup: %s", error)
        return False

    LOGGER.info("Data successfully backed up to %s.", destination)
    return True
