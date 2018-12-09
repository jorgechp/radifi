#include <memory>
#include <string>
#include <sstream>
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

bool RadifiServiceAPI::setCurrentVolume(const short& currentVolume){
  string requestURL = this->connectionURL
                      + "/station/volume";

  string jsonRequest = "{\"volume\":\"" + std::to_string(currentVolume) + "\"}";

  RestClient::Response response = RestClient::put(requestURL,"application/json",jsonRequest);
  return response.code == 204;
}

const short RadifiServiceAPI::getCurrentVolume(){
  string requestURL = this->connectionURL
                      + "/station/volume";

  RestClient::Response response = RestClient::get(requestURL);
  using json = nlohmann::json;
  json jsonParser = json::parse(response.body);
  short currentVolume = 0;

  if(response.code == 200 && !jsonParser.empty() ) {
    currentVolume = jsonParser["volume"];
    cout << jsonParser["volume"] << endl;
  }
  return currentVolume;

}

const string RadifiServiceAPI::getCurrentAlarm(){
  string requestURL = this->connectionURL
                      + "/alarm";
  RestClient::Response response = RestClient::get(requestURL);
  using json = nlohmann::json;
  json jsonParser = json::parse(response.body);
  string currentAlarmTime = "";
  if(response.code == 200 && !jsonParser.empty() ) {
    string currentAlarmHour = jsonParser["current_hour"];
    string currentAlarmMinute = jsonParser["current_minute"];
    currentAlarmTime = currentAlarmHour + ":" + currentAlarmMinute;
  }
  return currentAlarmTime;
}

bool RadifiServiceAPI::setCurrentAlarm(const string& alarmToSet){
  string requestURL = this->connectionURL
                      + "/alarm";

  std::vector<std::string> timeParts;
  std::string token;
  std::istringstream tokenStream(alarmToSet);
  char delimiter = ':';
  while (std::getline(tokenStream, token, delimiter))
  {
     timeParts.push_back(token);
  }

  string jsonRequest = "{\"hour\":\"" + timeParts[0] +"\", "
                      + "\"minute\": \"" + timeParts[1] + "\"}";

  RestClient::Response response = RestClient::put(
                                  requestURL,
                                  "application/json",
                                  jsonRequest);

  return response.code == 204;
}

bool RadifiServiceAPI::setAlarmEnabled(bool isAlarmEnabled){
  string requestURL = this->connectionURL
                      + "/alarm";
  string jsonRequest = "{\"enabled\":\"" + std::to_string(isAlarmEnabled) + "\"}";

  RestClient::Response response = RestClient::patch(requestURL
                                  ,"application/json"
                                  ,jsonRequest);
  using json = nlohmann::json;

  return response.code == 204;
}

bool RadifiServiceAPI::isAlarmEnabled(){
  string requestURL = this->connectionURL
                      + "/alarm";
  RestClient::Response response = RestClient::get(requestURL);
  using json = nlohmann::json;
  json jsonParser = json::parse(response.body);

  if(response.code == 200 && !jsonParser.empty() ) {
    return jsonParser["is_enabled"];
  }
  return false;
}

std::unique_ptr<Station> RadifiServiceAPI::getCurrentAlarmStation(){
  string requestURL = this->connectionURL
                      + "/alarm/station";
  RestClient::Response response = RestClient::get(requestURL);
  using json = nlohmann::json;
  json jsonParser = json::parse(response.body);

  if(response.code == 200 && !jsonParser.empty() ) {
      string stationName = jsonParser["alarm_name"];
      string stationURL = jsonParser["alarm_url"];
      return make_unique<Station>(stationName,stationURL);
  }
  return 0;
}

bool RadifiServiceAPI::setCurrentAlarmStation(Station& stationToSet){
  string requestURL = this->connectionURL
                      + "/alarm/station";

  string stationName = stationToSet.getStationName();
  string stationURL = stationToSet.getStationURL();


  string jsonRequest = "{\"alarm_name\":\"" + stationName +"\", "
                      + "\"alarm_url\": \"" + stationURL + "\"}";
  

  RestClient::Response response = RestClient::patch(requestURL
                                  ,"application/json"
                                  ,jsonRequest);
  return response.code == 200;

}
