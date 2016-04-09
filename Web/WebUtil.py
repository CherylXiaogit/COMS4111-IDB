from flask import make_response

def set_cookie_redirct(cookie_key, cookie_val, redirct_url):
    resp = make_response(redirect(redirct_url))
    resp.set_cookie(cookie_key, cookie_val)
    return resp