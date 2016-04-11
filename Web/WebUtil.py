from flask import make_response

def set_cookie_redirct(cookie_key, cookie_val, redirct_url):
    resp = make_response(redirect(redirct_url))
    resp.set_cookie(cookie_key, cookie_val)
    return resp

def delete_existing_user_cookie(resp):
    resp.set_cookie('username', '', expires=0)
    resp.set_cookie('email', '', expires=0)
    resp.set_cookie('user_id', '', expires=0)
