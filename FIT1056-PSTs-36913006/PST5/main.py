from pathlib import Path

import streamlit as st

from app.admin_utils import backup_data, init_logger
from gui.main_dashboard import launch

PROJECT_DIRECTORY = Path(__file__).resolve().parent


if __name__ == "__main__":
    init_logger(PROJECT_DIRECTORY / "logs" / "msms.log")

    # Streamlit reruns this script after interactions, so back up only once
    # during each browser session instead of creating a backup on every click.
    if "startup_backup_complete" not in st.session_state:
        backup_data(
            PROJECT_DIRECTORY / "data" / "msms.json",
            PROJECT_DIRECTORY / "data" / "backups",
        )
        st.session_state.startup_backup_complete = True

    launch()
