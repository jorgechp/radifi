#include <Wt/WAudio.h>
#include <Wt/WContainerWidget.h>
#include <string>
#include "radioContainer.h"

using namespace Wt;

RadioContainer::RadioContainer(){
  WAudio *audio = addWidget(Wt::cpp14::make_unique<WAudio>());
  audio->setOptions(Wt::PlayerOption::Controls);

}
