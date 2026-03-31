*** Settings ***
Documentation    DeepSeek API demo test using Robot Framework.
Library          robot_demo.api.deep_seek_keywords

*** Test Cases ***
DeepSeek Chat Completion Demo
    ${status}=    Call Deepseek Chat Completion Demo
    Should Match Regexp    ${status}    ^(success|missing_api_key|error)$
    Log    DeepSeek demo status: ${status}

