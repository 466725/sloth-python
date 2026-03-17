*** Settings ***
Documentation    Tangerine homepage checks with Robot + Playwright.
Resource         common.resource
Test Setup       Open Tangerine Homepage
Suite Setup      Open Browser Session
Suite Teardown   Close Browser Session

*** Test Cases ***
Homepage Title
    Page Title Should Contain    Tangerine

