#include <Wt/WContainerWidget.h>

using namespace Wt;

/**
* This widget controls remotely the volume of radify
*/
class VolumeWidget : public Wt::WContainerWidget{
public:
  /**
  * Default public constructor
  */
   VolumeWidget();

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
