*** Settings ***
Library   MyCustomizedLibrary
Resource  ./Login_Variables.robot

*** Keywords ***
Input Username Field
  [Arguments]   ${username}
  Input Text    ${USERNAME_FIELD}  ${username}

Input Password Field
  [Arguments]   ${password}
  Input Password  ${PASSWORD_FIELD}  ${password}

Clear Username Field
  [Arguments]   ${username}
  Clear Textfield Value    ${USERNAME_FIELD}

Clear Password Field
  [Arguments]   ${password}
  Clear Textfield Value    ${PASSWORD_FIELD}

Click Login Button
  Click Button   ${LOGIN_BUTTON}

Username Field Should Be Required
  Wait Until Alert Displayed
  Is Error Message    ${USERNAME_IS_REQUIRED_MESSAGE}

Password Field Should Be Required
  Wait Until Alert Displayed
  Is Error Message    ${PASSWORD_IS_REQUIRED_MESSAGE}

Username Field Should Be Valid
  Wait Until Alert Displayed
  Is Error Message    ${USERNAME_IS_INVALID_MESSAGE}

Login Should Be Failed With Message
  Wait Until Alert Displayed
  Is Error Message    ${AUTHEN_FAILED_MESSAGE}

Focus On Username Field
  Set Focus To Element    ${USERNAME_FIELD}

Focus On Password Field
  Set Focus To Element    ${PASSWORD_FIELD}

Focus On Login Button
  Set Focus To Element    ${LOGIN_BUTTON}

Login Page Should Be Appear
  Wait Until Element Is Visible  ${USERNAME_FIELD}
  Wait Until Element Is Visible  ${PASSWORD_FIELD}
  Wait Until Element Is Visible  ${LOGIN_BUTTON}
  Wait Until Location is    ${LOGIN_URL}

Login Page Should Be Disappeared
  Wait Until Element Is Not Visible  ${USERNAME_FIELD}
  Wait Until Element Is Not Visible  ${PASSWORD_FIELD}
  Wait Until Element Is Not Visible  ${LOGIN_BUTTON}

Main Header Contains User Name
  [Arguments]  ${name}
  Element Should Contain  ${MAIN_HEADER}  ${name}
