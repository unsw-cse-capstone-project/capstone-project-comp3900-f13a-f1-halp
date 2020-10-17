from datetime import datetime
from auction import db

class AuctionDetails(db.Model):
	AuctionID = db.Column(db.String, primary_key=True)
	PropertyID = db.Column(db.String, unique=True, nullable=False)
	SellerID = db.Column(db.Integer, nullable=False)
	AuctionStart = db.Column(db.DateTime, nullable=False)
	AuctionEnd = db.Column(db.DateTime, nullable=False)
	ReservePrice = db.Column(db.Float, nullable=False)
	MinBiddingGap = db.Column(db.Float, nullable=False)

	def __repr__(self):
		return f"AuctionDetails('{self.AuctionID}', '{self.PropertyID}', '{self.SellerID}')"