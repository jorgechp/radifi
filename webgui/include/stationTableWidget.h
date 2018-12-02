#include <vector>
#include <Wt/WContainerWidget.h>
#include <Wt/WTable.h>

#include "station.h"
#include"radifiServiceAPI.h"

using namespace Wt;

/**
* This class represent a table of Station instances.
*/
#pragma once
class StationTableWidget : public WTable{
public:
  /**
  * Default public constructor.
  */
  StationTableWidget(RadifiServiceAPI& api);

  /**
  * Add a station to the table as well as the service.
  * @param stationToAdd The Station instance to be added.
  * @return bool true if the new station were properly added. false if there is
  *              a duplicate.
  */
  bool addStation(Station &stationToAdd);

  /**
  * Insert a new station at the end of the station list.
  * @param stationToInsert The station to be inserted.
  */
  void insertStation(Station &stationToInsert);

  /**
  * Returns the number of stations.
  * @return int The number of stations.
  */
  int getNumStations();

  /**
  * Rederize the table.
  */
  void generateTable();
private:
  RadifiServiceAPI* api;

  std::vector<Station> stationVector; /*A vector with Station instances*/

  /**
  * Remove a station from the table.
  * @param stationIndex The index of the station to be removed.
  * @return boolean true if the item was removed. false if the item doesn't exits.
  */
  bool removeStation(unsigned int stationIndex);

  /**
  * Play a station from the table.
  * @param stationIndex The index of the station to be removed.
  * @return boolean true if the item was removed. false if the item doesn't exits.
  */
  bool sintonizeStation(unsigned int stationIndex);



};
