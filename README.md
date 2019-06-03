# AliExpressPriceTracker

This simple Python script will update a webpage with the latest pricing of the articles you specify in AliExpress. Great for integrating
into a Docker container with a crontab for checking prices regularly.

``setup.py`` configures the database for the tracking. ``tracker.py`` reads the database data and updates the webpage inside ``track_data`` accordingly.
