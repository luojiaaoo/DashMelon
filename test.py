from dataclasses import dataclass


@dataclass
class UserInfoFromSession_:
    user_id: int
    user_name: str
    user_department: str


class UserInfoFromSession(UserInfoFromSession_):
    def __init__(self, **kwargs):
        super().__init__(
            user_id=kwargs.get('user_id'),
            user_name=kwargs.get('user_name'),
            user_department=kwargs.get('user_department'),
        )


# 创建实例，传递多余参数 a=111
a = UserInfoFromSession(user_id=1, user_name='admin', user_department='admin', a=111)
print(a)
