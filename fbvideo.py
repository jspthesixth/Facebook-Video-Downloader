import mechanize
from bs4 import BeautifulSoup
import argparse

class FacebookVideoDownload:
    def __init__(self, username=None, password=None, video_url=None, video_name=None):
        self.username = username
        self.password = password
        self.video_url = video_url
        self.browser = mechanize.Browser()
        self.browser.set_handle_robots(False)
        self.browser.addheaders = [('User-agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/45.0.2454101')]
        self.link = None
        self.download_link = None
        self.video_list = []
        self.video_name = video_name

    def get_link(self):
        new_url = self.video_url.replace("https://www", "https://m")
        return new_url

    def login(self):
        if self.username != None and self.password != None:
            self.browser.open("https://m.facebook.com")       
            self.browser.select_form(nr=0)
            self.browser.form["email"] = self.username
            self.browser.form["pass"] = self.password
            self.browser.submit()
        else:
            pass

    def catch(self):
        self.new_url = self.get_link()
        try:
            html = self.browser.open(self.new_url) 
        except:
            print("Check video URL or login credentials!")
        else:
            with open("html.txt", "wb") as html_file:
                html_file.write(html.read())

    def get_video_link(self):
        try:
            with open("html.txt", encoding="utf8") as file:
                soup = BeautifulSoup(file.read(), features="lxml")
        except FileNotFoundError:
            print("Oopsie, something went wrong, check the URL or your login credentials!")
        else:
            a_tag = soup.find_all("a", {"href":True})
            for att in a_tag:
                a_value = att["href"]
                if "/video_redirect/" in a_value:
                    self.link = "https://m.facebook.com" + a_value
                    self.video_list.append(self.link)

    def download_video(self):
        self.browser.open(self.video_list[0])
        link = self.browser.geturl()
        if self.video_name != None:
            if ".mp4" not in self.video_name:
            	self.video_name += ".mp4"
            self.browser.retrieve(link, self.video_name)
        else:
            self.browser.retrieve(link, "video.mp4")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--username", type=str, required=True, help="Provide username and password if video is private.")
    parser.add_argument("-p", "--password", type=str, required=True, help="Provide password if video is private.")
    parser.add_argument("--url", type=str, required=True, help="Video URL is a required argument.")
    parser.add_argument("--output", type=str, required=False, help="Output video name. If non is given, video will be saved as video.mp4.")
    args = parser.parse_args()

    fb = FacebookVideoDownload(args.username, args.password, args.url, args.output)
    fb.login()
    fb.catch()
    fb.get_video_link()
    fb.download_video()