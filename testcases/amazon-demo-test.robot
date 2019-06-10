*** Settings ***
Documentation     Just a Robot Framework Demo test
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
${Browser}        Chrome    # By default, use chrome
@{credentials}    fake@gmail.com    fake    admin@gmail.com    admin
&{amazonDict}     username=fake@gmail.com    password=fake

*** Test Cases ***
Guest must sign in to check out
    [Documentation]    Basic test scenario based on amazon url for the purpose of Robot demo.
    [Tags]    Smoke
    Log To Console    %{username} runing test on %{os}
    Open Browser    http://www.amazon.com    ${Browser}
    Wait Until Page Contains    Your Amazon.com
    Input Text    id=twotabsearchtextbox    Ferrari 458
    Click Button    xpath=//*[@id="nav-search"]/form/div[2]/div/input
    Wait Until Page Contains    results for "Ferrari 458"
    Close Browser

Login with fake credentials from list variable
    [Tags]    smoke
    Open Browser    https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&switch_account=    Firefox
    Input Text    id=ap_email    @{credentials}[0]
    Input Password    id=ap_password    @{credentials}[1]
    Click Button    id=signInSubmit
    Close Browser

Login with user keyword
    [Tags]    smoke
    Open Browser    https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&switch_account=    Firefox
    Default Login
    Close Browser

Login with fake credentials from dictionary variable
    [Tags]    smoke
    Open Browser    https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&switch_account=    Chrome
    Input Text    id=ap_email    &{amazonDict}[username]
    Input Password    id=ap_password    &{amazonDict}[password]
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
    Input Text     id=ap_email     @{credentials}[0]
    Input Password    id=ap_password     @{credentials}[1]
    Click Button    id=signInSubmit
    Log To Console    Login with default info from list completed
