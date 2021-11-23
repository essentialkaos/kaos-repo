<p align="center"><a href="#readme"><img src="https://gh.kaos.st/kaos-repo.svg"/></a></p>

<p align="center"><a href="#installation">Installation</a> • <a href="#contributing-guidelines">Contributing Guidelines</a> • <a href="#deletion-policy">Deletion Policy</a> • <a href="#end-of-support-schedule">EoS Schedule</a> • <a href="#perfecto-and-bibop-check-status">CI status</a> • <a href="#license">License</a></p>

<br/>

This repository contains spec files and patches used for building RPM packages for [ESSENTIAL KAOS Public YUM Repository](https://yum.kaos.st).

### Installation

```bash
sudo yum install -y https://yum.kaos.st/get/$(uname -r).rpm
```

For some packages may be required [EPEL](https://fedoraproject.org/wiki/EPEL) and [Software Collection](https://wiki.centos.org/SpecialInterestGroup/SCLo) repository packages. You could install this packages by next command:

```
sudo yum install -y epel-release centos-release-scl
```

### Contributing Guidelines

If you want to add a new package to the repository, be ready to look after it. It's physically impossible to maintain and keep fresh a large number of packages, especially if you don't use them somewhere.

Also, bibop tests are mandatory for all new packages. It's the only way to test if the package is okay and does not affect other packages in the repository. bibop recipe syntax is easy to learn, so don't be afraid of it.

Also, please read our main [Contributing Guidelines](https://kaos.sh/contributing-guidelines#contributing-guidelines).

### Deletion Policy

Security is our first priority. We can't keep an outdated package in our repository for a long time. If a package spec were not updated for the several latest releases (especially with known vulnerabilities) of software, it would be deleted from the repository.

### End-of-Support Schedule

| CentOS/RHEL version | Updates     | Repository removal |
|---------------------|-------------|--------------------|
| `7.x`               | 1 Jan 2022  | 31 Dec 2022        |

### [_perfecto_](https://kaos.sh/perfecto) and [bibop](https://kaos.sh/bibop) check status

| Branch | Status |
|------------|--------|
| `master` | [![CI](https://kaos.sh/w/bibop/ci.svg?branch=master)](https://kaos.sh/w/kaos-repo/ci?query=branch:master) |
| `develop` | [![CI](https://kaos.sh/w/kaos-repo/ci.svg?branch=master)](https://kaos.sh/w/kaos-repo/ci?query=branch:develop) |

### License

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)

<p align="center"><a href="https://essentialkaos.com"><img src="https://gh.kaos.st/ekgh.svg"/></a></p>
