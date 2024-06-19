import subprocess

def run_script(script_name):
    """ Helper function to run a script using subprocess. """
    try:
        # Adjust the command if your scripts need different Python interpreters or specific arguments
        result = subprocess.run(['python', script_name], capture_output=True, text=True, check=True)
        print(f"Successfully ran {script_name}")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Failed to run {script_name}: {e}")
        print(e.output)

def main():
    # List of scripts in the order they need to be run
    scripts = [
        'patch.py',
        'app.py',
        'Super.py',
        'stitch.py',
        'pansharpen.py'
    ]

    for script in scripts:
        run_script(script)

if __name__ == "__main__":
    main()

##NEED TO TRY THIS