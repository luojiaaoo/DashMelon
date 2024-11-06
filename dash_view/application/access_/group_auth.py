from common.utilities.util_menu_access import MenuAccess
from typing import List
import feffery_antd_components as fac
import feffery_utils_components as fuc
from common.utilities.util_logger import Log
from dash_components import Card, Table
from dash import html
from dash import dcc
from database.sql_db.dao import dao_user
from typing import Dict
from dash_callback.application.access_ import role_mgmt_c  # noqa
from functools import partial
from i18n import translator

_ = partial(translator.t)


# 二级菜单的标题、图标和显示顺序
def get_title():
    return _('团队授权')


icon = None
order = 4
access_metas = ('团队授权-页面',)
logger = Log.get_logger(__name__)