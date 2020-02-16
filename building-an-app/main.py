import datetime
import beats
import weather_data
import pygame
# import play_midi

from flask import Flask, render_template, request
from google.cloud import datastore

app = Flask(__name__)


@app.route('/', methods=["GET", "POST"])
def index():
    city = ""
    weather = weather_data.WeatherData("chicago", "city")
    if request.method == 'POST':
        city = request.form.get("city_holder", None)
        weather = weather_data.WeatherData(city, "city")
        #times = NULL
        #weather = NULL

        beats.play(weather_data.WeatherData(city, "city"))

        def play_but_for_real():
            #pygame.mixer.pre_init(44100, 16, 2, 4096)
            pygame.init()

            pygame.mixer.music.load("./music.mid")
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.wait(1000)

        play_but_for_real()
    
    return render_template('index.html', weather=weather)

   


def root():
    # Store the current access time in Datastore.
    store_time(datetime.datetime.now())

    # Fetch the most recent 10 access times from Datastore.
    times = fetch_times(10)

    weather = weather_data.WeatherData("chicago", "city")

    return render_template(
        'index.html', times=times, weather=weather)


datastore_client = datastore.Client()

def fetch_times(limit):
    query = datastore_client.query(kind='visit')
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times

def store_time(dt):
    entity = datastore.Entity(key=datastore_client.key('visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)