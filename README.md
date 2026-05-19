# Order Management

Simple order management web application built with Python, Flask and SQLAlchemy.

## Features
- Manage articles, categories, clients and orders
- Automatic stock management (restocks on cancel, line removal, etc.)
- Simple PDF bill generation
- Dashboard with Google Charts

## Requirements
- Python 3.x
- PostgreSQL

## Setup
1. Clone or download the project
2. Rename `.env.exemple` to `.env` and fill in your PostgreSQL credentials
3. Create and activate a virtual environment:
```bash
    py -m venv venv
    venv\Scripts\activate
```
4. Install dependencies:
```bash
    pip install -r requirement.txt
```
5. Run the app:
```bash
    py -m flask --app main run
```

## Running tests
1. Create a `.env.test` file in the `tests/` folder with your test database credentials
2. Run:
```bash
    pytest tests/
```