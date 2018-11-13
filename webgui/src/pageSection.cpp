#include<string>
#include <Wt/WText.h>

#include"pageSection.h"

using namespace Wt;

PageSection::PageSection(const std::string& pageTitle,
  const std::string& open_h_tag,
  const std::string& close_h_tag){

  string finalTitle = open_h_tag + pageTitle + close_h_tag;
  addStyleClass("container");
  WText* title = addWidget(cpp14::make_unique<WText>(finalTitle));

}
