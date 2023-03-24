import yaml

def parse_logcat_file(file_path):
    with open(file_path, 'r') as file:
        log_lines = file.readlines()

    app_lifetimes = []
    current_app = None
    start_time = None

    for line in log_lines:
        if 'ActivityTaskManager: START' in line:
            # Start of a new app
            if current_app is not None:
                # End the previous app
                app_lifetimes.append((current_app, start_time, end_time))

            # Parse the app package name from the log line
            app_name = line.split(' ')[-1].strip()
            current_app = app_name
            start_time = line.split()[1]
            end_time = None
        elif 'Layer: Destroyed ActivityRecord' in line:
            # End of the current app
            if current_app is not None:
                end_time = line.split()[1]
                app_lifetimes.append((current_app, start_time, end_time))
                current_app = None
                start_time = None

    return app_lifetimes


log_file_path = 'logcat_file.txt'
app_lifetimes = parse_logcat_file(log_file_path)

# Output the dictionary to a YAML file
with open('output.yml', 'w') as file:
    yaml.dump(app_lifetimes, file)