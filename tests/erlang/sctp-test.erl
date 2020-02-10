#!/usr/bin/env escript
-export([main/1]).

main([]) ->
  case gen_sctp:open() of
    {ok, _} ->
      halt(0);
    _ ->
      halt(1)
  end.
