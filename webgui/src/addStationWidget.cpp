#include <Wt/WPushButton.h>
#include <Wt/WMessageBox.h>
#include <Wt/WLineEdit.h>
#include <Wt/WLengthValidator.h>
#include <Wt/WRegExpValidator.h>
#include"stationTableWidget.h"
#include"addStationWidget.h"

using namespace Wt;

AddStationWidget::AddStationWidget(StationTableWidget* tableWidgetToAdd ){
  this->tableWidget = tableWidgetToAdd;
  Wt::WLineEdit *stationName = addWidget(Wt::cpp14::make_unique<Wt::WLineEdit>());
  auto stationNameValidator = std::make_shared<Wt::WLengthValidator>(1,200);
  stationNameValidator->setMandatory(true);
  stationName->setWidth("230px");
  stationName->setFocus(true);
  stationName->setPlaceholderText("Nombre de la emisora");
  stationName->setValidator(stationNameValidator);

  Wt::WLineEdit *stationURL = addWidget(Wt::cpp14::make_unique<Wt::WLineEdit>());
  auto stationURLValidator = std::make_shared<Wt::WRegExpValidator>("(http://|https://)?[a-z0-9]+([-.]{1}[a-z0-9]+)*.[a-z]{2,5}(:[0-9]{1,5})?(/.*)?/g");
  stationURLValidator->setMandatory(true);
  stationURL->setWidth("585px");
  stationURL->setPlaceholderText("URL de la emisora");
  stationURL->setValidator(stationURLValidator);

  Wt::WPushButton *submitButton = addWidget(Wt::cpp14::make_unique<WPushButton>("Añadir"));
  submitButton->setStyleClass("btn-success");


  submitButton->clicked().connect([=] {
      bool isValid = true;
      if (stationName->validate() == Wt::ValidationState::InvalidEmpty) {
          stationName->setFocus();
          isValid = false;
      }
      if (isValid && stationURL->validate() == Wt::ValidationState::InvalidEmpty) {
          stationURL->setFocus();
          isValid = false;
      }

      if(isValid){
        this->addStation(stationName->valueText().toUTF8(),
            stationURL->valueText().toUTF8());
        stationName->setValueText("");
        stationURL->setValueText("");
      }


  });
}

void AddStationWidget::addStation(std::string stationName, std::string radioURL){
  Station stationToAdd = Station(stationName,radioURL);
  if(this->tableWidget->addStation(stationToAdd)){
    this->tableWidget->clear();
    this->tableWidget->generateTable();
  }else{
    std::cout << "gola\n";
    auto messageBox = this->addChild(
      Wt::cpp14::make_unique<Wt::WMessageBox>("Error",
            "<p>Esta emisora ya se encuentra añadida.</p>"
            ,Wt::Icon::Information, Wt::StandardButton::Ok));
    messageBox->setModal(true);
    messageBox->show();
    messageBox->buttonClicked().connect([=] {
      this->removeChild(messageBox);
    });
  }
}
