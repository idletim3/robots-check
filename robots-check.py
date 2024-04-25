import subprocess
import requests

COLORS = {
    100: '\033[97m',  # white
    200: '\033[92m',  # green
    300: '\033[93m',  # yellow
    400: '\033[91m',  # red
    500: '\033[94m'   # blue
}
RESET_COLOR = '\033[0m'


def execute_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    return output.decode(), error.decode()


try:
    url = input("Enter URL or IP address: ")

    response = requests.head(url)
    if response.status_code != 200:
        print("URL is not accessible.")
        exit()

    execute_command(f"curl -o robots.txt {url}/robots.txt")
    execute_command("grep 'Disallow:' robots.txt | awk '{print $2}' > disallowed.txt")

    responses = {100: [], 200: [], 300: [], 400: [], 500: []}

    with open("disallowed.txt", "r") as file:
        for line in file:
            endpoint = line.strip()
            try:
                request = requests.get(f'{url}{endpoint}')
                status_code = request.status_code
                responses[status_code // 100 * 100].append((endpoint, status_code))
            except Exception as e:
                print(f"Error for {endpoint}: {e}")

    with open("responses.txt", "w") as output_file:
        for status, endpoints in responses.items():
            output_file.write(f"{COLORS[status]}{status}:\n{RESET_COLOR}")
            if not endpoints:
                output_file.write("N/a\n")
            else:
                for endpoint, status_code in endpoints:
                    output_file.write(f"{COLORS[status]}{endpoint} - {status_code}{RESET_COLOR}\n")
            output_file.write("\n")


except Exception as e:
    print(f"Error: {e}")
