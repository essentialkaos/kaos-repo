<p align="center"><a href="#readme"><img src="https://gh.kaos.st/kaos-repo.svg"/></a></p>

<p align="center"><a href="#installation">Installation</a> • <a href="#contributing-guidelines">Contributing Guidelines</a> • <a href="#deletion-policy">Deletion Policy</a> • <a href="#end-of-support-schedule">EoS Schedule</a> • <a href="#perfecto-and-bibop-check-status">CI status</a> • <a href="#license">License</a></p>

<br/>

This repository contains spec files and patches used for building RPM packages for [ESSENTIAL KAOS Public YUM Repository](https://yum.kaos.st).

### Installation

```bash
sudo yum install -y https://yum.kaos.st/kaos-repo-latest.el$(grep 'CPE_NAME' /etc/os-release | tr -d '"' | cut -d':' -f5).noarch.rpm
```

For some packages may be required [EPEL](https://fedoraproject.org/wiki/EPEL) repository packages. You could install this packages by next command:

```
sudo yum install -y epel-release
```

### Contributing Guidelines

If you want to add a new package to the repository, be ready to look after it. It's physically impossible to maintain and keep fresh a large number of packages, especially if you don't use them somewhere.

Also, [bibop](https://kaos.sh/bibop) tests are mandatory for all new packages. It's the only way to test if the package is okay and does not affect other packages in the repository. `bibop` recipe syntax is [easy to learn](https://github.com/essentialkaos/bibop/blob/master/COOKBOOK.md), so don't be afraid of it.

Please find a minute to check out our main [Contributing Guidelines](https://kaos.sh/contributing-guidelines#contributing-guidelines).

### Deletion Policy

Security is our first priority. We can't keep an outdated package in our repository for a long time. If a package spec were not updated for the several latest releases (_especially with known vulnerabilities_) of software, it would be deleted from the repository.

### End-of-Support Schedule

| CentOS/RHEL version | Updates     | Repository removal |
|---------------------|-------------|--------------------|
| `7.x`               | 1 Jan 2023  | 1 Jun 2023         |
| `8.x`               | 1 Jan 2024  | 1 Jun 2024         |
| `9.x`               | 1 Jan 2026  | 1 Jun 2026         |

### [_perfecto_](https://kaos.sh/perfecto) and [bibop](https://kaos.sh/bibop) check status

| Branch | Status |
|------------|--------|
| `master` | [![CI](https://kaos.sh/w/kaos-repo/ci.svg?branch=master)](https://kaos.sh/w/kaos-repo/ci?query=branch:master) |
| `develop` | [![CI](https://kaos.sh/w/kaos-repo/ci.svg?branch=develop)](https://kaos.sh/w/kaos-repo/ci?query=branch:develop) |

### License

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)

<p align="center"><a href="https://essentialkaos.com"><img src="https://gh.kaos.st/ekgh.svg"/></a></p>
