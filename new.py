import datetime
import json

import yaml

def parse_logcat_file(log_file_path):
    with open(log_file_path, 'r') as log_file:
        log_lines = log_file.readlines()

    app_data = []

    current_app = None
    app_start_time = None

    for line in log_lines:
        if 'ActivityTaskManager: START' in line:
            if current_app is not None:
                # End of previous app, calculate lifespan
                app_end_time = datetime.datetime.strptime(line.split()[0] + ' ' + line.split()[1], '%m-%d %H:%M:%S.%f')
                lifespan = (app_end_time - app_start_time).total_seconds()
                app_data.append({
                    'app_path': current_app,
                    'ts_app_started': app_start_time.strftime('%m-%d %H:%M:%S.%f'),
                    'ts_app_closed': app_end_time.strftime('%m-%d %H:%M:%S.%f'),
                    'lifespan': '{:.3f}'.format(lifespan)
                })

            # Start of new app
            current_app = line.split("cmp=")[-1].split()[0].strip()
            app_start_time = datetime.datetime.strptime(line.split()[0] + ' ' + line.split()[1], '%m-%d %H:%M:%S.%f')

        elif 'Layer: Destroyed ActivityRecord' in line:
            if current_app is not None:
                # End of current app, calculate lifespan
                app_end_time = datetime.datetime.strptime(line.split()[0] + ' ' + line.split()[1], '%m-%d %H:%M:%S.%f')
                lifespan = (app_end_time - app_start_time).total_seconds()
                app_data.append({
                    'app_path': current_app,
                    'ts_app_started': app_start_time.strftime('%m-%d %H:%M:%S.%f'),
                    'ts_app_closed': app_end_time.strftime('%m-%d %H:%M:%S.%f'),
                    'lifespan': '{:.3f}'.format(lifespan)
                })
                current_app = None
                app_start_time = None

    return app_data

log_file_path = 'logcat_file.txt'
app_data = parse_logcat_file(log_file_path)

'''applications_list = []
for i, app in enumerate(app_data, start=1):
    application_dict = {
        'app_path': app['app_path'],
        'ts_app_started': app['ts_app_started'],
        'ts_app_closed': app['ts_app_closed'],
        'lifespan': app['lifespan']
    }
    application_name = 'application' + str(i)
    applications_list.append({application_name: application_dict})'''

with open('output.yml', 'w') as output_file:
    yaml.dump({'applications': app_data}, output_file)

with open('output.yml', 'r') as input_file:
    data = yaml.safe_load(input_file)

json_data = json.dumps(data)

with open('output.json', 'w') as output_file:
    output_file.write(json_data)

#fara applicaiton1 app2 app3 ....
