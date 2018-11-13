#include<string>
#include "pageContainer.h"

using namespace Wt;

/**
* This class represent the PlayList page.
*/
class PlayListContainer : public PageContainer{
public:
  /*
  * Public constructor.
  * @param pageTitle The title (header) of the page.
  */
  PlayListContainer(const std::string& pageTitle);
};
