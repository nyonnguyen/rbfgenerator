*** Settings ***
Library     MyCustomizedLibrary
Resource  ../Utilities/Utils.robot
Resource  ../Pages/Login/Login_Page.robot
Variables  Data/settings.yaml

*** Keywords ***
User Open Browser And Go To Webview
  [Arguments]  ${URL}
  Setup Browser
  Go To    ${URL}

Setup Browser
  ${settings} =  Convert To Dictionary  ${BROWSER}
  Setup Browser Driver  ${settings}

User Prepare The Test Environment
  User Open Browser And Go To Webview  ${WEB_URL}
  User Login Successfully To Webview    ${DEFAULT_USERNAME}   ${DEFAULT_PASSWORD}

User Cleanup The Test Environment
  Close Browser

User Cleanup Test Case
  Capture Page Screenshot

