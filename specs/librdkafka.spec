################################################################################

%ifarch i386
%define optflags -O2 -g -pipe -Wall -Wp,-D_FORTIFY_SOURCE=2 -fexceptions -fstack-protector --param=ssp-buffer-size=4 -m32 -march=i386 -mtune=atom -fasynchronous-unwind-tables
%endif

################################################################################

%define _posixroot        /
%define _root             /root
%define _bin              /bin
%define _sbin             /sbin
%define _srv              /srv
%define _home             /home
%define _lib32            %{_posixroot}lib
%define _lib64            %{_posixroot}lib64
%define _libdir32         %{_prefix}%{_lib32}
%define _libdir64         %{_prefix}%{_lib64}
%define _logdir           %{_localstatedir}/log
%define _rundir           %{_localstatedir}/run
%define _lockdir          %{_localstatedir}/lock
%define _cachedir         %{_localstatedir}/cache
%define _spooldir         %{_localstatedir}/spool
%define _loc_prefix       %{_prefix}/local
%define _loc_exec_prefix  %{_loc_prefix}
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_libdir       %{_loc_exec_prefix}/%{_lib}
%define _loc_libdir32     %{_loc_exec_prefix}/%{_lib32}
%define _loc_libdir64     %{_loc_exec_prefix}/%{_lib64}
%define _loc_libexecdir   %{_loc_exec_prefix}/libexec
%define _loc_sbindir      %{_loc_exec_prefix}/sbin
%define _loc_bindir       %{_loc_exec_prefix}/bin
%define _loc_datarootdir  %{_loc_prefix}/share
%define _loc_includedir   %{_loc_prefix}/include
%define _rpmstatedir      %{_sharedstatedir}/rpm-state
%define _pkgconfigdir     %{_libdir}/pkgconfig

%define __ln              %{_bin}/ln
%define __touch           %{_bin}/touch
%define __service         %{_sbin}/service
%define __chkconfig       %{_sbin}/chkconfig

################################################################################

%define realname       rdkafka
%define minor_ver      1

################################################################################

Summary:             Apache Kafka C/C++ client library
Name:                librdkafka
Version:             1.6.0
Release:             0%{?dist}
License:             2-clause BSD
Group:               Development/Libraries
URL:                 https://github.com/edenhill/librdkafka

Source0:             https://github.com/edenhill/%{name}/archive/v%{version}.tar.gz

BuildRoot:           %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:       make gcc gcc-c++ zlib-devel

Requires:            zlib

Provides:            %{name} = %{version}-%{release}

################################################################################

%description
C library implementation of the Apache Kafka protocol, containing both
Producer and Consumer support. It was designed with message delivery
reliability and high performance in mind, current figures exceed
800000 msgs/second for the producer and 3 million msgs/second for the consumer.

################################################################################

%package static
Summary:             Static libraries for librdkafka C development
Group:               Development/Libraries
Requires:            %{name} = %{version}

%description static
The %{name}-static package contains the static libraries for librdkafka.

################################################################################

%package devel
Summary:             Header files and libraries for librdkafka C development
Group:               Development/Libraries
Requires:            %{name} = %{version}

%description devel
The %{name}-devel package contains the header files and
libraries to develop applications using a Kafka databases.

################################################################################

%prep
%setup -q

%build
%configure

%{__make} %{?_smp_mflags}

%install
rm -rf %{buildroot}

%{make_install}

