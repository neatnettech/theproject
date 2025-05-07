Feature: Reactivating a previously deactivated record

  Scenario: Accept a new record that matches a deactivated record
    Given a record exists in the database with its active flag set to inactive
    And a new record is added that matches the deactivated record
    When the user accepts the new record in the staging area
    Then the system should reactivate the existing record by setting its active flag to active