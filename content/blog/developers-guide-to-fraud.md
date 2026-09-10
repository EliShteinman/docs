---
title: "What’s Changing in the World of Fraud Detection (And What Developers Need to Know About It)"
linkTitle: "What’s Changing in the World of Fraud Detection (And What Developers Need to Know About It)"
url: "/blog/developers-guide-to-fraud/"
description: "Developers are expected to level up their baked-in security measures, but that’s easier said than done. Here are some helpful tips."
date: 2023-03-13
blogCategories:
- "Tech"
authors:
- "Pam Baker"
lastmod: 2025-03-27
hidden: true
mirrored: true
---

*By Pam Baker, Contributor · Published 13 March 2023 · updated 27 March 2025*

![Blog tile image](/images/site-mirror/7836564e111a06c9259fa77b2cadc215a517b0d7-772x550.webp)

**Developers are expected to level up their baked-in security measures, but that’s easier said than done. Here are some helpful tips.**

Motivation to improve [fraud detection](/solutions/fraud-detection/) is at an all-time high for financial institutions. It’s not just common-place fraudulent transactions that are costing banks money, although those are costly enough. According to [an ABA Banking Journal report](https://bankingjournal.aba.com/2022/01/study-banks-see-rise-in-fraud-attempts-associated-costs-in-2021/#:~:text=Online%20banking%20accounted%20for%2033,down%20from%2029%25%20in%202020./), “For every dollar of fraud lost in 2021, U.S. financial services firms saw $4.00 in costs, up from $3.64 in 2020 before the pandemic.”

Staying on top of all the ways crooks cheat [financial systems](/industries/financial-services/) and software is a full-time job. But developers are expected to grok what’s happening now and to build in safeguards to prevent it, too.

Thankfully, there are tools and software to assist developers with this task, but it’s still a tall order to fill.

To that end, here are tips to help bring developers up to speed on what’s new in current fraud detection – and the actions they should be prepared to take.

## Understand the scope of the problem

Few developers are ignorant of the importance of security practices, but they may not realize the extent that it’s needed in financial technology (Fintech) or the urgency of finding workable practices. The bad guys are busy innovating too.

Fraud has always been a huge problem for banks and other financial institutions. But Fintechs are feeling the squeeze continuing to tighten. It’s hard to deliver flawless service for the 53% of the global population expected to be using digital banking by 2026 ([Juniper Green](https://www.juniperresearch.com/press/over-half-global-population-digital-banking), 2021) and keep the 48.6% of fraud reported to the FTC locked out. What greases the wheels for customers also lets fraudsters slide in with ease.

Synthetic fraud, which refers to the result of building a false identity from one or two stolen data points from real people, costs U.S. banks upwards of $20 billion, according to[ another ABA Banking Journal report](https://bankingjournal.aba.com/2021/10/report-synthetic-identity-fraud-results-in-20-billion-in-losses-in-2020/#:~:text=Synthetic%20identity%20fraud%2C%20where%20fraudsters,report%20from%20software%20company%20FiVerity./). Banks are under pressure from regulators to curb money laundering, and they face increasingly high penalties when they fall short. That’s a problem, given that about $2 trillion is laundered globally each year (according to a[ Deloitte report](https://www2.deloitte.com/content/dam/Deloitte/in/Documents/finance/Forensic/in-forensic-AML-Survey-report-2020-noexp.pdf)), and roughly half of it goes undetected across the entire financial industry.

Protections built on static checklists and data are doomed to failure in today’s fast-moving world. Designing more fluid user identification and authentication methods that can be checked in real-time is a better strategy. But it’s also more difficult to pull off without some help. Assistance can come in the form of internal or third-party tools or extra hands, but it can also result from tightening relationships with existing business partners. A lot can be accomplished by sharing more information that leads to building better inputs for fraud detection algorithms.

## Track the new and growing patterns in fraud

As with other cybersecurity issues, the key to prevention requires accurate pattern detection. But first, developers need an idea of where to look for emerging or evolving patterns.

“There is no crystal ball as to what is going to happen next in the world of fraud. But we can see some patterns getting stronger over the last year and a half,” says Baber Amin, chief product and operating officer at[ Veridium](https://veridiumid.com/), an identity authentication company. At the top of the list are account takeover fraud, synthetic identity fraud, and card not present fraud.

## Use new clues for better fraud detection

In injecting security protections in code to detect and reject fraud, developers often rely on their own experience or on company protocols to guide them. However, these practices are good only until the bad guys change the game.

“The number one thing to avoid is rule-based detection. That should be put out to pasture at this point,” says Amin.

So what can developers do to get a better idea of what protections to build into the software? Try looking outside of your organization for clues.

“Fintech companies need to work with other major vendors, like airlines, car rental companies, and major [retailers](/industries/retail/), to take in signals that raise or lower the potential risk of a transaction,” says Amin.

## Find newer ways to hide the API keys

Rule-based detection isn’t the only thing that isn’t working well. Much of the tried and true is going the way of the tired and trounced.

“The Fintech world has learned a lot of hard lessons over the last couple of years, and it has resulted in significant increases in fraud and data breaches,” warns Ted Miracco, CEO of[ Approov](https://approov.io/), a security provider for mobile apps. “Implementation of 2FA and use of technologies like code obfuscation for API keys and other ‘secrets’ has proven to be woefully inadequate for preventing fraud, as these approaches are easily circumvented by the determined hacker.”

Moving API keys to the cloud is safer than trying to obfuscate APIs that are hardcoded into the application. Another good tactic is mobile app attestation, which only allows genuine apps on untampered devices to access APIs, according to Miracco.

“This approach can both stop bots, emulators, and hacking frameworks from abusing APIs with stolen credentials acquired from the [dark web](https://www.csoonline.com/article/3249765/what-is-the-dark-web-how-to-access-it-and-what-youll-find.html) and also stop the increasingly popular man-in-the-middle (MITM) attacks,” Miracco adds.

## Find better, faster ways to detect anomalies

Rules-based detection has always struggled with distinguishing between risky and normal behaviors. AI is far better at pattern-checking and behavior labeling.

“Integrating AI and machine learning should be a given at this point,” says Stanislav Khilobochenko, vice president of customer services at[ Clario](https://clario.co/), an antivirus provider. “It’s the most reliable way to detect patterns and anomalies indicating fraud, and there’s really no way around it: you’ll need to adopt it at some point,”.

“You will have faster detection response, more accurate detection, and the ability to process more data. You will also have more scalability and customization to suit the needs of your business and customers,” Khilobochenko adds.

## Newer checklists for AI and ML

While not entirely new as concepts, some items require greater attention from developers than before. Examples include making allowances for freelancers and gig workers whose income and payment behaviors may deviate strongly from other banking customers.

“Geographic biases, racial biases, gender biases, or even only being trained with English data could mean fraudulent activity is overlooked or misidentified. For example, the irregular income patterns of freelancers could be flagged as suspicious if the system is trained mostly on traditional income patterns,” explains Khilobochenko.

For example, banks are using AI-based systems as part of identity authentication and transaction risk-scoring models. The huge behavior-based and identity-info datasets need to be updated frequently, with worldwide access, which may require technical upgrades to keep the architecture responsive.

“Obviously, this is a huge undertaking and why partnering with an AI firm might be the best way to integrate customized, effective machine learning into your applications,” Khilobochenko adds.

## Tap the root of all evil for more detection clues

Put another way, start looking for ways to catch fraud at its root. After all, the sooner you can detect a possible vulnerability, the more likely your block won’t miss.

“Deploy AI to look for Identity theft and synthetic identity account creation. A majority of fraud is rooted in fraudulent identities,” says Amin.

Identity theft is tricky to detect, so look for multiple ways to authenticate users. Two-factor authentication is not foolproof. Especially if the device or email is one of the authenticators.

## Level up your user authentication factors

Add more layers of user authentication where you can and look to automate much of it so there’s no additional burden on your users. One good way to do that is to leverage AI’s ability to scale complex models.

“Deploy AI to detect patterns and context around payment and purchases. Look for cohort or family member spending to detect [more] patterns,” says Amin.

To learn specific ways to improve your organization’s fraud detection, read [*Combat Fraud with Redis Enterprise*](/docs/combat-fraud-with-redis-enterprise/).
