#include<vector>

#include <Wt/WContainerWidget.h>
#include <Wt/WPushButton.h>

#include "station.h"

using namespace Wt;

/**
* This widget controls remotely the alarm settings
*/
class AlarmWidget : public Wt::WContainerWidget{
public:
  /**
  * Default public constructor
  */
   AlarmWidget();


private:
  /**
  * Updates the alarm button text
  * @param toggleAlarmtr The button to be updated.
  */
  void updateAlarmText(WPushButton* toggleAlarmtr);

  /**
  * Set the hour
  * @param hour The new hour to be setted.
  */
  void setHour(const short& hour);

  /**
  * Get the hour.
  * @return short The current hour.
  */
  const short getHour();

  /**
  * Set the minute
  * @param minute The new minute to be setted.
  */
  void setMinute(const short& minute);

  /**
  * Get the minute.
  * @return short The current minute.
  */
  const short getMinute();

  /**
  * Set the seconds
  * @param seconds The new seconds to be setted.
  */
  void setSeconds(const short& seconds);

  /**
  * Get the seconds.
  * @return short The current seconds.
  */
  const short getSeconds();


  /**
  * Toggle on/off the alarm.
  * @param is_alarm_enable The current status of the alarm.
  */
  void setAlarmEnabled(const bool& is_alarm_enable);

  /**
  * Get the alarm status.
  * @return bool The alarm status.
  */
  const bool isAlarmEnabled();


  /**
  * Set the station to be played when alarm is active
  * @param stationToSet The index of the station to set.
  */
  void setAlarmStation(int stationToSet);

  /**
  * Get the station being played when alarm is active.
  * @return The Station index.
  */
  int getAlarmStation();

  /**
  * Get a vector with the station list.
  */
  std::vector<Station*>* getStationList();

  /**
  * Updates, in the gui, the station selected at Radifi.
  * @param comboBox The comboBox instance to be updated.
  */
  void updateStationSelected(Wt::WComboBox& comboBox);


};
