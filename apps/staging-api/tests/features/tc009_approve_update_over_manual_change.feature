Feature: Overwriting manual changes via approved updates

  Scenario: Approve an update that overwrites a manual modification
    Given a record in the database has been manually modified
    And the import file contains updated data for the same record
    When the user approves the update in the staging area
    Then the manual modification should be overwritten with the new market data from the file