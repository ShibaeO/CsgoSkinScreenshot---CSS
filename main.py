import redis
from flask import Flask, request
from flask import jsonify, send_from_directory
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from worker import main
from config import huey

r = redis.Redis(host='localhost', port=6379, db=0)

app = Flask(__name__)

limiter = Limiter(app,
                  key_func=get_remote_address,
                  )
limiter.init_app(app)


@app.route("/inspect")
@limiter.limit("25/minute")
def index():
    if request.args.get("n"):

        a = request.args.get("n").split(" ")
        url = f"{a[0]}+{a[1]}%20{a[2]}"
        id = a[2]

        if len(url) < 110:
            return jsonify(success=False,
                           error="Invalid link provided",
                           total_screenshot=int(r.get('total_scr')),
                           queue_lenght=int(r.get('queue')),
                           inspect_link=url,
                           )
        else:

            r.incr("queue")
            main(url, id)

            return jsonify(success=True,
                           total_screenshot=int(r.get('total_scr')),
                           queue_lenght=int(r.get('queue')),
                           inspect_link=request.args.get("n"),
                           image_link=f"http://shibaeo.quetel.pro:5000/image/{id}.png",
                           )

    return jsonify(success=False,
                   error="No inspect link provided",
                   total_screenshot=int(r.get('total_scr')),
                   queue_lenght=int(r.get('queue')),
                   )


@app.route("/image/<path:filename>")
def show_image(filename):
    return send_from_directory("scr", filename, mimetype='image/jpeg', )


@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify(success=False,
                   error="Too many request calm down :)",
                   total_screenshot=int(r.get('total_scr')),
                   queue_lenght=int(r.get('queue')),
                   var=f"{e}",
                   )


if __name__ == "__main__":
    app.run(host="192.168.1.30")
