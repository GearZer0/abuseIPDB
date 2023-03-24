import csv
import requests
import itertools

API_KEYS = [
    'key1',
    'key2',
    'key3',
    'key4',
    'key5',
    'key6',
    'key7',
    'key8',
    'key9',
    'key10'
]  # Replace with your AbuseIPDB API keys

def get_abuseipdb_info(ip, api_key):
    url = f'https://api.abuseipdb.com/api/v2/check?ipAddress={ip}&verbose'
    headers = {'Key': api_key, 'Accept': 'application/json'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()['data']
        verdict = data['abuseConfidenceScore']
        resolved_domain = data['domain']
        hostname = data['hostnames'][0] if data['hostnames'] else None
        country = data['countryCode']
        return verdict, resolved_domain, hostname, country
    else:
        return None, None, None, None

if __name__ == '__main__':
    input_file = 'input.csv'
    output_file = 'output.csv'
    keys_cycle = itertools.cycle(API_KEYS)
    with open(input_file, 'r') as csv_file, open(output_file, 'w', newline='') as output_csv:
        reader = csv.reader(csv_file)
        writer = csv.writer(output_csv)
        writer.writerow(['IP Address', 'Verdict', 'Resolved Domain', 'Hostname', 'Country'])
        for row in reader:
            ip = row[0]
            api_key = next(keys_cycle)
            verdict, resolved_domain, hostname, country = get_abuseipdb_info(ip, api_key)
            writer.writerow([ip, verdict, resolved_domain, hostname, country])
            print(f'IP: {ip}, Verdict: {verdict}, Resolved Domain: {resolved_domain}, Hostname: {hostname}, Country: {country}')
