Feature: Rejecting deletion of records from file

  Scenario: Reject deletion of a record from file
    Given an existing record is present in the database
    And the import file marks the record for deletion
    When the user rejects the deletion in the staging area
    Then the record should remain in the database
    And its active flag should be set to active
    And a manual override flag should be set on the record