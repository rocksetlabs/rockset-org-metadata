# Rockset Org Metadata Script

This script retrieves metadata from a Rockset organization and saves it into JSON files. It supports various endpoints, such as users, collections, integrations, lambdas, aliases, views, and workspaces (ws). The script includes options for debugging, verbosity, and limiting the number of collections processed.

## Features

- Retrieves metadata from Rockset endpoints.
- Supports debugging and verbose modes.
- Allows limiting the number of collections processed.
- Saves each endpoint's data into separate JSON files.

## Requirements

- Python 3.9 or higher
- `requests` library
- `tqdm` library

## Installation

1. Create and activate a virtual environment:

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

2. Install the required packages:

    ```sh
    pip install requests tqdm
    ```

## Usage

Run the script with the required `--apiKey` argument. Additional optional arguments are available for debugging, verbosity, and limiting the number of collections processed.

    python3 rockset_org_metadata.py --apiKey your_api_key [--debug] [--verbose] [--limit COLLECTION_LIMIT]

### Arguments

- `--apiKey`: **(Required)** Your Rockset API key.
- `--debug`: **(Optional)** Enable debug mode for troubleshooting.
- `--verbose`: **(Optional)** Enable verbose mode for displaying exceptions.
- `--limit`: **(Optional)** Limit the number of collections processed.

### Example

    python3 rockset_org_metadata.py --apiKey <your apikey> --debug --verbose --limit 10

## Directory Structure

The script will create a `rockset_org` directory and save the JSON files for each endpoint in this directory.

## Exiting the Virtual Environment

To deactivate the virtual environment, use the following command:

    deactivate

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.

## Acknowledgements

This project uses the following libraries:

- [requests](https://pypi.org/project/requests/)
- [tqdm](https://pypi.org/project/tqdm/)

For more information, refer to the official Rockset documentation.
