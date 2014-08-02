import config

def listing(**k):
    return config.DB.select('items', **k)

def dating(**k):
    return config.DB.select('date_name', **k)

def naming(**k):
    return config.DB.select('server_name', **k)
