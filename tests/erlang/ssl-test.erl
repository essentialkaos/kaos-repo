#!/usr/bin/env escript
-export([main/1]).

url() ->
  "https://kaos.io".

ciphers() ->
  [
    #{cipher => chacha20_poly1305, key_exchange => ecdhe_rsa, mac => aead, prf => sha256}
  ].

ssl_options() ->
  [
    {ciphers, ciphers()},
    {versions, ['tlsv1.2']}
  ].

do_request() ->
  httpc:request(get, {url(), []}, [{ssl, ssl_options()}], []).

main([]) ->
  ssl:start(),
  inets:start(),
  RetCode = case do_request() of
    {ok, {_Status, _Headers, _Body}} -> 0;
    _ -> 1
  end,
  halt(RetCode).
