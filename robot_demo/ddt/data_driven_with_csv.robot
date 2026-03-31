*** Settings ***
Documentation     Data-driven calculator tests loaded from CSV using DataDriver.
Library           DataDriver    file=data_driven.csv    dialect=excel
Library           robot_demo.calculator.calculator_library.CalculatorLibrary
Test Template     Calculate

*** Test Cases ***
Calculator with CSV
	[Template]    Calculate
	${expression}    ${expected}

*** Keywords ***
Calculate
	[Arguments]    ${expression}    ${expected}
	Push buttons    C${expression}=
	Result should be    ${expected}


