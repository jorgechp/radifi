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

using namespace Wt;

AlarmWidget::AlarmWidget(){

    setStyleClass("form-inline groupBox-custom");

    /*
    * Time settings.
    */

    WVBoxLayout* groupBox = setLayout(cpp14::make_unique<WVBoxLayout>());
    WHBoxLayout* groupBoxDateSettings = groupBox->addLayout(cpp14::make_unique<WHBoxLayout>());
    WHBoxLayout* groupBoxStationSettings = groupBox->addLayout(cpp14::make_unique<WHBoxLayout>());

    groupBoxDateSettings->addWidget(cpp14::make_unique<WText>("Hora de la Alarma"),1);
    WTimeEdit* timeEditor = groupBoxDateSettings->addWidget(cpp14::make_unique<WTimeEdit>());
    timeEditor->setTime(Wt::WTime::currentTime());
    timeEditor->setStyleClass("form-control Wt-timeedit active timeEdit-input");
    WPushButton* okPtr = groupBoxDateSettings->addWidget(cpp14::make_unique<WPushButton>("Guardar Alarma"));
    WPushButton* toggleAlarmtr = groupBoxDateSettings->addWidget(cpp14::make_unique<WPushButton>());
    this->updateAlarmText(toggleAlarmtr);


    okPtr->clicked().connect([=] {
      WTime time = timeEditor->time();
      this->setHour(time.hour());
      this->setMinute(time.minute());
      this->setSeconds(time.second());

      int hourReturned = this->getHour();
      int minuteReturned = this->getMinute();
      int secondsReturned = this->getSeconds();

      WTime timeReturned = WTime(hourReturned,minuteReturned,secondsReturned);
      timeEditor->setTime(timeReturned);
    });

    toggleAlarmtr->clicked().connect([=] {
      this->setAlarmEnabled(! this->isAlarmEnabled());
      this->updateAlarmText(toggleAlarmtr);
    });

    /*
    * Station selection.
    */

    groupBoxStationSettings->addWidget(cpp14::make_unique<WText>("Emisora"),1);
    Wt::WComboBox* cb = groupBoxStationSettings->addWidget(Wt::cpp14::make_unique<Wt::WComboBox>(),1);
    cb->setMargin(10, Wt::Side::Right);


    std::vector<Station*>* lista_emisoras = this->getStationList();

    for (std::vector<Station*>::iterator it = lista_emisoras->begin() ; it != lista_emisoras->end(); ++it){
      cb->addItem((*it)->getStationName());
    }

    this->updateStationSelected(*cb);

    WPushButton* saveStationPtr = groupBoxStationSettings->addWidget(cpp14::make_unique<WPushButton>("Guardar Emisora"));
    saveStationPtr->clicked().connect([=] {
      this->setAlarmStation(cb->currentIndex());
      this->updateStationSelected(*cb);
    });

    /*
    * In case of error while connecting to the station, a local sound will be
    * played.
    */
    groupBox->addWidget(cpp14::make_unique<WText>("Si no es posible conectar con la emisora, se activará un sonido de alarma por defecto."));

}

void AlarmWidget::setHour(const short& hour){}

const short AlarmWidget::getHour(){ return 4;}

void AlarmWidget::setMinute(const short& minute){}

const short AlarmWidget::getMinute(){ return 4;}

void AlarmWidget::setSeconds(const short& seconds){}

const short AlarmWidget::getSeconds(){ return 4;}

void AlarmWidget::setAlarmEnabled(const bool& is_alarm_enable){}

const bool AlarmWidget::isAlarmEnabled(){ return false;}

void AlarmWidget::updateAlarmText(WPushButton* toggleAlarmtr){
  bool isAlarmEnabled = this->isAlarmEnabled();
  std::string toggleText = "Desactivar Alarma";
  if(!isAlarmEnabled){
    toggleText = "Activar Alarma";
  }
  toggleAlarmtr->setText(toggleText);

}


void AlarmWidget::setAlarmStation(int stationToSet){}


int AlarmWidget::getAlarmStation(){
  return 2;
}


std::vector<Station*>*  AlarmWidget::getStationList(){
  std::vector<Station*>* stationVector = new std::vector<Station*>();
  stationVector->push_back(new Station("hola","hola1"));
  stationVector->push_back(new Station("hola2","hola2"));
  stationVector->push_back(new Station("hola3","hola3"));
  stationVector->push_back(new Station("hola4","hola4"));
  return stationVector;
}

void AlarmWidget::updateStationSelected(Wt::WComboBox& comboBox){
  int remoteStationSelected = this->getAlarmStation();
  comboBox.setCurrentIndex(remoteStationSelected);
  std::cout << remoteStationSelected << std::endl;
}
