#!/bin/bash

echo "Creating the ~/.socialsdn configuration directory..."
mkdir ~/.socialsdn
echo "...Done."

echo ""

echo "Generating an identity private/public keypair..."
python3 create_identity_keypair.py
echo "...Done."
