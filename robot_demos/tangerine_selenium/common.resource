*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${TANGERINE_URL}                 https://www.tangerine.ca/en/personal
${LOGIN_BUTTON}                  id:login
${SIGNUP_BUTTON}                 id:menu_signup
${COOKIE_ACCEPT_BUTTON}          id:onetrust-accept-btn-handler
${BROWSER}                       chrome
${SELENIUM_TIMEOUT}              10s
${COOKIE_BANNER_TIMEOUT}         5s

*** Keywords ***
Open Browser Session
    Open Browser    about:blank    ${BROWSER}
    Maximize Browser Window
    Set Selenium Timeout    ${SELENIUM_TIMEOUT}
    Set Selenium Implicit Wait    ${SELENIUM_TIMEOUT}

Close Browser Session
    Capture Page Screenshot
    Close Browser

Open Tangerine Homepage
    Go To    ${TANGERINE_URL}
    Accept Cookies If Present

Accept Cookies If Present
    ${visible}=    Run Keyword And Return Status
    ...    Wait Until Element Is Visible
    ...    ${COOKIE_ACCEPT_BUTTON}
    ...    ${COOKIE_BANNER_TIMEOUT}
    IF    ${visible}
        Click Element    ${COOKIE_ACCEPT_BUTTON}
    END

Go To Sign In Page
    Click Element    ${LOGIN_BUTTON}

Go To Sign Up Page
    Go To Sign In Page
    Click Element    ${SIGNUP_BUTTON}

Page Title Should Contain
    [Arguments]    ${expected}
    ${title}=    Get Title
    Should Contain    ${title}    ${expected}

