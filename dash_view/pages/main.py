import feffery_antd_components as fac
from dash_view.framework.aside import render_aside_content
from dash_view.framework.head import render_head_content
from dash_view.framework.func import render_func_content
from common.utilities.util_menu_access import MenuAccess
import feffery_utils_components as fuc
from flask_babel import gettext as _  # noqa
import dash_callback.pages.main_c  # noqa


def render_content(menu_access: MenuAccess):
    return fac.AntdRow(
        [
            # 功能组件注入
            *render_func_content(),
            # 菜单列
            fac.AntdCol(
                fac.AntdSider(
                    render_aside_content(menu_access),
                    collapsible=False,
                    collapsedWidth=60,
                    trigger=None,
                    id='menu-collapse-sider',
                ),
                flex='None',
                className={
                    'background': 'rgb( 43, 47, 58)',
                },
            ),
            # 内容列
            fac.AntdCol(
                [
                    # head块，包括菜单折叠、面包屑导航、用户信息、全局功能按钮
                    fac.AntdRow(
                        render_head_content(menu_access),
                        align='middle',
                        className={
                            'height': '50px',
                            'boxShadow': '0 1px 4px rgba(0,21,41,.08)',
                            'flex': 'None',
                        },
                    ),
                    # tabs块
                    fac.AntdRow(
                        fuc.FefferyDiv(
                            fac.AntdTabs(
                                id='tabs-container',
                                tabPaneAnimated=True,
                                size='small',
                                # fix bug: 占位
                                items=[
                                    {
                                        'label': '',
                                        'key': 'init',
                                        'children': 'init',
                                    }
                                ],
                                type='editable-card',
                                className={
                                    'width': '100%',
                                    'height': '100%',
                                    'paddingLeft': '8px',
                                    'paddingRight': '8px',
                                },
                            ),
                            className={
                                'width': '100%',
                                'height': '100%',
                                '& .ant-tabs-content-holder > .ant-tabs-content': {
                                    'height': 'calc(100% - 10px)',  # 不知道为什么溢出了一部分，减去10像素
                                },
                                '& .ant-tabs-content-holder > .ant-tabs-content > .ant-tabs-tabpane': {
                                    'height': '100%',
                                },
                                '& .ant-tabs-nav': {
                                    'margin': '8px 0 8px 0',
                                },
                            },
                        ),
                        className={'flex': '1'},
                    ),
                ],
                flex='auto',
                className={'display': 'flex', 'flexDirection': 'column'},
            ),
        ],
        className={'width': '100vw', 'height': '100vh'},
        id='global-full-screen-container',
    )
