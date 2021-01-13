<p align="center"><a href="#readme"><img src="https://gh.kaos.st/kaos-repo.svg"/></a></p>

This repository contains spec files and patches used for building RPM packages for [ESSENTIAL KAOS Public YUM Repository](https://yum.kaos.st).

### Installation

```bash
sudo yum install -y https://yum.kaos.st/get/$(uname -r).rpm
```

For some packages may be required [EPEL](https://fedoraproject.org/wiki/EPEL) and [Software Collection](https://wiki.centos.org/SpecialInterestGroup/SCLo) repository packages. You could install this packages by next command:

```
sudo yum install -y epel-release centos-release-scl
```

### End-of-support schedule

| CentOS/RHEL version | Updates     | Repository removal |
|---------------------|-------------|--------------------|
| `6.x`               | 1 Jan 2020  | 31 Dec 2020        |
| `7.x`               | 1 Jan 2022  | 31 Dec 2022        |
| `8.x`               | —           | —                  |


### [_perfecto_](https://github.com/essentialkaos/perfecto) check status

| Branch                 | Status |
|------------------------|--------|
| `master` (_Stable_)    | [![Build Status](https://travis-ci.org/essentialkaos/kaos-repo.svg?branch=master)](https://travis-ci.org/essentialkaos/kaos-repo) |
| `develop` (_Unstable_) | [![Build Status](https://travis-ci.org/essentialkaos/kaos-repo.svg?branch=develop)](https://travis-ci.org/essentialkaos/kaos-repo) |

### License

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)

<p align="center"><a href="https://essentialkaos.com"><img src="https://gh.kaos.st/ekgh.svg"/></a></p>
