Feature: Approving new records from staging

  Scenario: Approve a new record that is not yet in the database
    Given a new record is found in the import file and is not present in the database
    When the user approves the new record in the staging area
    Then the new record should be added to the database and marked as active