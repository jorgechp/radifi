#include <string>
#include<vector>

#include <Wt/WTime.h>
#include <Wt/WText.h>
#include <Wt/WTimeEdit.h>
#include <Wt/WVBoxLayout.h>
#include <Wt/WHBoxLayout.h>
#include <Wt/WPushButton.h>
#include <Wt/WComboBox.h>

#include "alarmWidget.h"
#include "radifiServiceAPI.h"

using namespace Wt;

typedef list<tuple<string,string>> listOfStationTuples;

const string AlarmWidget::TIME_PATTERN_FORMAT = "hh:mm";

AlarmWidget::AlarmWidget(RadifiServiceAPI& api){
    this->api = &api;

    setStyleClass("form-inline groupBox-custom");

    /*
    * Time settings.
    */

    WVBoxLayout* groupBox = setLayout(cpp14::make_unique<WVBoxLayout>());
    WHBoxLayout* groupBoxDateSettings = groupBox->addLayout(cpp14::make_unique<WHBoxLayout>());
    WHBoxLayout* groupBoxCurrentStationSettings = groupBox->addLayout(cpp14::make_unique<WHBoxLayout>());
    WHBoxLayout* groupBoxNewStationSettings = groupBox->addLayout(cpp14::make_unique<WHBoxLayout>());

    groupBoxDateSettings->addWidget(cpp14::make_unique<WText>("Hora de la Alarma"));
    WTimeEdit* timeEditor = groupBoxDateSettings->addWidget(cpp14::make_unique<WTimeEdit>());
    string currentAlarmTime = this->getCurrentAlarmTime();

    WTime currentTimeAsWTime = this->parseTime(currentAlarmTime);

    timeEditor->setTime(currentTimeAsWTime);
    timeEditor->setStyleClass("form-control Wt-timeedit active timeEdit-input");
    WPushButton* okPtr = groupBoxDateSettings->addWidget(cpp14::make_unique<WPushButton>("Guardar Alarma"));
    WPushButton* toggleAlarmtr = groupBoxDateSettings->addWidget(cpp14::make_unique<WPushButton>());
    this->updateAlarmText(toggleAlarmtr);


    okPtr->clicked().connect([=] {
      WTime time = timeEditor->time();

      string formattedTime = time
                              .toString(AlarmWidget::TIME_PATTERN_FORMAT)
                              .toUTF8();
      this->api->setCurrentAlarm(formattedTime);

      string currentAlarmTime = this->getCurrentAlarmTime();

      WTime timeReturned = this->parseTime(currentAlarmTime);
      timeEditor->setTime(timeReturned);
      this->setAlarmEnabled(false);
      this->updateAlarmText(toggleAlarmtr);

    });

    toggleAlarmtr->clicked().connect([=] {
      this->setAlarmEnabled(! this->isAlarmEnabled());
      this->updateAlarmText(toggleAlarmtr);
    });

    /*
    * Current station
    */
    groupBoxCurrentStationSettings->
              addWidget(cpp14::make_unique<WText>("Emisora Actual"));
    this->stationName =
              groupBoxCurrentStationSettings->
              addWidget(Wt::cpp14::make_unique<Wt::WText>(""),3);
    this->updateCurrentStationText();


    /*
    * New Station selection.
    */

    groupBoxNewStationSettings->addWidget(cpp14::make_unique<WText>("Emisora"),1);
    this->cb = groupBoxNewStationSettings->addWidget(Wt::cpp14::make_unique<Wt::WComboBox>(),1);
    this->cb->setMargin(10, Wt::Side::Right);


    std::vector<Station*>* lista_emisoras = this->getStationList();

    for (std::vector<Station*>::iterator it = lista_emisoras->begin() ; it != lista_emisoras->end(); ++it){
      this->cb->addItem((*it)->getStationName());
    }

    WPushButton* saveStationPtr = groupBoxNewStationSettings->addWidget(cpp14::make_unique<WPushButton>("Guardar Emisora"));
    saveStationPtr->clicked().connect([&] {
        int currentSelectedStationIndex = this->cb->currentIndex();
        Station* stationSelected = lista_emisoras->at(currentSelectedStationIndex);

        if(this->api->setCurrentAlarmStation(*stationSelected)){

        }
    });

    /*
    * In case of error while connecting to the station, a local sound will be
    * played.
    */
    groupBox->addWidget(cpp14::make_unique<WText>("Si no es posible conectar con la emisora, se activará un sonido de alarma por defecto."));

}

const string AlarmWidget::getCurrentAlarmTime(){
  return this->api->getCurrentAlarm();
}

WTime AlarmWidget::parseTime(const string& timeToParse){
  WTime currentTimeAsWTime = Wt::WTime::currentTime();

  if(!timeToParse.empty()){
    currentTimeAsWTime = Wt::WTime::fromString(timeToParse,AlarmWidget::TIME_PATTERN_FORMAT);
  }
  return currentTimeAsWTime;
}

void AlarmWidget::setAlarmEnabled(const bool& isAlarmEnabled){
  this->api->setAlarmEnabled(isAlarmEnabled);
}

const bool AlarmWidget::isAlarmEnabled(){
  return this->api->isAlarmEnabled();
}

void AlarmWidget::updateAlarmText(WPushButton* toggleAlarmtr){
  bool isAlarmEnabled = this->isAlarmEnabled();

  std::string toggleText = "Desactivar Alarma";
  if(!isAlarmEnabled){
    toggleText = "Activar Alarma";
  }
  toggleAlarmtr->setText(toggleText);

}


void AlarmWidget::setAlarmStation(int stationToSet){}

  std::vector<Station*>*  AlarmWidget::getStationList(){
    listOfStationTuples listOfStations;
    this->api->getStationList(listOfStations);
    std::vector<Station*>* stationVector = new std::vector<Station*>();

    for (listOfStationTuples::iterator it=listOfStations.begin();
          it != listOfStations.end();
          ++it){
              tuple<string,string> stationDataTuple = *it;
              string stationName = std::get<0>(stationDataTuple);
              string stationURL = std::get<1>(stationDataTuple);
              stationVector->push_back(new Station(stationName,stationURL));
              }

    return stationVector;
}

void AlarmWidget::updateCurrentStationText(){
  auto currentAlarmStation = this->api->getCurrentAlarmStation();
  const string currentStationName = currentAlarmStation->getStationName();
  this->stationName->setText(currentStationName);
  currentAlarmStation.reset();
}
