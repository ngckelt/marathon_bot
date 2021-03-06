import aioschedule
from asyncio import sleep


from .timestamps import add_timestamps_for_marathon_members
from utils.timestamps_manage.timestamps_manage import check_timestamps
from .funnel_users import check_funnel_users, check_on_registration_funnel_users
from data.config import BASE_SLEEP_SECONDS, CHECK_TIMESTAMPS_INTERVAL


async def setup():
    aioschedule.every().hours.at(":00").do(check_timestamps)
    aioschedule.every().hours.at(":10").do(check_timestamps)
    aioschedule.every().hours.at(":20").do(check_timestamps)
    aioschedule.every().hours.at(":30").do(check_timestamps)
    aioschedule.every().hours.at(":40").do(check_timestamps)
    aioschedule.every().hours.at(":50").do(check_timestamps)
    aioschedule.every().hours.at(":00").do(add_timestamps_for_marathon_members)
    aioschedule.every().hours.at(":30").do(add_timestamps_for_marathon_members)
    aioschedule.every().minute.do(check_funnel_users)
    aioschedule.every().minute.do(check_on_registration_funnel_users)

    while True:
        await aioschedule.run_pending()
        await sleep(BASE_SLEEP_SECONDS)

