# Django Minimal Boilerplate

Django Minimal Boilerplate is a minimalistic Django project template that provides a starting point for your Django web applications. It includes essential configurations, directory structure, and a set of useful features to kickstart your development process.

## Features

- Django 3.2: The latest stable version of Django.
- Simple project structure: Provides a clean and organized project structure to help you start your development quickly.
- Customizable settings: Easily modify project settings to suit your specific needs.
- Database configuration: Pre-configured to use PostgreSQL by default, but you can easily switch to other databases like SQLite or MySQL.
- Environment variables: Uses the python-decouple library to manage environment variables for your local development and production deployment.
- Debug toolbar: Includes Django Debug Toolbar to assist with debugging during development.

## Getting Started

Follow these instructions to get a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)
- PostgreSQL

### Installation

1. Clone the repository:

```shell
git clone https://github.com/azadhmhd/django_minimal_boilerplate.git
```

2. Create a virtual environment and activate it:

```shell
python3 -m venv myenv
source myenv/bin/activate
```

3. Install the required Python packages:

```shell
pip install -r requirements.txt
```

4. Set up the environment variables:

- Rename the `.env.sample` file to `.env`.
- Open the `.env` file and provide the necessary values for the environment variables.


### Configuration

1. Migrations
- Apply the initial database migrations by running the following command:
```shell
python manage.py migrate
```

### Usage

To run the Django development server, execute the following command:
```shell
python manage.py runserver
```


Once the server is running, you can access the application by visiting `http://localhost:8000` in your web browser.

### Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bug fix.
3. Make the necessary changes and commit them.
4. Push your changes to your fork.
5. Submit a pull request with a detailed description of your changes.

### License

This project is licensed under the <u>**MIT License**</u>. Feel free to use and modify it according to your needs.

### Acknowledgements

We would like to acknowledge the following resources and projects that inspired and helped in the development of this boilerplate:

- Django
- PostgreSQL

### Contact

If you have any questions or suggestions, feel free to contact us at azadhmhd@gmail.com. We appreciate your feedback!


```shell
Feel free to customize and expand this README file to provide more detailed information about your Django Minimal Boilerplate project.

```
