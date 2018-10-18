*** Settings ***
Library           MyCustomizedLibrary
Resource          ./Home_Variables.robot

*** Keywords ***
Navigate To Home
  Go To  ${HOME_URL}
  Home Page Content Should Be Appeared

Logout
  Wait Until Element Is Visible    ${LOGOUT_BUTTON}
  Click Button    ${LOGOUT_BUTTON}

Home Page Content Should Be Appeared
  Wait Until Element Is Visible  ${HOME_PAGE_MAIN_TAB}
  Wait Until Element Is Visible  ${HOME_PRODUCT_LIST}

Click On Item On Home Page
    [Arguments]  ${p_name}  ${p_price}
    Click On Product Item  ${HOME_PRODUCT_LIST}  ${p_name}  ${p_price}
    Wait Until Element Is Visible  ${ADD_TO_CART_BUTTON}
