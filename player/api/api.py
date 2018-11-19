from flask_api import FlaskAPI


class API(object):

    def __init__(self, player, station_manager):
        self.__app = FlaskAPI(__name__)
        self.__player = player
        self.__station_manager = station_manager

    def start_api(self):
        self.__define_routes()
        self.__app.run(debug=True)

    def __define_routes(self):
        @self.__app.route('/station/current/',   methods=['GET'])
        def get_current_station():
            current_station = self.__player.get_current_station_url()
            if current_station != None:
                return {'url': current_station}
            else:
                return {}

        @self.__app.route('/station/<int:id>',  methods=['GET'])
        def get_station_info(id):
            if(id < len(self.__station_manager.get_stations_list())):
                station = self.__station_manager.get_stations_list()[id]
                return {'result': station}
            else:
                return {'result': False}

        @self.__app.route('/station/<int:id>',  methods=['DELETE'])
        def remove_station(id):
            if(id < len(self.__station_manager.get_stations_list())):
                station = self.__station_manager.remove_station(id)
                return {'result': station}
            else:
                return {'result': False}

        @self.__app.route('/station/<int:id>/play',  methods=['POST'])
        def play_station(id):
            if(id < len(self.__station_manager.get_stations_list())):
                station_url = self.__station_manager.get_stations_list()[id]['url']
                self.__player.play(station_url)
                is_played_successfully = self.__player.is_played_successfully()
                return {'result': is_played_successfully}
            else:
                return {'result': False}

        @self.__app.route('/station/stop',   methods=['POST'])
        def stop_station():
            is_deleted = self.__player.stop_sound()
            return {'result': is_deleted}

        @self.__app.route('/station/stations', methods=['GET'])
        def list_stations():
            return self.__station_manager.get_stations_list()

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



