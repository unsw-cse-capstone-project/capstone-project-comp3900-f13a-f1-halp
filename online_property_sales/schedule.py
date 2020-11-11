from models import *
import smtplib, ssl
from sqlalchemy import func, desc

def hourlyEmail():
    end(1)

def end(AuctionID_):
    highestBid = Bid.query.filter_by(AuctionID = AuctionID_).order_by(desc(Bid.Amount)).first()
    highestBidder = User.query.filter_by(id = highestBid.BidderID).first_or_404()
    otherBids = Bid.query.filter_by(AuctionID = AuctionID_)

    port = 465
    password = "AuctionWorldWideWeb1!"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("AuctionWorldWideWeb@gmail.com", password)

        server.sendmail('AuctionWorldWideWeb@gmail.com', highestBidder.email, "You are highest Bidder for auction " + str(AuctionID_))

        for otherBid in otherBids:
            otherBidder = User.query.filter_by(id = otherBid.BidderID).first_or_404()
            if otherBidder != highestBidder:
                otherBidder = User.query.filter_by(id = highestBid.BidderID).first_or_404()
                server.sendmail('AuctionWorldWideWeb@gmail.com', otherBidder.email, "You have not worn auction " + str(AuctionID_))