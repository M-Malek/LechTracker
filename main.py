import datetime

from flask import Flask, render_template, jsonify

app = Flask(__name__)


# Function responsible for finding Lech statistics
def lech_match_stats_finder():
    from bs4 import BeautifulSoup
    import requests
    url = "https://sportowefakty.wp.pl/pilka-nozna/lech-poznan/terminarz"
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")

    # Find match date:
    raw_table_dates = soup.find_all(class_='matches__headerbar')
    table_dates = []
    for date in raw_table_dates:
        table_dates.append(date.text.replace("\n", ""))

    # Find match hour:
    raw_hours = soup.find_all('time')
    hours = [hour.text for hour in raw_hours]

    # Find match data:
    raw_table_matches = soup.find_all(class_="cmatch")
    matches = []
    for match in raw_table_matches:
        spans = match.find_all('span')
        raw_data = [span.text for span in spans]
        raw_data = [entry for entry in raw_data if '\n' not in entry]
        raw_data = [not_vs for not_vs in raw_data if not_vs != 'vs']
        matches.append(raw_data)
    # Set all data together
    # print(len(matches), len(table_dates), len(raw_hours))
    result = []
    for num in range(len(matches)):
        try:
            def date_creator(raw_date):
                raw_date = raw_date.split('.')
                raw_date = [int(part) for part in raw_date]
                ready_date = datetime.datetime(raw_date[2], raw_date[1], raw_date[0])
                return ready_date.strftime("%Y.%m.%d")

            match_set = matches[num]
            match_set.append(table_dates[num])
            match_set.append(hours[num])
            if len(match_set) == 4:
                date = date_creator(match_set[2])
                summary = {'opponent_1': match_set[0], 'opponent_2': match_set[1], 'date': date,
                           'hour': match_set[3]}
            else:
                date = date_creator(match_set[3])
                summary = {'opponent_1': match_set[0], 'opponent_2': match_set[2], 'date': date,
                           'hour': match_set[4], 'score': match_set[1]}
            result.append(summary)
        except IndexError:
            break
    # Sorting result
    sorted_result = {}
    for entry in result:
        sorted_result[entry['date']] = entry
    sorted_result = dict(sorted(sorted_result.items()))
    ready_result = [sorted_result[res] for res in sorted_result]
    return ready_result


def lech_tables_stats():
    from bs4 import BeautifulSoup
    import requests
    url = "https://gol24.pl/ekstraklasa/tabela/"
    data = requests.get(url).text
    soup = BeautifulSoup(data, "html.parser")
    raw_table = soup.find('tbody')
    rows = raw_table.find_all('tr')
    result = {}
    for row in rows:
        position = row.find(class_='lp').text
        raw_club_name = row.find(class_='nazwa').find_all('a')[0].text
        club_name = raw_club_name.replace('\n', '')[28::]
        club_name_len = len(club_name) - club_name.count(' ') + 1
        club_name = club_name[0:club_name_len]
        points = row.find(class_='pkt').text
        played_matches = row.find(class_='liczbaMeczow').text
        result[position] = {'name': club_name, 'points': points, 'matches': played_matches}

    return result


# Function responsible for rendering Lech statistics as HTML site
@app.route("/")
def home():
    match_scores = lech_match_stats_finder()
    table_scores = lech_tables_stats()
    hour = datetime.datetime.now().strftime("%A, %d %b %Y, %H:%M")
    return render_template('index.html', hour=hour, match=match_scores, table_rank=table_scores)


# Function responsible for returning a .json file with Lech statistics as request result
@app.route('/json')
def json_stats():
    match_scores = lech_match_stats_finder()
    table_scores = lech_tables_stats()
    info = {'created_by': 'Michal Malek',
            "date": datetime.datetime.now().strftime("%A, %d %b %Y, %H:%M")}
    result = {'info': info, "match_statistics": match_scores, "table_statistics": table_scores}
    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True)
