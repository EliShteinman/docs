---
title: "Redis Labs Adds Two-Factor authentication to enhance account security"
linkTitle: "Redis Labs Adds Two-Factor authentication to enhance account security"
url: "/blog/redis-labs-adds-two-factor-authentication-enhance-account-security/"
description: "Today we’re introducing two-factor authentication (2FA) for Redis Enterprise, aimed at strengthening overall security and preventing unauthorized access. This enhancement can help protect your..."
date: 2018-09-04
blogCategories:
- "How To and Tutorials"
- "New Product Announcements"
- "Product Releases"
authors:
- "Aviad Abutbul"
lastmod: 2025-03-27
hidden: true
---

*By Aviad Abutbul, Senior Director of Product Management · Published 4 September 2018 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/0073e867b4e64f59de9047fdcde04295ba647e5c-772x550.webp)

Today we’re introducing two-factor authentication (2FA) for [Redis Enterprise](/redis-enterprise/), aimed at strengthening overall security and preventing unauthorized access. This enhancement can help protect your [Redis](https://redis.com) account and eliminate unauthorized access. While this setting is optional, we strongly recommend implementing it.

Here are the step-by-step instructions on how to enable 2-factor authentication:

#### Setting up 2FA on your Redis account

1. Log into your account, click on the top right menu button and navigate to your user profile by clicking on your name at the bottom of the right navigation pane:

![Redis Account User Profile](/images/site-mirror/fb75ee81450a153e3772e1304c89323e322af72a-578x424.webp)

2) In your user profile, click on the **‘Multi Factor Authentication’** button.

![Multi Factor Authentification](/images/site-mirror/4f4beda53fdead5567128dca675c86d7da91cb97-1374x154.webp)

3) Next, click **‘Activate Now.’**

![Activate Now](/images/site-mirror/eecdc2e33454d9d124981242b25583de5b7f2cef-1999x374.webp)

4) Start the process by entering your mobile phone number and click **‘Continue’**:

![Enter Your Phone Number](/images/site-mirror/ac3d8f52fd87770d94daffab0d3290b7d117f861-1482x854.webp)

Wait a few moments and check your phone. You should receive an SMS with your six-digit code for verification. Enter it and click **‘Verify.’**

That’s it. You are all set and ready to go.

If you prefer, you can also configure your Google Authenticator app ([iOS](https://itunes.apple.com/il/app/google-authenticator/id388497605?mt=8), [Android](https://play.google.com/store/apps/details?id=com.google.android.apps.authenticator2&hl=en)) by clicking on the **‘Configure’ **button next to that option.

![Google Authenticator Screen](/images/site-mirror/a7d812091ff9adac87472289002af02a53d1a06a-1999x722.webp)

Simply scan the barcode into your authenticator app and provide your verification code.

![Bar Code Authentification](/images/site-mirror/9b8ca89aeb454310dc1afb8177f587069e4f48ed-1550x1464.webp)

#### Frequently Asked Questions

**Q:** I don’t have a mobile phone. Can I add 2FA to my account?
**A:** Currently, this is not an option. You will need a mobile device to receive your 2FA codes via SMS.

**Q:** I enabled 2FA but now I want to disable it. How can I do that?
**A:** 2FA can be disabled through your Redis profile.

**Q:** I added 2FA to my account, but forgot my mobile phone today and don’t have it with me. Can I log in?
**A:** We highly recommend configuring with both SMS and the Google authenticator app so you will always have a fallback option.

**Q:** My phone was stolen. What should I do?
**A:** Disable 2FA so that someone else is not be able to log in as you, and then enable it with your new mobile phone.

#### Summary

We highly recommend you spend a few moments to enhance your account security by enabling 2FA on your Redis account.

For further information, feedback or suggestions, please contact us at [pm.group@redis.com](mailto:pm.group@redis.com).
