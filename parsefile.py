import datetime
import yaml

def parse_logcat_file(log_file_path):
    app_lifetimes = []

    with open(log_file_path, 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        if 'Displayed' in lines[i]:
            package_name, activity_name = lines[i].split()[8].split('/')[:2]
            start_time_str = lines[i].split()[1]
            start_time = datetime.datetime.strptime(start_time_str, '%m-%d %H:%M:%S.%f')
            for j in range(i+1, len(lines)):
                if 'Displayed' in lines[j] or 'Fatal Exception' in lines[j]:
                    end_time_str = lines[j-1].split()[1]
                    end_time = datetime.datetime.strptime(end_time_str, '%m-%d %H:%M:%S.%f')
                    app_lifetimes.append({'app_path': f"{package_name}/{activity_name}",
                                          'ts_app_started': start_time_str,
                                          'ts_app_closed': end_time_str,
                                          'lifespan': str(end_time - start_time)})
                    break
    with open('app_lifetimes.yml', 'w') as file:
        yaml.dump(app_lifetimes, file)

    return app_lifetimes

app_lifetimes = parse_logcat_file('logcat_file.txt')

with open('output.yml', 'w') as f:
    yaml.dump({'applications': [{'application_' + str(i + 1): app_lifetimes[k]} for i, k in enumerate(app_lifetimes)]}, f, default_flow_style=False)
