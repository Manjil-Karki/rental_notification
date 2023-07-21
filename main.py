import json
import pymysql
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta

def read_config(path):
    with open(path, 'r') as f:
        config = json.load(f)
        db_config = config['db_config']
        smtp_config = config['smtp_config']
        return db_config, smtp_config

def fetch_new_rentals(db_config):
    try:
        # Connect to the database
        conn = pymysql.connect(**db_config)
        cursor = conn.cursor()

        # Calculate the time one hour ago from now
        one_hour_ago = datetime.now() - timedelta(hours=1)
        now = datetime.now()

        one_hour_ago_str = one_hour_ago.strftime('%Y-%m-%d %H:%M:%S')
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')


        # Fetch new rentals within the last hour
        query = f"""
        SELECT r.rental_id, r.rental_date, c.first_name, c.last_name, f.title, co.country
        FROM rental r
        JOIN customer c ON r.customer_id = c.customer_id
        JOIN inventory i ON r.inventory_id = i.inventory_id
        JOIN film f ON i.film_id = f.film_id
        JOIN address a ON c.address_id = a.address_id
        JOIN city ci ON a.city_id = ci.city_id
        JOIN country co ON ci.country_id = co.country_id
        WHERE r.rental_date >= '{one_hour_ago_str}'
        AND r.rental_date <= '{now_str}'
        """
        cursor.execute(query)
        rentals = cursor.fetchall()

        cursor.close()
        conn.close()

        return rentals

    except Exception as e:
        print("Error fetching new rentals:", e)
        return []

def format_rentals(rentals):
    formatted_rentals = []
    for rental in rentals:
        rental_id, rental_date, first_name, last_name, film_title, customer_country = rental
        rental_date = rental_date.strftime("%Y-%m-%d %H:%M:%S")
        customer_name = f"{first_name} {last_name}"
        formatted_rentals.append((rental_id, rental_date, customer_name, film_title, customer_country))

    return formatted_rentals

def send_email(content, smtp_config):
    message = MIMEMultipart()
    message["From"] = smtp_config["sender_email"]
    message["To"] = smtp_config["receiver_email"]
    message["Subject"] = "Movies Rentals in the Last Hour"

    body = '''
    Following mentioned are the informations of movie rentals of last hour


    rental_id | rental_date | Customer Name | film_title | customer's country\n'''
    body_data = "\n".join([" | ".join(map(str, rental)) for rental in content])
    body = body + body_data
    message.attach(MIMEText(body, "plain"))

    with smtplib.SMTP(smtp_config["smtp_server"], smtp_config["smtp_port"]) as server:
        server.starttls()
        server.login(smtp_config["smtp_username"], smtp_config["smtp_password"])
        server.sendmail(smtp_config["sender_email"], smtp_config["receiver_email"], message.as_string())

if __name__ == "__main__":

    db_config, smtp_config = read_config("config.json")


    new_rentals = fetch_new_rentals(db_config)
    if new_rentals:
        formatted_rentals = format_rentals(new_rentals)
        send_email(formatted_rentals, smtp_config)
        print("Email sent successfully.")
    else:
        print("No new rentals in the last hour.")
