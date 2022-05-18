from instaclone.celery import app

# TODO: EXPLORE LOGGERS AND DEBUGGING IN CELERY


@app.task(name='sum_two_numbers')
def add(x, y):
    return x+y


@app.task(name='process_media')
def process_media(post_id):
    pass



