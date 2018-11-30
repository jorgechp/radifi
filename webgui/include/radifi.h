#include <Wt/WContainerWidget.h>
#include <Wt/WStackedWidget.h>

#include "radifiServiceAPI.h"

/**
* The main container widget.
*/
class Radifi : public Wt::WContainerWidget
{
public:
    /**
    * Public default constructor.
    */
    Radifi();

      ~Radifi() { if(this->apiREST != 0) delete this->apiREST;}

protected:
    /*
    * Handle the internal navigation.
    */
    void handleNavigation(const std::string &internalPath);
private:
    /* The stacked widget */
    Wt::WStackedWidget *mainStack_;

    RadifiServiceAPI *apiREST;
};
