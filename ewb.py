import requests, re, os, shutil, tkinter
from bs4 import BeautifulSoup
from tkinter import filedialog, simpledialog, messagebox
epb_path = "C:/Program Files (x86)/Steam/steamapps/workshop/content/383120"

def get_backup_path():
	backup_path = tkinter.filedialog.askdirectory(title="Please select the desired backup folder", initialdir="C:/")
	if backup_path:
		tkinter.messagebox.showinfo(title="Selected file", message="Selected: " + backup_path)
	else: 
		tkinter.messagebox.showerror(title="Error", message="No backup path selected. Please try again.")
	return backup_path

def get_epb_dirs(epb_path):
	epb_dirs = os.listdir(epb_path)
	return epb_dirs

def get_epb_files(epb_path, epb_dirs):
	epb_files = []
	temp = []
	for epb_dir in epb_dirs:
		temp = os.listdir(os.path.join(epb_path, epb_dir))
		for item in temp:
			file = os.path.join(epb_path, epb_dir, item)
			if os.path.isfile(file):
				if os.path.splitext(file)[1] in [".epb", ".jpg"]:
					epb_files.append(file)
	return epb_files

def get_steam_id():
	steam_id = tkinter.simpledialog.askstring(title="Steam ID", prompt="Please enter the Steam ID to be backed up")
	return steam_id

def get_workshop_url(steam_id):
	workshop_url = "https://steamcommunity.com/profiles/" + steam_id + "/myworkshopfiles/?appid=383120"
	return workshop_url

def test_workshop_url(workshop_url):
	r = requests.get(workshop_url)
	if "Error" in r.text:
		tkinter.messagebox.showerror(title="Error", message="Sorry, that's not a valid Steam ID. See the readme for info on how to locate your Steam ID.")
		return False
	else:
		return True

def get_build_urls(workshop_url):
	urls = []
	r = requests.get(workshop_url + "&p=1&numperpage=30").text
	soup = BeautifulSoup(r, "html.parser")
	q, mod = divmod(int(soup.find("div", class_="workshopBrowsePagingInfo").string.split()[3]), 30)
	pages = q if mod == 0 else q + 1
	for n in range(0, pages):
		print(workshop_url + "&p=" + str(n + 1) + "&numperpage=30")
		r = requests.get(workshop_url + "&p=" + str(n + 1) + "&numperpage=30").text
		soup = BeautifulSoup(r, "html.parser")
		links = soup.select("div.workshopItem > a.ugc")
		for link in links:
			if link.has_attr("href"):
				urls.append(link['href'])
	return urls

def backup(backup_path, epb_path, epb_dirs, epb_files, urls):
	#TODO: move this into tkinter
	#TODO: Maybe split Steam downloads from unifcation with epb???
	i = 1
	for url in urls:
		print(f"trying {i}...")
		r = requests.get(url).text
		soup = BeautifulSoup(r, "html.parser")
		title = re.findall("::(.*)<", str(soup.find("title")))[0].replace(":", " -").replace("/", "-")
		print(f"Found build: {title}")
		print("Starting download from Steam...")
		path = os.path.join(backup_path, title)
		os.mkdir(path)
		description = soup.find("div", class_="workshopItemDescription").get_text()
		with open(path + "/" + title + ".txt", "w") as f:
			f.write(description)
		imgs = soup.select("div.highlight_strip_screenshot > img")
		n = 1
		for img in imgs:
			with open(path + "/" + title + str(n) + ".jpg", "wb") as f:
				f.write(requests.get(img['src'].split("?")[0]).content)
			n += 1
		print("Download completed, moving epb...")
		found_epb = False
		found_jpg = False
		for file in epb_files:
			f, ext = os.path.splitext(file)
			f = os.path.split(f)[1]
			if f == title:
				shutil.copy2(file, path)
				if ext == '.epb':
					found_epb = True
				if ext == '.jpg':
					found_jpg = True
		if not found_epb:
			print("EPB file not found.")
		if not found_jpg:
			print("JPG file not found.")
		print(f"Backup completed: {title}\n")
		i += 1

def main():
	#TODO: make this all work in one tkinter window
	root = tkinter.Tk()
	root.title("Empyrion Workshop Backup")
	root.withdraw()

	backup_path = get_backup_path()
	if not backup_path:
		return
	epb_dirs = get_epb_dirs(epb_path)
	epb_files = get_epb_files(epb_path, epb_dirs)
	steam_id = get_steam_id()
	workshop_url = get_workshop_url(steam_id)
	if test_workshop_url(workshop_url):
		urls = get_build_urls(workshop_url)
	else:
		return
	backup(backup_path, epb_path, epb_dirs, epb_files, urls)

if __name__ == "__main__":
    main()
