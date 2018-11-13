#include <Wt/WContainerWidget.h>
#include <Wt/WStackedWidget.h>


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

protected:
    /*
    * Handle the internal navigation.
    */
    void handleNavigation(const std::string &internalPath);
private:
    /* The stacked widget */
    Wt::WStackedWidget *mainStack_;
};
