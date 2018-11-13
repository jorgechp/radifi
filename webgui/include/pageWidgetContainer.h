#include<string>
#include "pageSection.h"

using namespace std;


/**
* This class represent a page, with a title header.
*/
#pragma once
class PageWidgetContainer : public PageSection{
public:
  /**
  * Public constructor.
  * @param pageTitle The title of the page.
  */
  PageWidgetContainer(const std::string& pageTitle);
};
