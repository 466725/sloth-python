*** Settings ***
Documentation     Robot Framework Demo test
Suite Setup       Log To Console    Test Suite Started    
Suite Teardown    Suite Teardown Everything    
Test Setup        Log To Console    Test Case Started    
Test Teardown     Log To Console    Test Case Completed    
Library           SeleniumLibrary

Force Tags    Key-Feature
Default Tags    Smoke
Test Template
Test Timeout    5000
*** Variables ***
${URL}    https://www.amazon.ca/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=caflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.ca%2F%3Fref_%3Dnav_custrec_signin&switch_account=
${Browser}        Chrome    # By default, use chrome
@{CredentialsList}    fake@gmail.com    fake    admin@gmail.com    admin
&{CredentialsDict}     username=fake@gmail.com    password=fake

*** Test Cases ***
Guest must sign in to check out
    [Documentation]    Basic test scenario for the purpose of Robot demo
    [Tags]    Smoke
    Log To Console    %{username} runing test on %{os}
    Open Browser    ${URL}    ${Browser}
    Wait Until Page Contains    Sign in
    Input Text    xpath=.//input[@id="ap_email"]    @{CredentialsList}[0]
    Input Password    xpath=.//input[@id="ap_password"]    @{CredentialsList}[1]
    Click Button    xpath=.//input[@id="signInSubmit"]
    Wait Until Page Contains    Enter the characters you see
    Close Browser

Login with fake credentials from list variable
    [Tags]    smoke
    Open Browser    ${URL}    Firefox
    Input Text    id=ap_email    @{CredentialsList}[0]
    Input Password    id=ap_password    @{CredentialsList}[1]
    Click Button    id=signInSubmit
    Close Browser

Login with user keyword
    [Tags]    smoke
    Open Browser    ${URL}    Firefox
    Default Login
    Close Browser

Login with fake credentials from dictionary variable
    [Tags]    smoke
    Open Browser    ${URL}    Chrome
    Input Text    id=ap_email    &{CredentialsDict}[username]
    Input Password    id=ap_password    &{CredentialsDict}[password]
    Click Button    id=signInSubmit
    Close Browser
    Log To Console    Completed Successfully

*** Keywords ***
Suite Teardown Everything
    Log To Console    Suite Teardown started
    Close All Browsers
    Log To Console    Suite Teardown Completed
Default Login
    Log To Console    Login with default info from list started
    Input Text     id=ap_email     @{CredentialsList}[0]
    Input Password    id=ap_password     @{CredentialsList}[1]
    Click Button    id=signInSubmit
    Log To Console    Login with default info from list completed
