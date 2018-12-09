#include <string>
#include <list>
#include <tuple>
#include <memory>

#include "station.h"

using namespace std;

typedef list<tuple<string,string>> listOfStationTuples;

/**
* This class represent a page, with a title header.
*/
#pragma once
class RadifiServiceAPI {
public:
  RadifiServiceAPI(string &host, int port);


  /**
  * Request the service to play a radio station.
  *@param radioStation The id of the radio to be played.
  *@return bool true if the radio is playing, false otherwise.
  */
  bool playRadioStation(const int radioStation);

  /**
  * Request the service to stop the current streaming.
  *@return bool true if the radio was stopped, false otherwise.
  */
  bool stopRadioStation();

  /**
  * Add a new Station to the station list of the service.
  * @param name The name of the new station to be added.
  * @param url The url of the new station to be addd.
  * @return true if the insertion were correct, false otherwise.
  */
  bool addNewRadioStation(string& name, string& url);

  /**
  * Send the service a request to remove a radio station.
  * @param idStation The id of the station to be removed
  * @return true if the station was removed, false otherwise.
  */
  bool removeRadioStation(unsigned int idStation);

  /**
  * Get a list of station data from the service. Each station
  * is represented by a tuple with the name and the url of the station.
  * tuple<string,string>.
  *
  * @param listToFill A list<tuple<string,string>> of stations to be filled.
  */
  void getStationList(listOfStationTuples& listToFill);

  /**
  * Set a new volume for the system.
  * @param volumeToSet the desired volume.
  * @return true if the volume were changed. false otherwise.
  */
  bool setCurrentVolume(const short& volumeToSet);

  /**
  * Gets the current volume.
  * @return short the current volume.
  */
  const short getCurrentVolume();

  /**
  * Get the current alarm time.
  *
  * @return A string with the current alarm. Format: "hh:mm"
  */
  const string getCurrentAlarm();

  /**
  * Set the current alarm time.
  *
  * @param alarmToSet string a const string reference. Format: "hh:mm"
  * @return bool True if the alarm were changed, false otherwise.
  */
  bool setCurrentAlarm(const string& alarmToSet);

  /**
  * Toggles the alarm.
  * @param isAlarmEnabled true to enable the alarm, false otherwise.
  * @return bool True if the alarm were changed, false otherwise.
  */
  bool setAlarmEnabled(bool isAlarmEnabled);

  /**
  * Gets the current alarm status.
  *
  * @return bool True if the alarm is enabled, false if the alarm is disabled.
  */
  bool isAlarmEnabled();

  /**
  * Gets the current station selected as Station Alarm.
  *
  * @return std::unique_ptr<Station> A Station instance of the current station.
  */
  std::unique_ptr<Station> getCurrentAlarmStation();

  /**
  * Sets the station Alarm.
  * @param stationToSet A reference to the station instance to be selected.
  * @return bool true if the new station were properly selected, false otherwise.
  */
  bool setCurrentAlarmStation(Station& stationToSet);

private:

  string *host;
  string connectionURL;
  int port;
};
