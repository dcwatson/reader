from reader.models import LoginToken, User

class EmailTokenBackend (object):

    def authenticate(self, user_id=None, token=None):
        try:
            token_obj = LoginToken.objects.get(user__pk=user_id, token=token)
            user = token_obj.user
            token_obj.delete()
            return user
        except LoginToken.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
