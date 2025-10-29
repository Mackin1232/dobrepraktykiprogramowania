import bcrypt


hashed_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt())

USERS_DB = {
    "admin": hashed_pw
}