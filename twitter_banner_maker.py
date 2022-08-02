from PIL import Image, ImageDraw, ImageFont

class BannerMaker:
	'''Class for creating a banner image.'''

	def __init__(self, followers):
		#Follower count
		self.followers = followers

		#Banner size
		self.width = 1500
		self.height = 500

		#Fonts style and size
		self.font_size = 60
		self.follower_font_size = 90
		self.font = ImageFont.truetype(
				"Poppins-Medium.ttf", self.font_size)
		self.follower_font = ImageFont.truetype(
				"Poppins-Medium.ttf", self.follower_font_size)

		self.img = Image.open("base.png")
		self.base = ImageDraw.Draw(self.img)

		self.text_prep(self.followers)
		self.make_banner(self.base)
		self.save_banner(self.img)

	def text_prep(self, followers):
		#Text preparation
		self.follower_count = str(followers)
		self.f_text_width, self.f_text_height = (
			self.font.getsize(self.follower_count))

		self.top_text = "The number changes when you follow me!"
		self.t_text_width, self.t_text_height = (
			self.font.getsize(self.top_text))

	def make_banner(self, base):
		#Adding the text to the banner, "making" it
		#Top text
		base.text(
			((self.width - self.t_text_width)/2 + 1, 
				(self.height - self.font_size)/2 - 50), 
			self.top_text,
			font = self.font, 
			fill = (255, 255, 255),
			)

		#Follower count
		base.text(
			((self.width - self.f_text_width)/2 + 1, 
				(self.height - self.follower_font_size)/2 + 70), 
			self.follower_count,
			font = self.follower_font, 
			fill = (255, 255, 255),
			)

	def save_banner(self, image):
		#Show and save the banner.
		image.save("banner.png")