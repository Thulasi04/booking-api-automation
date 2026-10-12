# Booking API Automation Framework

## Overview

This project is an API automation testing framework developed using **Python, Playwright, and Pytest** to validate the RESTful Booker API.

The framework automates API operations and validates HTTP status codes, response data, and expected behavior. It is designed to demonstrate API testing fundamentals, reusable code, and automated test execution.

## Application Under Test

- **Application:** RESTful Booker
- **Base URL:** https://restful-booker.herokuapp.com

RESTful Booker is a demo API that provides booking-related operations for practicing and learning API testing.

## Technologies Used

- **Python** – Programming language
- **Playwright** – API request handling
- **Pytest** – Test execution and test organization
- **pytest-html** – HTML test reporting

## Features

- Automated API testing using Playwright and Pytest
- Reusable API client methods
- Validation of HTTP response status codes
- Validation of response data and booking details
- Testing of booking-related API operations
- Test execution through Pytest
- HTML test report generation

## API Operations

The RESTful Booker API supports the following operations:

| HTTP Method | Operation | Purpose |
|---|---|---|
| GET | Retrieve bookings | Fetch booking IDs or booking details |
| POST | Create booking | Create a new booking |
| PUT | Update booking | Update booking details |
| PATCH | Partial update | Modify selected booking fields |
| DELETE | Delete booking | Remove a booking |

The actual automated coverage depends on the test cases implemented in this repository.


