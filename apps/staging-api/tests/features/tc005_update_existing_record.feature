Feature: Updating existing records with file data

  Scenario: Approve update when file data matches an existing record
    Given an existing record is present in the database
    And the import file contains updated data for the same record
    When the user approves the update in the staging area
    Then the existing record in the database should be updated with the new data from the file