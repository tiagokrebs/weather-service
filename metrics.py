from prometheus_client import CollectorRegistry, Counter, write_to_textfile

PROM_FILE_PATH = './metrics.prom'
registry = CollectorRegistry()

def increment_execution_count():
    # Load the existing metrics from the file
    try:
        with open(PROM_FILE_PATH, 'r') as f:
            registry = CollectorRegistry()
            c = Counter('weather_cli_executions_total', 'Number of times the weather CLI has been executed', registry=registry)
            for line in f:
                if line.startswith('weather_cli_executions_total'):
                    current_value = float(line.split()[-1])
                    break
            c._value.set(current_value + 1)
    except FileNotFoundError:
        registry = CollectorRegistry()
        c = Counter('weather_cli_executions_total', 'Number of times the weather CLI has been executed', registry=registry)
        c._value.set(1)

    # Write the updated metrics back to the file
    write_to_textfile(PROM_FILE_PATH, registry)