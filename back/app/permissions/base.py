from needs import Need
from werkzeug.exceptions import Unauthorized


class BaseNeed(Need):
    error = Unauthorized('''
        The server couldn\'t provide that resource with the credentials
        provided.  Check that you are logged in.
    ''')
