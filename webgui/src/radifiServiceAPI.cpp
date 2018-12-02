#include <memory>
#include <string>
#include <list>
#include <iostream>

#include "restclient-cpp/restclient.h"
#include "radifiServiceAPI.h"
#include "station.h"
#include "json.hpp"

using namespace std;

typedef list<tuple<string,string>> listOfStationTuples;



RadifiServiceAPI::RadifiServiceAPI(string &host, int port){
  this->host = &host;
  this->port = port;
  this->connectionURL = host + ":" + std::to_string(port);
}


bool RadifiServiceAPI::playRadioStation(const int radioStation){
  string requestURL = this->connectionURL
                      + "/station/"
                      + std::to_string(radioStation)
                      + "/"
                      + "play";

  RestClient::Response response = RestClient::post(requestURL,"application/json","{}");

  if(response.code == 200) return true;
  return false;
}

bool RadifiServiceAPI::stopRadioStation(){
  string requestURL = this->connectionURL
                      + "/station/stop";

  RestClient::Response response = RestClient::post(requestURL,"application/json","{}");

  if(response.code == 200) return true;

  return false;
}

bool RadifiServiceAPI::addNewRadioStation(string& name, string& url){
  string requestURL = this->connectionURL
                      + "/station";
  string jsonRequest = "{\"name\":\"" + name +"\", "
                      + "\"url\": \"" + url + "\"}";

  RestClient::Response response = RestClient::put(requestURL,"application/json",jsonRequest);

  if(response.code == 200) return true;

  return false;
}

bool RadifiServiceAPI::removeRadioStation(unsigned int idStation){
  string requestURL = this->connectionURL
                      + "/station/"
                      + std::to_string(idStation);
  RestClient::Response response = RestClient::del(requestURL);
  return response.code == 200;  
}

void RadifiServiceAPI::getStationList(listOfStationTuples& listToFill){
  string requestURL = this->connectionURL
                      + "/station/stations";
  RestClient::Response response = RestClient::get(requestURL);
  using json = nlohmann::json;
  json jsonParser = json::parse(response.body);

  if(response.code == 200 && !jsonParser.empty() ) {

    int numOfStations = jsonParser["stations"].size();
    string stationName;
    string stationURL;

    for(int stationIndex = 0; stationIndex < numOfStations; ++stationIndex){
      stationName = jsonParser["stations"][stationIndex]["name"];
      stationURL = jsonParser["stations"][stationIndex]["url"];

      listToFill.push_back(make_tuple(stationName,stationURL));
    }
  }
}
