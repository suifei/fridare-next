import os
import sys
import click
import webbrowser
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, IntPrompt, Confirm
from .patcher import FridaPatcher
from rich.panel import Panel
from rich.text import Text

console = Console()

def display_menu():
    table = Table(title="FridaPatcher Menu")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    
    table.add_row("1", "Patch Frida")
    table.add_row("2", "Settings")
    table.add_row("3", "Upgrade")
    table.add_row("4", "About")
    table.add_row("5", "Exit")
    
    console.print(table)


def show_help():
    help_text = Text.from_markup(
        "[bold]Available commands:[/bold]\n"
        "(s)elect: Choose a version to patch\n"
        "(n)ext: Go to the next page\n"
        "(p)rev: Go to the previous page\n"
        "(h)elp: Show this help message\n"
        "(e)xit: Return to main menu\n"
        "You can also enter a version number directly (e.g., 16.0.19)"
    )
    console.print(Panel(help_text, title="Help", border_style="green"))

def patch_frida(patcher):
    page = 1
    per_page = 10
    
    while True:
        console.print("Fetching Frida releases...", style="yellow")
        releases, error = patcher.get_frida_releases(page, per_page)
        
        if error:
            console.print(f"Failed to fetch Frida releases: {error}", style="bold red")
            if Confirm.ask("Do you want to configure proxy settings?"):
                configure_proxy(patcher)
                continue
            else:
                return

        if not releases:
            console.print("No more releases found.", style="yellow")
            break

        table = Table(title=f"Available Frida Releases (Page {page})")
        table.add_column("Index", style="cyan")
        table.add_column("Version", style="magenta")
        table.add_column("Release Date", style="green")
        
        for i, release in enumerate(releases, 1):
            table.add_row(str(i), release['tag_name'], release['published_at'])
        
        console.print(table)
        
        # 添加导航提示
        navigation_hint = Text.from_markup(
            "[bold]Navigation:[/bold] (s)elect, (n)ext, (p)rev, (h)elp, (e)xit, or enter version number"
        )
        console.print(Panel(navigation_hint, border_style="blue"))
        
        navigation = Prompt.ask(
            "Choose an action or enter version number",
            default="s"
        ).lower()
        
        if navigation in ["n", "next"]:
            page += 1
            continue
        elif navigation in ["p", "prev"]:
            if page > 1:
                page -= 1
                continue
            else:
                console.print("Already on the first page.", style="yellow")
                continue
        elif navigation in ["h", "help"]:
            show_help()
            continue
        elif navigation in ["e", "exit"]:
            return
        elif navigation in ["s", "select"]:
            while True:
                choice = IntPrompt.ask("Select a version (enter the index)")
                if 1 <= choice <= len(releases):
                    selected_release = releases[choice-1]
                    break
                console.print("Invalid choice. Please try again.", style="bold red")
        else:
            # 检查是否输入了版本号
            version_input = navigation.strip()
            matching_release = next((r for r in releases if r['tag_name'] == version_input), None)
            if matching_release:
                selected_release = matching_release
            else:
                console.print(f"Version '{version_input}' not found. Please try again.", style="bold red")
                continue
        
        # 处理选定的版本
        os_modules = patcher.get_os_modules(selected_release['assets'])
        table = Table(title=f"Available Modules for {selected_release['tag_name']}")
        table.add_column("Index", style="cyan", justify="right")
        table.add_column("Module Type", style="green")
        table.add_column("OS", style="cyan")
        table.add_column("Arch", style="magenta")
        table.add_column("Files", style="yellow")
        
        module_types = list(os_modules.keys())
        # 按 module, os, arch 分类
        last_module_type = None
        last_os_type = None
        for index, module_type in enumerate(module_types, 1):
            os_types = os_modules[module_type]
            for os_type, archs in os_types.items():
                for arch, assets in archs.items():
                    for file in assets:
                        # 添加到表格
                        if module_type == last_module_type:
                            module_type = ""
                        else:
                            last_module_type = module_type
                        if os_type == last_os_type:
                            os_type = ""
                        else:
                            last_os_type = os_type

                        number_of_index = str(index)

                        table.add_row(number_of_index, module_type, os_type, arch, file['name'])

        
        console.print(table)

        while True:
            module_choice = Prompt.ask("Select a module type (enter index or name)", choices=[str(i) for i in range(1, len(module_types)+1)] + module_types)
            if module_choice.isdigit() and 1 <= int(module_choice) <= len(module_types):
                module_type = module_types[int(module_choice) - 1]
                break
            elif module_choice in module_types:
                module_type = module_choice
                break
            else:
                console.print("Invalid choice. Please try again.", style="bold red")
        os_type = Prompt.ask("Select an OS type", choices=list(os_modules[module_type].keys()))
        arch = Prompt.ask("Select an architecture", choices=list(os_modules[module_type][os_type].keys()))
        
        assets = os_modules[module_type][os_type][arch]
        if len(assets) == 1:
            selected_asset = assets[0]
        else:
            for i, asset in enumerate(assets, 1):
                console.print(f"{i}. {asset['name']}")
            file_choice = IntPrompt.ask("Select a file", min_value=1, max_value=len(assets))
            selected_asset = assets[file_choice - 1]
        
        action = Prompt.ask("Choose an action", choices=["1", "2", "3"], default="1")
        
        if action == "1":
            console.print(f"Downloading original {selected_asset['name']}...", style="yellow")
            filename = patcher.download_file(selected_asset['browser_download_url'], os.path.join(patcher.download_dir, selected_asset['name']))
            if filename:
                console.print(f"Downloaded to {filename}", style="bold green")
            else:
                console.print("Download failed", style="bold red")
        elif action == "2":
            console.print(f"Downloading and patching {selected_asset['name']}...", style="yellow")
            filename = patcher.download_file(selected_asset['browser_download_url'], os.path.join(patcher.download_dir, selected_asset['name']))
            if filename:
                console.print(f"Downloaded to {filename}", style="green")
                if patcher.patch_frida(filename):
                    console.print("Frida patched successfully!", style="bold green")
                else:
                    console.print("Failed to patch Frida.", style="bold red")
            else:
                console.print("Download failed", style="bold red")
        elif action == "3":
            return  # 返回到版本选择

        if not Confirm.ask("Do you want to patch another file?"):
            return

