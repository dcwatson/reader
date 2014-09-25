from .models import LoginToken

class EmailTokenBackend (object):

    def authenticate(self, user_id=None, token=None):
        try:
            token_obj = LoginToken.objects.get(user__pk=user_id, token=token)
            return token_obj.user
        except LoginToken.DoesNotExist:
            return None

    def get_user(self, user_id):
        from django.contrib import auth
        User = auth.get_user_model()
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
