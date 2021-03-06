#include <vector>
#include <algorithm>
#include <Wt/WLength.h>
#include <Wt/WTableRow.h>
#include <Wt/WText.h>
#include <Wt/WPushButton.h>




#include "stationTableWidget.h"
#include"radifiServiceAPI.h"

using namespace Wt;

StationTableWidget::StationTableWidget(RadifiServiceAPI& api){
  this->api = &api;
  addStyleClass("table form-inline");
}

bool StationTableWidget::addStation(Station& stationToAdd){
  std::vector<Station>::iterator findIter =
                                        std::find(this->stationVector.begin(),
                                        this->stationVector.end(), stationToAdd);
  if(findIter == this->stationVector.end()){
    string stationName = stationToAdd.getStationName();
    string stationURL = stationToAdd.getStationURL();
    bool isAdded = this->api->addNewRadioStation(stationName
                                                ,stationURL);
    if(isAdded){
      this->insertStation(stationToAdd);
    }
    return isAdded;
  }else{
    return false;
  }
}

void StationTableWidget::insertStation(Station& stationToInsert){
  this->stationVector.push_back(stationToInsert);
}

int StationTableWidget::getNumStations(){
  return this->stationVector.size();
}

bool StationTableWidget::sintonizeStation(unsigned int stationIndex){
  if(stationIndex < this->stationVector.size()){
    this->api->stopRadioStation();
    return this->api->playRadioStation(stationIndex);
  }
  return false;
}

bool StationTableWidget::removeStation(unsigned int stationIndex){
  if(stationIndex < this->getNumStations()){
    bool isDeleted = false;
    if(stationIndex < this->stationVector.size()){
      isDeleted = this->api->removeRadioStation(stationIndex);
    }

    if(isDeleted){
      this->stationVector.erase(this->stationVector.begin()+stationIndex);
      return true;
    }
  }
  return false;
}

void StationTableWidget::generateTable(){
  int numOfStations = this->getNumStations();
  if(numOfStations > 0){
    std::vector<Station>::iterator iter;
    Station *currentStation;
    int currentRow = 0;
    WPushButton *sintonizeButton = 0;
    WPushButton *removeButton = 0;
    for(iter = this->stationVector.begin(); iter != this->stationVector.end(); iter++){
      currentStation = &(*iter);
      auto* newTableRow = insertRow(currentRow,cpp14::make_unique<WTableRow>());
      newTableRow->elementAt(0)->addWidget(cpp14::make_unique<WText>(currentStation->getStationName()));
      newTableRow->elementAt(1)->addWidget(cpp14::make_unique<WText>(currentStation->getStationURL()));
      sintonizeButton = newTableRow->elementAt(2)->addWidget(cpp14::make_unique<Wt::WPushButton>("Sintonizar"));
      sintonizeButton->setStyleClass("btn-success");
      sintonizeButton->clicked().connect([=] {
        this->sintonizeStation(currentRow);
      });
      removeButton = newTableRow->elementAt(3)->addWidget(cpp14::make_unique<Wt::WPushButton>("Eliminar"));
      removeButton->setStyleClass("btn-warning");
      removeButton->clicked().connect([=] {
        this->removeStation(currentRow);
        this->clear();
        this->generateTable();
      });
      ++currentRow;
    }
  }else{
    elementAt(0, 0)->addWidget(cpp14::make_unique<WText>("No playList found."));
  }
}
