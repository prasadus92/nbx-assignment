#!/bin/bash

echo "Running the DB Init script..."
python ./init-db.py

echo "Starting the service..."
python ./userservice/__main__.py
