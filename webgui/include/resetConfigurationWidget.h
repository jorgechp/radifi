#include <Wt/WContainerWidget.h>

#include "radifiServiceAPI.h"

using namespace Wt;

/**
* This widget allow to reset all the configuration.
*/
class ResetConfigurationWidget : public Wt::WContainerWidget{
private:
  RadifiServiceAPI* api;
public:
  /**
  * Default public constructor
  *
  * @param api a reference to the API instance.
  */
   ResetConfigurationWidget(RadifiServiceAPI& api);

   /**
   * Remove all the stations from the radifi system
   */
   void removeAllStations();

   /**
   * Remove all the alarms setted on the radifi system.
   */
   void removeAlarm();

   /**
   *Remove all the stations and all the alams setted on the radifi systems.
   */
   void fullReset();
};
