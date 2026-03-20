*** Settings ***
Documentation    Tangerine sign-up page checks with SeleniumLibrary.
Resource         common.resource
Test Setup       Open Tangerine Homepage
Test Teardown    Capture Failure Artifacts
Suite Setup      Open Browser Session
Suite Teardown   Close Browser Session

*** Test Cases ***
Sign Up Page Title
    Go To Sign Up Page
    Page Title Should Contain    Tangerine

