*** Settings ***
Library    playwright_keywords.py


*** Keywords ***
Capture Failure Artifacts
	Run Keyword And Ignore Error    Attach Failure Artifacts

