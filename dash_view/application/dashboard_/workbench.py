from common.utilities.util_menu_access import MenuAccess
from typing import List
from common.utilities.util_logger import Log
from functools import partial
from i18n import translator

_ = partial(translator.t)


# 二级菜单的标题、图标和显示顺序
def get_title():
    return _('工作台')


icon = None
order = 1
logger = Log.get_logger(__name__)

access_metas = ('工作台-页面',)


def render_content(menu_access: MenuAccess, **kwargs):
    access_metas: List[str] = menu_access.all_access_metas
    logger.debug(f'用户：{menu_access.user_name}，访问：{__name__}，参数列表：{kwargs}，权限元：{menu_access.all_access_metas}')
    return str(kwargs)
