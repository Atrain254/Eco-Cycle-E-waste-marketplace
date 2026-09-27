# Eco-Cycle E-Waste Marketplace

Eco-Cycle is a Django web application for listing unwanted electronics and connecting their owners with people interested in salvaging or reusing them. Users can browse listings, search by title or description, filter by category, and view estimated salvage values.

The app includes account types for households and Jua Kali technicians, item listings with optional photos, and a claim flow for available items.

## Features

- Browse available e-waste listings and search by keyword or category.
- Register as a household or technician and sign in to the site.
- Create listings with a description, condition, category, and optional image.
- Calculate an estimated salvage value from the category's base rate and the item's condition:
	- Working: 100% of the base rate
	- Partially working: 50% of the base rate
	- Dead: 15% of the base rate
- Claim an item so it no longer appears among available marketplace listings.
- View a dashboard with claimed items or listing information.

Role-specific permissions are not yet fully implemented. Creating a listing is not currently restricted to signed-in users, and new listings are assigned to the first user in the database rather than the person submitting the form. Claiming an item requires sign-in but is not restricted to technician accounts. The household dashboard currently displays all items rather than only items listed by that user.

## Technology

- Python and Django
- Django templates, HTML, and Bootstrap 5
- SQLite for local development
- Playwright for a browser-based marketplace check

## Requirements

- Python 3.12 or newer
- pip

## Run Locally

Open a terminal in the repository directory and run:

```bash
git clone https://github.com/Atrain254/Eco-Cycle-E-waste-marketplace.git
cd Eco-Cycle-E-waste-marketplace
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

On macOS or Linux:

```bash
source .venv/bin/activate
```

Install dependencies, create the database tables, and create an administrator account:

```bash
python -m pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
```

Start the development server:

```bash
python manage.py runserver
```

Open [http://127.0.0.1:8000/](http://127.0.0.1:8000/) to visit the marketplace. The root URL redirects to `/marketplace/`. Sign in to the admin site at [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) and add one or more categories with base salvage rates before creating listings.

## Run the Browser Check

The included Playwright script expects the development server to be running. In a second terminal, activate the virtual environment and install Playwright if needed:

```bash
python -m pip install playwright
python -m playwright install chromium
python ui_tests.py
```

The script opens Chromium in headed mode and checks that the marketplace loads and its search field can be used. It is a small UI smoke check, not a comprehensive automated test suite. Django's `marketplace/tests.py` does not currently define tests.

## Project Layout

```text
ecocycle/                 Django project settings and URL configuration
marketplace/              Marketplace models, views, forms, and templates
media/item_images/        Uploaded listing images
manage.py                 Django management commands
ui_tests.py               Playwright browser smoke check
```

## Development Note

The included Django settings are for local development. Before deploying, replace the development secret key, turn off debug mode, configure allowed hosts, and review Django's deployment security checklist.

## Credits

- **Author:** Vinjo Sibabi Archilles
- **Institution:** Kabarak University