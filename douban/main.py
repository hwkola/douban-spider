from scrapy.cmdline import execute
from pathlib import Path
import sys


sys.path.append(Path.cwd() / 'spiders')

# execute(['scrapy', 'crawl', 'movies'])
execute(['scrapy', 'crawl', 'books'])
