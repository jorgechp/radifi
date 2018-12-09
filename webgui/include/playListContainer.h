#include<string>

#include "pageContainer.h"
#include "radifiServiceAPI.h"
#include "stationTableWidget.h"

using namespace Wt;

/**
* This class represent the PlayList page.
*/
class PlayListContainer : public PageContainer{
private:
  RadifiServiceAPI* api;
  StationTableWidget* tableWidget;

  /**
  * Insert the radio stations obtained from the service.
  */
  void addStationsFromService();
public:
  /**
  * Public constructor.
  * @param pageTitle The title (header) of the page.
  */
  PlayListContainer(const std::string& pageTitle,
                    RadifiServiceAPI& api);
};
