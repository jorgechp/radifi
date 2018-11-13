#include <Wt/WHBoxLayout.h>

#include "header.h"
#include "headerMenu.h"
#include "radioContainer.h"


Header::Header(){
  /*
  * We use a BoxLayout for keep the horizontal order in the header.
  */
  auto hbox = setLayout(Wt::cpp14::make_unique<Wt::WHBoxLayout>());

  hbox->addWidget(Wt::cpp14::make_unique<HeaderMenu>(),1);
  hbox->addWidget(Wt::cpp14::make_unique<RadioContainer>());



}
