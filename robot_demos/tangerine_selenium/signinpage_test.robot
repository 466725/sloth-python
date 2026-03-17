*** Settings ***
Documentation    Tangerine sign-in page checks with SeleniumLibrary.
Resource         common.resource
Test Setup       Open Tangerine Homepage
Suite Setup      Open Browser Session
Suite Teardown   Close Browser Session

*** Test Cases ***
Sign In Page Title
    Go To Sign In Page
    Page Title Should Contain    Tangerine

