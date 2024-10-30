from database.sql_db.dao.user import get_all_menu_item_and_access_meta, get_user_info, UserInfo
from typing import Dict, List, Set
from common.utilities.util_logger import Log

logger = Log.get_logger(__name__)


class MenuAccess:
    default_menu_item_and_access_meta = (
        'person.personal_info:show',
        'person.personal_setting:show',
        'dashboard.workbench:show',
    )

    @classmethod
    def get_dict_menu_item_and_access_meta(cls, user_name: str) -> Dict[str, List[str]]:
        """获取用户可访问的菜单项权限字典

        根据用户名获取该用户可以访问的所有菜单项和应用权限，并将其整理为字典格式。
        这个方法主要用于权限控制，快速查找用户是否有特定菜单项的访问权限。

        参数:
        user_name (str): 用户名，用于查询用户权限。

        返回:
        Dict[str, List[str]]: 一个字典，其中键是菜单项的模块路径，值是对应的权限列表。
        """
        # 比如 menu_item:  dashboard.workbench:log_info,冒号前为视图的包路径，后面为权限列表
        all_menu_item_and_access_meta: Set[str] = get_all_menu_item_and_access_meta(user_name=user_name)
        all_menu_item_and_access_meta.update(cls.default_menu_item_and_access_meta)
        dict_menu_item_and_access_meta = dict()
        for _menu_item_and_access_meta in all_menu_item_and_access_meta:
            module_path, access = _menu_item_and_access_meta.split(':')
            if dict_menu_item_and_access_meta.get(module_path) is None:
                dict_menu_item_and_access_meta[module_path] = [access]
            else:
                dict_menu_item_and_access_meta[module_path].append(access)
        return dict_menu_item_and_access_meta

    @classmethod
    def gen_menu(self, menu_item: Set[str]):
        dict_level1_level2 = dict()
        for per_menu_item in menu_item:
            level1_name, level2_name = per_menu_item.split('.')
            if dict_level1_level2.get(level1_name) is None:
                dict_level1_level2[level1_name] = [level2_name]
            else:
                dict_level1_level2[level1_name].append(level2_name)

        def get_title(module_path):
            from dash_view import application  # noqa

            return eval(f'application.{module_path}.get_title()')

        def get_order(module_path):
            from dash_view import application  # noqa

            try:
                return eval(f'application.{module_path}.order')
            except:
                logger.warning(f'{module_path}没有定义order属性')
                return 999

        def get_icon(module_path):
            from dash_view import application  # noqa

            try:
                return eval(f'application.{module_path}.icon')
            except:
                return None

        # 根据order属性排序
        dict_level1_level2 = dict(sorted(dict_level1_level2.items(), key=lambda x: get_order(f'{x[0]}')))
        for level1, level2 in dict_level1_level2.items():
            level2.sort(key=lambda x: get_order(f'{level1}.{x}'))

        menu = [
            {
                'component': 'SubMenu',
                'props': {
                    'key': f'/{level1_name}',
                    'title': get_title(f'{level1_name}'),
                    'icon': get_icon(f'{level1_name}'),
                },
                'children': [
                    {
                        'component': 'Item',
                        'props': {
                            'key': f'/{level1_name}/{level2_name}',
                            'title': get_title(f'{level1_name}.{level2_name}'),
                            'icon': get_icon(f'{level1_name}.{level2_name}'),
                            'href': f'/{level1_name}/{level2_name}',
                        },
                    }
                    for level2_name in level2_name_list
                ],
            }
            for level1_name, level2_name_list in dict_level1_level2.items()
        ]
        return menu

    def __init__(self, user_name) -> None:
        self.user_name = user_name
        self.user_info: UserInfo = get_user_info(user_name)
        # 菜单项 -> 权限元的字典
        self.dict_menu_item_and_access_meta = self.get_dict_menu_item_and_access_meta(user_name)
        # 所有菜单项
        self.menu_item = set(list(self.dict_menu_item_and_access_meta.keys()))
        # 生成AntdMenu的菜单格式
        self.menu = self.gen_menu(self.menu_item)

    def get_access_metas(self, module_path: str) -> List[str]:
        """获取用户可访问的权限元"""
        # 传进来的是__name__包路径，去掉前缀才是菜单项
        menu_item_name = module_path.replace('dash_view.application.', '')
        return self.dict_menu_item_and_access_meta.get(menu_item_name)


def get_menu_access() -> MenuAccess:
    """
    在已登录状态下，获取菜单访问权限。

    本函数通过JWT（JSON Web Token）解码来获取当前用户的访问权限信息，并返回一个包含用户名的MenuAccess对象。
    如果解码无效，强制退出登录；如果过期则可选择性退出登录或者不管。

    参数:
    无

    返回:
    MenuAccess: 包含用户访问权限信息的MenuAccess对象。
    """
    from common.utilities import util_jwt
    from config.dash_melon_conf import LoginConf

    rt_access = util_jwt.jwt_decode_from_session(
        verify_exp=True,
        force_logout_if_exp=LoginConf.JWT_EXPIRED_FORCE_LOGOUT,
        ignore_exp=not LoginConf.JWT_EXPIRED_FORCE_LOGOUT,
        force_logout_if_invalid=True,
    )
    return MenuAccess(user_name=rt_access['user_name'])
