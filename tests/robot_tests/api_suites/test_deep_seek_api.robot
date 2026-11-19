*** Settings ***
Documentation    DeepSeek API demo test using Robot-only RequestsLibrary.
Library          RequestsLibrary
Library          Collections
Library          OperatingSystem

*** Variables ***
${DEFAULT_DEEPSEEK_URL}      https://api.deepseek.com
${MODEL}                     deepseek-chat

*** Test Cases ***
DeepSeek Chat Completion Demo With RequestsLibrary
    # Get the direct DeepSeek API key from the environment.
    ${api_key}=    Get Environment Variable    AI_GEN_API_KEY    ${EMPTY}
    Skip If    '${api_key}' == ''    AI_GEN_API_KEY environment variable is not set. Set it with your DeepSeek API key.

    ${base_url}=    Get Environment Variable    AI_GEN_BASE_URL    ${DEFAULT_DEEPSEEK_URL}
    Log    Using base URL: ${base_url}
    Log    Using model: ${MODEL}

    ${headers}=    Create Dictionary
    ...    Authorization=Bearer ${api_key}
    ...    Content-Type=application/json

    ${message}=    Create Dictionary    role=user    content=Hello, respond with a single line greeting.
    ${messages}=    Create List    ${message}
    ${payload}=    Create Dictionary    model=${MODEL}    messages=${messages}    stream=${False}

    Create Session    deepseek    ${base_url}    verify=False
    ${response}=    POST On Session    deepseek    /chat/completions    json=${payload}    headers=${headers}

    # Expect 200 for successful response
    Should Be Equal As Integers    ${response.status_code}    200

    # Verify response has expected fields
    ${json_response}=    Get From Dictionary    ${response.json()}    choices
    Log    Response: ${json_response}
    Should Not Be Empty    ${json_response}

    ${first_choice}=    Get From List    ${json_response}    0
    ${message_obj}=    Get From Dictionary    ${first_choice}    message
    ${content}=    Get From Dictionary    ${message_obj}    content

    Should Not Be Empty    ${content}
    Log    AI Response: ${content}
