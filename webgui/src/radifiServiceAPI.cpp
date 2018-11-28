#include "restclient-cpp/restclient.h"
#include "radifiServiceAPI.h"

#include <string>
#include<iostream>
using namespace std;

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
                      + "\"url\": " + url + "\"}";

  RestClient::Response response = RestClient::put(requestURL,"application/json",jsonRequest);

  if(response.code == 200) return true;

  return false;
}
