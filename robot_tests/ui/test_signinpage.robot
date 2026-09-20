*** Settings ***
Documentation    Tangerine sign-in page checks with Robot + Playwright.
Resource         common.resource
Test Setup       Open Tangerine Homepage
Test Teardown    Capture Failure Artifacts
Suite Setup      Open Browser Session
Suite Teardown   Close Browser Session

*** Test Cases ***
Sign In Page Title
    Go To Sign In Page
    Page Title Should Contain    Tangerine

