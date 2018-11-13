#include "addStationWidget.h"
#include "playListContainer.h"
#include "stationTableWidget.h"
#include "pageWidgetContainer.h"

using namespace Wt;

PlayListContainer::PlayListContainer(const std::string& pageTitle)
                  :PageContainer(pageTitle){


  PageWidgetContainer* addStationWidgetContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Añadir emisora"));


  PageWidgetContainer* radioStationListContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Lista de emisoras"));
  WContainerWidget* tableWidgetContainer = radioStationListContainer->addWidget(cpp14::make_unique<WContainerWidget>());
  StationTableWidget* tableWidget = tableWidgetContainer->addWidget(cpp14::make_unique<StationTableWidget>());

  AddStationWidget* addStationWidget = addStationWidgetContainer->addWidget(cpp14::make_unique<AddStationWidget>(tableWidget));


  tableWidgetContainer->setOverflow(Wt::Overflow::Auto,Wt::Orientation::Vertical);

  Station station1("Radio Almaina", "https://www.radioalmaina.org/radio_almaina.m3u");
  Station station2("Radio La Colifata", "http://streamall.alsolnet.com:443/lacolifata");
  Station station3("WCPE", "http://audio-ogg.ibiblio.org:8000/wcpe.ogg.m3u");

  tableWidget->addStation(station1);
  tableWidget->addStation(station2);
  tableWidget->addStation(station3);

  tableWidget->generateTable();



}
