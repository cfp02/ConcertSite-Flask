# website_html_keys = {
#     'crossroadspresents.com': {
#         'which-website': 'crossroadspresents.com',
#         'url': 'https://crossroadspresents.com/pages/events',
#         'container-tag-name': ('div', 'edit-tour-container'),
#         'tour-name': ('div', 'edit-tour-name'),
#         'tour-venue': ('div', 'edit-tour-venue'),
#         'tour-date': ('div', 'edit-tour-date'),
#         'tour-openers': ('div', 'edit-tour-namesubs'),
#     },
#     'ticketliquidator':{
#         'which-website': 'ticketliquidator',
#         'url': 'https://www.ticketliquidator.com/search?q=',
#         'container-tag-name': ('div', 'geo-event geo-alt-row  formatted'),
#         'tour-name': ('span', 'event-name'),
#         'tour-venue': ('span', 'venue-name'),
#         'tour-date': ('input', 'event-date'),
#         'tour-openers': ('span', 'event-city'),
#     }
# }

website_html_keys = {
    'crossroadspresents.com': {
        'which_website': 'crossroadspresents.com',
        'base_url': 'https://crossroadspresents.com/pages/events',
        'container_tag_tuple': ('div', 'edit-tour-container'),
        'tour_name_tag_tuple': ('div', 'edit-tour-name'),
        'tour_venue_tag_tuple': ('div', 'edit-tour-venue'),
        'tour_date_tag_tuple': ('div', 'edit-tour-date'),
        'tour_openers_tag_tuple': ('div', 'edit-tour-namesubs'),
    },
    'ticketliquidator':{
        'which_website': 'ticketliquidator',
        'base_url': 'https://www.ticketliquidator.com/search?q=',
        'container_tag_tuple': ('div', 'geo-event geo-alt-row  formatted'),
        'tour_name_tag_tuple': ('span', 'event-name'),
        'tour_venue_tag_tuple': ('span', 'venue-name'),
        'tour_date_tag_tuple': ('input', 'event-date'),
        'tour_openers_tag_tuple': ('span', 'event-city'),
    }
}

ticketliqidator_queries_boston = [
    'boston+concerts+august&allLoadMore=20',
    # 'boston+concerts+september&allLoadMore=20',
    # 'boston+concerts+october&allLoadMore=20',
    # 'boston+concerts+november&allLoadMore=20',
    # 'boston+concerts+december&allLoadMore=20'
]

ticketliqidator_queries_worcester = [
    'worcester+concerts+august&allLoadMore=20',
    'worcester+concerts+september&allLoadMore=20',
    'worcester+concerts+october&allLoadMore=20',
    'worcester+concerts+november&allLoadMore=20',
    'worcester+concerts+december&allLoadMore=20'
]

