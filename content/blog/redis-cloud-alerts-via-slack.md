---
title: "How to Receive Redis Cloud Alerts via Slack"
linkTitle: "How to Receive Redis Cloud Alerts via Slack"
url: "/blog/redis-cloud-alerts-via-slack/"
description: "Several Redis Cloud customers have requested a way for alerts to be delivered on Slack channels. While these notifications are currently available only through email, there is a workaround with..."
date: 2022-11-22
blogCategories:
- "How To and Tutorials"
- "Tech"
authors:
- "Nic Gibson"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Nic Gibson, Contributor · Published 22 November 2022 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/e52cffc4ae0ae4a941d16aec9562a67df2a9536b-772x550.webp)

**Several Redis Cloud customers have requested a way for alerts to be delivered on Slack channels. While these notifications are currently available only through email, there is a workaround with similar results. This how-to outlines the process step-by-step.**

Staying on top of your Redis Cloud performance is mission-critical. While thresholds and configurations are established in the Redis Cloud interface, the important alerts that signal high memory usage, for example, are delivered by email.

You want to stay on top of some situations and act quickly. For example, a database is affected by latency, or a team wants an alert once a database has crossed a 90% capacity threshold. The current notification system requires an administrator to decide who receives email alerts and for what purpose.

However, many people rely on Slack for timely notifications rather than email. Here’s how to integrate them with Redis Cloud – as long as you have a paid Slack account.

## How to manage Redis Cloud alerts on Slack

To use a Slack channel, an email address is required. Redis customers can take the email address associated with the Slack account and use it to receive alert emails. The instructions are the same for both the Slack desktop and web UIs.

Note: A paid Slack account is required.

### Create a channel

![How To Receive Redis Cloud Alerts Via Slack](/images/site-mirror/2fde19d495227796f20433c79a668115d69387a8-1078x1060.webp)

Is a DevOps channel already in use? Skip this step if that’s the case.

Otherwise, create a new channel. Skip the add “Add people” dialog at this point. In some organizations, creating a channel is sometimes restricted, which may require an admin.

![How To Receive Redis Cloud Alerts Via Slack](/images/site-mirror/c2ee4c4093b8430c971c56ce6a2544f9d0f8fbd5-1222x660.webp)

At the top, select “Get Notifications for All Messages.”

Right below, right-click on the “Channel name.”

Select “View channel details” and set the desired notification.

### Connect the Slack channel email

![send emails to this channel image](/images/site-mirror/d49494fbb05fe89d4b0940efd2470d310d2223b6-1165x1134.webp)

From the top navigation bar, click the “Integrations” tab and click on “Send emails to this channel.”

![How To Receive Redis Cloud Alerts Via Slack](/images/site-mirror/1f62b68a61f93f4d29bbb742df2f226a29102a4f-1200x452.webp)

If this is a new channel, click the “Get Email Address” button. If it is restricted, ask an administrator for added permissions.

![How To Receive Redis Cloud Alerts Via Slack](/images/site-mirror/a13d6adf906f04e237d9f85df7e9b9b135ca1fdc-1164x522.webp)

Copy the email address to the clipboard.

### Get set up in Service Manager

![How To Receive Redis Cloud Alerts Via Slack](/images/site-mirror/e9ca3f229768551fb30717077b09e99d4a72de8d-600x789.webp)

Log into the Service Manager.

Create a new user on the Access Management screen. You can assign any name to this user. It should be assigned the role of *Viewer* as this is a notifications-only setup.

Next, paste in the email address copied in the previous step. Make sure the *Alert Emails* option is toggled. Click the **Add User **below.

![How To Receive Redis Cloud Alerts Via Slack](/images/site-mirror/e5dcd682f6cb2bcbe8b61f0734d2e3a49f5c9fdf-1752x292.webp)

The activation email for this new user will be sent to the Slack channel. Go back to the channel; there should be an invitation email from Redis Cloud.

![How To Receive Redis Cloud Alerts Via Slack](/images/site-mirror/44b62b2ded525dee0dc27390366b96645eeb2548-1662x1042.webp)

Click on the message to expand it out, and accept the invitation by clicking the **Join Redis **button.

Establish a password.

…And done! Redis Cloud alerts should now be enabled in Slack.

### Next steps

Test the settings to verify everything is in order and get started on your app performance optimization team strategies.
