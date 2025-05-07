Feature: Rejecting new records from staging

  Scenario: Reject a new record that is not yet in the database
    Given a new record is found in the import file and is not present in the database
    When the user rejects the new record in the staging area
    Then the record should be added to the database and marked as inactive with a manual override flag