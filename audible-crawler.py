import hashlib
import json
import os
import re

import requests
from bs4 import BeautifulSoup



def save_category_list(json_path):
	if os.path.isfile(json_path):
		with open(json_path) as f:
			jo = json.load(f)
		return jo

	with open("cache/genres.html") as f:
		soup = BeautifulSoup(f.read(), "lxml")

	links = soup.find_all("a")
	categoryLinks = [a for a in links if "categoryLink" in a['class']]
	subCategoryLinks = [a for a in links if "subCategoryLink" in a['class']]

	jo = dict(
		categories = [dict(title=a.text, href=a['href'].split("?")[0]) for a in categoryLinks],
		sub_categories = [dict(title=a.text, href=a['href'].split("?")[0]) for a in subCategoryLinks]
	)
	with open(json_path, "w") as f:
		json.dump(jo, f, sort_keys=True)
	print(f"Saved: {json_path} ({len(categoryLinks)} categories, {len(subCategoryLinks)} sub_categories)")
	return jo


def main():
	cats = save_category_list("data/cats.json")
	print(cats['categories'])


if __name__ == '__main__':
	main()
