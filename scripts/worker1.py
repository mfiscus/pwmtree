from flask import Flask

app = Flask(__name__)
app.config.update(
    CELERY_BROKER_URL='zeromq://localhost:6379',
    CELERY_RESULT_BACKEND='zeromq://localhost:6379'
)
celery = make_celery(app)


@celery.task()
def add_together(a, b):
    return a + b