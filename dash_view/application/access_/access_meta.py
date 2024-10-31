from common.utilities.util_menu_access import MenuAccess
from typing import List
import feffery_antd_components as fac
import feffery_utils_components as fuc
from common.utilities.util_logger import Log
from dash import html
from dash_components import ShadowDiv
from dash import dcc
from database.sql_db.dao import dao_user
import dash_callback.application.personal_info_c  # noqa
from flask_babel import gettext as _  # noqa


# 二级菜单的标题、图标和显示顺序
def get_title():
    return _('权限列表')


icon = None
logger = Log.get_logger(__name__)
order = 1

access_metas = (
    '权限列表-页面',
)

# def render_content():
