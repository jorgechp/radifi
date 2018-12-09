#include <Wt/WContainerWidget.h>
#include <Wt/WNavigationBar.h>
#include <Wt/WStackedWidget.h>
#include <Wt/WMenu.h>
#include <Wt/WText.h>


#include "headerMenu.h"

using namespace Wt;
using namespace std;

HeaderMenu::HeaderMenu(){

  Wt::WNavigationBar *navigation = addWidget(Wt::cpp14::make_unique<Wt::WNavigationBar>());
  navigation->setResponsive(false);


  auto menu = navigation->addMenu(Wt::cpp14::make_unique<Wt::WMenu>());
  menu->setStyleClass("nav nav-tabs");
  menu->addItem("Emisoras")->setLink(Wt::WLink(Wt::LinkType::InternalPath, "/playList"));
  menu->addItem("Configuration")->setLink(Wt::WLink(Wt::LinkType::InternalPath, "/config"));

}
