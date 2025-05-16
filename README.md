# Expense Manager

A professional and modular expense management system built with Python and FastAPI. This application helps individuals or organizations track and manage their expenses efficiently.

## Features

- Add, update, and delete expenses
- Categorize and filter expenses
- RESTful API structure
- MySQL database integration
- Modular architecture
- Configurable environments
- Unit testing with Pytest

## Installation

```bash
git clone https://github.com/yourusername/expense-manager.git
cd expense-manager
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
pip install -r requirements.txt
```

## Configuration

Set up your environment variables using a `.env` file or directly in `config/settings.py`. Make sure to configure your MySQL database credentials correctly.

## Running the Application

```bash
uvicorn main:app --reload
```

## Running Tests

```bash
pytest
```

## Contributing

We welcome contributions from the community to improve and expand this project.

To contribute:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add Your Feature'`)
4. Push to the branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

Please make sure your code adheres to PEP8 standards and is well-tested.

We appreciate all kinds of contributions including bug reports, feature requests, documentation updates, and code improvements.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**Let's build a better financial future together!**
