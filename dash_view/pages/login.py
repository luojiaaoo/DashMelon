import feffery_utils_components as fuc
import feffery_antd_components as fac
from config.dash_melon_conf import ShowConf, JwtConf, LoginConf
from dash import dcc
import dash_callback.pages.login_c  # noqa


def render_content():
    return fuc.FefferyDiv(
        children=[
            fuc.FefferyDiv(
                id='login-container',
                children=[
                    fuc.FefferyDiv(
                        children=ShowConf.APP_NAME,
                        className={
                            'font-weight': 'bold',
                            'letter-spacing': '2px',
                            'font-family': "'Microsoft YaHei', sans-serif",
                            'font-size': '30px',
                            'height': '15%',
                            'display': 'flex',
                            'justify-content': 'center',
                            'align-items': 'center',
                            'color': 'rgb(245,245,245)',
                            'padding': '20px 0 0 0',
                        },
                    ),
                    fac.AntdTabs(
                        items=[
                            {
                                'key': '账号密码登录',
                                'label': fac.AntdText(
                                    '账号密码登录',
                                    className={
                                        'color': 'rgb(22,119,255)',
                                    },
                                ),
                                'children': [
                                    fac.AntdSpace(
                                        [
                                            fac.AntdForm(
                                                [
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='login-username',
                                                            prefix=fac.AntdIcon(icon='antd-user'),
                                                            placeholder='请输入用户名',
                                                            className={
                                                                'margin-top': '20px',
                                                            },
                                                        ),
                                                        className={'margin-bottom': 0},
                                                    ),
                                                    fac.AntdFormItem(
                                                        fac.AntdInput(
                                                            id='login-password',
                                                            prefix=fac.AntdIcon(icon='antd-lock'),
                                                            mode='password',
                                                            passwordUseMd5=True,
                                                            placeholder='请输入密码',
                                                            className={
                                                                'margin-top': '25px',
                                                            },
                                                        ),
                                                        className={'margin-bottom': 0},
                                                    ),
                                                ],
                                            ),
                                            fac.AntdFlex(
                                                [
                                                    fac.AntdInput(
                                                        id='login-verify-code-input',
                                                        prefix=fac.AntdIcon(icon='antd-right'),
                                                        placeholder='请输入验证码',
                                                        allowClear=True,
                                                        className={
                                                            'margin-right': '20px',
                                                        },
                                                    ),
                                                    fuc.FefferyCaptcha(
                                                        id='login-verify-code-pic',
                                                        width=100,
                                                        charNum=LoginConf.VERIFY_CODE_CHAR_NUM,
                                                    ),
                                                ],
                                                id='login-verify-code-container',
                                                className={
                                                    'margin-top': '20px',
                                                },
                                                style={
                                                    'display': 'None',
                                                },
                                            ),
                                            fac.AntdCheckbox(
                                                id='login-keep-login-status',
                                                label=f'保持{f"{JwtConf.JWT_EXPIRE_MINUTES//60}小时" if JwtConf.JWT_EXPIRE_MINUTES//60<24 else f"{JwtConf.JWT_EXPIRE_MINUTES//60//24}天"}免登录',
                                                checked=False,
                                                className={
                                                    'margin-top': '10px',
                                                    'font-weight': 'bold',
                                                    'letter-spacing': '2px',
                                                    'font-family': "'Microsoft YaHei', sans-serif",
                                                    'font-size': '12px',
                                                    'color': 'rgb(245,245,245)',
                                                },
                                            ),
                                            fac.AntdButton(
                                                '登录',
                                                id='login-submit',
                                                type='primary',
                                                block=True,
                                                className={
                                                    'margin-top': '35px',
                                                    'height': '3em',
                                                    'border-radius': '1.5em',
                                                },
                                            ),
                                            dcc.Store(id='login-store-need-vc', storage_type='local'),
                                            dcc.Store(id='login-store-fc', storage_type='local'),
                                            fuc.FefferyTimeout(id='timeout-trigger-verify-code', delay=0),
                                            dcc.Location(id='login-location-no-refresh', refresh=False),
                                            fac.Fragment(id='login-location-refresh-container'),
                                            dcc.Store(id='login-password-sha256'),
                                            fac.Fragment(id='login-message-container'),
                                        ],
                                        direction='vertical',
                                        className={
                                            'width': '100%',
                                        },
                                    )
                                ],
                            },
                        ],
                        className={
                            'height': '85%',
                            'width': '90%',
                        },
                    ),
                ],
                className={
                    'width': 'max(25%,300px)',
                    'height': 'max(40%,600px)',
                    'margin-right': '15%',
                    'backdrop-filter': 'blur(10px)',
                    'background-color': 'rgba(0, 0, 0, 0.15)',
                    'border-radius': '10px',
                    'display': 'flex',
                    'flex-direction': 'column',
                    'justify-content': 'center',
                    'align-items': 'center',
                    'box-shadow': '0 10px 20px rgba(0, 0, 0, 0.4)',
                    'border': '1px solid rgba(255, 255, 255, 0.4)',
                    'animation': 'float 2s ease-in-out infinite',
                },
            ),
        ],
        className={
            'display': 'flex',
            'background-image': 'url("/assets/imgs/login_background.jpeg")',
            'background-size': 'cover',
            'background-position': 'center center',
            'background-attachment': 'fixed',
            'background-repeat': 'no-repeat',
            'width': '100vw',
            'height': '100vh',
            'justify-content': 'flex-end',
            'align-items': 'center',
            '.ant-input-affix-wrapper, .ant-tabs-tab .ant-typography, .ant-btn': {
                'letter-spacing': '2px',
                'font-family': "'Microsoft YaHei', sans-serif",
                'font-size': '18px',
                'width': '100%',
                'padding': '10px 10px',
            },
        },
    )
