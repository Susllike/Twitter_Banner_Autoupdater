from PIL import Image, ImageDraw, ImageFont

class BannerMaker:
	'''Class for creating a banner image.'''

	def __init__(self, followers, latest_follower_file, latest_handle):
		#Follower count
		self.followers = followers

		#Latest follower
		self.latest_follower = self.image_prep(latest_follower_file)

		#Latest follower handle
		self.latest_handle = f"@{latest_handle}"

		#Banner size
		self.width = 1500
		self.height = 500

		#Fonts style and size
		self.follower_font_size = 90
		self.follower_font = ImageFont.truetype(
				"Poppins-Medium.ttf", self.follower_font_size)

		self.handle_font_size = 30
		self.handle_font = ImageFont.truetype(
				"Poppins-Medium.ttf", self.handle_font_size)

		self.img = Image.open("base.png")
		self.base = ImageDraw.Draw(self.img)

		self.text_prep(self.followers)
		self.make_banner(self.base)
		self.add_follower(self.img, self.latest_follower)
		self.save_banner(self.img)

	def image_prep(self, image):
		#Resize the image for the banner.
		img = Image.open(image)

		#Fixed resize scale since it's been calculated in advance
		img = img.resize((245, 245), Image.ANTIALIAS)

		return img

	def text_prep(self, followers):
		#Text preparation
		self.follower_count = str(followers)
		self.f_text_width, _ = (
			self.follower_font.getsize(self.follower_count))

		self.handle_width, _ = (
			self.handle_font.getsize(self.latest_handle))

	def make_banner(self, base):
		#Adding the text to the banner, "making" it.
		#Follower count
		base.text(
			(self.width/3 - self.f_text_width/2 + 1, 
				(self.height - self.follower_font_size)/2 + 70), 
			self.follower_count,
			font = self.follower_font, 
			fill = (255, 255, 255),
			)

		base.text(
			(1215 - self.handle_width/2, 425),
			self.latest_handle,
			font = self.handle_font,
			fill = (255, 255, 255),
			)

	def add_follower(self, base, follower):
		#Add the profile image of the latest follower to the banner.

		#Fixed position calculated beforehand
		base.paste(follower, (1092, 105))

	def save_banner(self, image):
		#Show and save the banner.

		#For testing the module purposes
		if __name__ == "__main__":
			image.save("test_banner.png")
		else:
			image.save("banner.png")

if __name__ == "__main__":
	#Testing purposes
	#banner = BannerMaker(2000000, "latest_follower_pfp.jpg", "Joe Doe")
	pass
