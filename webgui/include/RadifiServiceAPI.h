#include<string>

using namespace std;


/**
* This class represent a page, with a title header.
*/
class RadifiServiceAPI {
public:
  RadifiServiceAPI(string &host, int port);
private:
  string *host;
  string connectionURL;
  int port;

  bool checkConnection();

  bool playRadioStation(const int radioStation);

  bool stopRadioStation();


};
