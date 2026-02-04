*** Settings ***
Library    SeleniumLibrary

*** Variables ***

*** Test Cases ***
Amazon website home page
    Open Browser    https://www.amazon.com    Chrome
    Sleep    5
    Close Browser

*** Keywords ***
