<h1> Rental Notification System </h1>

A simple program to send e-mail notification hourly to a user notifying any new movie rentals in last hour. The program fetches data in folowing format:

<mark>
rental_id | rental_date | Customer Name | film_title | customer's country</mark>

All the mentioned columns were not in a single table thus join had to be used extensively to obtail all the necessary columns. The conceptual presentation of performed joins is displayed in the followinf ER-diagram:

![ER-diagram](images/sakila-db.png?raw=true "ER-diagram")

After joining tables and selecting necessary fields rows were selected which had rental_date belonging to last hour.

Then, for google SMTP server was setup and necessary credentials were used to send mail.

Finally, for the task of scheduling hourly query and sending notification simple cronjob was created in linux system as following using following command which would run the python script main.py hourly.

![cron job](images/cronjob.png?raw=true "cron job")

Final verification of scheduling and email is done as:

![exec log](images/exec-log.png?raw=true "exec log")

![mail-op](images/mail_op.png?raw=true "mail-op")


<h2> Setting Up </h2>

<ul>
<li> Download sakila db from mysql documentation </li>
<li> Import sakiladb to MySQL </li>
<li> The rental dates, dates back to 2005, 2006 run modify_rental_date script to update rental_date column to current relevent dates </li>
<li> Setup the python environment </li>
<li> Create a dedicated user for this operation</li>
<li> Get password for google SMTP </li>
<li> Setup configuration file config.json with help of sample_config.json </li>
<li> Start MySQL server </li>
<li> Start cornjob in linux </li>
<li> Add new cronjob to run hourly using crontab -e command </li>
<li> Monitor various log files created for proper execution of the program </li>
</ul>


