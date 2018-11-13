#include <Wt/WEnvironment.h>
#include <Wt/WApplication.h>

class Radifi : public Wt::WApplication
{
public:
    Radifi(const Wt::WEnvironment& env);

private:
    Wt::WLineEdit *nameEdit_;
    Wt::WText *greeting_;
};
