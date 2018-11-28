from datetime import datetime, timedelta
from time import sleep
import requests
import tempfile
import pytz

from polybot import Bot
from insight import fetch_images


class InsightImages(Bot):
    def init(self):
        self.state["last_img_time"] = datetime(2018, 11, 27, 20, 24, 51).replace(tzinfo=pytz.utc)
        self.state["last_time"] = datetime.now() - timedelta(days=1)

    def main(self):
        if "last_id" not in self.state:
            self.init()

        while True:
            if self.state["last_time"] > datetime.now() - timedelta(minutes=1):
                sleep(120)
                continue

            imgs = reversed(fetch_images())

            for img in imgs:
                if img["date_taken"] <= self.state["last_img_time"]:
                    continue
                self.post_image(img)
                self.state["last_img_time"] = img["date_taken"]
                self.state["last_time"] = datetime.now()
                break

            sleep(30)

    def post_image(self, img):
        with tempfile.NamedTemporaryFile(suffix=".png") as downloadfile:
            res = requests.get(img["url"])
            res.raise_for_status()
            for chunk in res.iter_content(chunk_size=1024):
                if chunk:
                    downloadfile.write(chunk)
            downloadfile.flush()

            text = (
                img["title"]
                + "\n\nTaken on: "
                + img["date_taken"].strftime("%Y/%m/%d %H:%M:%S")
            )
            self.post(text, downloadfile)


InsightImages("insightimages").run()
