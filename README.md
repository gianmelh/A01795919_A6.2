# A01795919_A6.2  
## Reservation System  
TC4017.10 – Pruebas de Software y Aseguramiento de la Calidad  

### 👤 Student  
Gianmel Joannelly Hernández Tosta  
Matrícula: A01795919  

---

## Description

This project implements a **Reservation System** in Python.  
The system allows managing:

- Customers
- Hotels
- Reservations
- JSON-based persistence
- Unit testing
- Static code analysis
- Code coverage measurement

The implementation follows **PEP-8 coding standards** and best practices in software quality assurance.

---

## Project Structure
A01795919_A6.2/
│
├── src/
│ ├── customer.py
│ ├── hotel.py
│ ├── reservation.py
│ ├── storage.py
│ └── exceptions.py
│
├── tests/
│ ├── test_customer.py
│ ├── test_hotel.py
│ ├── test_reservation.py
│ └── test_storage_invalid_json.py
│
├── data/
├── evidence/
└── README.md


---

## 🧪 Unit Testing

All tests were implemented using Python’s built-in `unittest` framework.

### Total Tests Executed:
- 18 tests
- Multiple negative test cases included
- All tests passed successfully

To execute tests:

```bash
python -m unittest -v