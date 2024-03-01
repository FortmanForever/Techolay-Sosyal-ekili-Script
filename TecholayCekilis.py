import requests
from bs4 import BeautifulSoup
import random
import tkinter as tk
from tkinter import messagebox

def get_usernames(url, page_count=1):
    usernames = []
    selected_usernames = set()
    for page in range(1, page_count + 1):
        response = requests.get(f"{url}?page={page}")
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            comments = soup.find_all(class_='message-userContent')
            for comment in comments:
                if "Katılıyorum." in comment.text:
                    username = comment.find_previous(class_='username').text.strip()
                    if username is None:
                        username = ""
                    if username not in selected_usernames:
                        usernames.append(username)
                        selected_usernames.add(username)
    return usernames

def select_winner(usernames):
    if usernames:
        winner = random.choice(usernames)
        return winner
    else:
        return None

def select_backup_winner(usernames, winner):
    remaining_users = [user for user in usernames if user != winner]
    if remaining_users:
        backup_winner = random.choice(remaining_users)
        return backup_winner
    else:
        return None

def run_giveaway():
    url = url_entry.get()
    page_count = int(page_count_entry.get())
    usernames = get_usernames(url, page_count)
   
    # Remove the first participant (the one who posted the initial message)
    if usernames:
        usernames.pop(0)
   
    total_participants_label.config(text=f"Katılanlar: {len(usernames)}")
   
    participant_list.delete(0, tk.END)
    for username in usernames:
        participant_list.insert(tk.END, username)
   
    winner_count = int(winner_count_entry.get())
    backup_count = int(backup_count_entry.get())
   
    winners = []
    backup_winners = []
   
    for _ in range(winner_count):
        winner = select_winner(usernames)
        if winner:
            winners.append(winner)
            usernames.remove(winner)
   
    for _ in range(backup_count):
        backup_winner = select_backup_winner(usernames, random.choice(winners) if winners else None)
        if backup_winner:
            backup_winners.append(backup_winner)
            usernames.remove(backup_winner)
   
    if winners:
        if backup_winners:
            winner_label.config(text=f"Kazananlar: {', '.join(winners)}\nYedek Kazananlar: {', '.join(backup_winners)}")
        else:
            winner_label.config(text=f"Kazananlar: {', '.join(winners)}\nYedek Kazanan bulunamadı.")
    else:
        winner_label.config(text="Katılım gösteren kullanıcı bulunamadı.")

# Create the main UI window
root = tk.Tk()
root.title("Çekiliş Kazanan Seçici")

# Create UI elements
url_label = tk.Label(root, text="Çekiliş Konusunun Linki:")
url_entry = tk.Entry(root, width=50)
page_count_label = tk.Label(root, text="Sayfa Sayısı:")
page_count_entry = tk.Entry(root, width=10)
winner_count_label = tk.Label(root, text="Kazanan Sayısı:")
winner_count_entry = tk.Entry(root, width=10)
backup_count_label = tk.Label(root, text="Yedek Kazanan Sayısı:")
backup_count_entry = tk.Entry(root, width=10)
run_button = tk.Button(root, text="Çekilişi Başlat", command=run_giveaway)
total_participants_label = tk.Label(root, text="")
participant_list = tk.Listbox(root, width=50, height=10)
winner_label = tk.Label(root, text="")

# Arrange UI elements
url_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
url_entry.grid(row=0, column=1, padx=10, pady=5, sticky="w")
page_count_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
page_count_entry.grid(row=1, column=1, padx=10, pady=5, sticky="w")
winner_count_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
winner_count_entry.grid(row=2, column=1, padx=10, pady=5, sticky="w")
backup_count_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
backup_count_entry.grid(row=3, column=1, padx=10, pady=5, sticky="w")
run_button.grid(row=4, column=0, columnspan=2, pady=10)
total_participants_label.grid(row=5, column=0, columnspan=2)
participant_list.grid(row=6, column=0, columnspan=2, pady=10)
winner_label.grid(row=7, column=0, columnspan=2, pady=5)

# Start the UI event loop
root.mainloop()
