# Project: Automated Email Monitoring and Alert System

## Overview

This project aims to automate the monitoring of critical emails related to down services or devices in various production environments. By leveraging core Python skills and the Gmail API, the system reduces the need for manual intervention by automatically reading emails from a designated Gmail inbox, processing the content, and sending alerts to the appropriate teams based on predefined rules.

## Features
Automated Email Monitoring: The system continuously monitors the Gmail inbox for new emails from critical/down services or devices.
Customizable Rules: A CSV file is used to define the rules, including sender details and specific keywords to match in the email content.
Email Parsing: Upon receiving an email, the system parses the content to identify relevant details such as service name, issue description, etc.
Alert Routing: Based on the parsed information and rules defined in the CSV file, the system routes the email or a summary alert to the appropriate team.

## Error Handling:

The system includes error handling mechanisms to manage cases where the email content doesn't match any rule or if any other issue arises.

## Prerequisites
1. Python 3.10
2. Gmail App password
3. csv
4. re
5. smtplib
6. email
7. pandas
8. Django
9. yaml
10. box

## Installation
Clone the Repository:

git clone https://github.com/Shivam-Shane/Service_monitoring.git

Install the Required Libraries:

pip install . 

Follow the instructions here to enable the Gmail APP password
https://support.google.com/mail/answer/185833?hl=en
Update the config.yaml with the Gmail User mail and password.

Update the email.csv file with the necessary details

Subject: The specific service or device name to match in the email.

Email_list: The email address of the sender to monitor.

Name: Human-readable name of service for your own convenient

additional_recipients: List of additional email(CC)

Last Sent: Empty(will ensure when was the last mail sent for the specific service)

sent_for_critical: Initial Empty (Whether it was sent of critical)
sent_for_down: Initial empty (Whether it was sent off down)



## Usage
Run the Script:

main.py

The script will start monitoring the Gmail inbox for new emails based on the rules defined in email.csv.
When an email matches the criteria, an alert will be sent to the relevant team.

### Update config.yaml from UI
Run in command line: 

python gamil_monitoring/manage.py runserver 0.0.0.0:1999

Open the browser at htts://127.0.0.1:1999


## Logs:

All actions and errors are logged for troubleshooting and auditing purposes. Check the logs/ directory for log files.


## Customization

Adding New Rules: Modify the email_rules.csv file to include new sender email addresses, service names, and alert emails as needed.

Extending Functionality: You can extend the system by adding more sophisticated parsing, and filtering logic, or integrating with other notification systems like Slack, SMS, etc.

## Contribution
Feel free to fork this project, submit pull requests, or report issues. Contributions to enhance the functionality and make the system more robust are welcome!

## License
This project is licensed under the GNU GENERAL PUBLIC LICENSE - see the LICENSE file for details.

## Contact
For any questions or support, please contact the project maintainer at sk0551460@gmail.com

## Support the Project
Help us continue developing and improving this project by:

### Following Us on Social Media: 

Stay updated with our latest work by following us on LinkedIn at https://www.linkedin.com/in/shivam-2641081a0/

Buying Me a Book: https://buymeacoffee.com/shivamshane
