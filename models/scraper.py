import html.entities
import time,json
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright
import html
import re
def search_duckduckgo(query: str,
                      pos_start: int = 1,
                      keep_knowledge_graph: bool = True,
                      max_results: int = 10,
                      filter_to_domains:list=[],
                      safe_search:bool=True):
    start = time.time()
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True, executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0"
        )
        MWT:float = 0.0
        page = context.new_page()

        # Navigate to DuckDuckGo
        if filter_to_domains:
            query += " site:" + " OR site:".join(filter_to_domains)
        url = f"https://duckduckgo.com/?t=h_&q={query}&ia=web"
        if not safe_search:
            url += "&kp=-2"
        
        page.goto(url)
        page.wait_for_selector("li.wLL07_0Xnd1QZpzpfR4W")

        # Handle pagination for the specified starting position and max results
        for _ in range(int(pos_start / 10)):
            page.click("button.wE5p3MOcL8UVdJhgH3V1")
            page.wait_for_timeout(5)
            MWT += 0.005
        for _ in range(-(-max_results // 10)):  # Ceil division
            page.click("button.wE5p3MOcL8UVdJhgH3V1")
            page.wait_for_timeout(5)
            MWT += 0.005

        # Extract the page content
        html_content = page.content()
        soup = BeautifulSoup(html.unescape(html_content), "html.parser")
        browser.close()

        # Parse results
        results = []
        knowledge_graph_data = {}

        # Extract knowledge graph data
        if keep_knowledge_graph:
            knowledge_graph_section = soup.find("div", class_="Cwg3TAWR68fVkDBMYLUZ")
            if knowledge_graph_section:
                knowledge_graph_data["title"] = html.unescape(
                    knowledge_graph_section.find("h2", class_="Ee2e63EzQ9F3xq9wsGDY").text
                )
                knowledge_graph_data["description"] = html.unescape(
                    knowledge_graph_section.find("span").text
                )
                text_snippets = knowledge_graph_section.find_all("span", class_="expandableItem")
                knowledge_graph_data["text_snippets"] = html.unescape("".join(
                    [html.unescape(snippet.text) for snippet in text_snippets]
                ))

        # Extract search results
        parent_results = soup.find_all("li", class_="wLL07_0Xnd1QZpzpfR4W")
        position = 1
        for child in parent_results:
            try:
                res = {
                    "icon": "https:" + child.find("img").get("src"),
                    "link": child.find("a", class_="Rn_JXVtoPVAFyGkcaXyK VkOimy54PtIClAT3GMbr")["href"],
                    "title": html.unescape(
                        child.find("span", class_="EKtkFWMYpwzMKOYr0GYm LQVY1Jpkk8nyJ6HBWKAk").text
                    ),
                    "snippet": html.unescape(
                        child.find("span", class_="kY2IgmnCmOGjharHErah").text
                    ),
                    "position": position,
                    "belongsToPage": (position - 1) // 10 + 1
                }

                # Extract sub-results if available
                sub_results = child.find_all("li", class_="gyDT4qronqJu4BgQBq2F")
                if sub_results:
                    res["sub_results"] = []
                    for result in sub_results:
                        sub_res = {
                            "title": html.unescape(
                                result.find("h3", class_="EKtkFWMYpwzMKOYr0GYm LQVY1Jpkk8nyJ6HBWKAk").text
                            ),
                            "snippet": html.unescape(
                                result.find("span", class_="kY2IgmnCmOGjharHErah").text
                            ),
                            "link": result.find("a").get("href")
                        }
                        res["sub_results"].append(sub_res)

                results.append(res)
                position += 1
            except Exception:
                continue

        # Trim results to match pos_start and max_results
        results = results[pos_start - 1:]
        results = results[:max_results]

        # Construct final response
        response = {
            "organic": results,
            "duration": str(time.time() - start),
            "mandatoryWaitTime": str(MWT)
        }
        if knowledge_graph_data:
            response["knowledge_graph"] = knowledge_graph_data

        return response

def qwant_knowledge(query: str):
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=True, executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0"
        )
        page = context.new_page()

        # Navigate to DuckDuckGo
        
        url = f"https://api.qwant.com/v3/ia/knowledge?q={query}&locale=de_ch&tgp=1"
        
        page.goto(url)
        
        


        # Extract knowledge graph data
        try:
            return json.loads(page.content().split("<pre>")[1].split("</pre>")[0])  
        except Exception as e:
            return e
        finally:
            browser.close()



def mojeek_summary(query:str):
    url = f"https://www.mojeek.com/search?q={query}&mal=1"
    with sync_playwright() as p:
        # Launch browser in headless mode
        browser = p.chromium.launch(headless=False, executable_path=r"C:\Program Files\Google\Chrome\Application\chrome.exe")
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36 OPR/115.0.0.0"
        )
        page = context.new_page()
        
        page.goto(url)
        page.wait_for_selector("div#kalid")
        page.wait_for_timeout(5000)

        soup = BeautifulSoup(page.content(), 'html.parser')
        text = soup.find("div", class_="content").decode_contents()

        text = re.sub(r'<span class="src">.*?<\/span>', '', text, flags=re.DOTALL)
        words = text.replace("</span>", "")
        return words
    # Usage



    
""" Example Response:
{"status":"success","data":{"query":{"locale":"de_ch","query":"valorant"},"result":{"title":"Valorant","description":"Valorant ist ein kostenfrei spielbarer Ego-Shooter von Riot Games, der am 2. Juni 2020 für Windows veröffentlicht wurde.\nDas Spiel stellt eine Mischung aus Helden- und Taktik-Shooter dar. Zwei Fünferteams spielen gegeneinander. Die Spieler übernehmen...","thumbnail":{"landscape":"https://s1.qwant.com/thumbr/0x220/1/8/046fe7342c8fa74a54a34e4df1e074542e4b52e5064bf82b6f5f67e98011e6/1024px-Valorant_logo_-_pink_color_version.svg.png?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Ff%2Ffc%2FValorant_logo_-_pink_color_version.svg%2F1024px-Valorant_logo_-_pink_color_version.svg.png&amp;q=0&amp;b=1&amp;p=0&amp;a=0","portrait":"https://s2.qwant.com/thumbr/300x0/7/4/5723fdb24e03c01d70bd7698bcd526856cb1b86dab0b13b1ac62807e6056ba/1024px-Valorant_logo_-_pink_color_version.svg.png?u=https%3A%2F%2Fupload.wikimedia.org%2Fwikipedia%2Fcommons%2Fthumb%2Ff%2Ffc%2FValorant_logo_-_pink_color_version.svg%2F1024px-Valorant_logo_-_pink_color_version.svg.png&amp;q=0&amp;b=1&amp;p=0&amp;a=0"},"url":"https://de.wikipedia.org/wiki/Valorant","infobox_type":"video_game"}}}
"""

# print(qwant_knowledge("valorant"))

