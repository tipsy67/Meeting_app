from api_app.tasks.tg_messages import send_messages_about_conference_task


async def create_conference(conference_id):
    await send_messages_about_conference_task.kiq(conference_id)
