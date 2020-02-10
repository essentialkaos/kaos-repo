#!/usr/bin/env escript
-export([main/1]).

main([]) -> 
  [{_,_,Info}] = crypto:info_lib(),
  io:fwrite("~s~n", [binary_to_list(Info)]).
