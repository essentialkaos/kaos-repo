<p align="center"><a href="#readme"><img src=".github/images/card.svg"/></a></p>

<p align="center"><a href="#installation">Installation</a> • <a href="#contributing-guidelines">Contributing Guidelines</a> • <a href="#deletion-policy">Deletion Policy</a> • <a href="#end-of-support-schedule">EoS Schedule</a> • <a href="#perfecto-and-bibop-check-status">CI status</a> • <a href="#license">License</a></p>

<br/>

This repository contains spec files and patches used for building RPM packages for [EK Public Repository](https://pkgs.kaos.st).

> [!IMPORTANT]
> **Due to the malicious actions of some users, crawlers and AI scrapers, bandwidth to the public repository is limited. However, if you wish to use the repository in your infrastructure, please create a [new issue ticket](https://github.com/essentialkaos/kaos-repo/issues/new) and we will provide you with unique credentials for repository access with higher bandwidth limits.**

### Installation

```bash
sudo dnf install -y https://pkgs.kaos.st/kaos-repo-latest.el$(grep 'CPE_NAME' /etc/os-release | tr -d '"' | cut -d':' -f5).noarch.rpm
```

Some packages have dependencies from [EPEL](https://fedoraproject.org/wiki/EPEL) repository. You could add this repository by following commands:

```bash
# Alma Linux / Rocky Linux
sudo dnf install -y epel-release

# Oracle Linux 8
sudo dnf install -y oracle-epel-release-el8

# Oracle Linux 9
sudo dnf install -y oracle-epel-release-el9

# Oracle Linux 10
sudo dnf install -y oracle-epel-release-el10
```

Some packages have dependencies from [CodeReady Builder](https://developers.redhat.com/blog/2018/11/15/introducing-codeready-linux-builder) repository. You can enable this repository by following commands:

```bash
# Alma Linux / Rocky Linux
sudo dnf config-manager --set-enabled crb

# Oracle Linux 8
sudo dnf config-manager --set-enabled ol8_codeready_builder

# Oracle Linux 9
sudo dnf config-manager --set-enabled ol9_codeready_builder

# Oracle Linux 10
sudo dnf config-manager --set-enabled ol10_codeready_builder
```

#### Update credentials using `config-manager`

```bash
sudo dnf config-manager --save --setopt=kaos-release.username=my_unique_credentials
sudo dnf config-manager --save --setopt=kaos-testing.username=my_unique_credentials
```

### Contributing Guidelines

If you want to add a new package to the repository, be ready to look after it. It's physically impossible to maintain and keep fresh a large number of packages, especially if you don't use them somewhere.

Also, [bibop](https://kaos.sh/bibop) tests are mandatory for all new packages. It's the only way to test if the package is okay and does not affect other packages in the repository. `bibop` recipe syntax is [easy to learn](https://github.com/essentialkaos/bibop/blob/master/COOKBOOK.md), so don't be afraid of it.

Please find a minute to check out our main [Contributing Guidelines](https://kaos.sh/contributing-guidelines#contributing-guidelines).

### Deletion Policy

Security is our first priority. We can't keep an outdated package in our repository for a long time. If a package spec were not updated for the several latest releases (_especially with known vulnerabilities_) of software, it would be deleted from the repository.

We keep at least the last 5 minor versions (_with all releases_) of each package. In some cases (_e.g. programming languages_) we keep more versions of packages. If a version has a critical security vulnerability it may be removed from the repository at any time.

### End-of-Support Schedule

| EL version | Updates     | Repository removal |
|------------|-------------|--------------------|
| `8.x`      | 1 Jun 2025  | 31 Dec 2025        |
| `9.x`      | 1 Sep 2027  | 31 Dec 2027        |
| `10.x`     | 1 Sep 2030  | 31 Dec 2030        |

### [_perfecto_](https://kaos.sh/perfecto) and [bibop](https://kaos.sh/bibop) check status

| Branch | Status |
|--------|--------|
| `master` | [![CI](https://kaos.sh/w/kaos-repo/ci.svg?branch=master)](https://kaos.sh/w/kaos-repo/ci?query=branch:master) |
| `develop` | [![CI](https://kaos.sh/w/kaos-repo/ci.svg?branch=develop)](https://kaos.sh/w/kaos-repo/ci?query=branch:develop) |

### License

[Apache License, Version 2.0](https://www.apache.org/licenses/LICENSE-2.0)

<p align="center"><a href="https://essentialkaos.com"><img src="https://gh.kaos.st/ekgh.svg"/></a></p>
