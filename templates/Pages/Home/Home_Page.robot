*** Settings ***
Library           MyCustomizedLibrary
Resource          ./Home_Actions.robot

*** Keywords ***
User Should See The Content Of Home Page
  Home Page Content Should Be Appeared

User Navigate To Home Page
  Navigate To Home
  Wait Until Home Page Is Loaded

User Clicks On Item ${name} With Price ${price}
  Click On Item On Home Page   ${name}  ${price}
