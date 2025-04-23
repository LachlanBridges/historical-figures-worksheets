# 🧠 Historical Figures Worksheets

> A homeschool-friendly generator of LaTeX-based educational worksheets about key historical figures.

[**📦 View latest release →**](https://github.com/LachlanBridges/historical-figures-worksheets/releases/tag/latest)

---

## ✨ What It Does

This project creates **simple, child-friendly printable worksheets** about famous historical figures, designed for ages **6–8**. It works great as a basic **reading comprehension** or discussion activity.

Each worksheet includes:
- A short biography and image
- Why the figure is important
- 3-5 multiple-choice questions
- Clean, printable LaTeX layout

It also auto-generates a combined PDF with a *clickable table of contents*, making it easy to quickly find and print any specific historical figure.

---

## 🔧 How It Works

1. **Data Files**: Profiles are stored as `.json` files in `data/`, written for children aged 6–8.
2. **Images**: Downloaded automatically from Wikipedia into `images/`.
3. **Rendering**: `scripts/main.py` uses a Jinja2 LaTeX template to build individual worksheets.
4. **Compilation**: PDFs are compiled with `lualatex`.
5. **Release**: A GitHub Action builds and uploads all worksheets to the **latest GitHub Release**.

---

## 🗂 Project Structure

```
data/               # JSON data for each historical figure
images/             # Downloaded portrait images
output/pdf/         # Individual compiled PDFs
output/pdf/compiled # Merged PDF with table of contents
scripts/            # Python scripts for building & automation
templates/          # LaTeX worksheet template (Jinja2)
```

---

## 🚀 GitHub Actions

Pushing a tag named `latest` (e.g. `git push origin latest`) triggers an automatic build:

- Installs LaTeX and Python
- Generates and compiles all PDFs
- Uploads them as release assets at:

📎 [**Releases > latest**](https://github.com/LachlanBridges/historical-figures-worksheets/releases/tag/latest)

---

## 📝 License

MIT License © Lachlan Bridges
