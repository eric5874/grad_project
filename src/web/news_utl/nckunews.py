import requests
import pandas as pd
from bs4 import BeautifulSoup

def fetch_announcements():
    url = "https://www.csie.ncku.edu.tw/zh-hant/admission/csie"  # Update with the actual announcement page URL
    response = requests.get(url)
    response.encoding = 'utf-8'

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        announcements = soup.find_all("li", class_="li-title d-flex w-100 justify-content-between")

        # Initialize a DataFrame to store the announcements
        announcements_df = pd.DataFrame(columns=['title', 'date', 'link', 'badge'])

        for announcement in announcements:
            # Extract title
            title = announcement.find("a").get_text(strip=True)

            # Extract and build the full link
            link = announcement.find("a")["href"]
            full_link = f"https://www.csie.ncku.edu.tw{link}"  # Ensure the URL is complete

            # Extract date
            date = announcement.find("small", class_="float-right").get_text(strip=True)

            # Extract badge (if available)
            badge = announcement.find("span", class_="badge")
            badge_text = badge.get_text(strip=True) if badge else "無"

            # Append the data to the DataFrame
            announcements_df = announcements_df._append({
                'title': title,
                'date': date,
                'link': full_link,
                'badge': badge_text
            }, ignore_index=True)

        return announcements_df

    else:
        print("無法連接至公告頁面")
        return None

if __name__ == '__main__':
    announcements_df = fetch_announcements()
    if announcements_df is not None:
        print(announcements_df)
        announcements_df.to_csv('announcements.csv', index=False)  # Save to CSV
