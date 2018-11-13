#include<string>
#include <Wt/WText.h>

#include"pageWidgetContainer.h"

using namespace Wt;

PageWidgetContainer::PageWidgetContainer(const std::string& pageTitle)
    :PageSection(pageTitle,"<h2>","</h2>"){}
