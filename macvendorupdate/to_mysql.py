"""
    This file contains the functions for the option mysql
"""
import re

from modules.database_settings import DatabaseSettings
from modules.database_actions import DatabaseActions
from misc_functions import (
    download_file,
    get_values_from_line,
    strip_and_concat,
    end_steps
)

from global_values import OUI_FILE, OUI_URL


def update_mysql():
    """
        Writes the info from the file into the MySQL table.

        NOTE: Read README.md to know the needed table structure
    """
    # create database_config object
    database_config = DatabaseSettings()

    # ask for database config
    database_config.ask_for_setup()

    # test db connection
    conn = database_config.check_db_connection()

    # create object for database actions
    database_action = DatabaseActions(conn)

    # download oui.txt
    download_file(OUI_URL, OUI_FILE)

    # parsing oui.txt data
    with open(OUI_FILE) as infile:
        for line in infile:
            if re.search("(hex)", line):
                mac, vendor = get_values_from_line(line)

                if mac != '' and vendor != '':
                    sql = "INSERT INTO mac_vendors "
                    sql += "(oui,vendor) "
                    sql += "VALUES ("
                    sql += strip_and_concat(mac, vendor, False)
                    sql += ")"

                    database_action.execute_query(sql)

    database_action.close_database()

    end_steps(OUI_FILE)
