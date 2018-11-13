#include <Wt/WContainerWidget.h>

using namespace Wt;

/**
* This widget controls remotely the time.
*/
class TimeWidget : public Wt::WContainerWidget{
public:
  /**
  * Default public constructor
  */
   TimeWidget();

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


};
