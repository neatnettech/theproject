Feature: Deleting records via staging approval

  Scenario: Approve deletion of a record from file
    Given an existing record is present in the database
    And the import file marks the record for deletion
    When the user approves the deletion in the staging area
    Then the record should remain in the database
    And its active flag should be set to inactive
    And it should no longer appear as active in the system