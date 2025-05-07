Feature: Reactivating a deactivated record via rejection of a matching new one

  Scenario: Reject a new record that matches a deactivated record
    Given a record exists in the database with its active flag set to inactive
    And a new record is added that matches the deactivated record
    When the user rejects the new record in the staging area
    Then the system should reactivate the existing record and set a manual override flag