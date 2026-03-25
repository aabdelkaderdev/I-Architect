<!-- Source: https://docs.celeryq.dev/en/main/history/whatsnew-4.1.html -->

This document describes the current stable version of Celery (5.6).
For development docs,
[go here](https://docs.celeryq.dev/en/main/history/whatsnew-4.1.html).

# What’s new in Celery 4.1 (latentcall)

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

The 4.1.0 release continues to improve our efforts to provide you with
the best task execution platform for Python.

This release is mainly a bug fix release, ironing out some issues and regressions
found in Celery 4.0.0.

We added official support for Python 3.6 and PyPy 5.8.0.

This is the first time we release without Ask Solem as an active contributor.
We’d like to thank him for his hard work in creating and maintaining Celery over the years.

Since Ask Solem was not involved there were a few kinks in the release process
which we promise to resolve in the next release.
This document was missing when we did release Celery 4.1.0.
Also, we did not update the release codename as we should have.
We apologize for the inconvenience.

For the time being, I, Omer Katz will be the release manager.

Thank you for your support!

*— Omer Katz*

### 

Acey <[huiwang.e@gmail.com](mailto:huiwang.e%40gmail.com)>
Acey9 <[huiwang.e@gmail.com](mailto:huiwang.e%40gmail.com)>
Alan Hamlett <[alanhamlett@users.noreply.github.com](mailto:alanhamlett%40users.noreply.github.com)>
Alan Justino da Silva <[alan.justino@yahoo.com.br](mailto:alan.justino%40yahoo.com.br)>
Alejandro Pernin <[ale.pernin@gmail.com](mailto:ale.pernin%40gmail.com)>
Alli <[alzeih@users.noreply.github.com](mailto:alzeih%40users.noreply.github.com)>
Andreas Pelme <[andreas@pelme.se](mailto:andreas%40pelme.se)>
Andrew de Quincey <[adq@lidskialf.net](mailto:adq%40lidskialf.net)>
Anthony Lukach <[anthonylukach@gmail.com](mailto:anthonylukach%40gmail.com)>
Arcadiy Ivanov <[arcadiy@ivanov.biz](mailto:arcadiy%40ivanov.biz)>
Arnaud Rocher <[cailloumajor@users.noreply.github.com](mailto:cailloumajor%40users.noreply.github.com)>
Arthur Vigil <[ahvigil@mail.sfsu.edu](mailto:ahvigil%40mail.sfsu.edu)>
Asif Saifuddin Auvi <[auvipy@users.noreply.github.com](mailto:auvipy%40users.noreply.github.com)>
Ask Solem <[ask@celeryproject.org](mailto:ask%40celeryproject.org)>
BLAGA Razvan-Paul <[razvan.paul.blaga@gmail.com](mailto:razvan.paul.blaga%40gmail.com)>
Brendan MacDonell <[macdonellba@gmail.com](mailto:macdonellba%40gmail.com)>
Brian Luan <[jznight@gmail.com](mailto:jznight%40gmail.com)>
Brian May <[brian@linuxpenguins.xyz](mailto:brian%40linuxpenguins.xyz)>
Bruno Alla <[browniebroke@users.noreply.github.com](mailto:browniebroke%40users.noreply.github.com)>
Chris Kuehl <[chris@techxonline.net](mailto:chris%40techxonline.net)>
Christian <[github@penpal4u.net](mailto:github%40penpal4u.net)>
Christopher Hoskin <[mans0954@users.noreply.github.com](mailto:mans0954%40users.noreply.github.com)>
Daniel Hahler <[github@thequod.de](mailto:github%40thequod.de)>
Daniel Huang <[dxhuang@gmail.com](mailto:dxhuang%40gmail.com)>
Derek Harland <[donkopotamus@users.noreply.github.com](mailto:donkopotamus%40users.noreply.github.com)>
Dmytro Petruk <[bavaria95@gmail.com](mailto:bavaria95%40gmail.com)>
Ed Morley <[edmorley@users.noreply.github.com](mailto:edmorley%40users.noreply.github.com)>
Eric Poelke <[epoelke@gmail.com](mailto:epoelke%40gmail.com)>
Felipe <[fcoelho@users.noreply.github.com](mailto:fcoelho%40users.noreply.github.com)>
François Voron <[fvoron@gmail.com](mailto:fvoron%40gmail.com)>
GDR! <[gdr@gdr.name](mailto:gdr%40gdr.name)>
George Psarakis <[giwrgos.psarakis@gmail.com](mailto:giwrgos.psarakis%40gmail.com)>
J Alan Brogan <[jalanb@users.noreply.github.com](mailto:jalanb%40users.noreply.github.com)>
James Michael DuPont <[JamesMikeDuPont@gmail.com](mailto:JamesMikeDuPont%40gmail.com)>
Jamie Alessio <[jamie@stoic.net](mailto:jamie%40stoic.net)>
Javier Domingo Cansino <[javierdo1@gmail.com](mailto:javierdo1%40gmail.com)>
Jay McGrath <[jaymcgrath@users.noreply.github.com](mailto:jaymcgrath%40users.noreply.github.com)>
Jian Yu <[askingyj@gmail.com](mailto:askingyj%40gmail.com)>
Joey Wilhelm <[tarkatronic@gmail.com](mailto:tarkatronic%40gmail.com)>
Jon Dufresne <[jon.dufresne@gmail.com](mailto:jon.dufresne%40gmail.com)>
Kalle Bronsen <[bronsen@nrrd.de](mailto:bronsen%40nrrd.de)>
Kirill Romanov <[djaler1@gmail.com](mailto:djaler1%40gmail.com)>
Laurent Peuch <[cortex@worlddomination.be](mailto:cortex%40worlddomination.be)>
Luke Plant <[L.Plant.98@cantab.net](mailto:L.Plant.98%40cantab.net)>
Marat Sharafutdinov <[decaz89@gmail.com](mailto:decaz89%40gmail.com)>
Marc Gibbons <[marc\_gibbons@rogers.com](mailto:marc_gibbons%40rogers.com)>
Marc Hörsken <[mback2k@users.noreply.github.com](mailto:mback2k%40users.noreply.github.com)>
Michael <[michael-k@users.noreply.github.com](mailto:michael-k%40users.noreply.github.com)>
Michael Howitz <[mh@gocept.com](mailto:mh%40gocept.com)>
Michal Kuffa <[beezz@users.noreply.github.com](mailto:beezz%40users.noreply.github.com)>
Mike Chen <[yi.chen.it@gmail.com](mailto:yi.chen.it%40gmail.com)>
Mike Helmick <[michaelhelmick@users.noreply.github.com](mailto:michaelhelmick%40users.noreply.github.com)>
Morgan Doocy <[morgan@doocy.net](mailto:morgan%40doocy.net)>
Moussa Taifi <[moutai10@gmail.com](mailto:moutai10%40gmail.com)>
Omer Katz <[omer.drow@gmail.com](mailto:omer.drow%40gmail.com)>
Patrick Cloke <[clokep@users.noreply.github.com](mailto:clokep%40users.noreply.github.com)>
Peter Bittner <[django@bittner.it](mailto:django%40bittner.it)>
Preston Moore <[prestonkmoore@gmail.com](mailto:prestonkmoore%40gmail.com)>
Primož Kerin <[kerin.primoz@gmail.com](mailto:kerin.primoz%40gmail.com)>
Pysaoke <[pysaoke@gmail.com](mailto:pysaoke%40gmail.com)>
Rick Wargo <[rickwargo@users.noreply.github.com](mailto:rickwargo%40users.noreply.github.com)>
Rico Moorman <[rico.moorman@gmail.com](mailto:rico.moorman%40gmail.com)>
Roman Sichny <[roman@sichnyi.com](mailto:roman%40sichnyi.com)>
Ross Patterson <[me@rpatterson.net](mailto:me%40rpatterson.net)>
Ryan Hiebert <[ryan@ryanhiebert.com](mailto:ryan%40ryanhiebert.com)>
Rémi Marenco <[remi.marenco@gmail.com](mailto:remi.marenco%40gmail.com)>
Salvatore Rinchiera <[srinchiera@college.harvard.edu](mailto:srinchiera%40college.harvard.edu)>
Samuel Dion-Girardeau <[samuel.diongirardeau@gmail.com](mailto:samuel.diongirardeau%40gmail.com)>
Sergey Fursov <[GeyseR85@gmail.com](mailto:GeyseR85%40gmail.com)>
Simon Legner <[Simon.Legner@gmail.com](mailto:Simon.Legner%40gmail.com)>
Simon Schmidt <[schmidt.simon@gmail.com](mailto:schmidt.simon%40gmail.com)>
Slam <[3lnc.slam@gmail.com](mailto:3lnc.slam%40gmail.com)>
Static <[staticfox@staticfox.net](mailto:staticfox%40staticfox.net)>
Steffen Allner <[sa@gocept.com](mailto:sa%40gocept.com)>
Steven <[rh0dium@users.noreply.github.com](mailto:rh0dium%40users.noreply.github.com)>
Steven Johns <[duoi@users.noreply.github.com](mailto:duoi%40users.noreply.github.com)>
Tamer Sherif <[tamer.sherif@flyingelephantlab.com](mailto:tamer.sherif%40flyingelephantlab.com)>
Tao Qingyun <[845767657@qq.com](mailto:845767657%40qq.com)>
Tayfun Sen <[totayfun@gmail.com](mailto:totayfun%40gmail.com)>
Taylor C. Richberger <[taywee@gmx.com](mailto:taywee%40gmx.com)>
Thierry RAMORASOAVINA <[thierry.ramorasoavina@orange.com](mailto:thierry.ramorasoavina%40orange.com)>
Tom ‘Biwaa’ Riat <[riat.tom@gmail.com](mailto:riat.tom%40gmail.com)>
Viktor Holmqvist <[viktorholmqvist@gmail.com](mailto:viktorholmqvist%40gmail.com)>
Viraj <[vnavkal0@gmail.com](mailto:vnavkal0%40gmail.com)>
Vivek Anand <[vivekanand1101@users.noreply.github.com](mailto:vivekanand1101%40users.noreply.github.com)>
Will <[paradox41@users.noreply.github.com](mailto:paradox41%40users.noreply.github.com)>
Wojciech Żywno <[w.zywno@gmail.com](mailto:w.zywno%40gmail.com)>
Yoichi NAKAYAMA <[yoichi.nakayama@gmail.com](mailto:yoichi.nakayama%40gmail.com)>
YuLun Shih <[shih@yulun.me](mailto:shih%40yulun.me)>
Yuhannaa <[yuhannaa@gmail.com](mailto:yuhannaa%40gmail.com)>
abhinav nilaratna <[anilaratna2@bloomberg.net](mailto:anilaratna2%40bloomberg.net)>
aydin <[adigeaydin@gmail.com](mailto:adigeaydin%40gmail.com)>
csfeathers <[csfeathers@users.noreply.github.com](mailto:csfeathers%40users.noreply.github.com)>
georgepsarakis <[giwrgos.psarakis@gmail.com](mailto:giwrgos.psarakis%40gmail.com)>
orf <[tom@tomforb.es](mailto:tom%40tomforb.es)>
shalev67 <[shalev67@gmail.com](mailto:shalev67%40gmail.com)>
sww <[sww@users.noreply.github.com](mailto:sww%40users.noreply.github.com)>
tnir <[tnir@users.noreply.github.com](mailto:tnir%40users.noreply.github.com)>
何翔宇(Sean Ho) <[h1x2y3awalm@gmail.com](mailto:h1x2y3awalm%40gmail.com)>

Note

This wall was automatically generated from git history,
so sadly it doesn’t not include the people who help with more important
things like answering mailing-list questions.

## 

### 

We now run our unit test suite and integration test suite on Python 3.6.x
and PyPy 5.8.0.

We expect newer versions of PyPy to work but unfortunately we do not have the
resources to test PyPy with those versions.

The supported Python Versions are:

- CPython 2.7
- CPython 3.4
- CPython 3.5
- CPython 3.6
- PyPy 5.8 (`pypy2`)

## 

### 

#### New DynamoDB Results Backend

We added a new results backend for those of you who are using DynamoDB.

If you are interested in using this results backend, refer to [AWS DynamoDB backend settings](../userguide/configuration.html#conf-dynamodb-result-backend) for more information.

#### Elasticsearch

The Elasticsearch results backend is now more robust and configurable.

See [Elasticsearch backend settings](../userguide/configuration.html#conf-elasticsearch-result-backend) for more information
about the new configuration options.

#### Redis

The Redis results backend can now use TLS to encrypt the communication with the
Redis database server.

See [Redis backend settings](../userguide/configuration.html#conf-redis-result-backend).

#### MongoDB

The MongoDB results backend can now handle binary-encoded task results.

This was a regression from 4.0.0 which resulted in a problem using serializers
such as MsgPack or Pickle in conjunction with the MongoDB results backend.

### 

The task schedule now updates automatically when new tasks are added.
Now if you use the Django database scheduler, you can add and remove tasks from the schedule without restarting Celery beat.

### 

The `disable_sync_subtasks` argument was added to allow users to override disabling
synchronous subtasks.

See [Avoid launching synchronous subtasks](../userguide/tasks.html#task-synchronous-subtasks)

### 

Multiple bugs were resolved resulting in a much smoother experience when using Canvas.