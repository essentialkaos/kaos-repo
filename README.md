<p align="center"><a href="#readme"><img src="https://gh.kaos.st/kaos-repo.svg"/></a></p>

This repository contains spec files and patches used for building RPM packages for [ESSENTIAL KAOS Public YUM Repository](https://yum.kaos.st).

### Installation

#### CentOS/RHEL 6.x

```
[sudo] yum install -y https://yum.kaos.st/kaos-repo-latest.el6.noarch.rpm
```

#### CentOS/RHEL 7.x

```
[sudo] yum install -y https://yum.kaos.st/kaos-repo-latest.el7.noarch.rpm
```

For some packages may be required [EPEL](https://fedoraproject.org/wiki/EPEL) and [Software Collection](https://wiki.centos.org/SpecialInterestGroup/SCLo) repository packages. You could install this packages by next command:

```
[sudo] yum install -y epel-release centos-release-scl
```

### [_perfecto_](https://github.com/essentialkaos/perfecto) Check Status

| Branch                 | Status |
|------------------------|--------|
| `master` (_Stable_)    | [![Build Status](https://travis-ci.org/essentialkaos/kaos-repo.svg?branch=master)](https://travis-ci.org/essentialkaos/kaos-repo) |
| `develop` (_Unstable_) | [![Build Status](https://travis-ci.org/essentialkaos/kaos-repo.svg?branch=develop)](https://travis-ci.org/essentialkaos/kaos-repo) |

### License

[EKOL](https://essentialkaos.com/ekol)

<p align="center"><a href="https://essentialkaos.com"><img src="https://gh.kaos.st/ekgh.svg"/></a></p>
