# Macros that test various C library quirks
# $PostgreSQL: pgsql/config/c-library.m4,v 1.31 2005/02/24 01:34:45 tgl Exp $


# PGAC_VAR_INT_TIMEZONE
# ---------------------
# Check if the global variable `timezone' exists. If so, define
# HAVE_INT_TIMEZONE.
AC_DEFUN([PGAC_VAR_INT_TIMEZONE],
[AC_CACHE_CHECK(for int timezone, pgac_cv_var_int_timezone,
[AC_TRY_LINK([#include <time.h>
int res;],
  [#ifndef __CYGWIN__
res = timezone / 60;
#else
res = _timezone / 60;
#endif],
  [pgac_cv_var_int_timezone=yes],
  [pgac_cv_var_int_timezone=no])])
if test x"$pgac_cv_var_int_timezone" = xyes ; then
  AC_DEFINE(HAVE_INT_TIMEZONE,, [Define to 1 if you have the global variable 'int timezone'.])
fi])# PGAC_VAR_INT_TIMEZONE


# PGAC_STRUCT_TIMEZONE
# ------------------
# Figure out how to get the current timezone.  If `struct tm' has a
# `tm_zone' member, define `HAVE_TM_ZONE'.  Also, if the
# external array `tzname' is found, define `HAVE_TZNAME'.
# This is the same as the standard macro AC_STRUCT_TIMEZONE, except that
# tzname[] is checked for regardless of whether we find tm_zone.
AC_DEFUN([PGAC_STRUCT_TIMEZONE],
[AC_REQUIRE([AC_STRUCT_TM])dnl
AC_CHECK_MEMBERS([struct tm.tm_zone],,,[#include <sys/types.h>
#include <$ac_cv_struct_tm>
])
if test "$ac_cv_member_struct_tm_tm_zone" = yes; then
  AC_DEFINE(HAVE_TM_ZONE, 1,
            [Define to 1 if your `struct tm' has `tm_zone'. Deprecated, use
             `HAVE_STRUCT_TM_TM_ZONE' instead.])
fi
AC_CACHE_CHECK(for tzname, ac_cv_var_tzname,
[AC_TRY_LINK(
[#include <time.h>
#ifndef tzname /* For SGI.  */
extern char *tzname[]; /* RS6000 and others reject char **tzname.  */
#endif
],
[atoi(*tzname);], ac_cv_var_tzname=yes, ac_cv_var_tzname=no)])
if test $ac_cv_var_tzname = yes; then
    AC_DEFINE(HAVE_TZNAME, 1,
              [Define to 1 if you have the external array `tzname'.])
fi
])# PGAC_STRUCT_TIMEZONE


# PGAC_FUNC_GETTIMEOFDAY_1ARG
# ---------------------------
# Check if gettimeofday() has only one arguments. (Normal is two.)
# If so, define GETTIMEOFDAY_1ARG.
AC_DEFUN([PGAC_FUNC_GETTIMEOFDAY_1ARG],
[AC_CACHE_CHECK(whether gettimeofday takes only one argument,
pgac_cv_func_gettimeofday_1arg,
[AC_TRY_COMPILE([#include <sys/time.h>],
[struct timeval *tp;
struct timezone *tzp;
gettimeofday(tp,tzp);],
[pgac_cv_func_gettimeofday_1arg=no],
[pgac_cv_func_gettimeofday_1arg=yes])])
if test x"$pgac_cv_func_gettimeofday_1arg" = xyes ; then
  AC_DEFINE(GETTIMEOFDAY_1ARG,, [Define to 1 if gettimeofday() takes only 1 argument.])
fi
AH_VERBATIM(GETTIMEOFDAY_1ARG_,
[@%:@ifdef GETTIMEOFDAY_1ARG
@%:@ define gettimeofday(a,b) gettimeofday(a)
@%:@endif])dnl
])# PGAC_FUNC_GETTIMEOFDAY_1ARG


# PGAC_FUNC_GETPWUID_R_5ARG
# ---------------------------
# Check if getpwuid_r() takes a fifth argument (later POSIX standard, not draft version)
# If so, define GETPWUID_R_5ARG
AC_DEFUN([PGAC_FUNC_GETPWUID_R_5ARG],
[AC_CACHE_CHECK(whether getpwuid_r takes a fifth argument,
pgac_func_getpwuid_r_5arg,
[AC_TRY_COMPILE([#include <sys/types.h>
#include <pwd.h>],
[uid_t uid;
struct passwd *space;
char *buf;
size_t bufsize;
struct passwd **result;
getpwuid_r(uid, space, buf, bufsize, result);],
[pgac_func_getpwuid_r_5arg=yes],
[pgac_func_getpwuid_r_5arg=no])])
if test x"$pgac_func_getpwuid_r_5arg" = xyes ; then
  AC_DEFINE(GETPWUID_R_5ARG,, [Define to 1 if getpwuid_r() takes a 5th argument.])
fi
])# PGAC_FUNC_GETPWUID_R_5ARG


# PGAC_FUNC_STRERROR_R_INT
# ---------------------------
# Check if strerror_r() returns an int (SUSv3) rather than a char * (GNU libc)
# If so, define STRERROR_R_INT
AC_DEFUN([PGAC_FUNC_STRERROR_R_INT],
[AC_CACHE_CHECK(whether strerror_r returns int,
pgac_func_strerror_r_int,
[AC_TRY_COMPILE([#include <string.h>],
[#ifndef _AIX
int strerror_r(int, char *, size_t);
#else
/* Older AIX has 'int' for the third argument so we don't test the args. */
int strerror_r();
#endif],
[pgac_func_strerror_r_int=yes],
[pgac_func_strerror_r_int=no])])
if test x"$pgac_func_strerror_r_int" = xyes ; then
  AC_DEFINE(STRERROR_R_INT,, [Define to 1 if strerror_r() returns a int.])
fi
])# PGAC_FUNC_STRERROR_R_INT


# PGAC_UNION_SEMUN
# ----------------
# Check if `union semun' exists. Define HAVE_UNION_SEMUN if so.
# If it doesn't then one could define it as
# union semun { int val; struct semid_ds *buf; unsigned short *array; }
AC_DEFUN([PGAC_UNION_SEMUN],
[AC_CHECK_TYPES([union semun], [], [],
[#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>])])# PGAC_UNION_SEMUN


# PGAC_STRUCT_SOCKADDR_UN
# -----------------------
# If `struct sockaddr_un' exists, define HAVE_UNIX_SOCKETS.
# (Requires test for <sys/un.h>!)
AC_DEFUN([PGAC_STRUCT_SOCKADDR_UN],
[AC_CHECK_TYPES([struct sockaddr_un], [AC_DEFINE(HAVE_UNIX_SOCKETS, 1, [Define to 1 if you have unix sockets.])], [],
[#include <sys/types.h>
#ifdef HAVE_SYS_UN_H
#include <sys/un.h>
#endif
])])# PGAC_STRUCT_SOCKADDR_UN


# PGAC_STRUCT_SOCKADDR_STORAGE
# ----------------------------
# If `struct sockaddr_storage' exists, define HAVE_STRUCT_SOCKADDR_STORAGE.
# If it is missing then one could define it.
AC_DEFUN([PGAC_STRUCT_SOCKADDR_STORAGE],
[AC_CHECK_TYPES([struct sockaddr_storage], [], [],
[#include <sys/types.h>
#ifdef HAVE_SYS_SOCKET_H
#include <sys/socket.h>
#endif
])])# PGAC_STRUCT_SOCKADDR_STORAGE

# PGAC_STRUCT_SOCKADDR_STORAGE_MEMBERS
# --------------------------------------
# Check the members of `struct sockaddr_storage'.  We need to know about
# ss_family and ss_len.  (Some platforms follow RFC 2553 and call them
# __ss_family and __ss_len.)  We also check struct sockaddr's sa_len;
# if we have to define our own `struct sockaddr_storage', this tells us
# whether we need to provide an ss_len field.
AC_DEFUN([PGAC_STRUCT_SOCKADDR_STORAGE_MEMBERS],
[AC_CHECK_MEMBERS([struct sockaddr_storage.ss_family,
		   struct sockaddr_storage.__ss_family,
		   struct sockaddr_storage.ss_len,
		   struct sockaddr_storage.__ss_len,
		   struct sockaddr.sa_len], [], [],
[#include <sys/types.h>
#ifdef HAVE_SYS_SOCKET_H
#include <sys/socket.h>
#endif
])])# PGAC_STRUCT_SOCKADDR_STORAGE_MEMBERS


# PGAC_STRUCT_ADDRINFO
# -----------------------
# If `struct addrinfo' exists, define HAVE_STRUCT_ADDRINFO.
AC_DEFUN([PGAC_STRUCT_ADDRINFO],
[AC_CHECK_TYPES([struct addrinfo], [], [],
[#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
])])# PGAC_STRUCT_ADDRINFO


# PGAC_FUNC_POSIX_SIGNALS
# -----------------------
# Check to see if the machine has the POSIX signal interface. Define
# HAVE_POSIX_SIGNALS if so. Also set the output variable HAVE_POSIX_SIGNALS
# to yes or no.
#
# Note that this test only compiles a test program, it doesn't check
# whether the routines actually work. If that becomes a problem, make
# a fancier check.
AC_DEFUN([PGAC_FUNC_POSIX_SIGNALS],
[AC_CACHE_CHECK(for POSIX signal interface, pgac_cv_func_posix_signals,
[AC_TRY_LINK([#include <signal.h>
],
[struct sigaction act, oact;
sigemptyset(&act.sa_mask);
act.sa_flags = SA_RESTART;
sigaction(0, &act, &oact);],
[pgac_cv_func_posix_signals=yes],
[pgac_cv_func_posix_signals=no])])
if test x"$pgac_cv_func_posix_signals" = xyes ; then
  AC_DEFINE(HAVE_POSIX_SIGNALS,, [Define to 1 if you have the POSIX signal interface.])
fi
HAVE_POSIX_SIGNALS=$pgac_cv_func_posix_signals
AC_SUBST(HAVE_POSIX_SIGNALS)])# PGAC_FUNC_POSIX_SIGNALS


# PGAC_FUNC_SNPRINTF_LONG_LONG_INT_FORMAT
# ---------------------------------------
# Determine which format snprintf uses for long long int.  We handle
# %lld, %qd, %I64d.  The result is in shell variable
# LONG_LONG_INT_FORMAT.
#
# MinGW uses '%I64d', though gcc throws an warning with -Wall,
# while '%lld' doesn't generate a warning, but doesn't work.
#
AC_DEFUN([PGAC_FUNC_SNPRINTF_LONG_LONG_INT_FORMAT],
[AC_MSG_CHECKING([snprintf format for long long int])
AC_CACHE_VAL(pgac_cv_snprintf_long_long_int_format,
[for pgac_format in '%lld' '%qd' '%I64d'; do
AC_TRY_RUN([#include <stdio.h>
typedef long long int ac_int64;
#define INT64_FORMAT "$pgac_format"

ac_int64 a = 20000001;
ac_int64 b = 40000005;

int does_int64_snprintf_work()
{
  ac_int64 c;
  char buf[100];

  if (sizeof(ac_int64) != 8)
    return 0;			/* doesn't look like the right size */

  c = a * b;
  snprintf(buf, 100, INT64_FORMAT, c);
  if (strcmp(buf, "800000140000005") != 0)
    return 0;			/* either multiply or snprintf is busted */
  return 1;
}
main() {
  exit(! does_int64_snprintf_work());
}],
[pgac_cv_snprintf_long_long_int_format=$pgac_format; break],
[],
[pgac_cv_snprintf_long_long_int_format=cross; break])
done])dnl AC_CACHE_VAL

LONG_LONG_INT_FORMAT=''

case $pgac_cv_snprintf_long_long_int_format in
  cross) AC_MSG_RESULT([cannot test (not on host machine)]);;
  ?*)    AC_MSG_RESULT([$pgac_cv_snprintf_long_long_int_format])
         LONG_LONG_INT_FORMAT=$pgac_cv_snprintf_long_long_int_format;;
  *)     AC_MSG_RESULT(none);;
esac])# PGAC_FUNC_SNPRINTF_LONG_LONG_INT_FORMAT


# PGAC_FUNC_PRINTF_ARG_CONTROL
# ---------------------------------------
# Determine if printf supports %1$ argument selection, e.g. %5$ selects
# the fifth argument after the printf print string.
# This is not in the C99 standard, but in the Single Unix Specification (SUS).
# It is used in our language translation strings.
#
AC_DEFUN([PGAC_FUNC_PRINTF_ARG_CONTROL],
[AC_MSG_CHECKING([whether printf supports argument control])
AC_CACHE_VAL(pgac_cv_printf_arg_control,
[AC_TRY_RUN([#include <stdio.h>
#include <string.h>

int main()
{
  char buf[100];

  /* can it swap arguments? */
  snprintf(buf, 100, "%2\$d %1\$d", 3, 4);
  if (strcmp(buf, "4 3") != 0)
    return 1;
  return 0;
}],
[pgac_cv_printf_arg_control=yes],
[pgac_cv_printf_arg_control=no],
[pgac_cv_printf_arg_control=cross])
])dnl AC_CACHE_VAL
AC_MSG_RESULT([$pgac_cv_printf_arg_control])
])# PGAC_FUNC_PRINTF_ARG_CONTROL

# $PostgreSQL: pgsql/config/general.m4,v 1.9 2006/11/30 22:21:23 tgl Exp $

# This file defines new macros to process configure command line
# arguments, to replace the brain-dead AC_ARG_WITH and AC_ARG_ENABLE.
# The flaw in these is particularly that they only differentiate
# between "given" and "not given" and do not provide enough help to
# process arguments that only accept "yes/no", that require an
# argument (other than "yes/no"), etc.
#
# The point of this implementation is to reduce code size and
# redundancy in configure.in and to improve robustness and consistency
# in the option evaluation code.


# Convert type and name to shell variable name (e.g., "enable_long_strings")
m4_define([pgac_arg_to_variable],
          [$1[]_[]patsubst($2, -, _)])


# PGAC_ARG(TYPE, NAME, HELP-STRING,
#          [ACTION-IF-YES], [ACTION-IF-NO], [ACTION-IF-ARG],
#          [ACTION-IF-OMITTED])
# ----------------------------------------------------------
# This is the base layer. TYPE is either "with" or "enable", depending
# on what you like. NAME is the rest of the option name, HELP-STRING
# as usual. ACTION-IF-YES is executed if the option is given without
# an argument (or "yes", which is the same); similar for ACTION-IF-NO.

AC_DEFUN([PGAC_ARG],
[
pgac_args="$pgac_args pgac_arg_to_variable([$1],[$2])"
m4_case([$1],

enable, [
AC_ARG_ENABLE([$2], [$3], [
  case [$]enableval in
    yes)
      m4_default([$4], :)
      ;;
    no)
      m4_default([$5], :)
      ;;
    *)
      $6
      ;;
  esac
],
[$7])[]dnl AC_ARG_ENABLE
],

with, [
AC_ARG_WITH([$2], [$3], [
  case [$]withval in
    yes)
      m4_default([$4], :)
      ;;
    no)
      m4_default([$5], :)
      ;;
    *)
      $6
      ;;
  esac
],
[$7])[]dnl AC_ARG_WITH
],

[m4_fatal([first argument of $0 must be 'enable' or 'with', not '$1'])]
)
])# PGAC_ARG

# PGAC_ARG_CHECK()
# ----------------
# Checks if the user passed any --with/without/enable/disable
# arguments that were not defined. Just prints out a warning message,
# so this should be called near the end, so the user will see it.

AC_DEFUN([PGAC_ARG_CHECK],
[for pgac_var in `set | sed 's/=.*//' | $EGREP 'with_|enable_'`; do
  for pgac_arg in $pgac_args with_gnu_ld; do
    if test "$pgac_var" = "$pgac_arg"; then
      continue 2
    fi
  done
  pgac_txt=`echo $pgac_var | sed 's/_/-/g'`
  AC_MSG_WARN([option ignored: --$pgac_txt])
done])# PGAC_ARG_CHECK

# PGAC_ARG_BOOL(TYPE, NAME, DEFAULT, HELP-STRING, 
#               [ACTION-IF-YES], [ACTION-IF-NO])
# -----------------------------------------------
# Accept a boolean option, that is, one that only takes yes or no.
# ("no" is equivalent to "disable" or "without"). DEFAULT is what
# should be done if the option is omitted; it should be "yes" or "no".
# (Consequently, one of ACTION-IF-YES and ACTION-IF-NO will always
# execute.)

AC_DEFUN([PGAC_ARG_BOOL],
[PGAC_ARG([$1], [$2], [$4], [$5], [$6], 
          [AC_MSG_ERROR([no argument expected for --$1-$2 option])],
          [m4_case([$3],
                   yes, [pgac_arg_to_variable([$1], [$2])=yes
$5],
                   no,  [pgac_arg_to_variable([$1], [$2])=no
$6],
                   [m4_fatal([third argument of $0 must be 'yes' or 'no', not '$3'])])])[]dnl
])# PGAC_ARG_BOOL


# PGAC_ARG_REQ(TYPE, NAME, HELP-STRING, [ACTION-IF-GIVEN], [ACTION-IF-NOT-GIVEN])
# -------------------------------------------------------------------------------
# This option will require an argument; "yes" or "no" will not be
# accepted.

AC_DEFUN([PGAC_ARG_REQ],
[PGAC_ARG([$1], [$2], [$3],
          [AC_MSG_ERROR([argument required for --$1-$2 option])],
          [AC_MSG_ERROR([argument required for --$1-$2 option])],
          [$4],
          [$5])])# PGAC_ARG_REQ


# PGAC_ARG_OPTARG(TYPE, NAME, HELP-STRING, [DEFAULT-ACTION], [ARG-ACTION]
#                 [ACTION-ENABLED], [ACTION-DISABLED])
# -----------------------------------------------------------------------
# This will create an option that behaves as follows: If omitted, or
# called with "no", then set the enable_variable to "no" and do
# nothing else. If called with "yes", then execute DEFAULT-ACTION. If
# called with argument, set enable_variable to "yes" and execute
# ARG-ACTION. Additionally, execute ACTION-ENABLED if we ended up with
# "yes" either way, else ACTION-DISABLED.
#
# The intent is to allow enabling a feature, and optionally pass an
# additional piece of information.

AC_DEFUN([PGAC_ARG_OPTARG],
[PGAC_ARG([$1], [$2], [$3], [$4], [],
          [pgac_arg_to_variable([$1], [$2])=yes
$5],
          [pgac_arg_to_variable([$1], [$2])=no])
dnl Add this code only if there's a ACTION-ENABLED or ACTION-DISABLED.
m4_ifval([$6[]$7],
[
if test "[$]pgac_arg_to_variable([$1], [$2])" = yes; then
  m4_default([$6], :)
m4_ifval([$7],
[else
  $7
])[]dnl
fi
])[]dnl
])# PGAC_ARG_OPTARG
