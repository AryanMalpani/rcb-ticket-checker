# RCB Ticket Checker 🏏

## The Problem

I'm a big RCB fan and always look forward to catching a match at Chinnaswamy. But getting tickets on the RCB site is an F'ing pain. On top of that, RCB never mentions the *time* of ticket release — just the date.

What you're left with is a full day of refreshing the site and still ending up disappointed because tickets sell out in under a minute.

## The Solution

A script. Plain old inspect element gives you the API call to get available events — I just automated that.

Run this on the day RCB announces sales and you'll be the **first one alerted the moment tickets drop**. Not knowing the exact release time is no longer a disadvantage — it's your edge.

> **Pro tip:** Pre-login to the site before running this. Otherwise your head start is wasted on the login screen.

---

## How It Works

- Polls the RCB ticketing API every 5 seconds
- Compares the response to the last saved state (`last_response.json`)
- On change, fires **3 Slack notifications** in quick succession
- Stops and alerts on any unexpected error

> I have seen other scripts as well before this but most of them load the full page and scrape HTML/CSS to detect ticket availability. This script pings the **TicketGenie API** that the RCB site itself uses to fetch match listings — the same call your browser makes. The difference is probably just a few milliseconds, but it's cleaner.

---
## Setup
Add your slack webhook details, then

```bash
pip install requests
```

To run:

```bash
python checker.py
```

> **Note:** I have used slack because it was easy to integrate for me and gave me fast notifs. But you can also use **telegram bots** or **twilio** for notifs. Shouldn't be a problem to change the code in the age of AI :)

## Configuration

| Variable | Description |
|---|---|
| `SLACK_WEBHOOK_URL` | Incoming webhook URL for your Slack channel |
| `URL` | RCB ticket API endpoint |

> **Note:** Do not commit your Slack webhook URL.

## Collaborate

I'm completely open to taking this further — auto-fetching available seats, locking them, auto-filling customer details. Open an issue and let's build it.

**Ee Sala Cup Namde!!! 🔴⚫**