def upgrade(patcher):
    console.print("Checking for updates...", style="yellow")
    latest_version, download_url = patcher.check_for_updates()
    
    if latest_version:
        console.print(f"A new version is available: {latest_version}", style="green")
        if Confirm.ask("Do you want to download the new version?"):
            webbrowser.open(download_url)
            console.print("Please download and install the new version manually.", style="yellow")
        else:
            console.print("Update cancelled.", style="yellow")
    else:
        console.print("You are already running the latest version.", style="green")

def about(patcher):
    console.print("FridaPatcher v0.1", style="bold green")
    console.print("A tool for patching and managing Frida installations.")

def display_settings_menu():
    table = Table(title="Settings Menu")
    table.add_column("Option", style="cyan", no_wrap=True)
    table.add_column("Description", style="magenta")
    
    table.add_row("1", "Configure Auto-Install")
    table.add_row("2", "Configure Proxy")
    table.add_row("3", "Configure Download Directory")
    table.add_row("4", "Back to Main Menu")
    
    console.print(table)

def configure_auto_install(patcher):
    auto_install = patcher.settings.get_setting("auto_install")
    enabled = Confirm.ask("Enable auto-install?", default=auto_install["enabled"])
    if enabled:
        ios_ip = Prompt.ask("Enter iOS device IP", default=auto_install["ios_ip"])
        ios_port = Prompt.ask("Enter iOS device Port", default=auto_install["ios_port"])
    else:
        ios_ip = ""
        ios_port = ""
    
    patcher.settings.update_setting("auto_install", {
        "enabled": enabled,
        "ios_ip": ios_ip,
        "ios_port": ios_port
    })
    console.print("Auto-install settings updated.", style="green")

def configure_proxy(patcher):
    proxy = patcher.settings.get_setting("proxy")
    enabled = Confirm.ask("Enable proxy?", default=proxy["enabled"])
    if enabled:
        proxy_type = Prompt.ask("Enter proxy type", choices=["http", "socks4", "socks5", "socks5h", "socks5a"], default=proxy["type"])
        ip = Prompt.ask("Enter proxy IP", default=proxy["ip"])
        port = Prompt.ask("Enter proxy Port", default=proxy["port"])
        username = Prompt.ask("Enter proxy username (optional)", default=proxy["username"])
        password = Prompt.ask("Enter proxy password (optional)", default=proxy["password"], password=True)
    else:
        proxy_type = "http"
        ip = ""
        port = ""
        username = ""
        password = ""
    
    patcher.settings.update_setting("proxy", {
        "enabled": enabled,
        "type": proxy_type,
        "ip": ip,
        "port": port,
        "username": username,
        "password": password
    })
    console.print("Proxy settings updated.", style="green")
    
    if proxy_type.startswith("socks"):
        console.print("Note: For SOCKS proxy support, make sure you have installed the 'requests[socks]' package.", style="yellow")
        if Confirm.ask("Do you want to install SOCKS support now?"):
            import subprocess
            subprocess.run([sys.executable, "-m", "pip", "install", "requests[socks]"])

def configure_download_dir(patcher):
    current_dir = patcher.settings.get_setting("download_dir")
    new_dir = Prompt.ask("Enter new download directory", default=current_dir)
    if os.path.isdir(new_dir) or Confirm.ask(f"Directory {new_dir} does not exist. Create it?"):
        os.makedirs(new_dir, exist_ok=True)
        patcher.settings.update_setting("download_dir", new_dir)
        patcher.download_dir = new_dir
        console.print(f"Download directory updated to: {new_dir}", style="green")
    else:
        console.print("Download directory not updated", style="yellow")

def settings(patcher):
    while True:
        display_settings_menu()
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4"], default="4")
        
        if choice == "1":
            configure_auto_install(patcher)
        elif choice == "2":
            configure_proxy(patcher)
        elif choice == "3":
            configure_download_dir(patcher)
        elif choice == "4":
            console.print("Exiting settings...", style="bold green")
            break
        else:
            console.print("Invalid choice. Please try again.", style="bold red")
        
        console.print("\nPress Enter to continue...", style="italic")
        input()

@click.command()
def main():
    patcher = FridaPatcher()
    console.print("Welcome to FridaPatcher!", style="bold blue")
    
    while True:
        display_menu()
        choice = Prompt.ask("Enter your choice", choices=["1", "2", "3", "4", "5"], default="5")
        
        if choice == "1":
            patch_frida(patcher)
        elif choice == "2":
            settings(patcher)
        elif choice == "3":
            upgrade(patcher)
        elif choice == "4":
            about(patcher)
        elif choice == "5":
            console.print("Exiting FridaPatcher. Goodbye!", style="bold green")
            break
        else:
            console.print("Invalid choice. Please try again.", style="bold red")
        
        console.print("\nPress Enter to continue...", style="italic")
        input()

if __name__ == "__main__":
    main()