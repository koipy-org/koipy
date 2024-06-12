import tzlocal
from apscheduler.schedulers.asyncio import AsyncIOScheduler

scheduler = AsyncIOScheduler(timezone=str(tzlocal.get_localzone()))

