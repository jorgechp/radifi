#include <Wt/WContainerWidget.h>

using namespace Wt;

/**
* This widget allow to reset all the configuration.
*/
class ResetConfigurationWidget : public Wt::WContainerWidget{
public:
  /**
  * Default public constructor
  */
   ResetConfigurationWidget();

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
