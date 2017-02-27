# {{ project_name }}

## Development Setup

    # Setup
    cp {{ project_name }}/settings/{__,}local_settings.py
    make setup_dev

    # run local server
    make dev

## Production Setup

    # Setup
    make setup_prod

    # run production server
    make prod

## Test Setup

    # Setup
    make setup_test
    
    # run test
    make test
