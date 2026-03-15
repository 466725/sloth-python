*** Settings ***
Library    SeleniumLibrary

*** Variables ***

*** Test Cases ***
Tangerine website home page
    Open Browser    https://www.tangerine.com    Chrome
    Sleep    5
    Close Browser

*** Keywords ***
