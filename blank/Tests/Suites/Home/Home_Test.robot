*** Settings ***
Library           <Library-name>
Resource          <Resource-page>
Resource          Base_Test.robot

Suite Setup       <Prepare-for-test-suite>

Suite Teardown    <Cleanup-for-test-suite>

*** Keywords ***
Keyword 1
  <Action go here>

Keyword 2
  <Action go here>

*** Test Cases ***
Test Case 1
  <Test steps go here>

Test Case 2
  <Test steps go here>