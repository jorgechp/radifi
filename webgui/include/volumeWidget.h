#include <Wt/WContainerWidget.h>

#include "radifiServiceAPI.h"

using namespace Wt;

/**
* This widget controls remotely the volume of radify
*/
class VolumeWidget : public Wt::WContainerWidget{
private:
  RadifiServiceAPI* api;
public:
  /**
  * Default public constructor
  */
   VolumeWidget(RadifiServiceAPI& api);

   /**
   * Set the volume
   * @param volume The new volume to be setted.
   */
   void setVolume(const short& volume);

   /**
   * Get the volume.
   * @return short The current volume.
   */
   const short getVolume();
};
