#include<string>
#include <Wt/WContainerWidget.h>
#include"stationTableWidget.h"

using namespace Wt;

/**
* Represents a form to add a new station.
*/
class AddStationWidget : public WContainerWidget{
private:
  StationTableWidget* tableWidget;
  void addStation(std::string stationName, std::string radioURL);
public:
  /*
  * Default constructor.
  */
  AddStationWidget(StationTableWidget* tableWidgetToAdd );


};
