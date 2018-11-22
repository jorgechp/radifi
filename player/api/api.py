from flask_api import FlaskAPI
from flask import request, Response


class API(object):

    def __init__(self, player, station_manager,alarm_manager):
        self.__app = FlaskAPI(__name__)
        self.__player = player
        self.__station_manager = station_manager
        self.__alarm_manager = alarm_manager

    def start_api(self):
        self.__define_routes()
        self.__app.run(debug=True)

    def __define_routes(self):
        @self.__app.route('/station/current/',   methods=['GET'])
        def get_current_station():
            current_station = self.__player.get_current_station_url()
            if current_station != None:
                res = {'url': current_station}
                status = 200
            else:
                res = {}
                status = 404
            return Response(res, status=status, mimetype='application/json')

        @self.__app.route('/station/<int:id>',  methods=['GET'])
        def get_station_info(id):
            if(id < len(self.__station_manager.get_stations_list())):
                station = self.__station_manager.get_stations_list()[id]
                res = {'result': station}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return Response(res, status=status, mimetype='application/json')

        @self.__app.route('/station',  methods=['PUT'])
        def add_station():
            if not request.json or not 'name' in request.json or not 'url' in request.json:
                return Response({}, status=400, mimetype='application/json')

            url = request.json['url']
            name = request.json['name']
            id =  self.__station_manager.add_station(name,url)
            new_station = {}
            status = 409
            if id > -1:
                self.__station_manager.save_stations_list()

                new_station = {
                    'id' : id,
                    'name' : name,
                    'url' : url
                }
                status = 200
            return Response(new_station, status=status, mimetype='application/json')  # Throws a HTML ERROR CODE 409

        @self.__app.route('/station/<int:id>',  methods=['DELETE'])
        def remove_station(id):
            if(id < len(self.__station_manager.get_stations_list())):
                station = self.__station_manager.remove_station(id)
                self.__station_manager.save_stations_list()
                res = {'result': station}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return Response(res, status=status, mimetype='application/json')

        @self.__app.route('/station/<int:id>/play',  methods=['POST'])
        def play_station(id):
            if(id < len(self.__station_manager.get_stations_list())):
                station_url = self.__station_manager.get_stations_list()[id]['url']
                self.__player.play(station_url)
                is_played_successfully = self.__player.is_played_successfully()
                res = {'result': is_played_successfully}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return Response(res, status=status, mimetype='application/json')

        @self.__app.route('/station/stop',   methods=['POST'])
        def stop_station():
            is_deleted = self.__player.stop_sound()
            res = {'result': is_deleted}
            return Response(res, status=200, mimetype='application/json')

        @self.__app.route('/station/stations', methods=['GET'])
        def list_stations():
            return Response(self.__station_manager.get_stations_list(), status=200, mimetype='application/json')

        @self.__app.route('/alarm',  methods=['GET'])
        def get_current_alarm():
            current_alarm = self.__alarm_manager.get_current_alarm()
            res = {'current_alarm' : current_alarm}
            return Response(res, status=200, mimetype='application/json')

        @self.__app.route('/alarm',  methods=['PUT'])
        def set_alarm():
            if not request.json or not 'hour' in request.json or not 'minute' in request.json:
                return Response({}, status=400, mimetype='application/json')
            self.__alarm_manager.set_current_alarm(request.json['hour'])
            self.__alarm_manager.set_current_alarm(request.json['minute'])
            self.__alarm_manager.save_status()
            return Response("", status=200, mimetype='application/json')


        @self.__app.route('/alarm',  methods=['DELETE'])
        def remove_alarm():
            self.__alarm_manager.set_current_alarm("00:00:00")
            self.__alarm_manager.save_status()
            return Response("", status=200, mimetype='application/json')

        @self.__app.route('/alarm', methods=['PATCH'])
        def enable_alarm():
            if not request.json or not 'enabled' in request.json:
                return Response("", status=404, mimetype='application/json')
            if request.json['enabled'] == "yes" or request.json['enabled'] == "no":
                self.__alarm_manager.set_current_alarm(request.json['enabled'])
                self.__alarm_manager.save_status()
                return Response("", status=200, mimetype='application/json')
            return Response("", status=204, mimetype='application/json')


        @self.__app.route('/time/current',  methods=['GET'])
        def get_current_time():
            pass

        @self.__app.route('/time/current',  methods=['POST'])
        def set_time():
            pass



