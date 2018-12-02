#include<string>

#include "pageContainer.h"
#include"radifiServiceAPI.h"

using namespace Wt;

/**
* This class represent the PlayList page.
*/
class PlayListContainer : public PageContainer{
private:
  RadifiServiceAPI* api;
  StationTableWidget* tableWidget;
  void addStationsFromService();
public:
  /*
  * Public constructor.
  * @param pageTitle The title (header) of the page.
  */
  PlayListContainer(const std::string& pageTitle,
                    RadifiServiceAPI& api);
};
