from sqlalchemy import select

from tg_app.bot.databases.sql_models import async_session, User


async def set_user(tg_id):
    async with async_session() as session:
        user = await session.scalar(select(User).where(User.id == tg_id))
        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()
