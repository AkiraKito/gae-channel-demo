======
readme
======

----
説明
----
基本的には GAE/Py の Channel API のデモ。
*正常には動きません*

GAE for Python SDK 1.5.1 で Channel API に追加された `user presence`_ を試してみようと書いてみたが、
`/_ah/channel/connected/` と `/_ah/channel/disconnected/` にマップしたハンドラが何故か動かなかったのでこの場に晒す。

--------
事の次第
--------
`user presence`_ のドキュメントには connect/disconnect したときに POST が投げられると書いてあるし、開発環境のログにもそのように出ているが、ハンドラ内に仕込んだログメッセージは出力されなかったので、おそらくハンドラの post() メソッドが呼ばれてないんだろう。

また、ためしに `/_ah/channel/connected/` に対応するハンドラに get() メソッドを作って呼んでみたところ正常に動作したため、URIとハンドラクラスのマッピングがおかしいわけでもないらしい。

原因不明すぎ

----
補足
----
なお `user presence`_ が試せればそれでいいと思っていたため `token の期限が切れた場合 <http://code.google.com/intl/en/appengine/docs/python/channel/overview.html#Tokens_and_Security>`_ は考慮していない

.. _user presence: http://code.google.com/intl/en/appengine/docs/python/channel/overview.html#Tracking_Client_Connections_and_Disconnections

