"""
This module contains the APIRest of the Radifi System. It is composed with the class API, which
handle all the request received by the APIRest Flask server.
"""

import json

from flask_api import FlaskAPI
from flask import request, Response

from music.music_player import MusicPlayer
from output.lcd.lcd_manager import LCDManager
from planning.alarm_manager import AlarmManager
from planning.time_manager import TimeManager
from station.station_manager import StationManager


class API:
    """
    The class API represent all the entry points to Radifi service.
    Its handle all the request in a proper format and redirect them
    to the different manager class which conforms the Radifi service.
    """

    _DEFAULT_MIMETPYE = 'application/json'

    def __init__(self, player_manager: MusicPlayer,
                 station_manager: StationManager,
                 time_manager: TimeManager,
                 alarm_manager: AlarmManager,
                 lcd_manager: LCDManager):
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
            :type lcd_manager: LCDManager
            :param lcd_manager: The LCD output subsystem
        """

        self._app = FlaskAPI(__name__)
        self._player_manager = player_manager
        self._station_manager = station_manager
        self._time_manager = time_manager
        self._alarm_manager = alarm_manager
        self._lcd_manager = lcd_manager

    def start_api(self):
        """
        Runs the FlaskAPI server, starting the APIRest service.
        """
        self._define_station_routes()
        self._define_alarm_routes()
        self._define_time_routes()
        self._define_other_routes()
        self._app.run(debug=True, use_reloader=False, host='0.0.0.0')

    def _lcd_print_message(self, is_busy_player: bool, upper_message="") -> None:
        """
        Sends a text to the LCD manager to show different information regarding the status of the player.

        If the player is busy, send the name of the resource which is being played and executes a time updating.
        If the player is not busy, executes a time updating.

        ARGUMENTS:
            :param is_busy_player: True if the player is playing music.
            :type is_busy_player: bool
            :param upper_message: The message to be show in the upper panel of the LCD.
            :type upper_message: str
        """

        self._lcd_manager.is_busy_lcd = is_busy_player
        if is_busy_player:
            self._lcd_manager.print_message(upper_text=upper_message)
        TimeManager.print_lcd_time(self._lcd_manager)

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
            * Change station volume.
            * Play stop the streaming of a radio station.
        """

        @self._app.route('/station/volume', methods=['GET'])
        def get_volume():
            """
            Gets the current volume of the player. GET request.
            :return: A Response object, 200 status code if the volume were changed.
            :rtype Response
            """
            current_volume = self._player_manager.get_current_volume()
            status = 423
            res = {}
            if current_volume != -1 :
                current_volume_left, current_volume_right = current_volume
                volume_total = int((current_volume_left + current_volume_right) * 0.5)
                res = {
                    "volume_left" : current_volume_left,
                    "volume_right" : current_volume_right,
                    "volume" : volume_total

                   }
                status = 200
            return self._handle_http_response(res, status)


        @self._app.route('/station/volume', methods=['PUT'])
        def set_volume():
            """
            Sets the current volume of the player. PUT request.

            PARAMETERS:
                - name : volume
                  in: query
                  type: int
                  required: true
                  description: The desired volume.

            RETURN:
                :return: A Response object.
                :rtype: Response
            """
            if not request.json or 'volume' not in request.json:
                return self._handle_http_response("", 400)
            self._player_manager.set_current_volume(int(request.json["volume"]))
            return self._handle_http_response({}, 204)


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
            Get the information about a station

            RETURN:
                :return: A Response object. 200 status code if the station exists.
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
                station_info = self._station_manager.get_stations_list()[id_station]
                station_url = station_info['url']
                station_name = station_info['name']
                self._player_manager.play(station_url)
                is_played_successfully = self._player_manager.is_played_successfully()
                if is_played_successfully:
                    self._lcd_print_message(True, station_name)
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
            Lists all the streaming stations.

            RETURN:
                :return: A Response object. 200 status code if the station is playing.
                :rtype: Response
            """
            station_list = {"stations" : self._station_manager.get_stations_list()}

            return self._handle_http_response(station_list, 200)

        @self._app.route('/station/stations', methods=['DELETE'])
        def remove_all_stations():
            """
            Removes all the stations. A DELETE request is required.

            RETURN:
                :return: A Response object. 204 status code if all the stations were removed.
                :rtype: Response
            """
            is_removed = self._station_manager.remove_all_stations()

            if is_removed:
                self.save_stations_list()
                code = 204
            else:
                code = 400

            return self._handle_http_response({}, code)

    #
    # ENTRY POINTS FOR ALARM MANAGEMENT ROUTES
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
            res = {
                    'current_hour': current_alarm[0],
                    'current_minute': current_alarm[1],
                    'is_enabled': bool(current_alarm[2]),

                   }
            return self._handle_http_response(res, 200)

        @self._app.route('/alarm/station', methods=['GET'])
        def get_current_alarm_radio_station():
            """
            Get information about the current station selected as alarm,. GET request.

            RETURN:
                :return: A Response object.
                :rtype: Response
            """

            current_station = self._alarm_manager.get_current_alarm_radio_station()

            res = {
                'alarm_name': current_station[0],
                'alarm_url': current_station[1],

            }
            return self._handle_http_response(res, 200)

        @self._app.route('/alarm/station/<int:id_station>', methods=['PATCH'])
        def set_current_alarm_radio_station(id_station):
            """
            Sets the new alarm radio station.

            PARAMETERS:
                - name : id_station
                  in: query
                  type: int
                  required: true
                  description: The id of the station

            RETURN:

                :return: True if the radio station was set, false otherwise.
                :rtype: bool
            """

            if id_station < len(self._station_manager.get_stations_list()):
                station = self._station_manager.get_stations_list()[id_station]

                station_name = station["name"]
                station_url = station["url"]

                is_selected = self._alarm_manager.set_current_alarm_radio_station(station_name, station_url)
                self._alarm_manager.save_status()
                if is_selected:
                    status = 200
                    res = {'result': True}
                else:
                    status = 400
                    res = {'result': False}
            else:
                res = {'result': False}
                status = 404
            return self._handle_http_response(res, status)


        @self._app.route('/alarm', methods=['PUT'])
        def set_alarm():
            """
            Sets a new alarm. PUT request.

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
            hour = request.json['hour']
            minute = request.json['minute']
            if (hour < 0 or hour > 24) and (minute < 0 or minute > 59):
                return self._handle_http_response("", 400)
            self._alarm_manager.set_current_alarm(hour, minute)
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
            self._alarm_manager.toggle_alarm(False)
            self._alarm_manager.save_status()
            return self._handle_http_response("", 204)

        @self._app.route('/alarm', methods=['PATCH'])
        def enable_alarm():
            """
            Removes the current alarm. A DELETE request is required.

            RETURN:
                :return: A Response object. 204 status code if the station is playing.
                :rtype: Response
            """
            self._alarm_manager.toggle_alarm(True)
            self._alarm_manager.save_status()
            return self._handle_http_response("", 204)

        @self._app.route('/alarm/play', methods=['GET'])
        def play_alarm():
            """
            Starts playing the current alarm. A GET request is required.

            RETURN:
                :return: A Response object. 204 status code if the station is playing.
                  406 otherwise.
                :rtype: Response
            """

            self._player_manager.play_alarm(is_default_song=True)
            is_played = self._player_manager.is_played_successfully()
            if is_played:
                self._lcd_print_message(True, "ALARM!!!")
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
            if self._player_manager.stop_player():
                self._lcd_print_message(False)
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

        @self._app.route('/time', methods=['POST'])
        def set_current_time():
            """
            Updates the system time.

            RETURN:
                :return: A Response object. 200 status code with the current system time
                  as data response.
                :rtype: Response
            """
            self._time_manager.update_system_time()
            return self._handle_http_response({}, 200)

        @self._app.route('/time', methods=['PUT'])
        def set_specific_time_():
            """
            Updates the system time to a certain time.

            PARAMETERS:
                - name : year
                  in: request
                  type: int
                  required: true
                  description: The year to be set.

                - name : month
                  in: request
                  type: int
                  required: true
                  description: The month to be set.

                - name : day
                  in: request
                  type: int
                  required: true
                  description: The day to be set.

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
                :return: A Response object. 200 status code with the current system time
                  as data response.
                :rtype: Response
            """

            if not request.json or 'year' not in request.json or 'day' not in request.json or 'month' not in request.json:
                return self._handle_http_response("", 400)

            if not request.json or 'hour' not in request.json or 'minute' not in request.json:
                return self._handle_http_response("", 400)

            year = request.json['year']
            month = request.json['month']
            day = request.json['day']
            hour = request.json['hour']
            minute = request.json['minute']

            if year < 1970 or year > 9999:
                return self._handle_http_response("", 400)

            if month < 1 or month > 12:
                return self._handle_http_response("", 400)

            if day < 1 or day > 31:
                return self._handle_http_response("", 400)

            if (hour < 0 or hour > 24) and (minute < 0 or minute > 59):
                return self._handle_http_response("", 400)

            self._time_manager.set_system_time(year, month, day, hour, minute)
            return self._handle_http_response({}, 200)

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
