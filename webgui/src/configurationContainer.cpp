
#include "configurationContainer.h"
#include "pageWidgetContainer.h"
#include "volumeWidget.h"
#include "alarmWidget.h"
#include "resetConfigurationWidget.h"
#include "radifiServiceAPI.h"

using namespace Wt;

ConfigurationContainer::ConfigurationContainer(const std::string& pageTitle,
RadifiServiceAPI& api)
: PageContainer(pageTitle){
  this->api = &api;

  PageWidgetContainer* volumeWidgetContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Volumen"));
  PageWidgetContainer* alarmWidgetContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Alarma"));
  PageWidgetContainer* resetWidgetContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Reiniciar configuración"));


  VolumeWidget* volumeWidget = volumeWidgetContainer->addWidget(cpp14::make_unique<VolumeWidget>(*this->api));
  AlarmWidget* alarmWidget = alarmWidgetContainer->addWidget(cpp14::make_unique<AlarmWidget>(*this->api));
  ResetConfigurationWidget* resetConfigurationWidget = resetWidgetContainer->addWidget(cpp14::make_unique<ResetConfigurationWidget>(*this->api));


}
