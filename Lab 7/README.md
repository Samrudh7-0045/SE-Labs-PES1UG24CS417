# Lab 7: Fuzz Testing for Input Validation Bugs

**Course:** Software Engineering (UE22CS351A)  
**Name:** Samrudh Patil  
**SRN:** PES1UG24CS417  
**Roll No:** 52  

## Overview
This folder contains the complete Lab 7 deliverables:
- processor.py / isa_application.py: Corrected application code with comprehensive input validation.
- 	est_processor.py / 	est_visa_application.py: Hypothesis property-based fuzz testing suite and edge-case unit tests.
- Lab7_PES1UG24CS417.pdf: Consolidated PDF submission report containing execution evidence screenshots, bug analysis table, reflection, and full source code.
- screenshots/: High-resolution execution evidence screenshots.

## Test Results
Ran pytest test_processor.py -v:
- **28 / 28 Passed (100% success)** across 6 property-based fuzz tests and 22 edge-case input validation tests.
