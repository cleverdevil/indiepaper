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


Sample
------

If you wanted to save this interesting article from The Verge to your read later
channel, which you have created in Aperture with an API key of XXXXXXX, you
would create the request as follows:

```
POST / HTTP/1.1
Host: indiepaper.cleverdevil.io
Content-Type: application/x-www-form-urlencoded
Authorization: Bearer XXXXXXXX
mp-destination: https://aperture.p3k.io/micropub

url=https://www.theverge.com/2018/6/27/17509888/oumuamua-interstellar-comet-asteroid-solar-system-trajectory
```

Indiepaper Public Service
-------------------------

Indiepaper is available as a hosted service at
[https://indiepaper.cleverdevil.io](https://indiepaper.cleverdevil.io). If you
visit the website, you'll also find a useful tool to generate you a "Read Later"
bookmarklet for saving articles via Indiepaper.


iOS Workflow
------------

There is an [iOS Workflow](https://cleverdevil.io/s/hgmKUXa4o2jaHozClixV.wflow)
available for sending URLs into Indiepaper throughout the system. Download and
install the workflow, then change the Authorization header and mp-destination
header to match your use case.
