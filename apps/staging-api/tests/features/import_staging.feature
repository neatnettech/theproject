Feature: Staging import

  Scenario: Import a directory file
    Given a valid CSV file "tests/test_data/sample.csv"
    When I POST it to "/api/v1/staging/import/SAPA/USER"
    Then the response status code should be 200
    And the response should contain "Data imported for directory SAPA"