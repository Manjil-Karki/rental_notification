from main import read_config
import pymysql
import datetime
from datetime import datetime, timedelta


def find_difference_and_update(db_config):
    try:
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        min_date_query = "SELECT MIN(rental_date) FROM rental;"
        cursor.execute(min_date_query)
        min_date_result = cursor.fetchone()
        min_date = min_date_result[0]


        current_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        difference = current_month - min_date

        update_query = "UPDATE rental SET rental_date = rental_date + INTERVAL %s DAY;"
        cursor.execute(update_query, (difference.days,))
        conn.commit()

        cursor.close()
        conn.close()

        print("Dates updated successfully.")

    except Exception as e:
        print("Error updating dates:", e)




if __name__ == "__main__":
    db_config, _ = read_config("config.json")

    find_difference_and_update(db_config)
