import json

from flask_api import FlaskAPI
from flask import request, Response


class API(object):

    def __init__(self, player, station_manager,time_manager,alarm_manager):
        self._app = FlaskAPI(__name__)
        self._player = player
        self._station_manager = station_manager
        self._time_manager = time_manager
        self._alarm_manager = alarm_manager

    def start_api(self):
        self.__define_routes()
        self._app.run(debug=True)

    def _handle_http_response(self, data_response, html_code = 200):
        mimetype = 'application/json'
        if data_response == "":
            return Response({}, status=html_code, mimetype=mimetype)
        else:
            data_as_json = json.dumps(data_response, ensure_ascii=False)
            return Response(data_as_json, status=html_code, mimetype=mimetype)

    def __define_routes(self):
        @self._app.route('/station/current/', methods=['GET'])
        def get_current_station():
            current_station = self._player.get_current_station_url()
            if current_station != None:
                res = {'url': current_station}
                status = 200
            else:
                res = {}
                status = 404
            return self._handle_http_response(res, status)

        @self._app.route('/station/<int:id>', methods=['GET'])
        def get_station_info(id):
            if(id < len(self._station_manager.get_stations_list())):
                station = self._station_manager.get_stations_list()[id]
                res = {'result': station}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return self._handle_http_response(res, status)

        @self._app.route('/station', methods=['PUT'])
        def add_station():
            if not request.json or not 'name' in request.json or not 'url' in request.json:
                return Response({}, status=400, mimetype='application/json')

            url = request.json['url']
            name = request.json['name']
            id =  self._station_manager.add_station(name, url)
            new_station = {}
            status = 409   # Throws a HTML ERROR CODE 409
            if id > -1:
                self._station_manager.save_stations_list()

                new_station = {
                    'id' : id,
                    'name' : name,
                    'url' : url
                }
                status = 200
            return self._handle_http_response(new_station, status)

        @self._app.route('/station/<int:id>', methods=['DELETE'])
        def remove_station(id):
            if(id < len(self._station_manager.get_stations_list())):
                station = self._station_manager.remove_station(id)
                self._station_manager.save_stations_list()
                res = {'result': station}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return self._handle_http_response(res, status)

        @self._app.route('/station/<int:id>/play', methods=['POST'])
        def play_station(id):
            if(id < len(self._station_manager.get_stations_list())):
                station_url = self._station_manager.get_stations_list()[id]['url']
                self._player.play(station_url)
                is_played_successfully = self._player.is_played_successfully()
                res = {'result': is_played_successfully}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return self._handle_http_response(res, status)

        @self._app.route('/station/stop', methods=['POST'])
        def stop_station():
            is_deleted = self._player.stop_sound()
            res = {'result': is_deleted}
            return self._handle_http_response(res, 200)

        @self._app.route('/station/stations', methods=['GET'])
        def list_stations():
            return Response(self._station_manager.get_stations_list(), status=200, mimetype='application/json')

        @self._app.route('/alarm', methods=['GET'])
        def get_current_alarm():
            current_alarm = self._alarm_manager.get_current_alarm()
            res = {'current_alarm' : current_alarm}
            return self._handle_http_response(res, 200)

        @self._app.route('/alarm', methods=['PUT'])
        def set_alarm():
            if not request.json or not 'hour' in request.json or not 'minute' in request.json:
                return self._handle_http_response("", 400)
            self._alarm_manager.set_current_alarm(request.json['hour'])
            self._alarm_manager.set_current_alarm(request.json['minute'])
            self._alarm_manager.save_status()
            return self._handle_http_response("", 204)


        @self._app.route('/alarm', methods=['DELETE'])
        def remove_alarm():
            self._alarm_manager.set_current_alarm("00:00:00")
            self._alarm_manager.save_status()
            return self._handle_http_response("", 204)

        @self._app.route('/alarm', methods=['PATCH'])
        def enable_alarm():
            if not request.json or not 'enabled' in request.json:
                return self._handle_http_response("", 404)
            if request.json['enabled'] == "yes" or request.json['enabled'] == "no":
                self._alarm_manager.set_current_alarm(request.json['enabled'])
                self._alarm_manager.save_status()
                return self._handle_http_response("", 200)
            return self._handle_http_response("", 400)

        @self._app.route('/alarm/play', methods=['GET'])
        def play_alarm():
            if not request.args or not 'defaultSong' in request.args:
                is_default_song = 0
            else:
                is_default_song = request.args.get('defaultSong')
            is_default_song_as_boolean = bool(is_default_song)
            self._player.play_alarm(is_default_song_as_boolean)
            is_played = self._player.is_played_successfully()
            if is_played:
                return self._handle_http_response("", 204)
            else:
                return self._handle_http_response("", 406)

        @self._app.route('/alarm/stop', methods=['GET'])
        def stop_alarm():
            self._player.stop_player()
            return self._handle_http_response("", 204)

        @self._app.route('/time', methods=['GET'])
        def get_current_time():
            current_time = self._time_manager.get_current_time()
            res = {"time" : str(current_time)}
            return self._handle_http_response(res, 200)