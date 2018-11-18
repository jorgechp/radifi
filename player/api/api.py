from flask_api import FlaskAPI


class API(object):

    def __init__(self, player):
        self.__app = FlaskAPI(__name__)
        self.__player = player

    def start_api(self):
        self.__define_routes()
        self.__app.run(debug=True)

    def __define_routes(self):
        @self.__app.route('/station/current/')
        def get_current_station():
            current_station = self.__player.get_current_station_url()
            # current_station = "No current station" if current_station == None else current_station
            return {'url': current_station}

        @self.__app.route('/station/<int:id>/play')
        def play_station():
            station_url = "https://www.radioalmaina.org/radio_almaina.m3u"
            is_played_succesfully = self.__player.play(station_url)
            return {'result': is_played_succesfully}

        @self.__app.route('/station/stop')
        def stop_station():
            self.__player.stop_sound()

        @self.__app.route('/station/stations')
        def list_stations():
            list_of_stations = list()
            return list_of_stations

        @self.__app.route('/alarm/current',  methods=['GET'])
        def get_current_alarm():
            pass

        @self.__app.route('/alarm/current',  methods=['POST'])
        def set_alarm():
            pass

        @self.__app.route('/alarm/current',  methods=['DELETE'])
        def remove_alarm():
            pass


        @self.__app.route('/time/current',  methods=['GET'])
        def get_current_time():
            pass

        @self.__app.route('/time/current',  methods=['POST'])
        def set_time():
            pass



