
# Cognitive Assignment

This project is designed to provide a foundation for building cognitive applications. It includes necessary files and configurations for setting up the application, including Python scripts, a Dockerfile, and other project-specific settings.

## Table of Contents

1. [Project Structure](#project-structure)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Configuration](#configuration)
5. [Contributing](#contributing)
6. [License](#license)

## Project Structure

```
cognitive-assignment/
├── .git/                   # Git repository files
├── .gitignore              # Git ignore file
├── create_app.py           # Main application script
├── Dockerfile              # Docker configuration file
├── project/                # Project-specific modules and scripts
├── README.md               # This README file
├── requirements.txt        # Python dependencies
```

## Installation

### Prerequisites

- Python 3.10
- Docker (if you plan to use Docker)

### Clone the Repository

```bash
git clone https://github.com/kulich-d/cognitive-assignment.git
cd cognitive-assignment
```

### Install Dependencies

It's recommended to use a virtual environment to manage dependencies.

```bash
python -m venv venv
source venv/bin/activate  
pip install -r requirements.txt
```

## Usage

### Running the Application

To run the application locally, execute the following command:

```bash
# Start server
cd project
python  main.py
#Send request to server

curl  -X POST 'http://0.0.0.0:8000/congnitiv-analysis' \
-H 'accept: application/json' \
-F 'advertisement_image=@{path_to_image}' \
-F 'advertisement_heatmap_image=@{path_to_heatmap}'
```

### Using Docker

Build the Docker image:

```bash
docker build -t cognitive-assignment .
```

Run the Docker container:

```bash
docker run -e OPENAI_API_KEY={specify_OPENAI_API_KEY} \
-p {your_machine_port:default_8000}:{application_port:default_8000} cognitive-assignment
```

### Using Streamlit
```bash
#To run the application with Streamlit, follow these steps:
# - Build and Run Docker (if you haven't already):
# - Run Streamlit:
python streamlit run create_app.py
#This will start the Streamlit server and you can access the application via the provided URL in your terminal.
```



## Configuration

### Environment Variables

The application can be configured using environment variables. Create a `.env` file in the root directory and add your configuration settings there.
- `PORT`: The port on which the application will run. Default is 8000.
- `OPENAI_API_KEY`: Key for OPENAI API access 

### Configuration File

You can configure the application by changing the default parameters in `project/config/config.py`:

- `max_size`: Maximum image size in bytes. This is used to ensure the image size does not exceed the context window limit of the model. Default is 30000 bytes (30 KB).
- `logger_save_path`: Path to the logger file. Defaults to the main.py folder.
- `prompts_config_path`: Path to the .yaml prompts configuration file. Default is `project/analysis/prompts/data.yaml`


You can also configure prompts used in the application using configuration files located in the `project/analysis/prompts` directory.



