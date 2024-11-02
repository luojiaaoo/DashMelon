from database.sql_db.conn import pool
from typing import Dict, List, Set, Union
from itertools import chain
from dataclasses import dataclass
from datetime import datetime
import json


def exists_user_name(user_name: str) -> bool:
    with pool.get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """SELECT user_name FROM sys_user WHERE user_name = %s;""",
            (user_name,),
        )
        result = cursor.fetchone()
        return result is not None


def user_password_verify(user_name: str, password_sha256: str) -> bool:
    with pool.get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """SELECT user_name FROM sys_user WHERE user_name = %s and password_sha256 = %s;""",
            (user_name, password_sha256),
        )
        result = cursor.fetchone()
        return result is not None


def get_all_access_meta_for_setup_check() -> Set[str]:
    with pool.get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """SELECT access_metas FROM sys_role
            """
        )
        result = cursor.fetchall()
        return set(chain(*[json.loads(per_rt[0]) for per_rt in result]))


@dataclass
class UserInfo:
    user_name: str
    user_full_name: str
    user_status: str
    user_sex: str
    user_roles: List
    user_groups: Dict
    user_email: str
    phone_number: str
    update_datetime: datetime
    create_by: str
    create_datetime: datetime
    user_remark: str


def get_user_info(user_name: str) -> UserInfo:
    heads = (
        'user_name',
        'user_full_name',
        'user_status',
        'user_sex',
        'user_roles',
        'user_groups',
        'user_email',
        'phone_number',
        'update_datetime',
        'create_by',
        'create_datetime',
        'user_remark',
    )
    with pool.get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT {','.join(heads)} FROM sys_user WHERE user_name = %s;""",
            (user_name,),
        )
        result = cursor.fetchone()
        user_dict = dict(zip(heads, result))
        user_dict.update({'user_groups': json.loads(user_dict['user_groups'])})
        return UserInfo(**user_dict)


def get_roles_from_user_name(user_name: str) -> Set[str]:
    with pool.get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            """SELECT user_roles FROM sys_user WHERE user_name = %s;""",
            (user_name,),
        )
        result = cursor.fetchone()
        return set(json.loads(result[0]))


def get_access_meta_from_roles(roles: Union[List[str], Set[str]]) -> Set[str]:
    with pool.get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(
            f"""SELECT access_metas FROM sys_role WHERE role_name in ({','.join(['%s']*len(roles))});""",
            tuple(roles),
        )
        result = cursor.fetchall()
        return set(chain(*[json.loads(per_rt[0]) for per_rt in result]))


def get_user_access_meta_plus_role(user_name: str) -> Set[str]:
    roles = get_roles_from_user_name(user_name)
    return get_access_meta_from_roles(roles)
