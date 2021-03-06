from flask.sessions import SecureCookieSession, SecureCookieSessionInterface


class Session(SecureCookieSession):
    @property
    def user(self):
        from app.lib.database import db
        from app.models.user import User
        return (db.session.query(User)
            .filter(User.id==self.get('user_id'))
            .first())

    def get_dictionary(self):
        return {'user_id': self.get('user_id')}


class SessionInterface(SecureCookieSessionInterface):
    session_class = Session
