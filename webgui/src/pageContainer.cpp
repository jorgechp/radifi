#include<string>
#include <Wt/WText.h>

#include"pageContainer.h"

using namespace Wt;

PageContainer::PageContainer(const std::string& pageTitle)
    :PageSection(pageTitle,"<h1>","</h1>"){}
