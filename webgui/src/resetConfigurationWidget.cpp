#include <Wt/WPushButton.h>
#include <Wt/WVBoxLayout.h>

#include "resetConfigurationWidget.h"

using namespace Wt;


ResetConfigurationWidget::ResetConfigurationWidget(){
  WVBoxLayout* groupBox = setLayout(cpp14::make_unique<WVBoxLayout>());
  setStyleClass("groupBox-custom");

  WPushButton* removeRadioButton = groupBox->addWidget(cpp14::make_unique<WPushButton>("Eliminar todas las estaciones de radio"));
  WPushButton* removeAlarmButton = groupBox->addWidget(cpp14::make_unique<WPushButton>("Eliminar configuración de alarma"));
  WPushButton* removeConfigurationButton = groupBox->addWidget(cpp14::make_unique<WPushButton>("Reiniciar configuración"));



  removeRadioButton->clicked().connect([=] {
    this->removeAllStations();
  });

  removeAlarmButton->clicked().connect([=] {
    this->removeAlarm();
  });

  removeConfigurationButton->clicked().connect([=] {
    this->fullReset();
  });

}

void ResetConfigurationWidget::removeAllStations(){

}
void ResetConfigurationWidget::removeAlarm(){

}
void ResetConfigurationWidget::fullReset(){
  this->removeAllStations();
  this->removeAlarm();
}
