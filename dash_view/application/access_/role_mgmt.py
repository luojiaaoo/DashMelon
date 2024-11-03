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
import dash_callback.application.person_.personal_info_c  # noqa
from functools import partial
from i18n import translator

_ = partial(translator.t)


# 二级菜单的标题、图标和显示顺序
def get_title():
    return _('角色管理')


icon = None
logger = Log.get_logger(__name__)
order = 1

access_metas = ('角色管理-页面',)


def render_content(menu_access: MenuAccess, **kwargs):
    dict_access_meta2menu_item: Dict = menu_access.dict_access_meta2menu_item
    from config.access_factory import AccessFactory
    logger.debug(f'用户：{menu_access.user_name}，访问：{__name__}，参数列表：{kwargs}，权限元：{access_metas}')
    return fac.AntdFlex(
        [
            Card(
                Table(
                    id='role-mgmt-table',
                    columns=[
                        {'title': _('角色名称'), 'dataIndex': 'role_name'},
                        {'title': _('角色状态'), 'dataIndex': 'role_status'},
                        {'title': _('角色描述'), 'dataIndex': 'role_remark'},
                        {'title': _('更新时间'), 'dataIndex': 'update_datetime'},
                        {'title': _('更新人'), 'dataIndex': 'update_by'},
                        {'title': _('创建时间'), 'dataIndex': 'create_datetime'},
                        {'title': _('创建人'), 'dataIndex': 'create_by'},
                        {'title': _('操作'), 'dataIndex': 'operation', 'renderOptions': {'renderType': 'button'}},
                    ],
                    data=[
                        {
                            **i.__dict__,
                            'operation': [
                                {
                                    'content': '编辑',
                                    'type': 'primary',
                                    'custom': i.role_name,
                                },
                                {
                                    'content': '删除',
                                    'type': 'primary',
                                    'custom': i.role_name,
                                    'danger': True,
                                },
                            ],
                        }
                        for i in dao_user.get_role_info()
                    ],
                    pageSize=10,
                ),
                className={'flex': 'auto'},
            ),
            fac.AntdModal(
                children=[
                    fac.AntdForm(
                        [
                            fac.AntdFormItem(fac.AntdText('xxx', id='role-mgmt-update-role-name'), label=_('角色名')),
                            fac.AntdFormItem(fac.AntdSwitch(checked=True), label=_('角色状态')),
                            fac.AntdFormItem(fac.AntdInput(mode='text-area'), label=_('角色描述')),
                            fac.AntdFormItem(
                                fac.AntdTree(
                                    id='role-menu-access-tree-select',
                                    treeData=AccessFactory.get_antd_tree_data_menu_item_access_meta(),
                                    multiple=True,
                                    checkable=True,
                                    showLine=False,
                                ),
                                label=_('菜单权限'),
                            ),
                        ],
                        labelCol={'span': 5},
                        wrapperCol={'span': 19},
                    )
                ],
                destroyOnClose=False,
                renderFooter=True,
                okText=_('确定'),
                cancelText=_('取消'),
                title=_('角色编辑'),
                visible=True,
                mask=False,
                id='role-mgmt-change-modal',
            ),
            fac.AntdModal(
                children=[
                    fac.AntdText(_('您确定要删除角色')),
                    fac.AntdText(
                        'xxxx',
                        id='role-mgmt-delete-role-name',
                        type='danger',
                        underline=True,
                    ),
                    fac.AntdText('?'),
                ],
                destroyOnClose=False,
                renderFooter=True,
                okText=_('确定'),
                cancelText=_('取消'),
                okButtonProps={'danger': True},
                title=_('确认要删除？'),
                visible=True,
                mask=False,
                id='role-mgmt-delete-affirm-modal',
            ),
        ],
        gap='small',
        wrap='wrap',
    )
