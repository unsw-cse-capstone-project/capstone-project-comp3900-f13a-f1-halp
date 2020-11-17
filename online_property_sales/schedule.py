from models import *
from server import db
import smtplib, ssl
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from flask import render_template, request, redirect, url_for, flash

def hourlyEmail():
    since = datetime.now() - timedelta(minutes=1)
    auctions = AuctionDetails.query.filter(AuctionDetails.AuctionEnd<=datetime.now(), AuctionDetails.AuctionEnd>=since)
    for auction in auctions:
        end(auction.id)

def end(AuctionID_):
    auction = AuctionDetails.query.filter_by(id = AuctionID_).first()
    seller =  User.query.filter_by(id = auction.SellerID).first()
    property_ = Property.query.get(auction.PropertyID)

    highestBid = Bid.query.filter_by(AuctionID = AuctionID_).order_by(desc(Bid.Amount)).first()
    if highestBid != None:
        highestBidder = User.query.filter_by(id = highestBid.BidderID).first_or_404()
        if highestBid.Amount >= auction.ReservePrice:
            property_.status = "sold"
        else:
            property_.status = "Under Offer"
    else:
        property_.status = "Under Offer"
        
    db.session.commit()
    otherBids = Bid.query.filter_by(AuctionID = AuctionID_)

    port = 465
    password = "AuctionWorldWideWeb1!"
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("AuctionWorldWideWeb@gmail.com", password)
        if highestBid != None:
            address=''
            if property_.add_unit:
                address = property_.add_unit + "/"
            address+= property_.add_num +', '+ property_.add_suburb+', ' +property_.add_state + ', ' + property_.add_pc + ', Australia '

            server.sendmail('AuctionWorldWideWeb@gmail.com', highestBidder.email, "You are highest Bidder for auction of" + address)
            server.sendmail('AuctionWorldWideWeb@gmail.com', seller.email, "Auction of" + address + " has ended \n" + 
                highestBidder.login_name + " has won the auction\nYou may contact them via\nEmail: " +
                highestBidder.email + "\nPhone:" + highestBidder.phone_number)

        if highestBid == None:
            server.sendmail('AuctionWorldWideWeb@gmail.com', seller.email, "Auction of " + address + " has ended, there is no winner")

        for otherBid in otherBids:
            otherBidder = User.query.filter_by(id = otherBid.BidderID).first_or_404()
            if otherBidder != highestBidder:
                otherBidder = User.query.filter_by(id = highestBid.BidderID).first_or_404()
                server.sendmail('AuctionWorldWideWeb@gmail.com', otherBidder.email, "You have not worn auction " + address)