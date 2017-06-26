from django.contrib.auth.backends import ModelBackend


class FacebookBackend(ModelBackend):
    def authenticate(self, request, facebook_id):
        pass

    def get_user(self, user_id):
        pass
