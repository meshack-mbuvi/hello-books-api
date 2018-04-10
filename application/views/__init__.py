from application import jwt
# To be used for storing blacklisted tokens
blacklist = set()
users_table = {}
books_in_api = {}


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist