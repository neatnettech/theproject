Feature: Preserving manual changes by rejecting updates

  Scenario: Reject an update to preserve a manual modification
    Given a record in the database has been manually modified
    And the import file contains updated data for the same record
    When the user rejects the update in the staging area
    Then the manual change should be preserved
    And the system should prevent future automatic updates for that record