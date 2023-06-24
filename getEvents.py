import csv
import requests
from bs4 import BeautifulSoup
import pandas as pd

# the URLs of the Wikipedia pages
urls = [
    "https://en.wikipedia.org/wiki/Portal:Current_events/July_2021",
    "https://en.wikipedia.org/wiki/Portal:Current_events/August_2021",
    "https://en.wikipedia.org/wiki/Portal:Current_events/September_2021",
    "https://en.wikipedia.org/wiki/Portal:Current_events/October_2021",
    "https://en.wikipedia.org/wiki/Portal:Current_events/November_2021",
]

# an empty list to store all event data
data = []

for url in urls:
    # sending a GET request to the URL
    response = requests.get(url)

    # parsing the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # finding the relevant section on the page
    section = soup.select_one("#bodyContent")

    # extracting the events from the section
    events = section.select(".vevent")

    # processing the events and store the data
    for event in events:
        date = event.select_one(".current-events-title").text.strip().split("(")[0].strip()

        # Find the event content under the description section
        description = event.select_one(".current-events-content.description")

        # checking if the description section exists
        if description:
            # finding all <p><b> elements under the description section
            paragraphs = description.select("p b")

            # looping through the paragraphs and extract the titles and events
            for paragraph in paragraphs:
                title_text = paragraph.text.strip()

                # finding the associated event links under the <ul><li><a> structure
                event_links = paragraph.find_next("ul").find_all("li")

                # looping through the event links and extract the event text
                for event_link in event_links:
                    event_text = event_link.find("a").text.strip()

                    # creating a dictionary for the event data and append it to the list
                    data.append({
                        "Date": date,
                        "Title": title_text,
                        "Event": event_text
                    })

# creating a dataframe from the event data
df = pd.DataFrame(data)
df.drop_duplicates(keep=False, inplace=True)
# removing duplicate rows due to the raw HTML of Wikipedia
duplicateRows = df[df.duplicated()]

csv_file = "data/wikipedia_events.csv"
df.to_csv(csv_file, index=False)

print(f"Event data saved to '{csv_file}' successfully.")
