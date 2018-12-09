#include<vector>

#include <Wt/WContainerWidget.h>
#include <Wt/WPushButton.h>

#include "station.h"
#include "radifiServiceAPI.h"

using namespace Wt;

/**
* This widget controls remotely the alarm settings
*/
class AlarmWidget : public Wt::WContainerWidget{
public:
  const static string TIME_PATTERN_FORMAT;

  /**
  * Default public constructor
  * @param api An instance of the RadifiServiceAPI class.
  */
   AlarmWidget(RadifiServiceAPI& api);


private:
  RadifiServiceAPI* api;
  Wt::WComboBox* cb ;
  Wt::WText *stationName;  

  /**
  * Gets the current alarm time.
  *
  * @return A string with the current alarm time. Format: hh:mm
  */
  const string getCurrentAlarmTime();

  /**
  * Converts a string into a WTime instance. String must contain a date
  * with the pattern: hh:mm.
  *
  * @param timeToParse The string with the time to parse.
  * @return An WTime instance.
  */
  WTime parseTime(const string& timeToParse);

  /**
  * Updates the alarm button text
  * @param toggleAlarmtr The button to be updated.
  */
  void updateAlarmText(WPushButton* toggleAlarmtr);

  /**
  * Toggle on/off the alarm.
  * @param isAlarmEnabled The current status of the alarm.
  */
  void setAlarmEnabled(const bool& isAlarmEnabled);

  /**
  * Get the alarm status.
  * @return bool The alarm status.
  */
  const bool isAlarmEnabled();

  /**
  * Get a vector with the station list.
  */
  std::vector<Station*>* getStationList();

  void updateCurrentStationText();


};
