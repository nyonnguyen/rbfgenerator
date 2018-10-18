*** Settings ***
Library     MyCustomizedLibrary
Resource    ../Utilities/Utils.robot
Resource    ../Pages/Home/Home_Page.robot
Resource    ../Pages/Login/Login_Page.robot
Variables   Data/settings.yaml

#Suite Setup     User Prepare The Test Environment
#Suite Teardown  Close Browser

*** Keywords ***
User Prepare The Test Environment
  User Navigates To Webview
  User Login Successfully To Webview    ${DEFAULT_USERNAME}   ${DEFAULT_PASSWORD}

User Navigates To Webview
  User Open Browser And Go To Webview  ${LOGIN_URL}
