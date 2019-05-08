import hashlib
import bcrypt
from datetime import datetime, timedelta

async def create_path(seq, level):
    seq = str(seq).zfill(level*2)
    return '/'.join([seq[i:i+level] for i in range(0, len(seq), level)])

async def hash_path(val):
    blake2s = hashlib.blake2s(digest_size=4)
    blake2s.update(val.encode())
    return blake2s.hexdigest()

async def get_time(sec):
    if int(sec) > 2147483647:
        sec = 2147483647
    sec = timedelta(seconds=int(sec))
    d = datetime(1,1,1) + sec

    return "%d days %02d hours %02d min %02d sec" % (d.day-1, d.hour, d.minute, d.second)

async def get_size(size):
    size = int(size)
    power = 2 ** 10
    n = 0
    sufix = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB', 4: 'TB'}
    while size > power:
        size /= power
        n += 1
    return '{:.1f}'.format(round(size, 1))  + " " + sufix[n]


async def generate_password_hash(password):
    password_bin = password.encode('utf-8')
    hashed = bcrypt.hashpw(password_bin, bcrypt.gensalt())
    return hashed.decode('utf-8')


async def check_password_hash(plain_password, password_hash):
    plain_password_bin = plain_password.encode('utf-8')
    password_hash_bin = password_hash.encode('utf-8')
    is_correct = bcrypt.checkpw(plain_password_bin, password_hash_bin)
    return is_correct