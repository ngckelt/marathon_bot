import csv
import os
from utils.db_api.db import MarathonMembersModel
from datetime import datetime


async def create_document():
    now_date = datetime.now().strftime("%d-%m-%Y")

    upload_path = f"documents/{now_date}/"
    filename = f"{now_date}.csv"
    if not os.path.exists(upload_path):
        os.makedirs(upload_path, exist_ok=True)

    marathon_members = await MarathonMembersModel.get_marathon_members()
    with open(upload_path + filename, 'w') as csvfile:
        fieldnames = ['username', 'marathon_day', 'failed_days']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for marathon_member in marathon_members:
            writer.writerow(
                {
                    'username': marathon_member.username,
                    'marathon_day': marathon_member.marathon_day,
                    'failed_days': marathon_member.failed_days
                }
            )

    return upload_path + filename




