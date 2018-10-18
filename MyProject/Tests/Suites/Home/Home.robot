*** Settings ***
Library           MyCustomizedLibrary
Resource          ../../../Pages/Home/Home_Page.robot
Resource          Base_Test.robot

Suite Setup       User Prepare The Test Environment

Suite Teardown    Close Browser

*** Keywords ***

User Can View A Product Details At Home Page
    Navigate To Home
    User Clicks On Item Blouse With Price 27.00
