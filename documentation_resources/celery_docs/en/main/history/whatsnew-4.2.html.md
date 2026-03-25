<!-- Source: https://docs.celeryq.dev/en/main/history/whatsnew-4.2.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/whatsnew-4.2.html).

# What’s new in Celery 4.2 (windowlicker)

Author:
:   Omer Katz (`omer.drow at gmail.com`)

Celery is a simple, flexible, and reliable distributed system to
process vast amounts of messages, while providing operations with
the tools required to maintain such a system.

It’s a task queue with focus on real-time processing, while also
supporting task scheduling.

Celery has a large and diverse community of users and contributors,
you should come join us on IRC
or our mailing-list.

To read more about Celery you should go read the [introduction](../getting-started/introduction.html#intro).

While this version is backward compatible with previous versions
it’s important that you read the following section.

This version is officially supported on CPython 2.7, 3.4, 3.5 & 3.6
and is also supported on PyPy.

## 

The 4.2.0 release continues to improve our efforts to provide you with
the best task execution platform for Python.

This release is mainly a bug fix release, ironing out some issues and regressions
found in Celery 4.0.0.

Traditionally, releases were named after [Autechre](https://en.wikipedia.org/wiki/Autechre)’s track names.
This release continues this tradition in a slightly different way.
Each major version of Celery will use a different artist’s track names as codenames.

From now on, the 4.x series will be codenamed after [Aphex Twin](https://en.wikipedia.org/wiki/Aphex_Twin)’s track names.
This release is codenamed after his very famous track, [Windowlicker](https://youtu.be/UBS4Gi1y_nc?t=4m).

Thank you for your support!

*— Omer Katz*

### 

Aaron Harnly <[aharnly@wgen.net](mailto:aharnly%40wgen.net)>
Aaron Harnly <[github.com@bulk.harnly.net](mailto:github.com%40bulk.harnly.net)>
Aaron McMillin <[github@aaron.mcmillinclan.org](mailto:github%40aaron.mcmillinclan.org)>
Aaron Ross <[aaronelliotross@gmail.com](mailto:aaronelliotross%40gmail.com)>
Aaron Ross <[aaron@wawd.com](mailto:aaron%40wawd.com)>
Aaron Schumacher <[ajschumacher@gmail.com](mailto:ajschumacher%40gmail.com)>
abecciu <[augusto@becciu.org](mailto:augusto%40becciu.org)>
abhinav nilaratna <[anilaratna2@bloomberg.net](mailto:anilaratna2%40bloomberg.net)>
Acey9 <[huiwang.e@gmail.com](mailto:huiwang.e%40gmail.com)>
Acey <[huiwang.e@gmail.com](mailto:huiwang.e%40gmail.com)>
aclowes <[aclowes@gmail.com](mailto:aclowes%40gmail.com)>
Adam Chainz <[adam@adamj.eu](mailto:adam%40adamj.eu)>
Adam DePue <[adepue@hearsaycorp.com](mailto:adepue%40hearsaycorp.com)>
Adam Endicott <[adam@zoey.local](mailto:adam%40zoey.local)>
Adam Renberg <[tgwizard@gmail.com](mailto:tgwizard%40gmail.com)>
Adam Venturella <[aventurella@gmail.com](mailto:aventurella%40gmail.com)>
Adaptification <[Adaptification@users.noreply.github.com](mailto:Adaptification%40users.noreply.github.com)>
Adrian <[adrian@planetcoding.net](mailto:adrian%40planetcoding.net)>
adriano petrich <[petrich@gmail.com](mailto:petrich%40gmail.com)>
Adrian Rego <[arego320@gmail.com](mailto:arego320%40gmail.com)>
Adrien Guinet <[aguinet@quarkslab.com](mailto:aguinet%40quarkslab.com)>
Agris Ameriks <[ameriks@gmail.com](mailto:ameriks%40gmail.com)>
Ahmet Demir <[ahmet2mir+github@gmail.com](mailto:ahmet2mir+github%40gmail.com)>
air-upc <[xin.shli@ele.me](mailto:xin.shli%40ele.me)>
Aitor Gómez-Goiri <[aitor@gomezgoiri.net](mailto:aitor%40gomezgoiri.net)>
Akira Matsuzaki <[akira.matsuzaki.1977@gmail.com](mailto:akira.matsuzaki.1977%40gmail.com)>
Akshar Raaj <[akshar@agiliq.com](mailto:akshar%40agiliq.com)>
Alain Masiero <[amasiero@ocs.online.net](mailto:amasiero%40ocs.online.net)>
Alan Hamlett <[alan.hamlett@prezi.com](mailto:alan.hamlett%40prezi.com)>
Alan Hamlett <[alanhamlett@users.noreply.github.com](mailto:alanhamlett%40users.noreply.github.com)>
Alan Justino <[alan.justino@yahoo.com.br](mailto:alan.justino%40yahoo.com.br)>
Alan Justino da Silva <[alan.justino@yahoo.com.br](mailto:alan.justino%40yahoo.com.br)>
Albert Wang <[albert@zerocater.com](mailto:albert%40zerocater.com)>
Alcides Viamontes Esquivel <[a.viamontes.esquivel@gmail.com](mailto:a.viamontes.esquivel%40gmail.com)>
Alec Clowes <[aclowes@gmail.com](mailto:aclowes%40gmail.com)>
Alejandro Pernin <[ale.pernin@gmail.com](mailto:ale.pernin%40gmail.com)>
Alejandro Varas <[alej0varas@gmail.com](mailto:alej0varas%40gmail.com)>
Aleksandr Kuznetsov <[aku.ru.kz@gmail.com](mailto:aku.ru.kz%40gmail.com)>
Ales Zoulek <[ales.zoulek@gmail.com](mailto:ales.zoulek%40gmail.com)>
Alexander <[a.a.lebedev@gmail.com](mailto:a.a.lebedev%40gmail.com)>
Alexander A. Sosnovskiy <[alecs.box@gmail.com](mailto:alecs.box%40gmail.com)>
Alexander Koshelev <[daevaorn@gmail.com](mailto:daevaorn%40gmail.com)>
Alexander Koval <[kovalidis@gmail.com](mailto:kovalidis%40gmail.com)>
Alexander Oblovatniy <[oblalex@users.noreply.github.com](mailto:oblalex%40users.noreply.github.com)>
Alexander Oblovatniy <[oblovatniy@gmail.com](mailto:oblovatniy%40gmail.com)>
Alexander Ovechkin <[frostoov@gmail.com](mailto:frostoov%40gmail.com)>
Alexander Smirnov <[asmirnov@five9.com](mailto:asmirnov%40five9.com)>
Alexandru Chirila <[alex@alexkiro.com](mailto:alex%40alexkiro.com)>
Alexey Kotlyarov <[alexey@infoxchange.net.au](mailto:alexey%40infoxchange.net.au)>
Alexey Zatelepin <[ztlpn@yandex-team.ru](mailto:ztlpn%40yandex-team.ru)>
Alex Garel <[alex@garel.org](mailto:alex%40garel.org)>
Alex Hill <[alex@hill.net.au](mailto:alex%40hill.net.au)>
Alex Kiriukha <[akiriukha@cogniance.com](mailto:akiriukha%40cogniance.com)>
Alex Koshelev <[daevaorn@gmail.com](mailto:daevaorn%40gmail.com)>
Alex Rattray <[rattray.alex@gmail.com](mailto:rattray.alex%40gmail.com)>
Alex Williams <[alex.williams@skyscanner.net](mailto:alex.williams%40skyscanner.net)>
Alex Zaitsev <[azaitsev@gmail.com](mailto:azaitsev%40gmail.com)>
Ali Bozorgkhan <[alibozorgkhan@gmail.com](mailto:alibozorgkhan%40gmail.com)>
Allan Caffee <[allan.caffee@gmail.com](mailto:allan.caffee%40gmail.com)>
Allard Hoeve <[allard@byte.nl](mailto:allard%40byte.nl)>
allenling <[lingyiwang@haomaiyi.com](mailto:lingyiwang%40haomaiyi.com)>
Alli <[alzeih@users.noreply.github.com](mailto:alzeih%40users.noreply.github.com)>
Alman One <[alman@laptop.home](mailto:alman%40laptop.home)>
Alman One <[alman-one@laptop.home](mailto:alman-one%40laptop.home)>
alman-one <[masiero.alain@gmail.com](mailto:masiero.alain%40gmail.com)>
Amir Rustamzadeh <[amirrustam@users.noreply.github.com](mailto:amirrustam%40users.noreply.github.com)>
[anand21nanda@gmail.com](mailto:anand21nanda%40gmail.com) <[anand21nanda@gmail.com](mailto:anand21nanda%40gmail.com)>
Anarchist666 <[Anarchist666@yandex.ru](mailto:Anarchist666%40yandex.ru)>
Anders Pearson <[anders@columbia.edu](mailto:anders%40columbia.edu)>
Andrea Rabbaglietti <[silverfix@gmail.com](mailto:silverfix%40gmail.com)>
Andreas Pelme <[andreas@pelme.se](mailto:andreas%40pelme.se)>
Andreas Savvides <[andreas@editd.com](mailto:andreas%40editd.com)>
Andrei Fokau <[andrei.fokau@neutron.kth.se](mailto:andrei.fokau%40neutron.kth.se)>
Andrew de Quincey <[adq@lidskialf.net](mailto:adq%40lidskialf.net)>
Andrew Kittredge <[andrewlkittredge@gmail.com](mailto:andrewlkittredge%40gmail.com)>
Andrew McFague <[amcfague@wgen.net](mailto:amcfague%40wgen.net)>
Andrew Stewart <[astewart@twistbioscience.com](mailto:astewart%40twistbioscience.com)>
Andrew Watts <[andrewwatts@gmail.com](mailto:andrewwatts%40gmail.com)>
Andrew Wong <[argsno@gmail.com](mailto:argsno%40gmail.com)>
Andrey Voronov <[eyvoro@users.noreply.github.com](mailto:eyvoro%40users.noreply.github.com)>
Andriy Yurchuk <[ayurchuk@minuteware.net](mailto:ayurchuk%40minuteware.net)>
Aneil Mallavarapu <[aneil.mallavar@gmail.com](mailto:aneil.mallavar%40gmail.com)>
anentropic <[ego@anentropic.com](mailto:ego%40anentropic.com)>
anh <[anhlh2@gmail.com](mailto:anhlh2%40gmail.com)>
Ankur Dedania <[AbsoluteMSTR@gmail.com](mailto:AbsoluteMSTR%40gmail.com)>
Anthony Lukach <[anthonylukach@gmail.com](mailto:anthonylukach%40gmail.com)>
antlegrand <[2t.antoine@gmail.com](mailto:2t.antoine%40gmail.com)>
Antoine Legrand <[antoine.legrand@smartjog.com](mailto:antoine.legrand%40smartjog.com)>
Anton <[anton.gladkov@gmail.com](mailto:anton.gladkov%40gmail.com)>
Anton Gladkov <[atn18@yandex-team.ru](mailto:atn18%40yandex-team.ru)>
Antonin Delpeuch <[antonin@delpeuch.eu](mailto:antonin%40delpeuch.eu)>
Arcadiy Ivanov <[arcadiy@ivanov.biz](mailto:arcadiy%40ivanov.biz)>
areski <[areski@gmail.com](mailto:areski%40gmail.com)>
Armenak Baburyan <[kanemra@gmail.com](mailto:kanemra%40gmail.com)>
Armin Ronacher <[armin.ronacher@active-4.com](mailto:armin.ronacher%40active-4.com)>
armo <[kanemra@gmail.com](mailto:kanemra%40gmail.com)>
Arnaud Rocher <[cailloumajor@users.noreply.github.com](mailto:cailloumajor%40users.noreply.github.com)>
arpanshah29 <[ashah29@stanford.edu](mailto:ashah29%40stanford.edu)>
Arsenio Santos <[arsenio@gmail.com](mailto:arsenio%40gmail.com)>
Arthur Vigil <[ahvigil@mail.sfsu.edu](mailto:ahvigil%40mail.sfsu.edu)>
Arthur Vuillard <[arthur@hashbang.fr](mailto:arthur%40hashbang.fr)>
Ashish Dubey <[ashish.dubey91@gmail.com](mailto:ashish.dubey91%40gmail.com)>
Asif Saifuddin Auvi <[auvipy@gmail.com](mailto:auvipy%40gmail.com)>
Asif Saifuddin Auvi <[auvipy@users.noreply.github.com](mailto:auvipy%40users.noreply.github.com)>
ask <[ask@0x61736b.net](mailto:ask%400x61736b.net)>
Ask Solem <[ask@celeryproject.org](mailto:ask%40celeryproject.org)>
Ask Solem <[askh@opera.com](mailto:askh%40opera.com)>
Ask Solem Hoel <[ask@celeryproject.org](mailto:ask%40celeryproject.org)>
aydin <[adigeaydin@gmail.com](mailto:adigeaydin%40gmail.com)>
baeuml <[baeuml@kit.edu](mailto:baeuml%40kit.edu)>
Balachandran C <[balachandran.c@gramvaani.org](mailto:balachandran.c%40gramvaani.org)>
Balthazar Rouberol <[balthazar.rouberol@mapado.com](mailto:balthazar.rouberol%40mapado.com)>
Balthazar Rouberol <[balthazar.rouberol@ubertas.co.uk](mailto:balthazar.rouberol%40ubertas.co.uk)>
bartloop <[38962178+bartloop@users.noreply.github.com](mailto:38962178+bartloop%40users.noreply.github.com)>
Bartosz Ptaszynski <>
Batiste Bieler <[batiste.bieler@pix4d.com](mailto:batiste.bieler%40pix4d.com)>
bee-keeper <[ricbottomley@gmail.com](mailto:ricbottomley%40gmail.com)>
Bence Tamas <[mr.bence.tamas@gmail.com](mailto:mr.bence.tamas%40gmail.com)>
Ben Firshman <[ben@firshman.co.uk](mailto:ben%40firshman.co.uk)>
Ben Welsh <[ben.welsh@gmail.com](mailto:ben.welsh%40gmail.com)>
Berker Peksag <[berker.peksag@gmail.com](mailto:berker.peksag%40gmail.com)>
Bert Vanderbauwhede <[batlock666@gmail.com](mailto:batlock666%40gmail.com)>
Bert Vanderbauwhede <[bert.vanderbauwhede@ugent.be](mailto:bert.vanderbauwhede%40ugent.be)>
BLAGA Razvan-Paul <[razvan.paul.blaga@gmail.com](mailto:razvan.paul.blaga%40gmail.com)>
bobbybeever <[bobby.beever@yahoo.com](mailto:bobby.beever%40yahoo.com)>
bobby <[bobby.beever@yahoo.com](mailto:bobby.beever%40yahoo.com)>
Bobby Powers <[bobbypowers@gmail.com](mailto:bobbypowers%40gmail.com)>
Bohdan Rybak <[bohdan.rybak@gmail.com](mailto:bohdan.rybak%40gmail.com)>
Brad Jasper <[bjasper@gmail.com](mailto:bjasper%40gmail.com)>
Branko Čibej <[brane@apache.org](mailto:brane%40apache.org)>
BR <[b.rabiega@gmail.com](mailto:b.rabiega%40gmail.com)>
Brendan MacDonell <[macdonellba@gmail.com](mailto:macdonellba%40gmail.com)>
Brendon Crawford <[brendon@aphexcreations.net](mailto:brendon%40aphexcreations.net)>
Brent Watson <[brent@brentwatson.com](mailto:brent%40brentwatson.com)>
Brian Bouterse <[bmbouter@gmail.com](mailto:bmbouter%40gmail.com)>
Brian Dixon <[bjdixon@gmail.com](mailto:bjdixon%40gmail.com)>
Brian Luan <[jznight@gmail.com](mailto:jznight%40gmail.com)>
Brian May <[brian@linuxpenguins.xyz](mailto:brian%40linuxpenguins.xyz)>
Brian Peiris <[brianpeiris@gmail.com](mailto:brianpeiris%40gmail.com)>
Brian Rosner <[brosner@gmail.com](mailto:brosner%40gmail.com)>
Brodie Rao <[brodie@sf.io](mailto:brodie%40sf.io)>
Bruno Alla <[browniebroke@users.noreply.github.com](mailto:browniebroke%40users.noreply.github.com)>
Bryan Berg <[bdb@north-eastham.org](mailto:bdb%40north-eastham.org)>
Bryan Berg <[bryan@mixedmedialabs.com](mailto:bryan%40mixedmedialabs.com)>
Bryan Bishop <[kanzure@gmail.com](mailto:kanzure%40gmail.com)>
Bryan Helmig <[bryan@bryanhelmig.com](mailto:bryan%40bryanhelmig.com)>
Bryce Groff <[bgroff@hawaii.edu](mailto:bgroff%40hawaii.edu)>
Caleb Mingle <[mingle@uber.com](mailto:mingle%40uber.com)>
Carlos Garcia-Dubus <[carlos.garciadm@gmail.com](mailto:carlos.garciadm%40gmail.com)>
Catalin Iacob <[iacobcatalin@gmail.com](mailto:iacobcatalin%40gmail.com)>
Charles McLaughlin <[mclaughlinct@gmail.com](mailto:mclaughlinct%40gmail.com)>
Chase Seibert <[chase.seibert+github@gmail.com](mailto:chase.seibert+github%40gmail.com)>
ChillarAnand <[anand21nanda@gmail.com](mailto:anand21nanda%40gmail.com)>
Chris Adams <[chris@improbable.org](mailto:chris%40improbable.org)>
Chris Angove <[cangove@wgen.net](mailto:cangove%40wgen.net)>
Chris Chamberlin <[chamberlincd@gmail.com](mailto:chamberlincd%40gmail.com)>
chrisclark <[chris@untrod.com](mailto:chris%40untrod.com)>
Chris Harris <[chris.harris@kitware.com](mailto:chris.harris%40kitware.com)>
Chris Kuehl <[chris@techxonline.net](mailto:chris%40techxonline.net)>
Chris Martin <[ch.martin@gmail.com](mailto:ch.martin%40gmail.com)>
Chris Mitchell <[chris.mit7@gmail.com](mailto:chris.mit7%40gmail.com)>
Chris Rose <[offby1@offby1.net](mailto:offby1%40offby1.net)>
Chris St. Pierre <[chris.a.st.pierre@gmail.com](mailto:chris.a.st.pierre%40gmail.com)>
Chris Streeter <[chris@chrisstreeter.com](mailto:chris%40chrisstreeter.com)>
Christian <[github@penpal4u.net](mailto:github%40penpal4u.net)>
Christoph Burgmer <[christoph@nwebs.de](mailto:christoph%40nwebs.de)>
Christopher Hoskin <[mans0954@users.noreply.github.com](mailto:mans0954%40users.noreply.github.com)>
Christopher Lee <[chris@cozi.com](mailto:chris%40cozi.com)>
Christopher Peplin <[github@rhubarbtech.com](mailto:github%40rhubarbtech.com)>
Christopher Peplin <[peplin@bueda.com](mailto:peplin%40bueda.com)>
Christoph Krybus <[ckrybus@googlemail.com](mailto:ckrybus%40googlemail.com)>
clayg <[clay.gerrard@gmail.com](mailto:clay.gerrard%40gmail.com)>
Clay Gerrard <[clayg@clayg-desktop](mailto:clayg%40clayg-desktop).(none)>
Clemens Wolff <[clemens@justamouse.com](mailto:clemens%40justamouse.com)>
cmclaughlin <[mclaughlinct@gmail.com](mailto:mclaughlinct%40gmail.com)>
Codeb Fan <[codeb2cc@gmail.com](mailto:codeb2cc%40gmail.com)>
Colin McIntosh <[colin@colinmcintosh.com](mailto:colin%40colinmcintosh.com)>
Conrad Kramer <[ckrames1234@gmail.com](mailto:ckrames1234%40gmail.com)>
Corey Farwell <[coreyf@rwell.org](mailto:coreyf%40rwell.org)>
Craig Younkins <[cyounkins@Craigs-MacBook-Pro.local](mailto:cyounkins%40Craigs-MacBook-Pro.local)>
csfeathers <[csfeathers@users.noreply.github.com](mailto:csfeathers%40users.noreply.github.com)>
Cullen Rhodes <[rhodes.cullen@yahoo.co.uk](mailto:rhodes.cullen%40yahoo.co.uk)>
daftshady <[daftonshady@gmail.com](mailto:daftonshady%40gmail.com)>
Dan <[dmtaub@gmail.com](mailto:dmtaub%40gmail.com)>
Dan Hackner <[dan.hackner@gmail.com](mailto:dan.hackner%40gmail.com)>
Daniel Devine <[devine@ddevnet.net](mailto:devine%40ddevnet.net)>
Daniele Procida <[daniele@vurt.org](mailto:daniele%40vurt.org)>
Daniel Hahler <[github@thequod.de](mailto:github%40thequod.de)>
Daniel Hepper <[daniel.hepper@gmail.com](mailto:daniel.hepper%40gmail.com)>
Daniel Huang <[dxhuang@gmail.com](mailto:dxhuang%40gmail.com)>
Daniel Lundin <[daniel.lundin@trioptima.com](mailto:daniel.lundin%40trioptima.com)>
Daniel Lundin <[dln@eintr.org](mailto:dln%40eintr.org)>
Daniel Watkins <[daniel@daniel-watkins.co.uk](mailto:daniel%40daniel-watkins.co.uk)>
Danilo Bargen <[mail@dbrgn.ch](mailto:mail%40dbrgn.ch)>
Dan McGee <[dan@archlinux.org](mailto:dan%40archlinux.org)>
Dan McGee <[dpmcgee@gmail.com](mailto:dpmcgee%40gmail.com)>
Dan Wilson <[danjwilson@gmail.com](mailto:danjwilson%40gmail.com)>
Daodao <[daodaod@gmail.com](mailto:daodaod%40gmail.com)>
Dave Smith <[dave@thesmithfam.org](mailto:dave%40thesmithfam.org)>
Dave Smith <[dsmith@hirevue.com](mailto:dsmith%40hirevue.com)>
David Arthur <[darthur@digitalsmiths.com](mailto:darthur%40digitalsmiths.com)>
David Arthur <[mumrah@gmail.com](mailto:mumrah%40gmail.com)>
David Baumgold <[david@davidbaumgold.com](mailto:david%40davidbaumgold.com)>
David Cramer <[dcramer@gmail.com](mailto:dcramer%40gmail.com)>
David Davis <[daviddavis@users.noreply.github.com](mailto:daviddavis%40users.noreply.github.com)>
David Harrigan <[dharrigan118@gmail.com](mailto:dharrigan118%40gmail.com)>
David Harrigan <[dharrigan@dyn.com](mailto:dharrigan%40dyn.com)>
David Markey <[dmarkey@localhost.localdomain](mailto:dmarkey%40localhost.localdomain)>
David Miller <[david@deadpansincerity.com](mailto:david%40deadpansincerity.com)>
David Miller <[il.livid.dream@gmail.com](mailto:il.livid.dream%40gmail.com)>
David Pravec <[David.Pravec@danix.org](mailto:David.Pravec%40danix.org)>
David Pravec <[david.pravec@nethost.cz](mailto:david.pravec%40nethost.cz)>
David Strauss <[david@davidstrauss.net](mailto:david%40davidstrauss.net)>
David White <[dpwhite2@ncsu.edu](mailto:dpwhite2%40ncsu.edu)>
DDevine <[devine@ddevnet.net](mailto:devine%40ddevnet.net)>
Denis Podlesniy <[Haos616@Gmail.com](mailto:Haos616%40Gmail.com)>
Denis Shirokov <[dan@rexuni.com](mailto:dan%40rexuni.com)>
Dennis Brakhane <[dennis.brakhane@inoio.de](mailto:dennis.brakhane%40inoio.de)>
Derek Harland <[donkopotamus@users.noreply.github.com](mailto:donkopotamus%40users.noreply.github.com)>
derek\_kim <[bluewhale8202@gmail.com](mailto:bluewhale8202%40gmail.com)>
dessant <[dessant@users.noreply.github.com](mailto:dessant%40users.noreply.github.com)>
Dieter Adriaenssens <[ruleant@users.sourceforge.net](mailto:ruleant%40users.sourceforge.net)>
Dima Kurguzov <[koorgoo@gmail.com](mailto:koorgoo%40gmail.com)>
dimka665 <[dimka665@gmail.com](mailto:dimka665%40gmail.com)>
dimlev <[dimlev@gmail.com](mailto:dimlev%40gmail.com)>
dmarkey <[david@dmarkey.com](mailto:david%40dmarkey.com)>
Dmitry Malinovsky <[damalinov@gmail.com](mailto:damalinov%40gmail.com)>
Dmitry Malinovsky <[dmalinovsky@thumbtack.net](mailto:dmalinovsky%40thumbtack.net)>
dmollerm <[d.moller.m@gmail.com](mailto:d.moller.m%40gmail.com)>
Dmytro Petruk <[bavaria95@gmail.com](mailto:bavaria95%40gmail.com)>
dolugen <[dolugen@gmail.com](mailto:dolugen%40gmail.com)>
dongweiming <[ciici1234@hotmail.com](mailto:ciici1234%40hotmail.com)>
dongweiming <[ciici123@gmail.com](mailto:ciici123%40gmail.com)>
Dongweiming <[ciici123@gmail.com](mailto:ciici123%40gmail.com)>
dtheodor <[dimitris.theodorou@gmail.com](mailto:dimitris.theodorou%40gmail.com)>
Dudás Ádám <[sir.dudas.adam@gmail.com](mailto:sir.dudas.adam%40gmail.com)>
Dustin J. Mitchell <[dustin@mozilla.com](mailto:dustin%40mozilla.com)>
D. Yu <[darylyu@users.noreply.github.com](mailto:darylyu%40users.noreply.github.com)>
Ed Morley <[edmorley@users.noreply.github.com](mailto:edmorley%40users.noreply.github.com)>
Eduardo Ramírez <[ejramire@uc.cl](mailto:ejramire%40uc.cl)>
Edward Betts <[edward@4angle.com](mailto:edward%404angle.com)>
Emil Stanchev <[stanchev.emil@gmail.com](mailto:stanchev.emil%40gmail.com)>
Eran Rundstein <[eran@sandsquid](mailto:eran%40sandsquid).(none)>
ergo <[ergo@debian.Belkin](mailto:ergo%40debian.Belkin)>
Eric Poelke <[epoelke@gmail.com](mailto:epoelke%40gmail.com)>
Eric Zarowny <[ezarowny@gmail.com](mailto:ezarowny%40gmail.com)>
ernop <[ernestfrench@gmail.com](mailto:ernestfrench%40gmail.com)>
Evgeniy <[quick.es@gmail.com](mailto:quick.es%40gmail.com)>
evildmp <[daniele@apple-juice.co.uk](mailto:daniele%40apple-juice.co.uk)>
fatihsucu <[fatihsucu0@gmail.com](mailto:fatihsucu0%40gmail.com)>
Fatih Sucu <[fatihsucu@users.noreply.github.com](mailto:fatihsucu%40users.noreply.github.com)>
Feanil Patel <[feanil@edx.org](mailto:feanil%40edx.org)>
Felipe <[fcoelho@users.noreply.github.com](mailto:fcoelho%40users.noreply.github.com)>
Felipe Godói Rosário <[felipe.rosario@geru.com.br](mailto:felipe.rosario%40geru.com.br)>
Felix Berger <[bflat1@gmx.net](mailto:bflat1%40gmx.net)>
Fengyuan Chen <[cfy1990@gmail.com](mailto:cfy1990%40gmail.com)>
Fernando Rocha <[fernandogrd@gmail.com](mailto:fernandogrd%40gmail.com)>
ffeast <[ffeast@gmail.com](mailto:ffeast%40gmail.com)>
Flavio Percoco Premoli <[flaper87@gmail.com](mailto:flaper87%40gmail.com)>
Florian Apolloner <[apollo13@apolloner.eu](mailto:apollo13%40apolloner.eu)>
Florian Apolloner <[florian@apollo13](mailto:florian%40apollo13).(none)>
Florian Demmer <[fdemmer@gmail.com](mailto:fdemmer%40gmail.com)>
flyingfoxlee <[lingyunzhi312@gmail.com](mailto:lingyunzhi312%40gmail.com)>
Francois Visconte <[f.visconte@gmail.com](mailto:f.visconte%40gmail.com)>
François Voron <[fvoron@gmail.com](mailto:fvoron%40gmail.com)>
Frédéric Junod <[frederic.junod@camptocamp.com](mailto:frederic.junod%40camptocamp.com)>
fredj <[frederic.junod@camptocamp.com](mailto:frederic.junod%40camptocamp.com)>
frol <[frolvlad@gmail.com](mailto:frolvlad%40gmail.com)>
Gabriel <[gabrielpjordao@gmail.com](mailto:gabrielpjordao%40gmail.com)>
Gao Jiangmiao <[gao.jiangmiao@h3c.com](mailto:gao.jiangmiao%40h3c.com)>
GDR! <[gdr@gdr.name](mailto:gdr%40gdr.name)>
GDvalle <[GDvalle@users.noreply.github.com](mailto:GDvalle%40users.noreply.github.com)>
Geoffrey Bauduin <[bauduin.geo@gmail.com](mailto:bauduin.geo%40gmail.com)>
georgepsarakis <[giwrgos.psarakis@gmail.com](mailto:giwrgos.psarakis%40gmail.com)>
George Psarakis <[giwrgos.psarakis@gmail.com](mailto:giwrgos.psarakis%40gmail.com)>
George Sibble <[gsibble@gmail.com](mailto:gsibble%40gmail.com)>
George Tantiras <[raratiru@users.noreply.github.com](mailto:raratiru%40users.noreply.github.com)>
Georgy Cheshkov <[medoslav@gmail.com](mailto:medoslav%40gmail.com)>
Gerald Manipon <[pymonger@gmail.com](mailto:pymonger%40gmail.com)>
German M. Bravo <[german.mb@deipi.com](mailto:german.mb%40deipi.com)>
Gert Van Gool <[gertvangool@gmail.com](mailto:gertvangool%40gmail.com)>
Gilles Dartiguelongue <[gilles.dartiguelongue@esiee.org](mailto:gilles.dartiguelongue%40esiee.org)>
Gino Ledesma <[gledesma@apple.com](mailto:gledesma%40apple.com)>
gmanipon <[gmanipon@jpl.nasa.gov](mailto:gmanipon%40jpl.nasa.gov)>
Grant Thomas <[jgrantthomas@gmail.com](mailto:jgrantthomas%40gmail.com)>
Greg Haskins <[greg@greghaskins.com](mailto:greg%40greghaskins.com)>
gregoire <[gregoire@audacy.fr](mailto:gregoire%40audacy.fr)>
Greg Taylor <[gtaylor@duointeractive.com](mailto:gtaylor%40duointeractive.com)>
Greg Wilbur <[gwilbur@bloomberg.net](mailto:gwilbur%40bloomberg.net)>
Guillaume Gauvrit <[guillaume@gandi.net](mailto:guillaume%40gandi.net)>
Guillaume Gendre <[dzb.rtz@gmail.com](mailto:dzb.rtz%40gmail.com)>
Gun.io Whitespace Robot <[contact@gun.io](mailto:contact%40gun.io)>
Gunnlaugur Thor Briem <[gunnlaugur@gmail.com](mailto:gunnlaugur%40gmail.com)>
harm <[harm.verhagen@gmail.com](mailto:harm.verhagen%40gmail.com)>
Harm Verhagen <[harm.verhagen@gmail.com](mailto:harm.verhagen%40gmail.com)>
Harry Moreno <[morenoh149@gmail.com](mailto:morenoh149%40gmail.com)>
hclihn <[23141651+hclihn@users.noreply.github.com](mailto:23141651+hclihn%40users.noreply.github.com)>
hekevintran <[hekevintran@gmail.com](mailto:hekevintran%40gmail.com)>
honux <[atoahp@hotmail.com](mailto:atoahp%40hotmail.com)>
Honza Kral <[honza.kral@gmail.com](mailto:honza.kral%40gmail.com)>
Honza Král <[Honza.Kral@gmail.com](mailto:Honza.Kral%40gmail.com)>
Hooksie <[me@matthooks.com](mailto:me%40matthooks.com)>
Hsiaoming Yang <[me@lepture.com](mailto:me%40lepture.com)>
Huang Huang <[mozillazg101@gmail.com](mailto:mozillazg101%40gmail.com)>
Hynek Schlawack <[hs@ox.cx](mailto:hs%40ox.cx)>
Hynek Schlawack <[schlawack@variomedia.de](mailto:schlawack%40variomedia.de)>
Ian Dees <[ian.dees@gmail.com](mailto:ian.dees%40gmail.com)>
Ian McCracken <[ian.mccracken@gmail.com](mailto:ian.mccracken%40gmail.com)>
Ian Wilson <[ian.owings@gmail.com](mailto:ian.owings%40gmail.com)>
Idan Kamara <[idankk86@gmail.com](mailto:idankk86%40gmail.com)>
Ignas Mikalajūnas <[ignas.mikalajunas@gmail.com](mailto:ignas.mikalajunas%40gmail.com)>
Igor Kasianov <[super.hang.glider@gmail.com](mailto:super.hang.glider%40gmail.com)>
illes <[illes.solt@gmail.com](mailto:illes.solt%40gmail.com)>
Ilya <[4beast@gmail.com](mailto:4beast%40gmail.com)>
Ilya Georgievsky <[i.georgievsky@drweb.com](mailto:i.georgievsky%40drweb.com)>
Ionel Cristian Mărieș <[contact@ionelmc.ro](mailto:contact%40ionelmc.ro)>
Ionel Maries Cristian <[contact@ionelmc.ro](mailto:contact%40ionelmc.ro)>
Ionut Turturica <[jonozzz@yahoo.com](mailto:jonozzz%40yahoo.com)>
Iurii Kriachko <[iurii.kriachko@gmail.com](mailto:iurii.kriachko%40gmail.com)>
Ivan Metzlar <[metzlar@gmail.com](mailto:metzlar%40gmail.com)>
Ivan Virabyan <[i.virabyan@gmail.com](mailto:i.virabyan%40gmail.com)>
j0hnsmith <[info@whywouldwe.com](mailto:info%40whywouldwe.com)>
Jackie Leng <[Jackie.Leng@nelen-schuurmans.nl](mailto:Jackie.Leng%40nelen-schuurmans.nl)>
J Alan Brogan <[jalanb@users.noreply.github.com](mailto:jalanb%40users.noreply.github.com)>
Jameel Al-Aziz <[me@jalaziz.net](mailto:me%40jalaziz.net)>
James M. Allen <[james.m.allen@gmail.com](mailto:james.m.allen%40gmail.com)>
James Michael DuPont <[JamesMikeDuPont@gmail.com](mailto:JamesMikeDuPont%40gmail.com)>
James Pulec <[jpulec@gmail.com](mailto:jpulec%40gmail.com)>
James Remeika <[james@remeika.us](mailto:james%40remeika.us)>
Jamie Alessio <[jamie@stoic.net](mailto:jamie%40stoic.net)>
Jannis Leidel <[jannis@leidel.info](mailto:jannis%40leidel.info)>
Jared Biel <[jared.biel@bolderthinking.com](mailto:jared.biel%40bolderthinking.com)>
Jason Baker <[amnorvend@gmail.com](mailto:amnorvend%40gmail.com)>
Jason Baker <[jason@ubuntu.ubuntu-domain](mailto:jason%40ubuntu.ubuntu-domain)>
Jason Veatch <[jtveatch@gmail.com](mailto:jtveatch%40gmail.com)>
Jasper Bryant-Greene <[jbg@rf.net.nz](mailto:jbg%40rf.net.nz)>
Javier Domingo Cansino <[javierdo1@gmail.com](mailto:javierdo1%40gmail.com)>
Javier Martin Montull <[javier.martin.montull@cern.ch](mailto:javier.martin.montull%40cern.ch)>
Jay Farrimond <[jay@instaedu.com](mailto:jay%40instaedu.com)>
Jay McGrath <[jaymcgrath@users.noreply.github.com](mailto:jaymcgrath%40users.noreply.github.com)>
jbiel <[jared.biel@bolderthinking.com](mailto:jared.biel%40bolderthinking.com)>
jbochi <[jbochi@gmail.com](mailto:jbochi%40gmail.com)>
Jed Smith <[jed@jedsmith.org](mailto:jed%40jedsmith.org)>
Jeff Balogh <[github@jeffbalogh.org](mailto:github%40jeffbalogh.org)>
Jeff Balogh <[me@jeffbalogh.org](mailto:me%40jeffbalogh.org)>
Jeff Terrace <[jterrace@gmail.com](mailto:jterrace%40gmail.com)>
Jeff Widman <[jeff@jeffwidman.com](mailto:jeff%40jeffwidman.com)>
Jelle Verstraaten <[jelle.verstraaten@xs4all.nl](mailto:jelle.verstraaten%40xs4all.nl)>
Jeremy Cline <[jeremy@jcline.org](mailto:jeremy%40jcline.org)>
Jeremy Zafran <[jeremy.zafran@cloudlock.com](mailto:jeremy.zafran%40cloudlock.com)>
jerry <[jerry@stellaservice.com](mailto:jerry%40stellaservice.com)>
Jerzy Kozera <[jerzy.kozera@gmail.com](mailto:jerzy.kozera%40gmail.com)>
Jerzy Kozera <[jerzy.kozera@sensisoft.com](mailto:jerzy.kozera%40sensisoft.com)>
jespern <[jesper@noehr.org](mailto:jesper%40noehr.org)>
Jesper Noehr <[jespern@jesper-noehrs-macbook-pro.local](mailto:jespern%40jesper-noehrs-macbook-pro.local)>
Jesse <[jvanderdoes@gmail.com](mailto:jvanderdoes%40gmail.com)>
jess <[jessachandler@gmail.com](mailto:jessachandler%40gmail.com)>
Jess Johnson <[jess@grokcode.com](mailto:jess%40grokcode.com)>
Jian Yu <[askingyj@gmail.com](mailto:askingyj%40gmail.com)>
JJ <[jairojair@gmail.com](mailto:jairojair%40gmail.com)>
João Ricardo <[joaoricardo000@gmail.com](mailto:joaoricardo000%40gmail.com)>
Jocelyn Delalande <[jdelalande@oasiswork.fr](mailto:jdelalande%40oasiswork.fr)>
JocelynDelalande <[JocelynDelalande@users.noreply.github.com](mailto:JocelynDelalande%40users.noreply.github.com)>
Joe Jevnik <[JoeJev@gmail.com](mailto:JoeJev%40gmail.com)>
Joe Sanford <[joe@cs.tufts.edu](mailto:joe%40cs.tufts.edu)>
Joe Sanford <[josephsanford@gmail.com](mailto:josephsanford%40gmail.com)>
Joey Wilhelm <[tarkatronic@gmail.com](mailto:tarkatronic%40gmail.com)>
John Anderson <[sontek@gmail.com](mailto:sontek%40gmail.com)>
John Arnold <[johnar@microsoft.com](mailto:johnar%40microsoft.com)>
John Barham <[jbarham@gmail.com](mailto:jbarham%40gmail.com)>
John Watson <[john@dctrwatson.com](mailto:john%40dctrwatson.com)>
John Watson <[john@disqus.com](mailto:john%40disqus.com)>
John Watson <[johnw@mahalo.com](mailto:johnw%40mahalo.com)>
John Whitlock <[John-Whitlock@ieee.org](mailto:John-Whitlock%40ieee.org)>
Jonas Haag <[jonas@lophus.org](mailto:jonas%40lophus.org)>
Jonas Obrist <[me@ojii.ch](mailto:me%40ojii.ch)>
Jonatan Heyman <[jonatan@heyman.info](mailto:jonatan%40heyman.info)>
Jonathan Jordan <[jonathan@metaltoad.com](mailto:jonathan%40metaltoad.com)>
Jonathan Sundqvist <[sundqvist.jonathan@gmail.com](mailto:sundqvist.jonathan%40gmail.com)>
jonathan vanasco <[jonathan@2xlp.com](mailto:jonathan%402xlp.com)>
Jon Chen <[bsd@voltaire.sh](mailto:bsd%40voltaire.sh)>
Jon Dufresne <[jon.dufresne@gmail.com](mailto:jon.dufresne%40gmail.com)>
Josh <[kaizoku@phear.cc](mailto:kaizoku%40phear.cc)>
Josh Kupershmidt <[schmiddy@gmail.com](mailto:schmiddy%40gmail.com)>
Joshua “jag” Ginsberg <[jag@flowtheory.net](mailto:jag%40flowtheory.net)>
Josue Balandrano Coronel <[xirdneh@gmail.com](mailto:xirdneh%40gmail.com)>
Jozef <[knaperek@users.noreply.github.com](mailto:knaperek%40users.noreply.github.com)>
jpellerin <[jpellerin@jpdesk](mailto:jpellerin%40jpdesk).(none)>
jpellerin <[none@none](mailto:none%40none)>
JP <[jpellerin@gmail.com](mailto:jpellerin%40gmail.com)>
JTill <[jtillman@hearsaycorp.com](mailto:jtillman%40hearsaycorp.com)>
Juan Gutierrez <[juanny.gee@gmail.com](mailto:juanny.gee%40gmail.com)>
Juan Ignacio Catalano <[catalanojuan@gmail.com](mailto:catalanojuan%40gmail.com)>
Juan Rossi <[juan@getmango.com](mailto:juan%40getmango.com)>
Juarez Bochi <[jbochi@gmail.com](mailto:jbochi%40gmail.com)>
Jude Nagurney <[jude@pwan.org](mailto:jude%40pwan.org)>
Julien Deniau <[julien@sitioweb.fr](mailto:julien%40sitioweb.fr)>
julienp <[julien@caffeine.lu](mailto:julien%40caffeine.lu)>
Julien Poissonnier <[julien@caffeine.lu](mailto:julien%40caffeine.lu)>
Jun Sakai <[jsakai@splunk.com](mailto:jsakai%40splunk.com)>
Justin Patrin <[jpatrin@skyhighnetworks.com](mailto:jpatrin%40skyhighnetworks.com)>
Justin Patrin <[papercrane@reversefold.com](mailto:papercrane%40reversefold.com)>
Kalle Bronsen <[bronsen@nrrd.de](mailto:bronsen%40nrrd.de)>
kamalgill <[kamalgill@mac.com](mailto:kamalgill%40mac.com)>
Kamil Breguła <[mik-laj@users.noreply.github.com](mailto:mik-laj%40users.noreply.github.com)>
Kanan Rahimov <[mail@kenanbek.me](mailto:mail%40kenanbek.me)>
Kareem Zidane <[kzidane@cs50.harvard.edu](mailto:kzidane%40cs50.harvard.edu)>
Keith Perkins <[keith@tasteoftheworld.us](mailto:keith%40tasteoftheworld.us)>
Ken Fromm <[ken@frommworldwide.com](mailto:ken%40frommworldwide.com)>
Ken Reese <[krrg@users.noreply.github.com](mailto:krrg%40users.noreply.github.com)>
keves <[e@keves.org](mailto:e%40keves.org)>
Kevin Gu <[guqi@reyagroup.com](mailto:guqi%40reyagroup.com)>
Kevin Harvey <[kharvey@axialhealthcare.com](mailto:kharvey%40axialhealthcare.com)>
Kevin McCarthy <[me@kevinmccarthy.org](mailto:me%40kevinmccarthy.org)>
Kevin Richardson <[kevin.f.richardson@gmail.com](mailto:kevin.f.richardson%40gmail.com)>
Kevin Richardson <[kevin@kevinrichardson.co](mailto:kevin%40kevinrichardson.co)>
Kevin Tran <[hekevintran@gmail.com](mailto:hekevintran%40gmail.com)>
Kieran Brownlees <[kbrownlees@users.noreply.github.com](mailto:kbrownlees%40users.noreply.github.com)>
Kirill Pavlov <[pavlov99@yandex.ru](mailto:pavlov99%40yandex.ru)>
Kirill Romanov <[djaler1@gmail.com](mailto:djaler1%40gmail.com)>
komu <[komuw05@gmail.com](mailto:komuw05%40gmail.com)>
Konstantinos Koukopoulos <[koukopoulos@gmail.com](mailto:koukopoulos%40gmail.com)>
Konstantin Podshumok <[kpp.live@gmail.com](mailto:kpp.live%40gmail.com)>
Kornelijus Survila <[kornholijo@gmail.com](mailto:kornholijo%40gmail.com)>
Kouhei Maeda <[mkouhei@gmail.com](mailto:mkouhei%40gmail.com)>
Kracekumar Ramaraju <[me@kracekumar.com](mailto:me%40kracekumar.com)>
Krzysztof Bujniewicz <[k.bujniewicz@bankier.pl](mailto:k.bujniewicz%40bankier.pl)>
kuno <[neokuno@gmail.com](mailto:neokuno%40gmail.com)>
Kxrr <[Hi@Kxrr.Us](mailto:Hi%40Kxrr.Us)>
Kyle Kelley <[rgbkrk@gmail.com](mailto:rgbkrk%40gmail.com)>
Laurent Peuch <[cortex@worlddomination.be](mailto:cortex%40worlddomination.be)>
lead2gold <[caronc@users.noreply.github.com](mailto:caronc%40users.noreply.github.com)>
Leo Dirac <[leo@banyanbranch.com](mailto:leo%40banyanbranch.com)>
Leo Singer <[leo.singer@ligo.org](mailto:leo.singer%40ligo.org)>
Lewis M. Kabui <[lewis.maina@andela.com](mailto:lewis.maina%40andela.com)>
llllllllll <[joejev@gmail.com](mailto:joejev%40gmail.com)>
Locker537 <[Locker537@gmail.com](mailto:Locker537%40gmail.com)>
Loic Bistuer <[loic.bistuer@sixmedia.com](mailto:loic.bistuer%40sixmedia.com)>
Loisaida Sam <[sam.sandberg@gmail.com](mailto:sam.sandberg%40gmail.com)>
lookfwd <[lookfwd@gmail.com](mailto:lookfwd%40gmail.com)>
Loren Abrams <[labrams@hearsaycorp.com](mailto:labrams%40hearsaycorp.com)>
Loren Abrams <[loren.abrams@gmail.com](mailto:loren.abrams%40gmail.com)>
Lucas Wiman <[lucaswiman@counsyl.com](mailto:lucaswiman%40counsyl.com)>
lucio <[lucio@prometeo.spirit.net.ar](mailto:lucio%40prometeo.spirit.net.ar)>
Luis Clara Gomez <[ekkolabs@gmail.com](mailto:ekkolabs%40gmail.com)>
Lukas Linhart <[lukas.linhart@centrumholdings.com](mailto:lukas.linhart%40centrumholdings.com)>
Łukasz Kożuchowski <[lukasz.kozuchowski@10clouds.com](mailto:lukasz.kozuchowski%4010clouds.com)>
Łukasz Langa <[lukasz@langa.pl](mailto:lukasz%40langa.pl)>
Łukasz Oleś <[lukaszoles@gmail.com](mailto:lukaszoles%40gmail.com)>
Luke Burden <[lukeburden@gmail.com](mailto:lukeburden%40gmail.com)>
Luke Hutscal <[luke@creaturecreative.com](mailto:luke%40creaturecreative.com)>
Luke Plant <[L.Plant.98@cantab.net](mailto:L.Plant.98%40cantab.net)>
Luke Pomfrey <[luke.pomfrey@titanemail.com](mailto:luke.pomfrey%40titanemail.com)>
Luke Zapart <[drx@drx.pl](mailto:drx%40drx.pl)>
mabouels <[abouelsaoud@gmail.com](mailto:abouelsaoud%40gmail.com)>
Maciej Obuchowski <[obuchowski.maciej@gmail.com](mailto:obuchowski.maciej%40gmail.com)>
Mads Jensen <[mje@inducks.org](mailto:mje%40inducks.org)>
Manuel Kaufmann <[humitos@gmail.com](mailto:humitos%40gmail.com)>
Manuel Vázquez Acosta <[mvaled@users.noreply.github.com](mailto:mvaled%40users.noreply.github.com)>
Marat Sharafutdinov <[decaz89@gmail.com](mailto:decaz89%40gmail.com)>
Marcelo Da Cruz Pinto <[Marcelo\_DaCruzPinto@McAfee.com](mailto:Marcelo_DaCruzPinto%40McAfee.com)>
Marc Gibbons <[marc\_gibbons@rogers.com](mailto:marc_gibbons%40rogers.com)>
Marc Hörsken <[mback2k@users.noreply.github.com](mailto:mback2k%40users.noreply.github.com)>
Marcin Kuźmiński <[marcin@python-blog.com](mailto:marcin%40python-blog.com)>
marcinkuzminski <[marcin@python-works.com](mailto:marcin%40python-works.com)>
Marcio Ribeiro <[binary@b1n.org](mailto:binary%40b1n.org)>
Marco Buttu <[marco.buttu@gmail.com](mailto:marco.buttu%40gmail.com)>
Marco Schweighauser <[marco@mailrelay.ch](mailto:marco%40mailrelay.ch)>
mariia-zelenova <[32500603+mariia-zelenova@users.noreply.github.com](mailto:32500603+mariia-zelenova%40users.noreply.github.com)>
Marin Atanasov Nikolov <[dnaeon@gmail.com](mailto:dnaeon%40gmail.com)>
Marius Gedminas <[marius@gedmin.as](mailto:marius%40gedmin.as)>
mark hellewell <[mark.hellewell@gmail.com](mailto:mark.hellewell%40gmail.com)>
Mark Lavin <[markdlavin@gmail.com](mailto:markdlavin%40gmail.com)>
Mark Lavin <[mlavin@caktusgroup.com](mailto:mlavin%40caktusgroup.com)>
Mark Parncutt <[me@markparncutt.com](mailto:me%40markparncutt.com)>
Mark Story <[mark@freshbooks.com](mailto:mark%40freshbooks.com)>
Mark Stover <[stovenator@gmail.com](mailto:stovenator%40gmail.com)>
Mark Thurman <[mthurman@gmail.com](mailto:mthurman%40gmail.com)>
Markus Kaiserswerth <[github@sensun.org](mailto:github%40sensun.org)>
Markus Ullmann <[mail@markus-ullmann.de](mailto:mail%40markus-ullmann.de)>
martialp <[martialp@users.noreply.github.com](mailto:martialp%40users.noreply.github.com)>
Martin Davidsson <[martin@dropcam.com](mailto:martin%40dropcam.com)>
Martin Galpin <[m@66laps.com](mailto:m%4066laps.com)>
Martin Melin <[git@martinmelin.com](mailto:git%40martinmelin.com)>
Matt Davis <[matteius@gmail.com](mailto:matteius%40gmail.com)>
Matthew Duggan <[mgithub@guarana.org](mailto:mgithub%40guarana.org)>
Matthew J Morrison <[mattj.morrison@gmail.com](mailto:mattj.morrison%40gmail.com)>
Matthew Miller <[matthewgarrettmiller@gmail.com](mailto:matthewgarrettmiller%40gmail.com)>
Matthew Schinckel <[matt@schinckel.net](mailto:matt%40schinckel.net)>
mattlong <[matt@crocodoc.com](mailto:matt%40crocodoc.com)>
Matt Long <[matt@crocodoc.com](mailto:matt%40crocodoc.com)>
Matt Robenolt <[matt@ydekproductions.com](mailto:matt%40ydekproductions.com)>
Matt Robenolt <[m@robenolt.com](mailto:m%40robenolt.com)>
Matt Williamson <[dawsdesign@gmail.com](mailto:dawsdesign%40gmail.com)>
Matt Williamson <[matt@appdelegateinc.com](mailto:matt%40appdelegateinc.com)>
Matt Wise <[matt@nextdoor.com](mailto:matt%40nextdoor.com)>
Matt Woodyard <[matt@mattwoodyard.com](mailto:matt%40mattwoodyard.com)>
Mauro Rocco <[fireantology@gmail.com](mailto:fireantology%40gmail.com)>
Maxim Bodyansky <[maxim@viking](mailto:maxim%40viking).(none)>
Maxime Beauchemin <[maxime.beauchemin@apache.org](mailto:maxime.beauchemin%40apache.org)>
Maxime Vdb <[mvergerdelbove@work4labs.com](mailto:mvergerdelbove%40work4labs.com)>
Mayflower <[fucongwang@gmail.com](mailto:fucongwang%40gmail.com)>
mbacho <[mbacho@users.noreply.github.com](mailto:mbacho%40users.noreply.github.com)>
mher <[mher.movsisyan@gmail.com](mailto:mher.movsisyan%40gmail.com)>
Mher Movsisyan <[mher.movsisyan@gmail.com](mailto:mher.movsisyan%40gmail.com)>
Michael Aquilina <[michaelaquilina@gmail.com](mailto:michaelaquilina%40gmail.com)>
Michael Duane Mooring <[mikeumus@gmail.com](mailto:mikeumus%40gmail.com)>
Michael Elsdoerfer [michael@elsdoerfer.com](mailto:michael%40elsdoerfer.com) <[michael@puppetmaster](mailto:michael%40puppetmaster).(none)>
Michael Elsdorfer <[michael@elsdoerfer.com](mailto:michael%40elsdoerfer.com)>
Michael Elsdörfer <[michael@elsdoerfer.com](mailto:michael%40elsdoerfer.com)>
Michael Fladischer <[FladischerMichael@fladi.at](mailto:FladischerMichael%40fladi.at)>
Michael Floering <[michaelfloering@gmail.com](mailto:michaelfloering%40gmail.com)>
Michael Howitz <[mh@gocept.com](mailto:mh%40gocept.com)>
michael <[michael@giver.dpool.org](mailto:michael%40giver.dpool.org)>
Michael <[michael-k@users.noreply.github.com](mailto:michael-k%40users.noreply.github.com)>
michael <[michael@puppetmaster](mailto:michael%40puppetmaster).(none)>
Michael Peake <[michaeljpeake@icloud.com](mailto:michaeljpeake%40icloud.com)>
Michael Permana <[michael@origamilogic.com](mailto:michael%40origamilogic.com)>
Michael Permana <[mpermana@hotmail.com](mailto:mpermana%40hotmail.com)>
Michael Robellard <[mikerobellard@onshift.com](mailto:mikerobellard%40onshift.com)>
Michael Robellard <[mrobellard@onshift.com](mailto:mrobellard%40onshift.com)>
Michal Kuffa <[beezz@users.noreply.github.com](mailto:beezz%40users.noreply.github.com)>
Miguel Hernandez Martos <[enlavin@gmail.com](mailto:enlavin%40gmail.com)>
Mike Attwood <[mike@cybersponse.com](mailto:mike%40cybersponse.com)>
Mike Chen <[yi.chen.it@gmail.com](mailto:yi.chen.it%40gmail.com)>
Mike Helmick <[michaelhelmick@users.noreply.github.com](mailto:michaelhelmick%40users.noreply.github.com)>
mikemccabe <[mike@mcca.be](mailto:mike%40mcca.be)>
Mikhail Gusarov <[dottedmag@dottedmag.net](mailto:dottedmag%40dottedmag.net)>
Mikhail Korobov <[kmike84@gmail.com](mailto:kmike84%40gmail.com)>
Mikołaj <[mikolevy1@gmail.com](mailto:mikolevy1%40gmail.com)>
Milen Pavlov <[milen.pavlov@gmail.com](mailto:milen.pavlov%40gmail.com)>
Misha Wolfson <[myw@users.noreply.github.com](mailto:myw%40users.noreply.github.com)>
Mitar <[mitar.github@tnode.com](mailto:mitar.github%40tnode.com)>
Mitar <[mitar@tnode.com](mailto:mitar%40tnode.com)>
Mitchel Humpherys <[mitch.special@gmail.com](mailto:mitch.special%40gmail.com)>
mklauber <[matt+github@mklauber.com](mailto:matt+github%40mklauber.com)>
mlissner <[mlissner@michaeljaylissner.com](mailto:mlissner%40michaeljaylissner.com)>
monkut <[nafein@hotmail.com](mailto:nafein%40hotmail.com)>
Morgan Doocy <[morgan@doocy.net](mailto:morgan%40doocy.net)>
Morris Tweed <[tweed.morris@gmail.com](mailto:tweed.morris%40gmail.com)>
Morton Fox <[github@qslw.com](mailto:github%40qslw.com)>
Môshe van der Sterre <[me@moshe.nl](mailto:me%40moshe.nl)>
Moussa Taifi <[moutai10@gmail.com](mailto:moutai10%40gmail.com)>
mozillazg <[opensource.mozillazg@gmail.com](mailto:opensource.mozillazg%40gmail.com)>
mpavlov <[milen.pavlov@gmail.com](mailto:milen.pavlov%40gmail.com)>
mperice <[mperice@users.noreply.github.com](mailto:mperice%40users.noreply.github.com)>
mrmmm <[mohammad.almeer@gmail.com](mailto:mohammad.almeer%40gmail.com)>
Muneyuki Noguchi <[nogu.dev@gmail.com](mailto:nogu.dev%40gmail.com)>
m-vdb <[mvergerdelbove@work4labs.com](mailto:mvergerdelbove%40work4labs.com)>
nadad <[nadad6@gmail.com](mailto:nadad6%40gmail.com)>
Nathaniel Varona <[nathaniel.varona@gmail.com](mailto:nathaniel.varona%40gmail.com)>
Nathan Van Gheem <[vangheem@gmail.com](mailto:vangheem%40gmail.com)>
Nat Williams <[nat.williams@gmail.com](mailto:nat.williams%40gmail.com)>
Neil Chintomby <[mace033@gmail.com](mailto:mace033%40gmail.com)>
Neil Chintomby <[neil@mochimedia.com](mailto:neil%40mochimedia.com)>
Nicholas Pilon <[npilon@gmail.com](mailto:npilon%40gmail.com)>
nicholsonjf <[nicholsonjf@gmail.com](mailto:nicholsonjf%40gmail.com)>
Nick Eaket <[4418194+neaket360pi@users.noreply.github.com](mailto:4418194+neaket360pi%40users.noreply.github.com)>
Nick Johnson <[njohnson@limcollective.com](mailto:njohnson%40limcollective.com)>
Nicolas Mota <[nicolas\_mota@live.com](mailto:nicolas_mota%40live.com)>
nicolasunravel <[nicolas@unravel.ie](mailto:nicolas%40unravel.ie)>
Niklas Aldergren <[niklas@aldergren.com](mailto:niklas%40aldergren.com)>
Noah Kantrowitz <[noah@coderanger.net](mailto:noah%40coderanger.net)>
Noel Remy <[mocramis@gmail.com](mailto:mocramis%40gmail.com)>
NoKriK <[nokrik@nokrik.net](mailto:nokrik%40nokrik.net)>
Norman Richards <[orb@nostacktrace.com](mailto:orb%40nostacktrace.com)>
NotSqrt <[notsqrt@gmail.com](mailto:notsqrt%40gmail.com)>
nott <[reg@nott.cc](mailto:reg%40nott.cc)>
ocean1 <[ocean1@users.noreply.github.com](mailto:ocean1%40users.noreply.github.com)>
ocean1 <[ocean\_ieee@yahoo.it](mailto:ocean_ieee%40yahoo.it)>
ocean1 <[ocean.kuzuri@gmail.com](mailto:ocean.kuzuri%40gmail.com)>
OddBloke <[daniel.watkins@glassesdirect.com](mailto:daniel.watkins%40glassesdirect.com)>
Oleg Anashkin <[oleg.anashkin@gmail.com](mailto:oleg.anashkin%40gmail.com)>
Olivier Aubert <[contact@olivieraubert.net](mailto:contact%40olivieraubert.net)>
Omar Khan <[omar@omarkhan.me](mailto:omar%40omarkhan.me)>
Omer Katz <[omer.drow@gmail.com](mailto:omer.drow%40gmail.com)>
Omer Korner <[omerkorner@gmail.com](mailto:omerkorner%40gmail.com)>
orarbel <[orarbel@gmail.com](mailto:orarbel%40gmail.com)>
orf <[tom@tomforb.es](mailto:tom%40tomforb.es)>
Ori Hoch <[ori@uumpa.com](mailto:ori%40uumpa.com)>
outself <[yura.nevsky@gmail.com](mailto:yura.nevsky%40gmail.com)>
Pablo Marti <[pmargam@gmail.com](mailto:pmargam%40gmail.com)>
pachewise <[pachewise@users.noreply.github.com](mailto:pachewise%40users.noreply.github.com)>
partizan <[serg.partizan@gmail.com](mailto:serg.partizan%40gmail.com)>
Pär Wieslander <[wieslander@gmail.com](mailto:wieslander%40gmail.com)>
Patrick Altman <[paltman@gmail.com](mailto:paltman%40gmail.com)>
Patrick Cloke <[clokep@users.noreply.github.com](mailto:clokep%40users.noreply.github.com)>
Patrick <[paltman@gmail.com](mailto:paltman%40gmail.com)>
Patrick Stegmann <[code@patrick-stegmann.de](mailto:code%40patrick-stegmann.de)>
Patrick Stegmann <[wonderb0lt@users.noreply.github.com](mailto:wonderb0lt%40users.noreply.github.com)>
Patrick Zhang <[patdujour@gmail.com](mailto:patdujour%40gmail.com)>
Paul English <[paul@onfrst.com](mailto:paul%40onfrst.com)>
Paul Jensen <[pjensen@interactdirect.com](mailto:pjensen%40interactdirect.com)>
Paul Kilgo <[pkilgo@clemson.edu](mailto:pkilgo%40clemson.edu)>
Paul McMillan <[paul.mcmillan@nebula.com](mailto:paul.mcmillan%40nebula.com)>
Paul McMillan <[Paul@McMillan.ws](mailto:Paul%40McMillan.ws)>
Paulo <[PauloPeres@users.noreply.github.com](mailto:PauloPeres%40users.noreply.github.com)>
Paul Pearce <[pearce@cs.berkeley.edu](mailto:pearce%40cs.berkeley.edu)>
Pavel Savchenko <[pavel@modlinltd.com](mailto:pavel%40modlinltd.com)>
Pavlo Kapyshin <[i@93z.org](mailto:i%4093z.org)>
pegler <[pegler@gmail.com](mailto:pegler%40gmail.com)>
Pepijn de Vos <[pepijndevos@gmail.com](mailto:pepijndevos%40gmail.com)>
Peter Bittner <[django@bittner.it](mailto:django%40bittner.it)>
Peter Brook <[peter.d.brook@gmail.com](mailto:peter.d.brook%40gmail.com)>
Philip Garnero <[philip.garnero@corp.ovh.com](mailto:philip.garnero%40corp.ovh.com)>
Pierre Fersing <[pierref@pierref.org](mailto:pierref%40pierref.org)>
Piotr Maślanka <[piotr.maslanka@henrietta.com.pl](mailto:piotr.maslanka%40henrietta.com.pl)>
Piotr Sikora <[piotr.sikora@frickle.com](mailto:piotr.sikora%40frickle.com)>
PMickael <[exploze@gmail.com](mailto:exploze%40gmail.com)>
PMickael <[mickael.penhard@gmail.com](mailto:mickael.penhard%40gmail.com)>
Polina Giralt <[polina.giralt@gmail.com](mailto:polina.giralt%40gmail.com)>
precious <[vs.kulaga@gmail.com](mailto:vs.kulaga%40gmail.com)>
Preston Moore <[prestonkmoore@gmail.com](mailto:prestonkmoore%40gmail.com)>
Primož Kerin <[kerin.primoz@gmail.com](mailto:kerin.primoz%40gmail.com)>
Pysaoke <[pysaoke@gmail.com](mailto:pysaoke%40gmail.com)>
Rachel Johnson <[racheljohnson457@gmail.com](mailto:racheljohnson457%40gmail.com)>
Rachel Willmer <[rachel@willmer.org](mailto:rachel%40willmer.org)>
raducc <[raducc@users.noreply.github.com](mailto:raducc%40users.noreply.github.com)>
Raf Geens <[rafgeens@gmail.com](mailto:rafgeens%40gmail.com)>
Raghuram Srinivasan <[raghu@set.tv](mailto:raghu%40set.tv)>
Raphaël Riel <[raphael.riel@gmail.com](mailto:raphael.riel%40gmail.com)>
Raphaël Slinckx <[rslinckx@gmail.com](mailto:rslinckx%40gmail.com)>
Régis B <[github@behmo.com](mailto:github%40behmo.com)>
Remigiusz Modrzejewski <[lrem@maxnet.org.pl](mailto:lrem%40maxnet.org.pl)>
Rémi Marenco <[remi.marenco@gmail.com](mailto:remi.marenco%40gmail.com)>
rfkrocktk <[rfkrocktk@gmail.com](mailto:rfkrocktk%40gmail.com)>
Rick van Hattem <[rick.van.hattem@fawo.nl](mailto:rick.van.hattem%40fawo.nl)>
Rick Wargo <[rickwargo@users.noreply.github.com](mailto:rickwargo%40users.noreply.github.com)>
Rico Moorman <[rico.moorman@gmail.com](mailto:rico.moorman%40gmail.com)>
Rik <[gitaarik@gmail.com](mailto:gitaarik%40gmail.com)>
Rinat Shigapov <[rinatshigapov@gmail.com](mailto:rinatshigapov%40gmail.com)>
Riyad Parvez <[social.riyad@gmail.com](mailto:social.riyad%40gmail.com)>
rlotun <[rlotun@gmail.com](mailto:rlotun%40gmail.com)>
rnoel <[rnoel@ltutech.com](mailto:rnoel%40ltutech.com)>
Robert Knight <[robertknight@gmail.com](mailto:robertknight%40gmail.com)>
Roberto Gaiser <[gaiser@geekbunker.org](mailto:gaiser%40geekbunker.org)>
roderick <[mail@roderick.de](mailto:mail%40roderick.de)>
Rodolphe Quiedeville <[rodolphe@quiedeville.org](mailto:rodolphe%40quiedeville.org)>
Roger Hu <[rhu@hearsaycorp.com](mailto:rhu%40hearsaycorp.com)>
Roger Hu <[roger.hu@gmail.com](mailto:roger.hu%40gmail.com)>
Roman Imankulov <[roman@netangels.ru](mailto:roman%40netangels.ru)>
Roman Sichny <[roman@sichnyi.com](mailto:roman%40sichnyi.com)>
Romuald Brunet <[romuald@gandi.net](mailto:romuald%40gandi.net)>
Ronan Amicel <[ronan.amicel@gmail.com](mailto:ronan.amicel%40gmail.com)>
Ross Deane <[ross.deane@gmail.com](mailto:ross.deane%40gmail.com)>
Ross Lawley <[ross.lawley@gmail.com](mailto:ross.lawley%40gmail.com)>
Ross Patterson <[me@rpatterson.net](mailto:me%40rpatterson.net)>
Ross <[ross@duedil.com](mailto:ross%40duedil.com)>
Rudy Attias <[rudy.attias@gmail.com](mailto:rudy.attias%40gmail.com)>
rumyana neykova <[rumi.neykova@gmail.com](mailto:rumi.neykova%40gmail.com)>
Rumyana Neykova <[rumi.neykova@gmail.com](mailto:rumi.neykova%40gmail.com)>
Rune Halvorsen <[runefh@gmail.com](mailto:runefh%40gmail.com)>
Rune Halvorsen <[runeh@vorkosigan](mailto:runeh%40vorkosigan).(none)>
runeh <[runeh@vorkosigan](mailto:runeh%40vorkosigan).(none)>
Russell Keith-Magee <[russell@keith-magee.com](mailto:russell%40keith-magee.com)>
Ryan Guest <[ryanguest@gmail.com](mailto:ryanguest%40gmail.com)>
Ryan Hiebert <[ryan@ryanhiebert.com](mailto:ryan%40ryanhiebert.com)>
Ryan Kelly <[rkelly@truveris.com](mailto:rkelly%40truveris.com)>
Ryan Luckie <[rtluckie@gmail.com](mailto:rtluckie%40gmail.com)>
Ryan Petrello <[lists@ryanpetrello.com](mailto:lists%40ryanpetrello.com)>
Ryan P. Kelly <[rpkelly@cpan.org](mailto:rpkelly%40cpan.org)>
Ryan P Kilby <[rpkilby@ncsu.edu](mailto:rpkilby%40ncsu.edu)>
Salvatore Rinchiera <[srinchiera@college.harvard.edu](mailto:srinchiera%40college.harvard.edu)>
Sam Cooke <[sam@mixcloud.com](mailto:sam%40mixcloud.com)>
samjy <[sam+git@samjy.com](mailto:sam+git%40samjy.com)>
Sammie S. Taunton <[diemuzi@gmail.com](mailto:diemuzi%40gmail.com)>
Samuel Dion-Girardeau <[samueldg@users.noreply.github.com](mailto:samueldg%40users.noreply.github.com)>
Samuel Dion-Girardeau <[samuel.diongirardeau@gmail.com](mailto:samuel.diongirardeau%40gmail.com)>
Samuel GIFFARD <[samuel@giffard.co](mailto:samuel%40giffard.co)>
Scott Cooper <[scttcper@gmail.com](mailto:scttcper%40gmail.com)>
screeley <[screeley@screeley-laptop](mailto:screeley%40screeley-laptop).(none)>
sdcooke <[sam@mixcloud.com](mailto:sam%40mixcloud.com)>
Sean O’Connor <[sean@seanoc.com](mailto:sean%40seanoc.com)>
Sean Wang <[seanw@patreon.com](mailto:seanw%40patreon.com)>
Sebastian Kalinowski <[sebastian@kalinowski.eu](mailto:sebastian%40kalinowski.eu)>
Sébastien Fievet <[zyegfryed@gmail.com](mailto:zyegfryed%40gmail.com)>
Seong Won Mun <[longfinfunnel@gmail.com](mailto:longfinfunnel%40gmail.com)>
Sergey Fursov <[GeyseR85@gmail.com](mailto:GeyseR85%40gmail.com)>
Sergey Tikhonov <[zimbler@gmail.com](mailto:zimbler%40gmail.com)>
Sergi Almacellas Abellana <[sergi@koolpi.com](mailto:sergi%40koolpi.com)>
Sergio Fernandez <[ElAutoestopista@users.noreply.github.com](mailto:ElAutoestopista%40users.noreply.github.com)>
Seungha Kim <[seungha.dev@gmail.com](mailto:seungha.dev%40gmail.com)>
shalev67 <[shalev67@gmail.com](mailto:shalev67%40gmail.com)>
Shitikanth <[golu3990@gmail.com](mailto:golu3990%40gmail.com)>
Silas Sewell <[silas@sewell.org](mailto:silas%40sewell.org)>
Simon Charette <[charette.s@gmail.com](mailto:charette.s%40gmail.com)>
Simon Engledew <[simon@engledew.com](mailto:simon%40engledew.com)>
Simon Josi <[simon.josi@atizo.com](mailto:simon.josi%40atizo.com)>
Simon Legner <[Simon.Legner@gmail.com](mailto:Simon.Legner%40gmail.com)>
Simon Peeters <[peeters.simon@gmail.com](mailto:peeters.simon%40gmail.com)>
Simon Schmidt <[schmidt.simon@gmail.com](mailto:schmidt.simon%40gmail.com)>
skovorodkin <[sergey@skovorodkin.com](mailto:sergey%40skovorodkin.com)>
Slam <[3lnc.slam@gmail.com](mailto:3lnc.slam%40gmail.com)>
Smirl <[smirlie@googlemail.com](mailto:smirlie%40googlemail.com)>
squfrans <[frans@squla.com](mailto:frans%40squla.com)>
Srinivas Garlapati <[srinivasa.b.garlapati@gmail.com](mailto:srinivasa.b.garlapati%40gmail.com)>
Stas Rudakou <[stas@garage22.net](mailto:stas%40garage22.net)>
Static <[staticfox@staticfox.net](mailto:staticfox%40staticfox.net)>
Steeve Morin <[steeve.morin@gmail.com](mailto:steeve.morin%40gmail.com)>
Stefan hr Berder <[stefan.berder@ledapei.com](mailto:stefan.berder%40ledapei.com)>
Stefan Kjartansson <[esteban.supreme@gmail.com](mailto:esteban.supreme%40gmail.com)>
Steffen Allner <[sa@gocept.com](mailto:sa%40gocept.com)>
Stephen Weber <[mordel@gmail.com](mailto:mordel%40gmail.com)>
Steven Johns <[duoi@users.noreply.github.com](mailto:duoi%40users.noreply.github.com)>
Steven Parker <[voodoonofx@gmail.com](mailto:voodoonofx%40gmail.com)>
Steven <[rh0dium@users.noreply.github.com](mailto:rh0dium%40users.noreply.github.com)>
Steven Sklar <[steve@predata.com](mailto:steve%40predata.com)>
Steven Skoczen <[steven@aquameta.com](mailto:steven%40aquameta.com)>
Steven Skoczen <[steven@quantumimagery.com](mailto:steven%40quantumimagery.com)>
Steve Peak <[steve@stevepeak.net](mailto:steve%40stevepeak.net)>
stipa <[stipa@debian.local.local](mailto:stipa%40debian.local.local)>
sukrit007 <[sukrit007@gmail.com](mailto:sukrit007%40gmail.com)>
Sukrit Khera <[sukrit007@gmail.com](mailto:sukrit007%40gmail.com)>
Sundar Raman <[cybertoast@gmail.com](mailto:cybertoast%40gmail.com)>
sunfinite <[sunfinite@gmail.com](mailto:sunfinite%40gmail.com)>
sww <[sww@users.noreply.github.com](mailto:sww%40users.noreply.github.com)>
Tadej Janež <[tadej.janez@tadej.hicsalta.si](mailto:tadej.janez%40tadej.hicsalta.si)>
Taha Jahangir <[mtjahangir@gmail.com](mailto:mtjahangir%40gmail.com)>
Takeshi Kanemoto <[tak.kanemoto@gmail.com](mailto:tak.kanemoto%40gmail.com)>
TakesxiSximada <[takesxi.sximada@gmail.com](mailto:takesxi.sximada%40gmail.com)>
Tamer Sherif <[tamer.sherif@flyingelephantlab.com](mailto:tamer.sherif%40flyingelephantlab.com)>
Tao Qingyun <[845767657@qq.com](mailto:845767657%40qq.com)>
Tarun Bhardwaj <[mailme@tarunbhardwaj.com](mailto:mailme%40tarunbhardwaj.com)>
Tayfun Sen <[tayfun.sen@markafoni.com](mailto:tayfun.sen%40markafoni.com)>
Tayfun Sen <[tayfun.sen@skyscanner.net](mailto:tayfun.sen%40skyscanner.net)>
Tayfun Sen <[totayfun@gmail.com](mailto:totayfun%40gmail.com)>
tayfun <[tayfun.sen@markafoni.com](mailto:tayfun.sen%40markafoni.com)>
Taylor C. Richberger <[taywee@gmx.com](mailto:taywee%40gmx.com)>
taylornelson <[taylor@sourcedna.com](mailto:taylor%40sourcedna.com)>
Theodore Dubois <[tbodt@users.noreply.github.com](mailto:tbodt%40users.noreply.github.com)>
Theo Spears <[github@theos.me.uk](mailto:github%40theos.me.uk)>
Thierry RAMORASOAVINA <[thierry.ramorasoavina@orange.com](mailto:thierry.ramorasoavina%40orange.com)>
Thijs Triemstra <[info@collab.nl](mailto:info%40collab.nl)>
Thomas French <[thomas@sandtable.com](mailto:thomas%40sandtable.com)>
Thomas Grainger <[tagrain@gmail.com](mailto:tagrain%40gmail.com)>
Thomas Johansson <[prencher@prencher.dk](mailto:prencher%40prencher.dk)>
Thomas Meson <[zllak@hycik.org](mailto:zllak%40hycik.org)>
Thomas Minor <[sxeraverx@gmail.com](mailto:sxeraverx%40gmail.com)>
Thomas Wright <[tom.tdw@gmail.com](mailto:tom.tdw%40gmail.com)>
Timo Sugliani <[timo.sugliani@gmail.com](mailto:timo.sugliani%40gmail.com)>
Timo Sugliani <[tsugliani@tsugliani-desktop](mailto:tsugliani%40tsugliani-desktop).(none)>
Titusz <[tp@py7.de](mailto:tp%40py7.de)>
tnir <[tnir@users.noreply.github.com](mailto:tnir%40users.noreply.github.com)>
Tobias Kunze <[rixx@cutebit.de](mailto:rixx%40cutebit.de)>
Tocho Tochev <[tocho@tochev.net](mailto:tocho%40tochev.net)>
Tomas Machalek <[tomas.machalek@gmail.com](mailto:tomas.machalek%40gmail.com)>
Tomasz Święcicki <[tomislater@gmail.com](mailto:tomislater%40gmail.com)>
Tom ‘Biwaa’ Riat <[riat.tom@gmail.com](mailto:riat.tom%40gmail.com)>
Tomek Święcicki <[tomislater@gmail.com](mailto:tomislater%40gmail.com)>
Tom S <[scytale@gmail.com](mailto:scytale%40gmail.com)>
tothegump <[tothegump@gmail.com](mailto:tothegump%40gmail.com)>
Travis Swicegood <[development@domain51.com](mailto:development%40domain51.com)>
Travis Swicegood <[travis@domain51.com](mailto:travis%40domain51.com)>
Travis <[treeder@gmail.com](mailto:treeder%40gmail.com)>
Trevor Skaggs <[skaggs.trevor@gmail.com](mailto:skaggs.trevor%40gmail.com)>
Ujjwal Ojha <[ojhaujjwal@users.noreply.github.com](mailto:ojhaujjwal%40users.noreply.github.com)>
unknown <Jonatan@.(none)>
Valentyn Klindukh <[vklindukh@cogniance.com](mailto:vklindukh%40cogniance.com)>
Viktor Holmqvist <[viktorholmqvist@gmail.com](mailto:viktorholmqvist%40gmail.com)>
Vincent Barbaresi <[vbarbaresi@users.noreply.github.com](mailto:vbarbaresi%40users.noreply.github.com)>
Vincent Driessen <[vincent@datafox.nl](mailto:vincent%40datafox.nl)>
Vinod Chandru <[vinod.chandru@gmail.com](mailto:vinod.chandru%40gmail.com)>
Viraj <[vnavkal0@gmail.com](mailto:vnavkal0%40gmail.com)>
Vitaly Babiy <[vbabiy86@gmail.com](mailto:vbabiy86%40gmail.com)>
Vitaly <[olevinsky.v.s@gmail.com](mailto:olevinsky.v.s%40gmail.com)>
Vivek Anand <[vivekanand1101@users.noreply.github.com](mailto:vivekanand1101%40users.noreply.github.com)>
Vlad <[frolvlad@gmail.com](mailto:frolvlad%40gmail.com)>
Vladimir Gorbunov <[vsg@suburban.me](mailto:vsg%40suburban.me)>
Vladimir Kryachko <[v.kryachko@gmail.com](mailto:v.kryachko%40gmail.com)>
Vladimir Rutsky <[iamironbob@gmail.com](mailto:iamironbob%40gmail.com)>
Vladislav Stepanov <[8uk.8ak@gmail.com](mailto:8uk.8ak%40gmail.com)>
Vsevolod <[Vsevolod@zojax.com](mailto:Vsevolod%40zojax.com)>
Wes Turner <[wes.turner@gmail.com](mailto:wes.turner%40gmail.com)>
wes <[wes@policystat.com](mailto:wes%40policystat.com)>
Wes Winham <[winhamwr@gmail.com](mailto:winhamwr%40gmail.com)>
w- <[github@wangsanata.com](mailto:github%40wangsanata.com)>
whendrik <[whendrik@gmail.com](mailto:whendrik%40gmail.com)>
Wido den Hollander <[wido@widodh.nl](mailto:wido%40widodh.nl)>
Wieland Hoffmann <[mineo@users.noreply.github.com](mailto:mineo%40users.noreply.github.com)>
Wiliam Souza <[wiliamsouza83@gmail.com](mailto:wiliamsouza83%40gmail.com)>
Wil Langford <[wil.langford+github@gmail.com](mailto:wil.langford+github%40gmail.com)>
William King <[willtrking@gmail.com](mailto:willtrking%40gmail.com)>
Will <[paradox41@users.noreply.github.com](mailto:paradox41%40users.noreply.github.com)>
Will Thompson <[will@willthompson.co.uk](mailto:will%40willthompson.co.uk)>
winhamwr <[winhamwr@gmail.com](mailto:winhamwr%40gmail.com)>
Wojciech Żywno <[w.zywno@gmail.com](mailto:w.zywno%40gmail.com)>
W. Trevor King <[wking@tremily.us](mailto:wking%40tremily.us)>
wyc <[wayne@neverfear.org](mailto:wayne%40neverfear.org)>
wyc <[wyc@fastmail.fm](mailto:wyc%40fastmail.fm)>
xando <[sebastian.pawlus@gmail.com](mailto:sebastian.pawlus%40gmail.com)>
Xavier Damman <[xdamman@gmail.com](mailto:xdamman%40gmail.com)>
Xavier Hardy <[xavierhardy@users.noreply.github.com](mailto:xavierhardy%40users.noreply.github.com)>
Xavier Ordoquy <[xordoquy@linovia.com](mailto:xordoquy%40linovia.com)>
xin li <[xin.shli@ele.me](mailto:xin.shli%40ele.me)>
xray7224 <[xray7224@googlemail.com](mailto:xray7224%40googlemail.com)>
y0ngdi <[36658095+y0ngdi@users.noreply.github.com](mailto:36658095+y0ngdi%40users.noreply.github.com)>
Yan Kalchevskiy <[yan.kalchevskiy@gmail.com](mailto:yan.kalchevskiy%40gmail.com)>
Yohann Rebattu <[yohann@rebattu.fr](mailto:yohann%40rebattu.fr)>
Yoichi NAKAYAMA <[yoichi.nakayama@gmail.com](mailto:yoichi.nakayama%40gmail.com)>
Yuhannaa <[yuhannaa@gmail.com](mailto:yuhannaa%40gmail.com)>
YuLun Shih <[shih@yulun.me](mailto:shih%40yulun.me)>
Yury V. Zaytsev <[yury@shurup.com](mailto:yury%40shurup.com)>
Yuval Greenfield <[ubershmekel@gmail.com](mailto:ubershmekel%40gmail.com)>
Zach Smith <[zmsmith27@gmail.com](mailto:zmsmith27%40gmail.com)>
Zhang Chi <[clvrobj@gmail.com](mailto:clvrobj%40gmail.com)>
Zhaorong Ma <[mazhaorong@gmail.com](mailto:mazhaorong%40gmail.com)>
Zoran Pavlovic <[xcepticzoki@gmail.com](mailto:xcepticzoki%40gmail.com)>
ztlpn <[mvzp10@gmail.com](mailto:mvzp10%40gmail.com)>
何翔宇(Sean Ho) <[h1x2y3awalm@gmail.com](mailto:h1x2y3awalm%40gmail.com)>
許邱翔 <[wdv4758h@gmail.com](mailto:wdv4758h%40gmail.com)>

Note

This wall was automatically generated from git history,
so sadly it doesn’t not include the people who help with more important
things like answering mailing-list questions.

## 

### 

The supported Python Versions are:

- CPython 2.7
- CPython 3.4
- CPython 3.5
- CPython 3.6
- PyPy 5.8 (`pypy2`)

## 

### 

#### New Redis Sentinel Results Backend

Redis Sentinel provides high availability for Redis.
A new result backend supporting it was added.

#### Cassandra Results Backend

A new cassandra\_options configuration option was introduced in order to configure
the cassandra client.

See [Cassandra/AstraDB backend settings](../userguide/configuration.html#conf-cassandra-result-backend) for more information.

#### DynamoDB Results Backend

A new dynamodb\_endpoint\_url configuration option was introduced in order
to point the result backend to a local endpoint during development or testing.

See [AWS DynamoDB backend settings](../userguide/configuration.html#conf-dynamodb-result-backend) for more information.

#### Python 2/3 Compatibility Fixes

Both the CouchDB and the Consul result backends accepted byte strings without decoding them to Unicode first.
This is now no longer the case.

### 

Multiple bugs were resolved resulting in a much smoother experience when using Canvas.

### 

#### Bound Tasks as Error Callbacks

We fixed a regression that occurred when bound tasks are used as error callbacks.
This used to work in Celery 3.x but raised an exception in 4.x until this release.

In both 4.0 and 4.1 the following code wouldn’t work:

```
@app.task(name="raise_exception", bind=True)
def raise_exception(self):
    raise Exception("Bad things happened")

@app.task(name="handle_task_exception", bind=True)
def handle_task_exception(self):
    print("Exception detected")

subtask = raise_exception.subtask()

subtask.apply_async(link_error=handle_task_exception.s())
```

#### Task Representation

- Shadowing task names now works as expected.
  The shadowed name is properly presented in flower, the logs and the traces.
- argsrepr and kwargsrepr were previously not used even if specified.
  They now work as expected. See [Hiding sensitive information in arguments](../userguide/tasks.html#task-hiding-sensitive-information) for more information.

#### Custom Requests

We now allow tasks to use custom [`request`](../reference/celery.worker.request.html#celery.worker.request.Request "celery.worker.request.Request") classes
for custom task classes.

See [Requests and custom requests](../userguide/tasks.html#task-requests-and-custom-requests) for more information.

#### Retries with Exponential Backoff

Retries can now be performed with exponential backoffs to avoid overwhelming
external services with requests.

See [Automatic retry for known exceptions](../userguide/tasks.html#task-autoretry) for more information.

### 

Tasks were supposed to be automatically documented when using Sphinx’s Autodoc was used.
The code that would have allowed automatic documentation had a few bugs which are now fixed.

Also, The extension is now documented properly. See [Documenting Tasks with Sphinx](../userguide/sphinx.html#sphinx) for more information.