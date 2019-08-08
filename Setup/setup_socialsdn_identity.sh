#!/bin/bash

echo "Creating the ~/.socialsdn configuration directory..."
mkdir ~/.socialsdn
echo "...Done."

echo ""

echo "Generating an identity private/public keypair..."
python3 /opt/socialsdn/create_identity_keypair.py
echo "...Done."
