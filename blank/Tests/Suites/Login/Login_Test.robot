*** Settings ***
Library           <Library-name>
Resource          <Feature-page>
Variables         <Test-data-file>

Test Setup       <Prepate-for-login-test-suite>

Test Teardown    <Cleanup-for-login-test-suite>

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

Test Case 3
  <Test steps go here>
