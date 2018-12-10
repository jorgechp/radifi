#include <Wt/WPushButton.h>
#include <Wt/WVBoxLayout.h>
#include <Wt/WMessageBox.h>

#include "resetConfigurationWidget.h"
#include "radifiServiceAPI.h"

using namespace Wt;


ResetConfigurationWidget::ResetConfigurationWidget(RadifiServiceAPI& api){
  this->api = &api;
  WVBoxLayout* groupBox = setLayout(cpp14::make_unique<WVBoxLayout>());
  setStyleClass("groupBox-custom");

  WPushButton* removeRadioButton = groupBox->addWidget(cpp14::make_unique<WPushButton>("Eliminar todas las estaciones de radio"));
  WPushButton* removeAlarmButton = groupBox->addWidget(cpp14::make_unique<WPushButton>("Eliminar configuración de alarma"));
  WPushButton* removeConfigurationButton = groupBox->addWidget(cpp14::make_unique<WPushButton>("Reiniciar configuración"));



  removeRadioButton->clicked().connect([=] {
    auto messageBox = addChild(
	    Wt::cpp14::make_unique<Wt::WMessageBox>("¡CUIDADO!",
	          "<p>¿Realmente deseas eliminar todas las estaciones de radio?.</p>"
	          "<p>Esta acción no se puede deshacer.</p>",
                  Wt::Icon::Critical, Wt::StandardButton::Yes | Wt::StandardButton::No));
    messageBox->setModal(true);
    messageBox->buttonClicked().connect([=] {
        if (messageBox->buttonResult() == Wt::StandardButton::Yes)
	         this->removeAllStations();
        removeChild(messageBox);
    });
    messageBox->show();
  });

  removeAlarmButton->clicked().connect([=] {
    auto messageBox = addChild(
      Wt::cpp14::make_unique<Wt::WMessageBox>("¡CUIDADO!",
            "<p>¿Realmente deseas eliminar la alarma?.</p>"
            "<p>Esta acción no se puede deshacer.</p>",
                  Wt::Icon::Warning, Wt::StandardButton::Yes | Wt::StandardButton::No));
    messageBox->setModal(true);
    messageBox->buttonClicked().connect([=] {
        if (messageBox->buttonResult() == Wt::StandardButton::Yes)
           this->removeAlarm();
        removeChild(messageBox);
    });
    messageBox->show();

  });

  removeConfigurationButton->clicked().connect([=] {
    auto messageBox = addChild(
      Wt::cpp14::make_unique<Wt::WMessageBox>("¡¡CUIDADO!!",
            "<p>¿Realmente deseas eliminar eliminar todas las estaciones de radio y la alarma?.</p>"
            "<p>Esta acción no se puede deshacer.</p>",
                  Wt::Icon::Critical, Wt::StandardButton::Yes | Wt::StandardButton::No));
    messageBox->setModal(true);
    messageBox->buttonClicked().connect([=] {
        if (messageBox->buttonResult() == Wt::StandardButton::Yes){
           this->removeAllStations();
           this->removeAlarm();
         }
        removeChild(messageBox);
    });
    messageBox->show();
  });

}

void ResetConfigurationWidget::removeAllStations(){
  this->api->removeAllStations();

}
void ResetConfigurationWidget::removeAlarm(){
  this->api->removeAlarm();

}
void ResetConfigurationWidget::fullReset(){
  this->removeAllStations();
  this->removeAlarm();
}
