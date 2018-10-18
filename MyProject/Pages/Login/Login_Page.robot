*** Settings ***
Library           MyCustomizedLibrary
Resource          ./Login_Actions.robot

*** Keywords ***
User Input Username And Password
  [Arguments]  ${username}  ${password}
  Input Username Field      ${username}
  Input Password Field      ${password}
  Focus On Login Button

User Login To Webview
  [Arguments]  ${username}  ${password}
  User Input Username And Password    ${username}    ${password}
  Click Login Button

User Login Successfully To Webview
  [Arguments]   ${username}  ${password}
  User Login To Webview    ${username}    ${password}
  User Should Not See The Login Page

User Should See Message "Authentication failed" In Login Page
  Login Should Be Failed With Message

User Should See Message "An email address required" In Login Page
  Username Field Should Be Required

User Should See Message "Invalid email address" In Login Page
  Username Field Should Be Valid

User Should See Message "Password is required" In Login Page
  Password Field Should Be Required

User Should See The Login Page
  Login Page Should Be Appear

User Should Not See The Login Page
  Login Page Should Be Disappeared
