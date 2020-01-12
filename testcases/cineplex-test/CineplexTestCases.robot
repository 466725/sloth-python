*** Settings ***
Suite Setup     Log To Console      Test Suite Started
Suite Teardown  Suite Teardown Everything
Test Setup      Log To Console      Test Case Started
Test Teardown   Log To Console      Test Case Completed
Library  SeleniumLibrary

Force Tags      Key-Feature
Default Tags    SmokeTest
Test Template
Test Timeout    5000

*** Variables ***
${URL}  https://uat-www.cineplex.com
${Browser}  Chrome
@{CredentialList}   glory.leung@cineplex.com    Cineplex@2019
&{CredentialDict}   username=glory.leung@cineplex.com   password=Cineplex@2019

*** Test Cases ***
Attempt to Log into Cineplex UAT
    [Documentation]  Basic login scenario
    [Tags]  SmokeTest
    Log to Console     %{username} running test on %{os}
    Open Browser    ${URL}      ${Browser}
    Login to Cineplex

*** Keywords ***
Login to Cineplex
    click element  class:loginSignUp
    select frame    //iframe[@id='bootstrapModalIframe']
    input text  id:txtEmailAddress  glory.leung@cineplex.com
    input text  id:txtPassword  Cineplex@2019
    click element   id:btnLogin
Suite Teardown Everything
    Log To Console      Suite Teardown Started
    Close All Browsers
    Log To Console      Suite Teardown Completed