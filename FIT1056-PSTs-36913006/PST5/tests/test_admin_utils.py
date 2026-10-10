import json
import logging

from app.admin_utils import backup_data, init_logger


def test_backup_data_creates_matching_copy(tmp_path):
    # Arrange
    source = tmp_path / "data" / "msms.json"
    source.parent.mkdir()
    source.write_text(json.dumps({"students": []}), encoding="utf-8")
    backup_directory = tmp_path / "backups"

    # Act
    result = backup_data(source, backup_directory)
    backups = list(backup_directory.glob("msms_backup_*.json"))

    # Assert
    assert result is True
    assert len(backups) == 1
    assert backups[0].read_text(encoding="utf-8") == source.read_text(
        encoding="utf-8"
    )


def test_backup_data_returns_false_for_missing_source(tmp_path):
    # Act
    result = backup_data(tmp_path / "missing.json", tmp_path / "backups")

    # Assert
    assert result is False


def test_init_logger_writes_messages_to_file(tmp_path):
    # Arrange
    log_file = tmp_path / "logs" / "msms.log"

    # Act
    returned_path = init_logger(log_file)
    logging.getLogger("test").info("test message")
    logging.shutdown()

    # Assert
    assert returned_path == log_file
    assert "test message" in log_file.read_text(encoding="utf-8")
