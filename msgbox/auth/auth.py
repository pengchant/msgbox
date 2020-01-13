import datetime

import jwcrypto.jwk as jwk
import python_jwt as jwt

key = jwk.JWK.generate(kty='oct', size=256)


class JWTUtils:
    """
    通过JWT来生成token，校验访问者的信息
    """

    @staticmethod
    def encode_auth_token(user_id, login_time, timedela=None):
        """
        生成认证token
        :param user_id: int 用户编号/其他的标识
        :param login_time: int(timestamp) 登录时间
        :return: string
        """
        try:
            payload = {'usr_id': user_id, 'login_time': login_time}
            if timedela is None:
                timedela = datetime.timedelta(days=7)  # 默认为7天后失效
            token = jwt.generate_jwt(payload, key, 'HS256', timedela)
            return token
        except Exception as e:
            return None

    @staticmethod
    def decode_auth_token(auth_token):
        """
        验证token
        :param auth_token: string 待校验的token
        :return: (tuple)|none   如果校验成功则返回usrid和logintime的元组
        """
        try:
            _, playload = jwt.verify_jwt(auth_token, key, ['HS256'])
            if 'usr_id' in playload and 'login_time' in playload:
                return playload['usr_id'], playload['login_time']
            else:
                return None
        except Exception as e:
            return None
