Feature: Transition staging change

  Scenario: Submit a staging change for review
    Given an existing staging change with record key "ID000000ABCD"
    When I POST to "/api/v1/staging/<change_id>/transition" with action "submit"
    Then the response status code should be 200
    And the response should contain "Transition 'submit' applied successfully."