*** Settings ***
Library  MyCustomizedLibrary
Library  OperatingSystem
Variables      ../Tests/Data/settings.yaml

*** Keywords ***
User Open Browser And Go To Webview
  [Arguments]  ${URL}=${WEB_URL}
  Setup Browser
  Maximize Browser Window
  Go To    ${URL}

Setup Browser
  ${existed_var} =  Run Keyword And Return Status   Variable Should Exist   ${BROWSER_DRIVER_PATH}
  Run Keyword If    ${existed_var}
  ...   Setup Browser Driver  ${BROWSER}  ${BROWSER_DRIVER_PATH}
  ...   ELSE
  ...   Setup Browser Driver  ${BROWSER}

User Wait For ${waiting_time} Seconds
  Sleep   ${waiting_time}
