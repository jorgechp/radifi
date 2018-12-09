#include <string>
#include <Wt/WEnvironment.h>
#include <Wt/WApplication.h>
#include <Wt/WStackedWidget.h>
#include <Wt/WText.h>

#include "radifi.h"
#include "header.h"
#include "playListContainer.h"
#include "configurationContainer.h"
#include "radifiServiceAPI.h"

using namespace Wt;

Radifi::Radifi()
{
  std::string host = "http://localhost";
  int port = 5000;
  this->apiREST = new RadifiServiceAPI(host,port);

  mainStack_ = new WStackedWidget();
  addWidget(Wt::cpp14::make_unique<Header>());
  addWidget(std::unique_ptr<WStackedWidget>(mainStack_));
  handleNavigation("");
  WApplication::instance()->internalPathChanged().connect(this,&Radifi::handleNavigation);
}

void Radifi::handleNavigation(const std::string &internalPath){

 if(internalPath == "/config"){
    ConfigurationContainer *configurationContainer = mainStack_->addWidget(cpp14::make_unique<ConfigurationContainer>("Configuración",*this->apiREST));
    mainStack_->setCurrentWidget(configurationContainer);
  } else{
    PlayListContainer *playListContainer = mainStack_->addWidget(cpp14::make_unique<PlayListContainer>("Emisoras",*this->apiREST));
    mainStack_->setCurrentWidget(playListContainer);
  }
}
