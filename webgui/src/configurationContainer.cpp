
#include"configurationContainer.h"
#include"pageWidgetContainer.h"
#include"volumeWidget.h"
#include"alarmWidget.h"
#include"resetConfigurationWidget.h"

using namespace Wt;

ConfigurationContainer::ConfigurationContainer(const std::string& pageTitle)
: PageContainer(pageTitle){



  PageWidgetContainer* volumeWidgetContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Volumen"));
  PageWidgetContainer* alarmWidgetContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Alarma"));
  PageWidgetContainer* resetWidgetContainer = addWidget(cpp14::make_unique<PageWidgetContainer>("Reiniciar configuración"));


  VolumeWidget* volumeWidget = volumeWidgetContainer->addWidget(cpp14::make_unique<VolumeWidget>());
  AlarmWidget* alarmWidget = alarmWidgetContainer->addWidget(cpp14::make_unique<AlarmWidget>());
  ResetConfigurationWidget* resetConfigurationWidget = resetWidgetContainer->addWidget(cpp14::make_unique<ResetConfigurationWidget>());


}
