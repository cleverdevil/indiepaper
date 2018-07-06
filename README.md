Indiepaper
==========

A "read later" service for [Micropub](https://indieweb.org/Micropub) and 
[Microsub](https://indieweb.org/Microsub) servers.

Using Indiepaper
----------------

If you spend a lot of your time in an indie reader like
[Together](https://indieweb.org/Together),
[Indigenous](https://indieweb.org/Indigenous), or
[Monocle](https://indieweb.org/Monocle), you may want to save articles into a
"read later" queue.

Enter Indiepaper! You can send a special HTTP POST request to Indiepaper, and it
will extract the content of any article on the web (ad free!) and publish it to
the Micropub endpoint of your choosing. You can use this functionality with your
Microsub server, such as [Aperture](https://indieweb.org/Aperture), to publish
these articles for later consumption into a special channel.

Indiepaper is powered by [Mercury by Postlight
Labs](https://mercury.postlight.com/web-parser/).


Indiepaper Public Service
-------------------------

Indiepaper is available as a hosted service at
[https://indiepaper.io](https://indiepaper.io). If you visit the website, you'll
also find a useful tool to generate you a "Read Later" bookmarklet for saving
articles via Indiepaper, plus links to an iOS Workflow and a native macOS app.
