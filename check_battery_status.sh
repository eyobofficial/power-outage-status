#!/bin/bash

source /home/eyob/power-outage-status/venv/bin/activate

# Check power status (adjust path depending on your system)
POWER_FILE="/sys/class/power_supply/ACAD/online"

if [ ! -f "$POWER_FILE" ]; then
  echo "Power status file not found: $POWER_FILE"
  exit 1
fi

POWER_STATUS=$(cat $POWER_FILE)

if [ "$POWER_STATUS" -eq 1 ]; then
  STATUS="on"
else
  STATUS="off"
fi

# Run Django management command
python src/manage.py update_power_status --status "$STATUS"
