import json
import shutil
from pathlib import Path
import markdown

BASE_DIR = Path(__file__).resolve().parent.parent
GENERATOR_DIR = BASE_DIR / "generator"
CONTENT_DIR = BASE_DIR / "content"
PUBLIC_DIR = BASE_DIR / "public"
PUBLIC_POSTS_DIR = PUBLIC_DIR / "posts"
PUBLIC_ASSETS_DIR = PUBLIC_DIR / "assets"

ABOUT_URL = "https://nichlay.github.io/personal-website/"


def load_posts():
    posts_file = GENERATOR_DIR / "posts.json"
    with open(posts_file, "r", encoding="utf-8") as file:
        return json.load(file)


def copy_static_files():
    source_css = GENERATOR_DIR / "style.css"
    target_css = PUBLIC_DIR / "style.css"
    if source_css.exists():
        shutil.copyfile(source_css, target_css)

    source_assets = GENERATOR_DIR / "assets"
    if source_assets.exists():
        PUBLIC_ASSETS_DIR.mkdir(parents=True, exist_ok=True)
        for item in source_assets.iterdir():
            target = PUBLIC_ASSETS_DIR / item.name
            if item.is_file():
                shutil.copyfile(item, target)


def create_header(prefix=""):
    return f'''  <header class="topbar">
    <div class="topbar-inner">
      <a class="brand" href="{prefix}index.html">
        <img src="{prefix}assets/logo.png" alt="" class="brand-logo" onerror="this.style.display='none'" />
        <span>Blog</span>
      </a>

      <nav>
        <a href="{ABOUT_URL}">About</a>
      </nav>
    </div>
  </header>
'''


def create_blog_index(posts):
    post_items = ""
    for post in posts:
        post_items += f"""    <article class="post-list-item">
      <p class="post-date">{post["date"]}</p>
      <p class="post-category">{post["category"]}</p>
      <h2>
        <a href="posts/{post["slug"]}.html">{post["title"]}</a>
      </h2>
      <p class="post-excerpt">
        {post["excerpt"]}
      </p>
    </article>

"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>Blog</title>
  <meta name="description" content="Blog posts by Clayton Lie." />

  <link rel="stylesheet" href="style.css" />
</head>
<body>
{create_header(prefix="")}
  <main class="container">
{post_items}  </main>
</body>
</html>
"""
    (PUBLIC_DIR / "index.html").write_text(html, encoding="utf-8")


def create_post_pages(posts):
    PUBLIC_POSTS_DIR.mkdir(parents=True, exist_ok=True)
    for post in posts:
        content_path = CONTENT_DIR / post["content_file"]
        if not content_path.exists():
            raise FileNotFoundError(f"Missing content file: {content_path}")
        markdown_text = content_path.read_text(encoding="utf-8")
        content = markdown.markdown(markdown_text)
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />

  <title>{post["title"]} | Blog</title>
  <meta name="description" content="{post["excerpt"]}" />

  <link rel="stylesheet" href="../style.css" />
</head>
<body>
{create_header(prefix="../")}
  <main class="container">
    <article class="post">
      <p class="post-category">{post["category"]}</p>
      <h1>{post["title"]}</h1>
      <p class="post-date">{post["date"]}</p>

      <div class="post-content">
{content}
      </div>

      <a class="back-link" href="../index.html">← Back to blog</a>
    </article>
  </main>
</body>
</html>
'''
        (PUBLIC_POSTS_DIR / f"{post['slug']}.html").write_text(html, encoding="utf-8")


def main():
    posts = load_posts()
    copy_static_files()
    create_blog_index(posts)
    create_post_pages(posts)
    print("Blog generated successfully.")
    print(f"Generated files are inside: {PUBLIC_DIR}")


if __name__ == "__main__":
    main()
