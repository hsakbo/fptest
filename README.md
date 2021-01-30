# Requirement:<br>
- geckodriver (for ubuntu/debian: `sudo apt-get install geckodriver`, arch/manjaro: `sudo pacman -Sy geckodriver`)
- python and pip
- firefox

# Install<br>
```
python3 -m venv venv
source venv/bin/activate
pip3 install selenium pytest pytest-check
```

to exit virtual environment: `deactivate`

# Run all tests<br>
```
source venv/bin/activate
pytest -vs
```
