import datetime
from typing import Optional


class ReferencePoints:
    def __init__(self):
        """
        timedelta=0, означает мгновенную отправку
        """
        self.reference_points = [
            datetime.timedelta(0),
            datetime.timedelta(minutes=10),
            datetime.timedelta(hours=10),
            datetime.timedelta(days=1),
        ]

    @staticmethod
    async def check_target_time(
        start_time: datetime.datetime, delta_time: datetime.timedelta
    ) -> tuple[datetime.datetime, datetime.timedelta] | None:
        start_time = start_time.replace(tzinfo=datetime.timezone.utc)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        if delta_time == datetime.timedelta(0):
            target_time = current_time + datetime.timedelta(minutes=1)
            delta_time = start_time - target_time
        else:
            target_time = (start_time - delta_time).replace(
                tzinfo=datetime.timezone.utc
            )
        if target_time > current_time:
            return target_time, delta_time


reference_points = ReferencePoints()
