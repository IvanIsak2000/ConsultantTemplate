import sqlalchemy
import datetime
from typing import Union
from sqlalchemy import select, update, func, delete
from pydantic import BaseModel


from utils.db.models import *
from utils.logging.logger import logger
from utils.db.models import get_engine
async_session = get_engine()

class GetUser(BaseModel):
    user_id: int
    username: str
    full_name: str
    join_time: datetime.datetime
    is_banned: bool
    welcome_notif_id: int   
    feature_notif_id: int


class User():
    def __init__(
        self, 
        user_id: int = None,
        message = None
    ):
        self.user_id = user_id
        self.message = message

    async def is_banned_user(self) -> bool:
        try:
            async with async_session() as session:
                query = select(UserModel.is_banned).where(
                    UserModel.user_id == self.user_id)
                result = await session.execute(query)
                banned = result.scalars().first()
                if banned:
                    return True
                return False
        except TypeError:
            return False

    async def add_user(self) -> None:
        _user = self.message.from_user
        async with async_session() as session:
            async with session.begin():
                try:
                    local_time = datetime.datetime.now()
                    user = UserModel(
                        user_id=_user.id,
                        username=_user.username,
                        full_name=_user.full_name,
                        join_time=local_time)
                    session.add(user)
                    await session.commit()
                    await logger.info(
                        f'👤 Новый пользователь id={_user.id}, name={_user.full_name} зашёл',
                        extra={'full_data': self.message})
                except sqlalchemy.exc.IntegrityError:
                    pass

    async def get_user(self) -> GetUser:
        async with async_session() as session:
            async with session.begin():
                q = select(UserModel).where(UserModel.user_id == self.user_id)
                for i in await session.execute(q):
                    return GetUser(
                        user_id=i.UserModel.user_id,
                        username=i.UserModel.username,
                        full_name=i.UserModel.full_name,
                        join_time=i.UserModel.join_time,
                        is_banned=i.UserModel.is_banned,
                        status=i.UserModel.status,
                        sex=i.UserModel.sex,
                        old=i.UserModel.old,
                        goal=i.UserModel.goal,
                        time=i.UserModel.time,
                        fragment_number=i.UserModel.fragment_number,
                        welcome_notif_id=i.UserModel.welcome_notif_id,
                        feature_notif_id=i.UserModel.feature_notif_id
                    )

    async def get_users(self)  -> list[GetUser]:
        users = []
        async with async_session() as session:
            async with session.begin():
                q = select(UserModel).order_by(UserModel.join_time)
                for i in await session.execute(q):
                    users.append(GetUser(
                        user_id=i.UserModel.user_id,
                        username=i.UserModel.username,
                        full_name=i.UserModel.full_name,
                        join_time=i.UserModel.join_time,
                        is_banned=i.UserModel.is_banned,
                        status=i.UserModel.status,
                        sex=i.UserModel.sex,
                        old=i.UserModel.old,
                        goal=i.UserModel.goal,
                        time=i.UserModel.time,
                        fragment_number=i.UserModel.fragment_number,
                        welcome_notif_id=i.UserModel.welcome_notif_id,
                        feature_notif_id=i.UserModel.feature_notif_id
                        )
                    )
        return users

    async def update_welcome_msg_id(self, new_id: int) -> None:
        async with async_session() as session:
            async with session.begin():
                q = update(UserModel).where(
                    UserModel.user_id == self.user_id
                ).values(
                    welcome_notif_id=new_id
                )
                await session.execute(q)

    async def get_welcome_msg_id(self)  -> int:
        async with async_session() as session:
            async with session.begin():
                q = select(UserModel).where(
                    UserModel.user_id == self.user_id
                )
                for i in await session.execute(q):
                    if i == -1:
                        return -1
                    return i.UserModel.welcome_notif_id

    async def update_feature_msg_id(self, new_id: int) -> None:
        async with async_session() as session:
            async with session.begin():
                q = update(UserModel).where(
                    UserModel.user_id == self.user_id
                ).values(
                    feature_notif_id=new_id
                )
                await session.execute(q)
    
    async def get_feature_notif_id(self) -> int:
        async with async_session() as session:
            async with session.begin():
                q = select(UserModel).where(
                    UserModel.user_id == self.user_id
                )
                for i in await session.execute(q):
                    if i == -1:
                        return -1
                    return i.UserModel.feature_notif_id