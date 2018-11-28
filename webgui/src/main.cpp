#include <Wt/WApplication.h>
#include <Wt/WServer.h>

#include "radifi.h"

using namespace Wt;


std::unique_ptr<WApplication> createApplication(const WEnvironment& env)
{
  auto app = cpp14::make_unique<WApplication>(env);

  app->setTitle("Radi-fi");
  app->useStyleSheet("css/default.css");
  app->useStyleSheet("css/radifi.css");
  app->root()->addWidget(cpp14::make_unique<Radifi>());

  return app;
}


int main(int argc, char **argv)
{
  try {
    WServer server(argc, argv, WTHTTP_CONFIGURATION);
    server.addEntryPoint(EntryPointType::Application, createApplication);
    server.run();  
  } catch (WServer::Exception& e) {
    std::cerr << e.what() << std::endl;
  } catch (std::exception &e) {
    std::cerr << "exception: " << e.what() << std::endl;
  }
}
