# Mini Blog

A modern, beautiful Flask-based mini blog application.

## Features
- Create, edit, and delete posts
- Add comments to posts
- Author, tags, and timestamps
- Search posts
- Responsive, modern UI
- Dockerized for easy deployment

## Getting Started

### Local Development
1. Clone the repo
2. Create a virtual environment and install dependencies:
   ```
   python -m venv .venv
   .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. Run the app:
   ```
   flask run
   ```

### Docker
1. Build and run with Docker Compose:
   ```
   docker-compose up --build
   ```
2. Access at [http://localhost:5000](http://localhost:5000)

## Environment Variables
See `.env` for configuration.

## License
MIT
