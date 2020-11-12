from models import *
import smtplib, ssl
from sqlalchemy import func, desc
from datetime import datetime, timedelta

def hourlyEmail():
    since = datetime.now() - timedelta(hours=1)
    auctions = AuctionDetails.query.filter(AuctionDetails.AuctionEnd<=datetime.now(), AuctionDetails.AuctionEnd>=since)
    for auction in auctions:
        end(auction.id)

def end(AuctionID_):
    auction = AuctionDetails.query.filter_by(id = AuctionID_).first()
    seller =  User.query.filter_by(id = auction.SellerID).first()
    highestBid = Bid.query.filter_by(AuctionID = AuctionID_).order_by(desc(Bid.Amount)).first()
    if highestBid != None:
        highestBidder = User.query.filter_by(id = highestBid.BidderID).first_or_404()
    otherBids = Bid.query.filter_by(AuctionID = AuctionID_)

    port = 465
    password = "AuctionWorldWideWeb1!"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("AuctionWorldWideWeb@gmail.com", password)
        if highestBid != None:
            server.sendmail('AuctionWorldWideWeb@gmail.com', highestBidder.email, "You are highest Bidder for auction " + str(AuctionID_))
            server.sendmail('AuctionWorldWideWeb@gmail.com', seller.email, "Auction " + str(AuctionID_) + " has ended \n" + 
                highestBidder.login_name + " has won the auction\nYou may contact them via\nEmail: " +
                highestBidder.email + "\nPhone:" + highestBidder.phone_number)

        if highestBid == None:
            server.sendmail('AuctionWorldWideWeb@gmail.com', seller.email, "Auction " + str(AuctionID_) + " has ended, there is no winner")

        for otherBid in otherBids:
            otherBidder = User.query.filter_by(id = otherBid.BidderID).first_or_404()
            if otherBidder != highestBidder:
                otherBidder = User.query.filter_by(id = highestBid.BidderID).first_or_404()
                server.sendmail('AuctionWorldWideWeb@gmail.com', otherBidder.email, "You have not worn auction " + str(AuctionID_))