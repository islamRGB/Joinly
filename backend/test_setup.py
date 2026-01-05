import os
import sys

print("=" * 60)
print("Joinly Setup Verification")
print("=" * 60)

errors = []
warnings = []

print("\n1. Checking Python version...")
if sys.version_info < (3, 8):
    errors.append("Python 3.8+ required")
else:
    print(f"   ✓ Python {sys.version_info.major}.{sys.version_info.minor}")

print("\n2. Checking required packages...")
required_packages = [
    'flask', 'flask_cors', 'flask_socketio', 
    'toml', 'pydantic', 'colorlog', 'schedule'
]

for package in required_packages:
    try:
        __import__(package)
        print(f"   ✓ {package}")
    except ImportError:
        errors.append(f"Missing package: {package}")
        print(f"   ✗ {package} - NOT INSTALLED")

print("\n3. Checking folder structure...")
folders = [
    '../frontend-web',
    '../control-ui',
    '../frontend-web/assets',
    '../control-ui/assets',
    'config',
    'core',
    'api/http',
    'matchmaking',
    'bots',
    'storage',
    'services'
]

for folder in folders:
    if os.path.exists(folder):
        print(f"   ✓ {folder}")
    else:
        warnings.append(f"Missing folder: {folder}")
        print(f"   ⚠ {folder} - NOT FOUND")

print("\n4. Checking critical files...")
files = [
    'app.py',
    'bootstrap.py',
    'launcher.py',
    '../frontend-web/index.html',
    '../frontend-web/lobby.css',
    '../control-ui/index.html',
    '../control-ui/dashboard.css'
]

for file in files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        errors.append(f"Missing file: {file}")
        print(f"   ✗ {file} - NOT FOUND")

print("\n5. Checking config files...")
config_files = [
    'config/lobby.toml',
    'config/matchmaking.toml',
    'config/admin.toml'
]

for file in config_files:
    if os.path.exists(file):
        print(f"   ✓ {file}")
    else:
        warnings.append(f"Missing config: {file}")
        print(f"   ⚠ {file} - WILL USE DEFAULTS")

print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)

if not errors and not warnings:
    print("\n✓ All checks passed! Ready to launch Joinly.")
    print("\nTo start: python launcher.py")
elif not errors:
    print(f"\n⚠ {len(warnings)} warning(s):")
    for w in warnings:
        print(f"  - {w}")
    print("\nYou can still run Joinly, but some features may not work.")
else:
    print(f"\n✗ {len(errors)} error(s) found:")
    for e in errors:
        print(f"  - {e}")
    print(f"\n⚠ {len(warnings)} warning(s):")
    for w in warnings:
        print(f"  - {w}")
    print("\nPlease fix errors before running Joinly.")
    print("\nTo install missing packages:")
    print("  pip install -r requirements.txt")

print("\n" + "=" * 60)