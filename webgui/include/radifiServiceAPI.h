#include<string>

using namespace std;


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

  bool addNewRadioStation(string& name, string& url);
private:

  string *host;
  string connectionURL;
  int port;
};
