#include<string>

using namespace std;

/**
* Class to represent radio Stations. A radio station consists on a
* station name and a station URL.
*/
#pragma once
class Station{
public:
  /**
  * Default constructor.
  * @param stationName The name of the station.
  * @param stationURL The URL of the station.
  */
  Station(const string &stationName,
          const string &stationURL
  );

  /**
  * Gets the station name.
  * @return A string type.
  */
  const string& getStationName(){
    return this->stationName;
  }

  /**
  * Get the station URL.
  * @return A string type.
  */
  const string& getStationURL(){
    return this->stationURL;
  }

  /**
  * Equal comparator
  */
  bool operator==(const Station& rhs){
    return this->stationName == rhs.stationName
      && this->stationName == rhs.stationName;
  }
private:
  string stationName; /* The station name */
  string stationURL; /* The station URL */

};
