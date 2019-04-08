*** Settings ***
Library           MyCustomizedLibrary
Resource          ../Tests/Base_Test.robot
Resource          ../Pages/Login/Login_Page.robot
Variables         ../Tests/Data/Login/Login.yaml

Test Setup       User Navigates To Login Page

Test Teardown    User Cleanup Test

*** Keywords ***


*** Test Cases ***
#TC_1_1 User Could Not Login To Webview When Email Is Empty
#  [Tags]    TC_1_1
#  When User Login To Webview     ${TC01_1.USERNAME}    ${TC01_1.PASSWORD}
#  Then User Should See Message "An email address required" In Login Page
#
#TC_1_2 User Could Not Login To Webview When Password Is Empty
#  [Tags]    TC_1_2
#  When User Login To Webview    ${TC01_2.USERNAME}    ${EMPTY}
#  Then User Should See Message "Password is required" In Login Page
#
#TC_1_3 Invalid Email Could Not Login To Webview
#  [Tags]    TC_1_3
#  When User Login To Webview      ${TC01_3.USERNAME}    ${TC01_3.PASSWORD}
#  User Should See Message "Invalid email address" In Login Page
#
TC_1_4 Incorrect User Could Not Login To Webview
  [Tags]    TC_1_4
  When User Login To Webview      ${TC01_4.USERNAME}    ${TC01_4.PASSWORD}
  User Should See Message "Authentication failed" In Login Page

TC_1_5 Valid User Could Login To Webview
  [Tags]    TC_1_5
  When User Login To Webview      ${TC01_5.USERNAME}    ${TC01_5.PASSWORD}
  Then User Should Not See The Login Page


*** Keywords ***

User Navigates To Login Page
  User Open Browser And Go To Webview  ${LOGIN_URL}
  User Should See The Login Page

User Cleanup Test
  Capture Page Screenshot
  Close Browser

