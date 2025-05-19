import hashlib
import json
import os
import re

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate


session = requests.session()


def get_soup(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, "lxml")
	return soup


def url_to_local_json_path(url, base_dir="data"):
    normalized_url = url.strip().lower()
    url_hash = hashlib.md5(normalized_url.encode('utf-8')).hexdigest()
    filename = f"{url_hash}.json"
    local_path = os.path.join(base_dir, filename)
    return local_path


def parse_number(num_str):
	return int(num_str.replace(',', ''))


def time_to_minutes(time_str):
	# Use regex to extract hours and minutes
	match = re.search(r'(?:(\d+)\s*hrs?)?\s*(?:and\s*)?(?:(\d+)\s*mins?)?', time_str, re.IGNORECASE)
	if not match:
		return 0  # or raise ValueError("Invalid time format")

	hours = int(match.group(1)) if match.group(1) else 0
	minutes = int(match.group(2)) if match.group(2) else 0

	return hours * 60 + minutes


def extract_audiobook_metadata(element):
	metadata = {}

	# Title
	title_elem = element.select_one('h2.bc-heading')
	metadata['title'] = title_elem.text.strip() if title_elem else None

	# Series (usually second li in the first ul)
	try:
		series = element.select('ul.bc-list')[0].select('li.bc-list-item')[1].text.strip()
		metadata['series'] = series
	except IndexError:
		metadata['series'] = None

	# Author
	try:
		author_line = [li for li in element.select('ul.bc-list')[0].select('li.bc-list-item') if "By:" in li.text]
		metadata['author'] = author_line[0].text.replace("By:", "").strip() if author_line else None
	except IndexError:
		metadata['author'] = None

	# Narrators
	try:
		narr_line = [li for li in element.select('ul.bc-list')[0].select('li.bc-list-item') if "Narrated by:" in li.text]
		metadata['narrated_by'] = narr_line[0].text.replace("Narrated by:", "").strip() if narr_line else None
	except IndexError:
		metadata['narrated_by'] = None

	# Length
	try:
		length_line = [li for li in element.select('ul.bc-list')[0].select('li.bc-list-item') if "Length:" in li.text]
		metadata['length'] = length_line[0].text.replace("Length:", "").strip() if length_line else None
		metadata['minutes'] = time_to_minutes(metadata['length'])
	except IndexError:
		metadata['length'] = None

	# Ratings (Overall, Performance, Story)
	ratings = {}
	rating_labels = ['Overall', 'Performance', 'Story']
	rating_spans = element.select('span.bc-text.bc-pub-offscreen')
	for i, label in enumerate(rating_labels):
		if i < len(rating_spans):
			ratings[label.lower()] = rating_spans[i].text.strip()
	metadata['ratings'] = ratings

	# Review counts
	try:
		review_counts = [parse_number(div.text.strip().split(" ")[-1].strip()) for div in element.select('div.bc-col-responsive.bc-col-8')[:3]]
		metadata['review_counts'] = {
			'overall': review_counts[0] if len(review_counts) > 0 else None,
			'performance': review_counts[1] if len(review_counts) > 1 else None,
			'story': review_counts[2] if len(review_counts) > 2 else None,
		}
	except Exception:
		metadata['review_counts'] = {}

	# Description
	try:
		desc_paragraph = element.select_one('p.bc-text.bc-spacing-small.bc-spacing-top-none.bc-size-small.bc-color-base')
		if desc_paragraph and desc_paragraph.find_next_sibling('p'):
			metadata['description'] = desc_paragraph.find_next_sibling('p').text.strip()
		else:
			metadata['description'] = None
	except Exception:
		metadata['description'] = None

	# Cover image URL
	img_elem = element.select_one('img')
	metadata['cover_image'] = img_elem['src'] if img_elem else None

	# ASIN and URL
	asin_elem = element.select_one('div.adbl-asin-impression')
	metadata['asin'] = asin_elem['data-asin'] if asin_elem and 'data-asin' in asin_elem.attrs else None
	metadata['url'] = "https://www.audible.com" + asin_elem['data-url'] if asin_elem and 'data-url' in asin_elem.attrs else None

	return metadata


def get_category_books_data(category):
	full_url = f"https://www.audible.com{category['href']}"
	json_path = url_to_local_json_path(full_url)

	if os.path.isfile(json_path):
		with open(json_path) as f:
			jo = json.load(f)
		return jo

	print(f"{category['title']} => {category['href']}")
	soup = get_soup(full_url)
	bestseller_container = soup.find("div", attrs={ "data-widget": "carousel-BEST_SELLERS" })
	bestseller_products = bestseller_container.find_all("div", class_="carousel-product")

	jo = dict(
		category=category,
		bestsellers=[extract_audiobook_metadata(product) for product in bestseller_products]
	)
	with open(json_path, "w") as f:
		json.dump(jo, f, sort_keys=True, indent="\t")
	print(f"\tSaved: {json_path} ({len(bestseller_products)} bestsellers)")
	return jo


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
		json.dump(jo, f, sort_keys=True, indent="\t")
	print(f"Saved: {json_path} ({len(categoryLinks)} categories, {len(subCategoryLinks)} sub_categories)")
	return jo


def main():
	cats = save_category_list("data/cats.json")

	rows = []
	for category in cats['categories']:
		jo = get_category_books_data(category)
		minutes = [product['minutes'] for product in jo['bestsellers']]
		average_minutes = sum(minutes) // len(jo['bestsellers'])
		rows.append([
			category['title'], average_minutes,
			max(minutes), min(minutes)
		])

	rows.sort(key=lambda x:x[1])
	print(tabulate(
		rows, headers=["Category", "Average", "Max", "Min"],
		tablefmt="outline", showindex=range(1, len(rows)+1)
	))


if __name__ == '__main__':
	main()
