*** Settings ***
Documentation     Basic Robot Framework examples: Log, list variables, and dictionary variables.

*** Variables ***
${APP_NAME}        Sloth Python
@{COLORS}          red    green    blue
&{USER_PROFILE}    name=Weipeng    role=QA Engineer    city=Toronto

*** Test Cases ***
Log Example
    Log    Running basic Robot demo for ${APP_NAME}
    Log    This is an INFO log entry.    INFO

List Variable Example
    Log    Available colors: ${COLORS}
    Log    First color: ${COLORS}[0]
    FOR    ${color}    IN    @{COLORS}
        Log    Color item: ${color}
    END

Dictionary Variable Example
    Log    User profile: ${USER_PROFILE}
    Log    Name: ${USER_PROFILE}[name]
    Log    Role: ${USER_PROFILE}[role]
    Should Be Equal    ${USER_PROFILE}[city]    Toronto

If Else Example
    ${env}=    Set Variable    qa
    IF    '${env}' == 'prod'
        Log    Running PROD checks
    ELSE
        Log    Running NON-PROD checks: ${env}
    END
    Should Be Equal    ${env}    qa

If Else If Example
    ${env}=    Set Variable    stage
    IF    '${env}' == 'prod'
        Log    Running PROD checks
    ELSE IF    '${env}' == 'stage'
        Log    Running STAGE checks
    ELSE
        Log    Running checks for another env: ${env}
    END
    Should Be Equal    ${env}    stage
