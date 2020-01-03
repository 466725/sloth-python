*** Settings ***
Library  SeleniumLibrary

*** Variables ***

*** Test Cases ***
LoginTest
    open browser    https://uat-www.cineplex.com    chrome
    click element  class:loginSignUp
    select frame    //iframe[@id='bootstrapModalIframe']
    input text  id:txtEmailAddress  glory.leung@cineplex.com
    input text  id:txtPassword  Cineplex@2019
    click element   id:btnLogin
    close browser




*** Keywords ***
