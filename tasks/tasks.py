import aioschedule
from asyncio import sleep


from .timestamps import add_timestamps_for_marathon_members
from .funnel_users import check_funnel_users, check_on_registration_funnel_users


async def setup():
    aioschedule.every().hours.at(":30").do(add_timestamps_for_marathon_members)
    aioschedule.every().hours.at(":00").do(add_timestamps_for_marathon_members)

    aioschedule.every().minute.do(check_funnel_users)
    aioschedule.every().minute.do(check_on_registration_funnel_users)

    while True:
        await aioschedule.run_pending()
        await sleep(1)

