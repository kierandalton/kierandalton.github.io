#!/usr/bin/env python3
import os
import sys
from html.parser import HTMLParser
from datetime import datetime

class BookmarkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.bookmarks = {}  # folder_path -> list of (title, url)
        self.folder_stack = ["Root"]
        self.current_folder = "Root"
        self.in_h3 = False
        self.in_a = False
        self.current_url = None
        self.current_title = ""
        self.current_folder_name = ""

    def handle_starttag(self, tag, attrs):
        if tag == "h3":
            self.in_h3 = True
            self.current_folder_name = ""
        elif tag == "a":
            self.in_a = True
            self.current_title = ""
            for name, value in attrs:
                if name == "href":
                    self.current_url = value

    def handle_endtag(self, tag):
        if tag == "h3":
            self.in_h3 = False
            self.current_folder = self.current_folder_name.strip()
            self.folder_stack.append(self.current_folder)
        elif tag == "a":
            self.in_a = False
            if self.current_url:
                title = self.current_title.strip() or self.current_url
                key = self.get_folder_key()
                if key not in self.bookmarks:
                    self.bookmarks[key] = []
                self.bookmarks[key].append((title, self.current_url))
                self.current_url = None
        elif tag == "dl":
            if len(self.folder_stack) > 1:
                self.folder_stack.pop()
                self.current_folder = self.folder_stack[-1]

    def get_folder_key(self):
        return " / ".join(self.folder_stack)

    def handle_data(self, data):
        if self.in_h3:
            self.current_folder_name += data
        elif self.in_a:
            self.current_title += data

def main():
    print("=" * 60)
    print(" Pelican Drafts Generator from Browser Bookmarks ")
    print("=" * 60)

    # Search for bookmarks.html in the current folder
    default_filename = "bookmarks.html"
    filename = input(f"Enter path to bookmarks HTML file [{default_filename}]: ").strip()
    if not filename:
        filename = default_filename

    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        print("\nTo use this script:")
        print("1. Sync Chrome on your phone to Chrome or Edge on your desktop.")
        print("2. Open your desktop browser's Bookmark Manager.")
        print("3. Export bookmarks as an HTML file, name it 'bookmarks.html', and place it in this directory.")
        sys.exit(1)

    print("Parsing bookmarks...")
    with open(filename, "r", encoding="utf-8", errors="ignore") as f:
        html_content = f.read()

    parser = BookmarkParser()
    parser.feed(html_content)

    if not parser.bookmarks:
        print("No bookmarks found in the file.")
        sys.exit(0)

    # List folder selections
    folders = sorted(list(parser.bookmarks.keys()))
    print("\nAvailable Bookmark Folders:")
    for idx, folder in enumerate(folders, 1):
        count = len(parser.bookmarks[folder])
        print(f"[{idx}] {folder} ({count} links)")

    selection = input("\nSelect folder index to process (or 'all'): ").strip()
    
    selected_bookmarks = []
    selected_name = ""
    
    if selection.lower() == 'all':
        for folder in folders:
            selected_bookmarks.extend(parser.bookmarks[folder])
        selected_name = "All Bookmarks"
    else:
        try:
            sel_idx = int(selection) - 1
            if 0 <= sel_idx < len(folders):
                folder_key = folders[sel_idx]
                selected_bookmarks = parser.bookmarks[folder_key]
                selected_name = folder_key.split(" / ")[-1]
            else:
                print("Invalid index selection.")
                sys.exit(1)
        except ValueError:
            print("Invalid input.")
            sys.exit(1)

    if not selected_bookmarks:
        print("No links in the selected folder.")
        sys.exit(0)

    print(f"\nSelected '{selected_name}' with {len(selected_bookmarks)} links.")

    # Get batch configuration
    batch_size_str = input("Enter number of links per draft post [10]: ").strip()
    batch_size = 10
    if batch_size_str:
        try:
            batch_size = int(batch_size_str)
        except ValueError:
            pass

    posts_dir = os.path.join("content", "posts")
    os.makedirs(posts_dir, exist_ok=True)

    today = datetime.now().strftime("%Y-%m-%d")
    
    # Generate draft files
    num_batches = (len(selected_bookmarks) + batch_size - 1) // batch_size
    print(f"\nGenerating {num_batches} draft posts in {posts_dir}...")

    # Sanitize name for slug
    safe_name = "".join(c if c.isalnum() else "-" for c in selected_name.lower()).strip("-")
    safe_name = "-".join(filter(None, safe_name.split("-")))

    for i in range(num_batches):
        start_idx = i * batch_size
        end_idx = min(start_idx + batch_size, len(selected_bookmarks))
        batch = selected_bookmarks[start_idx:end_idx]

        batch_num = i + 1
        slug = f"reading-list-{safe_name}-batch-{batch_num}"
        title = f"Reading List: {selected_name} (Batch {batch_num})"
        filepath = os.path.join(posts_dir, f"{slug}.md")

        with open(filepath, "w", encoding="utf-8") as out:
            # Metadata header
            out.write(f"Title: {title}\n")
            out.write(f"Date: {today} {9 + (i % 8):02d}:00\n")
            out.write("Category: Reading\n")
            out.write("Status: draft\n")
            out.write(f"Slug: {slug}\n")
            out.write(f"Summary: Draft summaries and thoughts for reading list batch {batch_num}.\n\n")

            # Post Body
            out.write(f"Here is list of articles and items for this batch ({start_idx + 1} to {end_idx}). I will update each section with my notes as I read them.\n\n")
            out.write("## Articles in this Batch\n\n")

            for item_idx, (link_title, link_url) in enumerate(batch, start_idx + 1):
                out.write(f"### {item_idx}. [{link_title}]({link_url})\n")
                out.write("* **Source URL**: <{}>\n".format(link_url))
                out.write("* **Interesting Points**:\n")
                out.write("  * [Add your notes on what was interesting...]\n\n")

        print(f"  -> Generated: {filepath}")

    print("\nDone! You can run the Pelican build to see them in local draft previews.")
    print("Note: Pelican handles draft files by keeping them out of main lists unless specified in configuration.")

if __name__ == "__main__":
    main()
