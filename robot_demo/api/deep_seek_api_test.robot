*** Settings ***
Documentation    DeepSeek API demo test using Robot-only RequestsLibrary.
Library          RequestsLibrary
Library          Collections
Library          OperatingSystem

*** Variables ***
${DEFAULT_DEEP_SEEK_URL}    https://api.deepseek.com
${MODEL}                    deepseek-chat

*** Test Cases ***
DeepSeek Chat Completion Demo With RequestsLibrary
    ${api_key}=    Get Environment Variable    OPENAI_API_KEY    ${EMPTY}
    Skip If    '${api_key}' == ''    OPENAI_API_KEY is not set.
    ${base_url}=    Get Environment Variable    DEEP_SEEK_URL    ${DEFAULT_DEEP_SEEK_URL}

    ${headers}=    Create Dictionary
    ...    Authorization=Bearer ${api_key}
    ...    Content-Type=application/json

    ${message}=    Create Dictionary    role=user    content=Hello
    ${messages}=    Create List    ${message}
    ${payload}=    Create Dictionary    model=${MODEL}    messages=${messages}    stream=${False}

    Create Session    deepseek    ${base_url}
    ${response}=    POST On Session    deepseek    /chat/completions    json=${payload}    headers=${headers}
    Should Be Equal As Integers    ${response.status_code}    200

    ${response_json}=    Evaluate    $response.json()
    Dictionary Should Contain Key    ${response_json}    id
    Log    DeepSeek call succeeded with id: ${response_json}[id]

