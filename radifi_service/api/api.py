"""
This module contains the APIRest of the Radifi System. It is composed with the class API, which
handle all the request received by the APIRest Flask server.
"""

import json

from flask_api import FlaskAPI
from flask import request, Response


class API:
    """
    The class API represent all the entry points to Radifi service.
    Its handle all the request in a proper format and redirect them
    to the different manager class which conforms the Radifi service.
    """

    _DEFAULT_MIMETPYE = 'application/json'

    def __init__(self, player_manager, station_manager, time_manager, alarm_manager):
        """
        Constructor of the class.

        ARGUMENTS:
            :type player_manager: MusicPlayer
            :param player_manager: The player subsystem
            :type station_manager: StationManager
            :param station_manager: The station subsystem
            :type time_manager: TimeManager
            :param time_manager: The Time subsystem
            :type alarm_manager: AlarmManager
            :param alarm_manager: The alarm subsystem
        """
        self._app = FlaskAPI(__name__)
        self._player_manager = player_manager
        self._station_manager = station_manager
        self._time_manager = time_manager
        self._alarm_manager = alarm_manager

    def start_api(self):
        """
        Runs the FlaskAPI server, starting the APIRest service.
        """
        self._define_station_routes()
        self._define_alarm_routes()
        self._define_time_routes()
        self._define_other_routes()
        self._app.run(debug=True)

    @staticmethod
    def _handle_http_response(data_response: object, html_code: int = 200) -> Response:
        """
        Return a Http request with provided data and html status code. For more information
        about status code, please refer to
        http://www.iana.org/assignments/http-status-codes/http-status-codes.xhtml

        This method is static.

        ARGUMENTS:
            :param data_response: JSON array
            :type data_response: json
            :param html_code: HTTP status code
            :type html_code: int
        RETURN:
            :return: A Response instance
            :rtype: Response
        """

        if data_response == "":
            return Response({}, status=html_code, mimetype=API._DEFAULT_MIMETPYE)

        data_as_json = json.dumps(data_response, ensure_ascii=False)
        return Response(data_as_json, status=html_code, mimetype=API._DEFAULT_MIMETPYE)

    #
    # ENTRY POINTS FOR STATION MANAGMENT ROUTES
    #
    def _define_station_routes(self):
        """
        Define entry points functions related with the station management.
        The station management requires:

            * CRUD methods for the station list.
            * Check the current station.
            * Change the station to play.
            * Play stop the streaming of a radio station.
        """

        @self._app.route('/station/current/', methods=['GET'])
        def get_current_station():
            """
            Checks the current status of the Redifi service.

            RETURN:
            :return: A Response object. 200 status code if there is a station being played.
                400 otherwise.
            :rtype: Response
            """
            current_station = self._player_manager.get_current_station_url()
            if current_station is not None:
                res = {'url': current_station}
                status = 200
            else:
                res = {}
                status = 404
            return self._handle_http_response(res, status)

        @self._app.route('/station/<int:id_station>', methods=['GET'])
        def get_station_info(id_station):
            """
            Get the information about the station that is playing.

            RETURN:
                :return: A Response object. 200 status code if there is a station being played.
                400 otherwise.
                :rtype: Response
            """
            if id_station < len(self._station_manager.get_stations_list()):
                station = self._station_manager.get_stations_list()[id_station]
                res = {'result': station}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return self._handle_http_response(res, status)

        @self._app.route('/station', methods=['PUT'])
        def add_station():
            """
            Add a new radio station. A radio station is composed by a radio station name
            and the URL. Parameters must be sent using a PUT request.

            PARAMETERS:
                - name : name
                  in: query
                  type: string
                  required: true
                  description: The radio station name

                - name : url
                  in: query
                  type: string
                  required: true
                  description: The radio station url.

            RETURN:
                :return: A Response object. 200 status code if the new station was added properly.
                409 otherwise.
                :rtype: Response
            """
            if not request.json or 'name' not in request.json or 'url' not in request.json:
                return Response({}, status=400, mimetype='application/json')

            url = request.json['url']
            name = request.json['name']
            id_station = self._station_manager.add_station(name, url)
            new_station = {}
            status = 409  # Throws a HTML ERROR CODE 409
            if id_station > -1:
                self._station_manager.save_stations_list()

                new_station = {
                    'id': id_station,
                    'name': name,
                    'url': url
                }
                status = 200
            return self._handle_http_response(new_station, status)

        @self._app.route('/station/<int:id_station>', methods=['DELETE'])
        def remove_station(id_station):
            """
            Removes a radio station from the radifi service.
            Parameter must be sent using a DELETE request.

            PARAMETERS:
                - name : id_station
                  in: path
                  type: int
                  required: true
                  description: The id of the station name

            RETURN:
                :return: A Response object. 200 status code if the station was removed.
                404 if there is not a radio station with that id.
                :rtype: Response
            """
            if id_station < len(self._station_manager.get_stations_list()):
                station = self._station_manager.remove_station(id_station)
                self._station_manager.save_stations_list()
                res = {'result': station}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return self._handle_http_response(res, status)

        @self._app.route('/station/<int:id_station>/play', methods=['POST'])
        def play_station(id_station):
            """
            Starts playing a radio streaming. A POST request must be performed.

            PARAMETERS:
                - name : id_station
                  in: path
                  type: int
                  required: true
                  description: The id of the station name

            ARGUMENTS:
            :param id_station: The id of the station name
            :type id_station: int

            RETURN:
                :return: A Response object. 200 status code if the station is playing.
                404 if there is not a radio station with that id.
                :rtype: Response
            """
            num_of_stations = len(self._station_manager.get_stations_list())
            if id_station < num_of_stations:
                station_url = self._station_manager.get_stations_list()[id_station]['url']
                self._player_manager.play(station_url)
                is_played_successfully = self._player_manager.is_played_successfully()
                res = {'result': is_played_successfully}
                status = 200
            else:
                res = {'result': False}
                status = 404
            return self._handle_http_response(res, status)

        @self._app.route('/station/stop', methods=['POST'])
        def stop_station():
            """
            Stops the streaming service. A POST request must be performed.

            RETURN:
                :return: A Response object. 200 status code if the station is playing.
                :rtype: Response
            """
            is_stopped = self._player_manager.stop_player()
            res = {'result': is_stopped}
            return self._handle_http_response(res, 200)

        @self._app.route('/station/stations', methods=['GET'])
        def list_stations():
            """
            Stops the straming service. A GET request must be performed.

            RETURN:
                :return: A Response object. 200 status code if the station is playing.
                :rtype: Response
            """
            station_list = self._station_manager.get_stations_list()
            return self._handle_http_response(station_list, 200)

    #
    # ENTRY POINTS FOR ALARM MANAGMENT ROUTES
    #
    def _define_alarm_routes(self):
        """
        Define entry points functions related with the alarm management.
        The alarm management requires:

            * CRUD methods for the system alarm.
            * Play the alarm
            * Stop the alarm
            * Change the station to play.
        """

        @self._app.route('/alarm', methods=['GET'])
        def get_current_alarm():
            """
            Get information about the current alarm. GET request.

            RETURN:
                :return: A Response object. 200 status code if the station is playing.
                :rtype: Response
            """
            current_alarm = self._alarm_manager.get_current_alarm()
            res = {'current_alarm': current_alarm}
            return self._handle_http_response(res, 200)

        @self._app.route('/alarm', methods=['PUT'])
        def set_alarm():
            """
            Get information about the current alarm. PUT request.

            PARAMETERS:
                - name : hour
                  in: request
                  type: int
                  required: true
                  description: The hour to be set.

                - name : minute
                  in: request
                  type: int
                  required: true
                  description: The minute to be set.
            RETURN:
                :return: A Response object. 200 status code if the station is playing.
                :rtype: Response
            """
            if not request.json or 'hour' not in request.json or 'minute' not in request.json:
                return self._handle_http_response("", 400)
            self._alarm_manager.set_current_alarm(request.json['hour'])
            self._alarm_manager.set_current_alarm(request.json['minute'])
            self._alarm_manager.save_status()
            return self._handle_http_response("", 204)

        @self._app.route('/alarm', methods=['DELETE'])
        def remove_alarm():
            """
            Removes the current alarm. A DELETE request is required.

            RETURN:
                :return: A Response object. 204 status code if the station is playing.
                :rtype: Response
            """
            self._alarm_manager.set_current_alarm("00:00:00")
            self._alarm_manager.save_status()
            return self._handle_http_response("", 204)

        @self._app.route('/alarm', methods=['PATCH'])
        def enable_alarm():
            """
            Enable or Disable the current alarm. A PATCH request is required.

            PARAMETERS:
                - name : enabled
                  in: request
                  type: bool
                  required: true
                  description: True if the alarm must be enabled, False otherwise.

            RETURN:
                :return: A Response object. 204 status code if the station is playing.
                   400 otherwise.
                :rtype: Response
            """
            if not request.json or 'enabled' not in request.json:
                return self._handle_http_response("", 404)
            if request.json['enabled'] == "yes" or request.json['enabled'] == "no":
                self._alarm_manager.set_current_alarm(request.json['enabled'])
                self._alarm_manager.save_status()
                return self._handle_http_response("", 200)
            return self._handle_http_response("", 400)

        @self._app.route('/alarm/play', methods=['GET'])
        def play_alarm():
            """
            Starts playing the current alarm. A GET request is required.

            PARAMETERS:
                - name : defaultSong
                  in: request
                  type: int
                  required: false
                  description: 1 if we want to play the default song. 0 if we want to play the
                    radio station set as Alarm.

            RETURN:
                :return: A Response object. 204 status code if the station is playing.
                  406 otherwise.
                :rtype: Response
            """
            if not request.args or 'defaultSong' not in request.args:
                is_default_song = 0
            else:
                is_default_song = request.args.get('defaultSong')
            is_default_song_as_boolean = bool(is_default_song)
            self._player_manager.play_alarm(is_default_song_as_boolean)
            is_played = self._player_manager.is_played_successfully()
            if is_played:
                return self._handle_http_response("", 204)

            return self._handle_http_response("", 406)

        @self._app.route('/alarm/play', methods=['DELETE'])
        def stop_alarm():
            """
            Stop playing the current alarm. A DELETE request is required.

            RETURN:
                :return: A Response object. 204 status code if the station has been stopped.
                :rtype: Response
            """
            self._player_manager.stop_player()
            return self._handle_http_response("", 204)

    #
    # ENTRY POINTS FOR TIME MANAGMENT ROUTES
    #
    def _define_time_routes(self):
        """
        Define entry points functions related with the time management.
        The time management requires entry points for:

            * Get the current default system time.
        """

        @self._app.route('/time', methods=['GET'])
        def get_current_time():
            """
            Get the current default system time..

            RETURN:
                :return: A Response object. 200 status code with the current system time
                  as data response.
                :rtype: Response
            """
            current_time = self._time_manager.get_current_time()
            res = {"time": str(current_time)}
            return self._handle_http_response(res, 200)

    #
    # ENTRY POINTS FOR OTHER ROUTES
    #
    def _define_other_routes(self):
        """
        Define entry points for other types or functionality:

            * Shows the Welcome Message at the index page.
        """

        @self._app.route('/')
        def get_home_page():
            """
            Returns the home initial message when no entry point is defined.

            RETURNS:
            :return: A string with a welcome message.
            :rtype: str
            """
            return "Hello, World!"
