#include<string>
#include <Wt/WContainerWidget.h>

using namespace std;

/**
* This class represents the container of a widget, with a title.
*/
#pragma once
class PageSection : public Wt::WContainerWidget{
public:
  /**
  * Public constructor.
  * @param pageTitle The title of the widget.
  */
  PageSection(const std::string& pageTitle,
    const std::string& open_h_tag,
    const std::string& close_h_tag);

};
