```markdown
# Django Event Scheduler

A Django-based Event Scheduling and Registration System using the built-in SQLite database and styled with Tailwind CSS.

## Features

- **Event Management**:
  - List all events grouped by category.
  - Filter events by category.
  - View details of a single event and its attendees.

- **Registration System**:
  - Register for events using name and email (no login required).
  - Prevent duplicate registrations for the same event.
  - Cancel registrations easily.

- **Admin Interface**:
  - Manage event categories, events, and attendees.

- **Styling**:
  - Responsive and modern design using Tailwind CSS.

## Models

1. **EventCategory**
   - `name`: The name of the event category.

2. **Event**
   - `title`: The title of the event.
   - `date`: The date of the event.
   - `location`: The location of the event.
   - `category`: A foreign key to the `EventCategory`.

3. **Attendee**
   - `name`: The name of the attendee.
   - `email`: The email address of the attendee.

4. **Registration**
   - `attendee`: A foreign key to the `Attendee`.
   - `event`: A foreign key to the `Event`.
   - `registered_on`: The date and time the registration was made (auto-generated).

## Setup Instructions

### Prerequisites

- Python 3.8+
- Django 4.0+
- Node.js (for Tailwind CSS if using `django-tailwind`)

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/saaya-code/DjangoEventScheduler.git
   cd DjangoEventScheduler
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

5. Access the application at `http://127.0.0.1:8000/`.

### Tailwind CSS Setup

If you're using `django-tailwind` for styling:

1. Install the Tailwind app:

   ```bash
   python manage.py tailwind install
   ```

2. Start the Tailwind watcher:

   ```bash
   python manage.py tailwind start
   ```

For static files, ensure your Tailwind CSS files are included in the `static` directory.

### Admin Panel

To access the admin interface:

1. Create a superuser account:

   ```bash
   python manage.py createsuperuser
   ```

2. Log in at `http://127.0.0.1:8000/admin/`.

## Usage

- **View Events**: Browse events grouped by category.
- **Event Details**: View event details, including the list of attendees.
- **Register**: Register for events using your name and email.
- **Admin Management**: Control categories, events, and attendees through the admin interface.

## Folder Structure

```
DjangoEventScheduler/
├── event_scheduler/      # Main Django app
├── templates/            # HTML templates
├── static/               # Static files (Tailwind CSS, JavaScript, etc.)
├── db.sqlite3            # SQLite database
├── manage.py             # Django management script
└── requirements.txt      # Python dependencies
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes.

## License

This project is licensed under the [MIT License](LICENSE).

## Acknowledgments

- Built with [Django](https://www.djangoproject.com/) and [Tailwind CSS](https://tailwindcss.com/).
```
