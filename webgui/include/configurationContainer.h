#include<string>

#include"pageContainer.h"
#include "radifiServiceAPI.h"

using namespace std;

/**
* This class represents the Configuration webpage.
*/
class ConfigurationContainer : public PageContainer{
private:
  RadifiServiceAPI* api;
public:
  /**
  * Public constructor
  * @param pageTitle The title of the page.
  * @param api An instance of the RadifiServiceAPI class.
  */
  ConfigurationContainer(const std::string& pageTitle, RadifiServiceAPI& api);

  /**
  * Set the volume.
  * @param volumen The volumen to be setted.
  */
  void setVolume(const int& volume);

  /**
  * Update the Time.
  */
  void updateTime();

  /**
  * Set the alarm time.
  * @param hour The hour to be setted
  * @param minut The minute to be setted.
  */
  void setAlarmTime(const int& hour,const int& minute);

  /**
  * Set the alarm station.
  * @param stationName The station.
  */
  void setAlarmStation(const string& stationName);
};
