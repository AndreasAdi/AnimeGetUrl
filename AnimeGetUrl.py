from bs4 import BeautifulSoup
import sys
import traceback
import webbrowser
import requests


def main():
    try:
        baseurl = "https://gogoanime.ar"

        url = "https://gogoanime.ar/search.html?keyword="

        link_list = []
        search_result = False

        #print in green
        print('\033[92m' + "####################################" + '\033[0m')
        print('\033[92m' + "#                                  #" + '\033[0m')
        print('\033[92m' + "# AnimeGetUrl - v1.1 - by @Andreas #" + '\033[0m')
        print('\033[92m' + "#                                  #" + '\033[0m')
        print('\033[92m' + "####################################" + '\033[0m')
        while not search_result:
            # input for search
            search = input("\nSearch: ")

            # check if search is more than three characters
            if (len(search) < 3):
                print("Search must be atleast 3 characters")
                continue

            # spoof user agent
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'}
            result = requests.get(url+search, headers=headers)
            doc = BeautifulSoup(result.text, "html.parser")

            # find div with class "last_episodes

            div = doc.find_all("div", class_="last_episodes")

            # inside div find ul with class items then find all li
            for i in div:
                ul = i.find("ul", class_="items")
                li = ul.find_all("li")

            if (len(li) == 0):
                print("No results found")
                continue
            else:
                search_result = True
                break
        # find p with class "name" inside div

        name = div[0].find_all("p", class_="name")

        for idx, i in enumerate(name):
            # print in green if odd number

            if (idx % 2 == 0):
                print('\033[92m' + "[" + str(idx+1) +
                      "]" + i.text.strip() + '\033[0m')
            else:
                print("["+str(idx+1)+"]" + i.text.strip())

        # in name find all links
        for link in name:
            link_list.append(link.find_all("a")[0].get("href"))

        # input to select anime
        select = 999
        while (select > len(link_list) or select < 1):
            try:
                select = int(input("Select anime: "))
            except ValueError:
                print("Invalid input")
                select = 999
                continue

        # print (baseurl+ link_list[select-1]);
        episodepage = baseurl + link_list[select-1]

        # scrape episode page
        result = requests.get(episodepage, headers=headers)
        doc = BeautifulSoup(result.text, "html.parser")

        # find input with class movie_id
        movieid = doc.find_all("input", class_="movie_id")

        # find input with class default_ep
        default_ep = doc.find_all("input", class_="default_ep")

        # find input with class alias_anime
        alias_anime = doc.find_all("input", class_="alias_anime")
        ul = doc.find_all("ul", id="episode_page")

        # find all li inside ul
        li = ul[0].find_all("li")

        ep_start = li[0].find_all("a")[0].get("ep_start")
        ep_end = li[len(li)-1].find_all("a")[0].get("ep_end")

        # print(input[0].get("value"));
        # print(default_ep[0].get("value"));
        # print(alias_anime[0].get("value"));
        # print(ep_start);
        # print(ep_end);

        request_episode_url = "https://ajax.gogo-load.com/ajax/load-list-episode?ep_start=+" + \
            str(ep_start)+"&ep_end="+str(ep_end)+"&id=" + \
            str(movieid[0].get("value"))+"&default_ep=0&alias=" + \
            str(alias_anime[0].get("value"))

        # print(request_episode_url)

        result = requests.get(request_episode_url, headers=headers)
        doc = BeautifulSoup(result.text, "html.parser")

        # find all a inside li
        a = doc.find_all("a")

        episode_url_list = []
        for i in a:
            episode_url_list.append(i.get("href"))

        # sort list
        episode_url_list.reverse()

        # print(episode_url_list)

        exit = False

        while (exit == False):
            select_episode = 999
            try:
                # input for episode
                select_episode = int(
                    input("Enter the episode number (1-"+ep_end+"): "))
                if (select_episode > len(episode_url_list) or select_episode < 1):
                    print("Invalid episode number")
                    continue
            except KeyboardInterrupt:
                exit = True
                continue
            except:
                print("Invalid episode number")
                continue

            result = requests.get(
                baseurl+episode_url_list[select_episode-1].strip(), headers=headers)
            doc = BeautifulSoup(result.text, "html.parser")

            div = doc.find_all("div", class_="anime_muti_link")

            links = div[0].find_all("a")

            video_links = []
            # loop for all links and find data_video property
            for link in links:
                # print(link.get("data-video"))

                # if link does not contain https:// then add it
                if (link.get("data-video").find("https://") == -1):
                    link["data-video"] = "https:" + link.get("data-video")
                else:
                    link["data-video"] = link.get("data-video")
    
                video_links.append(link.get("data-video"))

                print("["+str(len(video_links))+"]" + link.get("data-video"))
                # print("\n")

            select_mirror = 999
            while (select_mirror > len(video_links) or select_mirror < 1):
                try:
                    select_mirror = int(input("Select Video Mirror: "))
                except ValueError:
                    print("Invalid input")
                    select_mirror = 999
                    continue

            webbrowser.open(video_links[select_mirror-1])

            # open first link in video_links in browser
            # webbrowser.open(video_links[0])

            # ask if user wants to watch another episode
            another = input("Watch another episode? (y/n): ")
            if (another == "n"):
                exit = True

        input("Press Enter to exit .....")
    except UnboundLocalError:
        print("No results found")
    except KeyboardInterrupt:
        print("Exiting")
    except Exception:
        traceback.print_exc(file=sys.stdout)

    sys.exit(0)


if __name__ == "__main__":
    main()
