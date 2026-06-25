AUTHOR = 'Kieran Dalton'
SITENAME = 'Kieran Dalton'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Zurich'

DEFAULT_LANG = 'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Custom theme
THEME = 'theme'

# Custom static paths to copy over
STATIC_PATHS = ['assets', 'documents', 'iframes', 'images', 'CNAME']

# Articles (Blog Posts) paths and URLs
ARTICLE_PATHS = ['posts']
ARTICLE_URL = 'blog/{slug}.html'
ARTICLE_SAVE_AS = 'blog/{slug}.html'

# Save the post listing page as blog.html
INDEX_SAVE_AS = 'blog.html'
INDEX_URL = 'blog.html'

# Static pages compile configuration
TEMPLATE_PAGES = {
    'home.html': 'index.html',
}

# Disable author, category, tag, and archive pages for simplicity
AUTHOR_SAVE_AS = ''
AUTHORS_SAVE_AS = ''
CATEGORY_SAVE_AS = ''
CATEGORIES_SAVE_AS = ''
TAGS_SAVE_AS = ''
TAG_SAVE_AS = ''
ARCHIVES_SAVE_AS = ''
YEAR_ARCHIVE_SAVE_AS = ''
MONTH_ARCHIVE_SAVE_AS = ''
DAY_ARCHIVE_SAVE_AS = ''
