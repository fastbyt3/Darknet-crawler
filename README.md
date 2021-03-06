# Darkathon'22 - Darknet crawler

## Problem statement

Crawling of darkweb to _identify and catalogue active and genuine darknet markets selling drugs_ (automatically add new markets and drop inactive/taken down markets)

Crawling of darknet markets to _identify drug traffickers on dark net based in India and the drugs they offer for sale_.

## Primary goals

1. Crawl darknet sites(starting with a hidden wiki) and find new http(s) tor sites
2. Save URLs into a Database
3. Index the URLs based on the 'body' content. Looking for keywords like drugs, sale, etc.
4. Save indexed data to DB and visualize it with **Kibana**

## To-Do

- [x] Configure python to connect to TOR
- [ ] Set up a database to store scraped links
- [ ] Develop a crawler to parse through text
- [ ] Identify keywords related to drug-sale and add to database
- [ ] Check specifically for dug sale in India and update in DB
- [ ] Periodically check sites in DB if they are still active
- [ ] Figure out a way to automatically find sites

> Happy hacking <3