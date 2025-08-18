# Sesh

A simple, powerful CLI application for tracking your work sessions with titles, tags, and timing. Perfect for developers, freelancers, and anyone who wants to monitor their productivity and categorize their work.

## Features

- **Session Tracking**: Start and stop work sessions with descriptive titles
- **Inline Tags**: Add tags directly in your session title using `+tag` syntax
- **Flexible Tagging**: Additional tags via command-line options
- **Real-time Status**: Check your current session progress and elapsed time
- **Local Storage**: All data stored locally in a SQLite database
- **Session History**: Persistent storage of completed sessions with unique IDs

## Installation

### Using uv (Recommended)

```bash
# Clone the repository
git clone https://github.com/nutabi/sesh.git
cd sesh

# Install with uv
uv sync
uv run sesh --help
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/nutabi/sesh.git
cd sesh

# Install in development mode
pip install -e .
```

## Quick Start

```bash
# Start a work session
sesh start working on documentation

# Start with inline tags
sesh start fix +bug in authentication system

# Check current status
sesh status

# Stop the session with completion notes
sesh stop "completed user authentication feature"
```

## Usage

### Starting a Session

```bash
# Basic usage
sesh start writing tests for the API

# With inline tags (words prefixed with +)
sesh start +python +testing writing unit tests

# With additional tags via options
sesh start -t urgent,review "code review session"

# Mixing inline tags and option tags
sesh start fix +bug in login system -t priority,backend
```

### Checking Status

```bash
sesh status
```

Example output:
```
Active Sesh: fix bug in authentication system
Tags: bug, backend, urgent
Start time: Monday, 18 August, 14:30:45
Elapsed time: 1h 23m 15s
```

### Stopping a Session

```bash
# Simple stop
sesh stop

# With completion details
sesh stop "completed the user authentication feature"

# Adding tags when stopping
sesh stop -t completed,tested "finished API endpoints"
```

### Reset (Development)

```bash
# Clear all data (with confirmation)
sesh reset

# Skip confirmation
sesh reset -y
```

## Tag System

Tags help organize and categorize your sessions for better productivity insights.

### Tag Rules

- Only lowercase letters, numbers, and hyphens
- Cannot start or end with hyphens
- Maximum 20 characters
- Examples: `python`, `web-dev`, `bug-fix`, `api2`

### Inline Tags

Add tags directly in your session title by prefixing words with `+`:

```bash
sesh start working on +python +cli application
# Title: "working on python cli application"
# Tags: python, cli
```

### Option Tags

Add tags using the `-t` or `--tag` option:

```bash
sesh start -t backend,api "building user endpoints"
# Tags: backend, api
```

### Tag Display

Tags with hyphens are displayed with spaces for better readability:
- Storage: `machine-learning` 
- Display: `machine learning`

## Data Storage

Sesh stores all data locally in your project directory:

- **Database**: `.sesh/store.db` (SQLite database)
- **Current Session**: `.sesh/current.json` (active session state)

The database includes:
- Session history with titles, details, start/end times
- Tag management and relationships
- Unique session IDs for reference

## Commands

| Command | Description |
|---------|-------------|
| `sesh start <title>` | Start a new work session |
| `sesh stop [details]` | Stop the current session |
| `sesh status` | Show current session information |
| `sesh reset` | Clear all session data ⚠️ |

## Examples

### Development Workflow

```bash
# Start coding session
sesh start +python +web-dev building user authentication

# Check progress
sesh status

# Take a break, stop session
sesh stop "implemented login endpoint, need to add tests"

# Start testing session
sesh start +testing +python writing tests for auth system

# Finish up
sesh stop -t completed "all tests passing"
```

### Bug Fixing

```bash
# Start bug investigation
sesh start investigate +bug in payment processing -t urgent

# Stop with findings
sesh stop "found the issue in payment validation logic"

# Start fixing
sesh start fix +bug payment validation -t urgent,backend

# Complete fix
sesh stop -t fixed,tested "payment bug resolved and tested"
```

## Requirements

- Python ≥ 3.13
- Dependencies: `click`, `whenever`

## Development

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=sesh
```

### Project Structure

```
src/sesh/
├── cli.py           # Main CLI interface
├── store.py         # Database operations
├── current.py       # Current session management
├── tag.py           # Tag validation and parsing
├── error.py         # Custom exceptions
└── command/         # Command handlers
    ├── start.py
    ├── stop.py
    ├── status.py
    └── reset.py
```

## Roadmap

### High Priority

- [ ] Enhanced `sesh status` with more details
- [ ] History command (`sesh log`) to view past sessions
- [ ] Better help text and documentation
- [ ] Auto-completion for tags

### Medium Priority

- [ ] Configuration management
- [ ] Editing sessions (`sesh edit`)
- [ ] Export/import functionality

### Low Priority

- [ ] Analytics and reporting
- [ ] Session syncing across devices
- [ ] Time tracking goals and notifications

## Contributing

Contributions are welcome! Please feel free to submit issues, feature requests, or pull requests.

## License

This project is open source. Please check the license file for details.