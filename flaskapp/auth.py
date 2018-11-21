import functools
from flask_login import current_user, LoginManager, fresh_login_required
from flaskapp.database import Credential

login_manager = LoginManager()


def admin_required(func):
    @functools.wraps(func)
    def _admin_required(*args, **kw):
        admin = current_user.is_authenticated and current_user.is_admin
        if not admin:
            return login_manager.unauthorized()
        return func(*args, **kw)
    return _admin_required


@login_manager.user_loader
def load_user(user_id):
    credential = Credential.query.get(user_id)
    if credential is not None:
        credential._authenticated = True
    return credential
