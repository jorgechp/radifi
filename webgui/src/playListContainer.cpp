#include <tuple>

#include <Wt/WPushButton.h>

#include "addStationWidget.h"
#include "playListContainer.h"
#include "stationTableWidget.h"
#include "pageWidgetContainer.h"
#include "radifiServiceAPI.h"


using namespace Wt;
using namespace std;

typedef list<tuple<string,string>> listOfStationTuples;

PlayListContainer::PlayListContainer(const std::string& pageTitle,
                    RadifiServiceAPI& api)
                  :PageContainer(pageTitle){

  this->api = &api;
  Wt::WPushButton *stopStationButton = addWidget(Wt::cpp14::make_unique<WPushButton>("Stop station"));
  stopStationButton->setStyleClass("btn-warning");
  stopStationButton->clicked().connect([&] {
      this->api->stopRadioStation();
  });
  PageWidgetContainer* addStationWidgetContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Añadir emisora"));


  PageWidgetContainer* radioStationListContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Lista de emisoras"));
  WContainerWidget* tableWidgetContainer = radioStationListContainer->addWidget(cpp14::make_unique<WContainerWidget>());
  this->tableWidget = tableWidgetContainer->addWidget(cpp14::make_unique<StationTableWidget>(api));

  AddStationWidget* addStationWidget = addStationWidgetContainer->addWidget(cpp14::make_unique<AddStationWidget>(this->tableWidget));


  tableWidgetContainer->setOverflow(Wt::Overflow::Auto,Wt::Orientation::Vertical);

  this->addStationsFromService();
  this->tableWidget->generateTable();
}

void PlayListContainer::addStationsFromService(){
  listOfStationTuples stationsFromService;
  this->api->getStationList(stationsFromService);

  for (listOfStationTuples::iterator it=stationsFromService.begin();
        it != stationsFromService.end();
        ++it){
            tuple<string,string> stationDataTuple = *it;
            string stationName = std::get<0>(stationDataTuple);
            string stationURL = std::get<1>(stationDataTuple);
            Station stationToAdd(stationName,stationURL);
            this->tableWidget->insertStation(stationToAdd);
  }
}
