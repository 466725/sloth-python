*** Settings ***
Documentation     Just a Robot Framework Demo test
Library           SeleniumLibrary

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

Open and then close Firefox browser
    [Tags]    smoke
    Open Browser    https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&switch_account=    Firefox
    Input Text    id=ap_email    @{credentials}[0]
    Input Password    id=ap_password    @{credentials}[1]
    Click Button    id=signInSubmit
    Close Browser

Open and then close Firefox browser with home-made keyword
    [Tags]    smoke
    Open Browser    https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&switch_account=    Firefox
    Login with default info
    Close Browser

Open and then close Chrome browser
    [Tags]    smoke
    Open Browser    https://www.amazon.com/ap/signin?_encoding=UTF8&ignoreAuthState=1&openid.assoc_handle=usflex&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.mode=checkid_setup&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&openid.ns.pape=http%3A%2F%2Fspecs.openid.net%2Fextensions%2Fpape%2F1.0&openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_signin&switch_account=    Chrome
    Input Text    id=ap_email    &{amazonDict}[username]
    Input Password    id=ap_password    &{amazonDict}[password]
    Click Button    id=signInSubmit
    Close Browser
    Log To Console    Completed Successfully

*** Keywords ***
Login with default info
    Input Text     id=ap_email     @{credentials}[0]
    Input Password    id=ap_password     @{credentials}[1]
    Click Button    id=signInSubmit
