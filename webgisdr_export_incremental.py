import os, shutil, datetime, smtplib, json
from datetime import datetime, timedelta
from dateutil.parser import parse
from subprocess import Popen
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Variables
backupDirectory = r"\\myserver\Backup\Incremental"
previousBackups = r"\\myserver\Backup\Incremental\Previous"
batFile = r"C:\Program Files\ArcGIS\Portal\tools\webgisdr\webgisdr_incremental_backup.bat"
days = 14    # Number of days to retain previous backups
sender_email = "my@email.com"
receiver_email = "your@email.com"
subject = "Incremental WebgisDR Output"
filename = r"C:\Program Files\ArcGIS\Portal\tools\webgisdr\webgisdrlogoutput.json"
smtp_server = "smtp.my.email" #Your SMTP server.  Gmail example: "smtp.gmail.com"
smtp_port = 587  #This is pretty standard, but adjust as necessary.

# Delete previous INCREMENTAL backups
print("Deleting previous INCREMENTAL backups in PREVIOUS folder older than {0} days".format(days))
for file in os.listdir(previousBackups):
    month = file[4:6]
    day = file[6:8]
    year = file[0:4]
    date = month + "-" + day + "-" + year
    dt = parse(date)
    newDate = datetime.now() - timedelta(days + 1)
    if dt < newDate:
        # Delete File
        os.remove(os.path.join(previousBackups, file))

# Move previous INCREMENTAL backups to Previous folder
print("Moving previous INCREMENTAL backups to PREVIOUS folder")
for file in os.listdir(backupDirectory):
    if 'INCREMENTAL' in file:
        shutil.move(os.path.join(backupDirectory, file), os.path.join(previousBackups, file))

# Run bat file
p = Popen(batFile)
stdout, stderr = p.communicate()

#define function to parse webgisdr output file and email contents
def send_email_with_json(sender_email, receiver_email, subject, filename, smtp_server, smtp_port):
  """
  Sends an email with the contents of a JSON file as the body.

  Args:
      sender_email (str): Email address of the sender.
      receiver_email (str): Email address of the recipient.
      subject (str): Subject of the email.
      filename (str): Path to the JSON file.
      smtp_server (str): SMTP server address.
      smtp_port (int): SMTP server port.
  """

  # Read JSON file
  with open(filename, 'r') as f:
    data = json.load(f)

  # Convert JSON data to string (optional: pretty print for readability)
  body = json.dumps(data, indent=4)

  # Create email message
  message = MIMEMultipart()
  message['From'] = sender_email
  message['To'] = receiver_email
  message['Subject'] = subject

  # Attach JSON content as plain text
  message.attach(MIMEText(body, 'plain'))

  # Send email
  with smtplib.SMTP(smtp_server, smtp_port) as server:
    server.starttls()
    # Add credentials for authentication if needed by your server
    server.login("dgierszcc@gmail.com", "eueb vhgx npkx xyfg")
    server.sendmail(sender_email, receiver_email, message.as_string())

  print(f"Email sent to {receiver_email} with contents of {filename}")

send_email_with_json(sender_email, receiver_email, subject, filename, smtp_server, smtp_port)