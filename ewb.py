import requests, re, os, shutil, tkinter
from bs4 import BeautifulSoup
from tkinter import filedialog, simpledialog, messagebox

root = tkinter.Tk()
root.title("Empyrion Workshop Backup")
root.withdraw()

backup_path = tkinter.filedialog.askdirectory(title="Please select the desired backup folder", initialdir="C:/")
tkinter.messagebox.showinfo(title="Selected file", message="Selected: " + backup_path)

epb_path = "C:/Program Files (x86)/Steam/steamapps/workshop/content/383120"
epb_dirs = os.listdir(epb_path)

steam_id = tkinter.simpledialog.askstring(title="Steam ID", prompt="Please enter the Steam ID to be backed up")
workshop_url = "https://steamcommunity.com/profiles/" + steam_id + "/myworkshopfiles/?appid=383120"

urls = []

r = requests.get(workshop_url + "&p=1&numperpage=30").text
soup = BeautifulSoup(r, "html.parser")
q, mod = divmod(int(soup.find("div", class_="workshopBrowsePagingInfo").string.split()[3]), 30)
pages = q if mod == 0 else  q + 1
for n in range(0, pages):
	print(workshop_url + "&p=" + str(n + 1) + "&numperpage=30")
	r = requests.get(workshop_url + "&p=" + str(n + 1) + "&numperpage=30").text
	soup = BeautifulSoup(r, "html.parser")
	links = soup.select("div.workshopItem > a.ugc")
	for link in links:
		if link.has_attr("href"):
			urls.append(link['href'])

i = 1
for url in urls:
	print("trying ", i)
	r = requests.get(url).text
	soup = BeautifulSoup(r, "html.parser")
	title = re.findall("::(.*)<", str(soup.find("title")))[0].replace(":", " -").replace("/", "-")
	print(title)
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
	print("download completed, moving epb")
	for epb_dir in epb_dirs:
		files = os.listdir(os.path.join(epb_path, epb_dir))
		for file in files:
			if file.split(".")[0] == title:
				shutil.copy2(os.path.join(epb_path, epb_dir, file), path)
	i += 1