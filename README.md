# Tuition Reminder Discord Bot (Development Branch)

This branch contains the in-progress version of the tuition-reminder bot.  
Core features are implemented and the project is being prepared for use on a real student Discord server.

## Current Features

- Automated tuition reminders:
  - 7 days before the end of the month
  - 1 day before the end of the month
  - on the due date
- Admin commands (role-restricted):
  - `/set_normal <value>` – set payment for regular months
  - `/set_holiday <value>` – set payment for holiday months (e.g. July/August)
- Configuration stored in JSON (persistent between restarts)
- Role-based access control for sensitive commands
- Basic unit tests for:
  - payment calculation logic
  - date progression
  - message templates

## Planned Work (on this branch)

- Refactor `messages.py`:
  - clearer, non-AI-like keys
  - grouped sections (reminders / broadcast / confirmations / errors / system)
- Input validation for payment values (must be > 0, reasonable, and differ from current value)
- Move configuration files into a dedicated `settings/` directory
- Add `/get_config` command (show current payment configuration)
- Add `/next_payment_info` command (manager-only)
- Introduce a `select_reminder_message(days_left, amount, date_str)` helper to simplify testing
- Add logging:
  - file-based log (e.g. `logs/bot.log`)
  - key events: config changes, reminders sent, errors, startup

## Status

Work in progress on the `develop` branch.  
The `main` branch will be updated after these items are implemented, tested, and verified on a test server.
