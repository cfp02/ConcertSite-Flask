


website_html_keys = {
    'crossroadspresents.com': {
        'which-website': 'crossroadspresents.com',
        'url': 'https://crossroadspresents.com/pages/events',
        'container-tag-name': ('div', 'edit-tour-container'),
        'tour-name': ('div', 'edit-tour-name'),
        'tour-venue': ('div', 'edit-tour-venue'),
        'tour-date': ('div', 'edit-tour-date'),
        'tour-openers': ('div', 'edit-tour-namesubs'),
    },
    'ticketliquidator':{
        'which-website': 'ticketliquidator',
        'url': 'https://www.ticketliquidator.com/search?q=',
        'container-tag-name': ('div', 'geo-event geo-alt-row  formatted'),
        'tour-name': ('span', 'event-name'),
        'tour-venue': ('span', 'venue-name'),
        'tour-date': ('input', 'event-date'),
        'tour-openers': ('span', 'event-city'),
    }
}

ticketliqidator_queries_boston = [
    'boston+concerts+january&allLoadMore=20',
    'boston+concerts+february&allLoadMore=20',
    'boston+concerts+march&allLoadMore=20',
    'boston+concerts+april&allLoadMore=20',
    'boston+concerts+may&allLoadMore=20'
]

ticketliqidator_queries_worcester = [
    'worcester+concerts+january&allLoadMore=20',
    'worcester+concerts+february&allLoadMore=20',
    'worcester+concerts+march&allLoadMore=20',
    'worcester+concerts+april&allLoadMore=20',
    'worcester+concerts+may&allLoadMore=20'
]

template_html_for_one_concert_crossroadspresents = """<!DOCTYPE html>
        <html>
        <div class="edit-tour-container" data-time="2024-01-20T23:30:00Z"><div class="edit-tour-image"> <img alt="Steve Rondo (18+)" title="Steve Rondo (18+)" src="https://s1.ticketm.net/dam/a/8f5/292515fe-83ab-47d4-bd3a-9616ce3a98f5_1637501_CUSTOM.jpg"><div class="edit-tour-status"></div></div><div class="edit-tour-details"><div dataid="vvG17Z9gDfkbdO" class="edit-tour-name">Steve Rondo (18+)</div><div class="edit-tour-namesubs">Sneaky Miles, Samantha McKaige</div><div class="edit-tour-venue">Brighton Music Hall presented by Citizens</div><div class="edit-tour-price">$18.00</div><div class="edit-tour-date">Saturday, January 20, 2024 • 6:30 PM</div><div class="edit-tour-info">This event is 18+ with valid I.D. Doors: 6:30 PM Show: 7 PM</div></div><div class="edit-tour-links"><a target="_blank" href="https://concerts.livenation.com/steve-rondo-18-boston-massachusetts-01-20-2024/event/01005F5ED41980E0" class="buy-event-btn">Buy Tickets</a><a class="more-info-event-btn" href="/pages/more-info-event?eventid=vvG17Z9gDfkbdO&amp;venueid=KovZpapwne">More Info</a></div></div>
        </html>
        """
template_html_once_concert_ticketliquidator = """<!DOCTYPE html>
        <html>
            <div onclick="window.location = this.querySelector('a').href" class="geo-event geo-alt-row  formatted" data-date="20240201" data-year="2024">
		<div class="geo-event-title">
			<a href="/tickets/6202325/cipha-sounds-tickets-thu-feb-1-2024-haymarket-lounge-at-city-winery-boston"><span class="event-name">Cipha Sounds</span></a>
		</div>
		<div class="geo-event-location">
			<span class="venue-name">Haymarket Lounge At City Winery - Boston</span> -
			<span>
				<span class="event-city">Boston</span>,
				<span class="event-state">MA</span>
			</span>
		</div>
		<div class="geo-event-date">
			<span class="event-day">Thu</span>
			<span>Feb 1</span>
			<span>7:30 PM</span>
			<span class="hide-mobile"> | </span>
				<span class="ticket-count">
					4 tickets left</span>
			<input type="hidden" value="February 01, 2024" class="event-date">
			<input type="hidden" value="07:30 PM" class="event-time">
			<input type="hidden" value="Other" class="event-parent-category">
			<input type="hidden" value="6202325" class="event-id">
		</div>
	<div class="geo-event-button"><a itemprop="url" href="/tickets/6202325/cipha-sounds-tickets-thu-feb-1-2024-haymarket-lounge-at-city-winery-boston"><span itemprop="name"><span>Tickets</span> <i class="fa fa-angle-right"></i></span></a><span class="event-ticket-count">
					4 tickets left</span></div></div>
        </html>
        """

boston_venues_list = {
    'brighton': 'Brighton Music Hall',
    'night live': 'Big Night Live',
    'blues': 'the House of Blues',
    'sinclair': 'the Sinclair',
    'paradise': 'Paradise Rock Club',
    'middle east': 'the Middle East',
    'mgm': 'MGM Music Hall',
    'crystal': 'the Crystal Ballroom',
    'royale': 'the Royale',
    'grand': 'the Grand',
    'garden': 'TD Garden',
    'agganis': 'Agganis Arena',
}

worcester_venues_list = {
    'palladium': 'The Palladium',
    'dcu': 'DCU Center',
    'electric haze': 'Electric Haze',
    'hanover': 'Hanover Theatre',
    'rails': 'Off the Rails',
}

other_venues_list = {
}