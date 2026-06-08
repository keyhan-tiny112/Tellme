import requests
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

con = Console()

# آدرس سرور FastAPI شما
BASE_URL = "http://127.0.0.1:8999"

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def set_user_name():
    while True:
        name = con.input("Enter your [blue]name[/blue] to join the [green]chat[/green]: ").strip()
        if name:
            try:
                response = requests.post(f"{BASE_URL}/SetName", json={"name": name})
                if response.status_code == 200:
                    con.print(f"Welcome [blue]{name}[/blue]! [green]Connection established.[/green]\n")
                    return name
                else:
                    con.print(f"[red]Error from server:[/red] {response.json().get('detail')}")
            except requests.exceptions.ConnectionError:
                con.log("[red]Could not connect to the server.[/red] Make sure FastAPI is running!")
                exit()
        else:
            con.print("[yellow]Name cannot be empty. Please try again.[/yellow]")

def get_messages():
    try:
        with Progress(
            SpinnerColumn(style="green"),
            TextColumn("[green]{task.description}"),
            transient=True,
            console=con,
        ) as progress:
            progress.add_task("Fetching messages...", total=None)
            response = requests.get(f"{BASE_URL}/GiveMsg", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        con.log(f"[red]Error fetching messages:[/red] {e}")
    return []

def send_message(msg):
    try:
        with Progress(
            SpinnerColumn(style="green"),
            TextColumn("[green]{task.description}"),
            transient=True,
            console=con,
        ) as progress:
            progress.add_task("Sending message...", total=None)
            response = requests.post(f"{BASE_URL}/SendMsg", json={"msg": msg}, timeout=5)
        return response.status_code == 200
    except Exception as e:
        con.log(f"[red]Error sending message:[/red] {e}")
        return False

def main():
    my_name = set_user_name()
    
    while True:
        con.print("================= [bold blue]TELLME[/bold blue] MESSENGER =================")
        con.print("Options: [1] Send Message  [2] Refresh/View Messages  [3] Exit")
        choice = con.input("Choose an option: ").strip()

        if choice == "1":
            msg_text = con.input("Type your message: ").strip()
            if msg_text:
                if send_message(msg_text):
                    con.print("[green]Message sent successfully![/green]")
            else:
                con.log("[yellow]Cannot send an empty message.[/yellow]")
                
        elif choice == "2":
            clear_screen()
            messages = get_messages()

            con.print(f"\n--- Chat History (Logged in as: {my_name}) ---")

            if not messages:
                con.log("[cyan]No messages yet. Be the first to type something![/cyan]")
            else:
                for m in messages:
                    con.print(f"[bold yellow][{m['sender']}][/bold yellow]: {m['msg']}")
                    
            con.print("---------------------------------------------\n")
            
        elif choice == "3":
            con.print("[green]Goodbye![/green]")
            break
        else:
            con.print("[red]Invalid option! Please enter 1, 2, or 3.[/red]")

if __name__ == "__main__":
    main()