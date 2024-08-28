# code by @rxxv
import requests
import random
import string
from colorama import Fore, Style

def print_rainbow(text):
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    for i, char in enumerate(text):
        print(colors[i % len(colors)] + char, end='')
    print(Style.RESET_ALL)

def generate_random_usernames(count, length):
    """Generate a list of random usernames."""
    usernames = []
    for _ in range(count):
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))
        usernames.append(username)
    return usernames

def load_usernames_from_file(filename):
    """Load usernames from a file."""
    with open(filename, "r") as file:
        return [line.strip() for line in file]

def check_username_availability(usernames):
    """Check the availability of usernames."""
    url_pattern = "https://api.solo.to/{}"

    headers = {
        'User-Agent': "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1 Ddg/17.4",
        'Accept': "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        'sec-fetch-site': "none",
        'sec-fetch-mode': "navigate",
        'accept-language': "en-GB,en;q=0.9",
        'sec-fetch-dest': "document",
        'Cookie': "cf_clearance=.hHn1Di9vW0Oku_TE9h6YkC1zNeXC5EN1Y8FuiKjzOg-1724815533-1.2.1.1-E0fdoq2dTmuh3dsovrzCizJif0AEOPVbWDALU15Tr2X.cU1r2ww3FgV5.GkEI7WViW580k3EoF_EbWZ5Gr_EeBlrbCX6JZRb6hFiDUg8i5WSrm28S59GzoeuijDTo7tE7BPKbp3KPFHJiimLPxIpW53TfVgSUFmyRGlBSDpXc4q5ugEUSLLOExA.8LgsmDZRPe3R.KYRHy1jBeGCahvownpVgSHIJYp2ov9zY7L_kg5TxoP0QgDRC_RUSk9UsoUkG0AAeic0IWUfAyxwOzUt8Ayima7PtIkzRRgBkoXeMLrYIfj4W9nbnZqiO9l1C9x2.B7GMGPppYVhsCMLD95MIAGnfA.qmE9Ey1JMsEru_34d8TJjvaCdZLaZd6taRy4m_tYegH8Z2CxZ7x48vJWpnrC_u9O.gT1EjryMiGcdjUsnuTuvyqBWhGUK0ITWgvfuGVotkY7RjK8FHlJFgeFx1DUm9YE3RqMx36wNR4yH2WA"
    }

    with open("valid.txt", "w") as valid_file:
        for username in usernames:
            url = url_pattern.format(username)
            response = requests.get(url, headers=headers)
            response_json = response.json()

            if response.status_code == 404 and response_json.get("message") == "page not found":
                print(Fore.GREEN + f"Username {username} is available." + Style.RESET_ALL)
                valid_file.write(username + "\n")
            elif response.status_code == 404 and response_json.get("message") == "page reserved or blocked":
                print(Fore.RED + f"Username {username} is reserved or blocked." + Style.RESET_ALL)
            elif response.status_code == 200 and "name" in response_json:
                print(Fore.YELLOW + f"Username {username} is taken." + Style.RESET_ALL)
            else:
                print(f"Unexpected response for username {username}: {response_json}")

def main():
    print_rainbow("Solo.to Username Checker by @rxxv")
    print("Select an option:")
    print("1 - Generate random usernames")
    print("2 - Read usernames from a file")

    choice = input("Enter your choice (1 or 2): ")

    if choice == '1':
        count = int(input("How many usernames to generate: "))
        length = int(input("How many characters per username: "))
        usernames = generate_random_usernames(count, length)
    elif choice == '2':
        filename = input("Enter the filename: ")
        usernames = load_usernames_from_file(filename)
    else:
        print("Invalid choice!")
        return

    check_username_availability(usernames)

if __name__ == "__main__":
    main()
