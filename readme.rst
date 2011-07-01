======
readme
======

----
説明
----
基本的には GAE/Py の Channel API のデモ。
*開発環境では正常に動きません。*
本番環境でなら動きます。

GAE for Python SDK 1.5.1 で Channel API に追加された `user presence`_ を試してみようと書いてみたが、
`/_ah/channel/connected/` と `/_ah/channel/disconnected/` にマップしたハンドラが(*開発環境では*)何故か動かなかったのでこの場に晒す。


--------
事の次第
--------
""""""""""""""
開発環境の場合
""""""""""""""
`user presence`_ のドキュメントには connect/disconnect したときに POST が投げられると書いてあるし、開発環境のログにもそのように出ているが、ハンドラ内に仕込んだログメッセージは出力されなかったので、おそらくハンドラの post() メソッドが呼ばれてないんだろう。

また、ためしに `/_ah/channel/connected/` に対応するハンドラに POST を投げてみたところ `200 OK` が返った。
URIとハンドラクラスのマッピングがおかしいわけでもないらしい。


""""""""
本番環境
""""""""
このままのコードで正常に動く。

ログによるとChannel APIは、開発環境では channel_service_stub で動いているが、本番環境ではXMPPベースで動いているらしい。
原因は開発環境のバグか？


----
補足
----
なお `user presence`_ が試せればそれでいいと思っていたため `token の期限が切れた場合 <http://code.google.com/intl/en/appengine/docs/python/channel/overview.html#Tokens_and_Security>`_ は考慮していない

.. _user presence: http://code.google.com/intl/en/appengine/docs/python/channel/overview.html#Tracking_Client_Connections_and_Disconnections

