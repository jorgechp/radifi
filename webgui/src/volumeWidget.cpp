#include <Wt/WLineEdit.h>
#include <Wt/WText.h>
#include <Wt/WBreak.h>
#include <Wt/WSlider.h>
#include <Wt/WLineEdit.h>

#include "volumeWidget.h"
#include "radifiServiceAPI.h"

using namespace Wt;

VolumeWidget::VolumeWidget(RadifiServiceAPI& api){
    this->api = &api;

    setStyleClass("form-inline");
    addWidget(Wt::cpp14::make_unique<Wt::WBreak>());
    int currentVolume = this->getVolume();
    Wt::WSlider *slider =
        addWidget(Wt::cpp14::make_unique<Wt::WSlider>());
    slider->resize(500, 50);
    slider->setTickPosition(Wt::WSlider::TickPosition::TicksAbove);
    slider->setTickInterval(10);
    slider->setMinimum(0);
    slider->setMaximum(100);
    slider->setValue(currentVolume);
    slider->valueChanged().connect([=] {
        this->setVolume(slider->value());
        /*
        * We need to get the current volume of radify in order to prevent
        * a bad synchronization between the web GUI and Radify system.
        */
        int currentVolume = this->getVolume();
        slider->setValue(currentVolume);
      });
    addWidget(Wt::cpp14::make_unique<Wt::WBreak>());

}

void VolumeWidget::setVolume(const short& volume){
  std::cout << "Volume set to " << volume << std::endl;
  this->api->setCurrentVolume(volume);
}

const short VolumeWidget::getVolume(){
  return this->api->getCurrentVolume();
}
