Feature: Rejecting updates for existing records

  Scenario: Reject update when file data matches an existing record
    Given an existing record is present in the database
    And the import file contains updated data for the same record
    When the user rejects the update in the staging area
    Then the original data in the database should be retained
    And the system should prevent future automatic updates for that record