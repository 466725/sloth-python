*** Settings ***
Documentation  Just a Robot Framework Demo test
Library  Selenium2Library


*** Variables ***
${Broswer} = chrome


*** Test Cases ***
Guest must sign in to check out
    [Documentation]  Present some information about this test case
    [Tags]  Smoke
    Open Browser  http://www.amazon.com  ${Broswer}
    Wait Until Page Contains  Your Amazon.com
    Input Text  id=twotabsearchtextbox   Ferrari 458
    Click Button    xpath=//*[@id="nav-search"]/form/div[2]/div/input
    Wait Until Page Contains  results for "Ferrari 458"
    Close Browser

Open and then close Chrome browser
    Open Browser    http://www.amazon.com     Chrome
    Close Browser
    Log To Console    Completed Successfully

Open and then close Firefox browser
    Open Browser    http://www.amazon.com    Firefox
    Close Browser


*** Keywords ***