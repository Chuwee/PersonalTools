import random
import webbrowser
import os

def open_link(link):
    webbrowser.open(link)

def ask_usefulness():
    while True:
        usefulness = input("Is the link useful? (Y/N): ").strip().lower()
        if usefulness == 'y' or usefulness == 'n':
            return usefulness
        else:
            print("Invalid input. Please enter 'Y' for Yes or 'N' for No.")

def label_link():
    while True:
        label = input("Enter a keyword to label the link: ").strip()
        if label:
            return label
        else:
            print("Invalid input. Please enter a keyword.")

def update_useful_links(link, label):
    with open("useful_links.txt", "a") as file:
        file.write(f"{link}  {label}\n")

def remove_link_from_file(link, file_path):
    with open(file_path, "r") as file:
        lines = file.readlines()
    with open(file_path, "w") as file:
        for line in lines:
            if line.strip() != link:
                file.write(line)

def main():
    file_path = "links.txt"
    with open(file_path, "r") as file:
        links = [line.strip() for line in file.readlines()]

    if not links:
        print("The links file is empty.")
        return

    while True:
        selected_link = random.choice(links)
        open_link(selected_link)
        usefulness = ask_usefulness()

        if usefulness == 'y':
            label = label_link()
            update_useful_links(selected_link, label)
        else:
            remove_link_from_file(selected_link, file_path)

        links.remove(selected_link)

        if not links:
            print("No more links available.")
            return

if __name__ == "__main__":
    main()
