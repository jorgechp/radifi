#include <restclient-cpp/restclient.h>
#include"RadifiServiceAPI.h"

RadifiServiceAPI::RadifiServiceAPI(string &host, int port){
  this->host = &host;
  this->port = port;
  this->connectionURL = host + ":" + std::to_string(port);
}


bool RadifiServiceAPI::playRadioStation(const int radioStation){
  RestClient::Response r = RestClient::get(this->connectionURL);
  return true;
}
