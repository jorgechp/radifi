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
  */
  void getStationList(listOfStationTuples& listToFill);

private:

  string *host;
  string connectionURL;
  int port;
};
