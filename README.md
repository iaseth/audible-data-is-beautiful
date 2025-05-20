
# Audible Data Is Beautiful

**Audible Data Is Beautiful** is a Python project that scrapes and analyzes audiobook bestseller data from Audible.com, organizing it by category and storing detailed metadata in structured JSON format. The data can then be used for statistical summaries, visualizations, or other insights.

---

## ✨ Features

* 📦 **Scrapes Audible bestsellers** by category
* 📄 **Parses rich audiobook metadata**: title, author, narrator, duration, ratings, review counts, series info, cover images, etc.
* 💾 **Saves structured JSON** locally using hashed filenames
* 📊 **Computes and displays summary statistics** (e.g., average audiobook length per category)
* 🧼 **Avoids repeated downloads** by caching results in the `data/` folder

---

## 📁 Project Structure

```
audible-data-is-beautiful/
├── audible-crawler.py     # Main script for scraping & saving data
├── cache/                 # Contains saved HTML (e.g., genres.html)
├── data/                  # Stores cached and processed JSON files
│   └── cats.json          # List of categories and subcategories
├── master.json            # Combined output of all categories
└── README.md              # Project documentation
```

---

## ⚙️ How It Works

1. **Read categories** from `cache/genres.html`, saved from Audible's "Browse" or "All Categories" page.
2. **Parse and save** all categories and subcategories into `data/cats.json`.
3. For each category:

   * Open the category page on Audible.
   * Extract the top 20 bestsellers from the "Best Sellers" carousel.
   * For each book, extract metadata and convert to structured format.
   * Save the data locally in a JSON file (`data/<urlhash>.json`).
4. **Combine all category data** into `master.json`.

---

## 🚀 Getting Started

### Prerequisites

* Python 3.x
* Required Python libraries:

  ```bash
  pip install requests beautifulsoup4 lxml tabulate
  ```

### Setup

1. Clone this repository:

   ```bash
   git clone https://github.com/iaseth/audible-data-is-beautiful.git
   cd audible-data-is-beautiful
   ```

2. Save the Audible categories page to `cache/genres.html`:

   * Open [Audible Browse Genres](https://www.audible.com/search)
   * Save the page as `genres.html` and move it to the `cache/` directory

3. Run the crawler:

   ```bash
   python audible-crawler.py
   ```

---

## 🧠 What Metadata is Extracted?

* `title`
* `series`
* `author`
* `narrated_by`
* `length` (in hours and minutes)
* `minutes` (numeric value of length)
* `ratings`: overall, performance, story
* `review_counts`: total reviews per rating category
* `description`
* `cover_image` (URL)
* `asin` (unique Audible ID)
* `url` (link to the book on Audible)

---

## 📊 Sample Output

The script prints a table like this showing average audiobook length:

```
+----+-------------------------------------------------+-----------+-------+-------+
|    | Category                                        |   Average |   Max |   Min |
+====+=================================================+===========+=======+=======+
|  1 | Relationships, Parenting & Personal Development |       466 |   883 |   151 |
|  2 | Home & Garden                                   |       471 |  1102 |    79 |
|  3 | Business & Careers                              |       480 |   907 |   222 |
|  4 | Health & Wellness                               |       506 |  1640 |   119 |
|  5 | Comedy & Humor                                  |       530 |  1087 |   109 |
|  6 | Sports & Outdoors                               |       539 |  1846 |    99 |
|  7 | Children's Audiobooks                           |       580 |  3863 |     8 |
|  8 | Biographies & Memoirs                           |       585 |  2217 |   227 |
|  9 | Arts & Entertainment                            |       591 |  1216 |   229 |
| 10 | Money & Finance                                 |       614 |  1686 |   137 |
| 11 | Education & Learning                            |       662 |  3111 |   113 |
| 12 | LGBTQ+                                          |       663 |  1359 |   136 |
| 13 | Computers & Technology                          |       664 |  1492 |   187 |
| 14 | Travel & Tourism                                |       708 |  3111 |   100 |
| 15 | Mystery, Thriller & Suspense                    |       712 |  1459 |   440 |
| 16 | Politics & Social Sciences                      |       713 |  2048 |   138 |
| 17 | Erotica                                         |       728 |  1413 |   227 |
| 18 | Science & Engineering                           |       746 |  1640 |   221 |
| 19 | Religion & Spirituality                         |       832 |  5881 |   138 |
| 20 | Literature & Fiction                            |       949 |  1927 |   240 |
| 21 | Romance                                         |      1034 |  2221 |   108 |
| 22 | History                                         |      1093 |  3431 |   227 |
| 23 | Science Fiction & Fantasy                       |      1135 |  2025 |   371 |
| 24 | Teen & Young Adult                              |      1143 |  4157 |   287 |
+----+-------------------------------------------------+-----------+-------+-------+
```

---

## 📂 Output Files

* `data/cats.json` — categories and subcategories
* `data/<md5>.json` — bestsellers per category
* `master.json` — full aggregated data from all categories

---

## 📄 License

MIT License. See `LICENSE` file.

---

## 🙋‍♀️ Author

[**@iaseth**](https://github.com/iaseth) — built for data visualization and insight into the Audible catalog.
