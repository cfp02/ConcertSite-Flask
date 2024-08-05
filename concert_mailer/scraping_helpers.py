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

unique_venues = {
    'palladium': {
        'other_names': ['the palladium', 'the palladium downstairs', 'the palladium upstairs'],
    },
    'fenway': {
        'other_names': ['fenway park']
    },
    'td garden': {
        'other_names': ['the garden']
    },
    'house of blues': {
        'other_names': ['hob']
    },
    'city winery': {
        'other_names': ['city winery - boston']
    },
    'paradise rock club': {
        'other_names': ['paradise']
    },
    'brighton music hall': {
        'other_names': ['brighton']
    },
    'royale': {
        'other_names': ['the royale']
    },
    'sinclair': {
        'other_names': ['the sinclair']
    },

}