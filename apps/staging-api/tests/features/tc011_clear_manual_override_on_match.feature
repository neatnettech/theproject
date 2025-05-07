Feature: Clearing manual override on data reconciliation

  Scenario: File update matches manual change
    Given a record in the database has been manually modified
    And the import file contains updated data that matches the manual changes
    When the system detects the update
    Then the manual override flag should be cleared
    And the user should be notified about the data reconciliation