%clean
rm -rf %{buildroot}

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md CONFIGURATION.md INTRODUCTION.md CONFIGURATION.md STATISTICS.md
%doc LICENSE LICENSES.txt
%{_docdir}/%{name}/*.md
%{_docdir}/%{name}/*.txt
%{_docdir}/%{name}/LICENSE
%{_libdir}/%{name}.so
%{_libdir}/%{name}.so.%{minor_ver}
%{_libdir}/%{name}++.so
%{_libdir}/%{name}++.so.%{minor_ver}

%files static
%defattr(-,root,root,-)
%{_libdir}/%{name}.a
%{_libdir}/%{name}++.a

%files devel
%defattr(-,root,root,-)
%{_includedir}/%{name}/*
%{_libdir}/%{name}.so
%{_libdir}/%{name}++.so
%{_pkgconfigdir}/%{realname}.pc
%{_pkgconfigdir}/%{realname}++.pc
%{_pkgconfigdir}/%{realname}-static.pc
%{_pkgconfigdir}/%{realname}++-static.pc

################################################################################

%changelog
* Fri Feb 12 2021 Anton Novojilov <andy@essentialkaos.com> - 1.6.0-0
- Incremental rebalancing with sticky consumer group partition assignor
- Sticky producer partitioning (sticky.partitioning.linger.ms) - achieves
  higher throughput and lower latency through sticky selection of random
  partition
- AdminAPI: Add support for DeleteRecords(), DeleteGroups() and
  DeleteConsumerGroupOffsets()
- Producer scalability for exactly once semantics - allows a single
  transactional producer to be used for multiple input partitions.
- AdminAPI: Added DeleteRecords()
- KIP-229: AdminAPI: Added DeleteGroups().
- AdminAPI: Added DeleteConsumerGroupOffsets().
- AdminAPI: Added support for broker-side default partition count
  and replication factor for CreateTopics().
- Use reentrant rand_r() on supporting platforms which decreases lock
  contention.
- Added assignor debug context for troubleshooting consumer partition
  assignments.
- Updated to OpenSSL v1.1.1i when building dependencies.
- Update bundled lz4 (used when ./configure --disable-lz4-ext) to v1.9.3
  which has vast performance improvements.
- Added rd_kafka_conf_get_default_topic_conf() to retrieve the
  default topic configuration object from a global configuration object.
- Added conf debugging context to debug - shows set configuration
  properties on client and topic instantiation. Sensitive properties
  are redacted.
- Added rd_kafka_queue_yield() to cancel a blocking queue call.
- Will now log a warning when multiple ClusterIds are seen, which is an
  indication that the client might be erroneously configured to connect to
  multiple clusters which is not supported.
- Added rd_kafka_seek_partitions() to seek multiple partitions to
  per-partition specific offsets.
- Fix a use-after-free crash when certain coordinator requests were retried.
- The C++ oauthbearer_set_token() function would call free() on
  a new-created pointer, possibly leading to crashes or heap corruption.
- The consumer assignment and consumer group implementations have been
  decoupled, simplified and made more strict and robust.
- Partition fetch state was not set to STOPPED if OffsetCommit failed.
- The session timeout is now enforced locally also when the coordinator
  connection is down, which was not previously the case.
- Transaction commit or abort failures on the broker, such as when the
  producer was fenced by a newer instance, were not propagated to the
  application resulting in failed commits seeming successful.
  This was a critical race condition for applications that had a delay after
  producing messages (or sendings offsets) before committing or
  aborting the transaction. This issue has now been fixed and test coverage
  improved.
- The transactional producer API would return RD_KAFKA_RESP_ERR__STATE
  when API calls were attempted after the transaction had failed, we now
  try to return the error that caused the transaction to fail in the first
  place, such as RD_KAFKA_RESP_ERR__FENCED when the producer has
  been fenced, or RD_KAFKA_RESP_ERR__TIMED_OUT when the transaction
  has timed out.
- Transactional producer retry count for transactional control protocol
  requests has been increased from 3 to infinite, retriable errors
  are now automatically retried by the producer until success or the
  transaction timeout is exceeded. This fixes the case where
  rd_kafka_send_offsets_to_transaction() would fail the current
  transaction into an abortable state when CONCURRENT_TRANSACTIONS was
  returned by the broker (which is a transient error) and the 3 retries
  were exhausted.
- Calling rd_kafka_topic_new() with a topic config object with
  message.timeout.ms set could sometimes adjust the global linger.ms
  property (if not explicitly configured) which was not desired, this is now
  fixed and the auto adjustment is only done based on the
  default_topic_conf at producer creation.
- rd_kafka_flush() could previously return RD_KAFKA_RESP_ERR__TIMED_OUT
  just as the timeout was reached if the messages had been flushed but
  there were now no more messages. This has been fixed.

* Fri Feb 12 2021 Anton Novojilov <andy@essentialkaos.com> - 1.5.3-0
- Fix a use-after-free crash when certain coordinator requests were retried.
- Consumer would not filter out messages for aborted transactions
  if the messages were compressed.
- Consumer destroy without prior close() could hang in certain
  cgrp states.
- Fix possible null dereference in Message::errstr().
- The roundrobin partition assignment strategy could get stuck in an
  endless loop or generate uneven assignments in case the group members
  had asymmetric subscriptions (e.g., c1 subscribes to t1,t2 while c2
  subscribes to t2,t3).

* Fri Oct 30 2020 Gleb Goncharov <g.goncharov@fun-box.ru> - 1.5.2-0
- Consumer configs on producers and vice versa will now be logged with
  warning messages on client instantiation.
- There was an incorrect call to zlib's inflateGetHeader() with
  unitialized memory pointers that could lead to the GZIP header of a fetched
  message batch to be copied to arbitrary memory.
- rd_kafka_topic_opaque() (used by the C++ API) would cause object
  refcounting issues when used on light-weight (error-only) topic objects
  such as consumer errors.
- Handle name resolution failures when formatting IP addresses in error logs,
  and increase printed hostname limit to ~256 bytes (was ~60).
- Broker sockets would be closed twice (thus leading to potential race
  condition with fd-reuse in other threads) if a custom socket_cb would
  return error.
- The roundrobin partition.assignment.strategy could crash (assert)
  for certain combinations of members and partitions.
- The C++ KafkaConsumer destructor did not destroy the underlying
  C rd_kafka_t instance, causing a leak if close() was not used.
- Expose rich error strings for C++ Consumer Message->errstr().
- The consumer could get stuck if an outstanding commit failed during
  rebalancing.
- Topic authorization errors during fetching are now reported only once.
- Topic authorization errors are now properly propagated for produced messages,
  both through delivery reports and as ERR_TOPIC_AUTHORIZATION_FAILED
  return value from produce*().
- Treat cluster authentication failures as fatal in the transactional
  producer.
- The transactional producer code did not properly reference-count partition
  objects which could in very rare circumstances lead to a use-after-free bug
  if a topic was deleted from the cluster when a transaction was using it.
- ERR_KAFKA_STORAGE_ERROR is now correctly treated as a retriable
  produce error.
- Messages that timed out locally would not fail the ongoing transaction.
- EndTxnRequests (sent on commit/abort) are only retried in allowed
  states.

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 1.3.0-0
- Updated to the latest release

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 1.2.2-0
- Updated to the latest release

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 1.2.1-0
- Updated to the latest release

* Tue Dec 17 2019 Anton Novojilov <andy@essentialkaos.com> - 1.2.0-0
- Updated to the latest release

* Fri Jul 12 2019 Anton Novojilov <andy@essentialkaos.com> - 1.1.0-0
- Updated to the latest release
- Static libraries moved to separate package

* Wed Jun 05 2019 Gleb Goncharov <inbox@gongled.ru> - 1.0.1-0
- Updated to the latest release

* Wed Feb 07 2018 Anton Novojilov <andy@essentialkaos.com> - 0.11.3-0
- Updated to the latest release

* Fri Nov 17 2017 Anton Novojilov <andy@essentialkaos.com> - 0.11.1-0
- Updated to the latest release

* Wed May 10 2017 Anton Novojilov <andy@essentialkaos.com> - 0.9.5-0
- Updated to the latest release

* Wed Mar 22 2017 Anton Novojilov <andy@essentialkaos.com> - 0.9.4-0
- Updated to the latest release

* Sat Feb 18 2017 Anton Novojilov <andy@essentialkaos.com> - 0.9.3-0
- Updated to the latest release

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 0.9.2-0
- Updated to the latest release

* Sat Jun 18 2016 Anton Novojilov <andy@essentialkaos.com> - 0.9.1-0
- Updated to the latest release

* Tue Apr 05 2016 Gleb Goncharov <inbox@gongled.ru> - 0.9.0.99-0
- Initial build
