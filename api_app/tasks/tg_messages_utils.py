import datetime


class ReferencePoints:
    def __init__(self):
        self.reference_points = [
            datetime.timedelta(minutes=10),
            datetime.timedelta(hours=10),
            datetime.timedelta(days=1),
        ]

    @staticmethod
    async def check_target_time(
            start_time: datetime.datetime, delta_time: datetime.timedelta
    ) -> datetime.datetime | None:
        target_time = (start_time - delta_time).replace(tzinfo=datetime.timezone.utc)
        current_time = datetime.datetime.now(datetime.timezone.utc)
        if target_time > current_time:
            return target_time


reference_points = ReferencePoints()
