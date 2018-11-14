################################################################################

%{!?python_sitelib: %global python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?rhel} == 5
%define __python /usr/bin/python26
%endif

################################################################################

Summary:              Radically simple IT automation
Name:                 ansible
Version:              2.6.7
Release:              0%{?dist}
URL:                  http://www.ansible.com
License:              GPLv3
Group:                Development/Libraries

Source:               http://releases.ansible.com/ansible/%{name}-%{version}.tar.gz

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:            noarch

%if 0%{?rhel} && 0%{?rhel} <= 5
BuildRequires:        python26-devel
BuildRequires:        python26-setuptools

Requires:             python26-PyYAML python26-paramiko python26-jinja2
Requires:             python26-keyczar python26-httplib2 python26-setuptools
Requires:             python26-six
%endif

%if 0%{?rhel} && 0%{?rhel} > 5
BuildRequires:        python2-devel
BuildRequires:        python-setuptools

Requires:             PyYAML python-markupsafe python-paramiko python-jinja2
Requires:             python-keyczar python-httplib2 python-setuptools
Requires:             python-crypto python-six
%endif

%if 0%{?fedora} >= 18
BuildRequires:        python-devel
BuildRequires:        python-setuptools

Requires:             PyYAML python-paramiko python-jinja2 python-keyczar
Requires:             python-httplib2 python-setuptools python-six
%endif

%if 0%{?suse_version}
BuildRequires:        python-devel
BuildRequires:        python-setuptools

Requires:             python-paramiko python-jinja2 python-keyczar python-yaml
Requires:             python-httplib2 python-setuptools python-six
%endif

Requires:             sshpass

################################################################################

%description

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and orchestration engine. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

################################################################################

%prep
%setup -q

%build
python setup.py build

%install
rm -rf %{buildroot}

python setup.py install -O1 --prefix=%{_prefix} --root=%{buildroot}

if expr x'%{python_sitelib}' : 'x.*dist-packages/\?' ; then
    DEST_DIR='%{buildroot}%{python_sitelib}'
    SOURCE_DIR=$(echo "$DEST_DIR" | sed 's/dist-packages/site-packages/g')
    if [[ -d "$SOURCE_DIR" && ! -d "$DEST_DIR" ]] ; then
        mv $SOURCE_DIR $DEST_DIR
    fi
fi

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_datadir}/%{name}

cp examples/hosts %{buildroot}%{_sysconfdir}/%{name}/
cp examples/ansible.cfg %{buildroot}%{_sysconfdir}/%{name}/
cp -v docs/man/man1/*.1 %{buildroot}%{_mandir}/man1/

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.rst PKG-INFO COPYING
%doc %{_mandir}/man1/%{name}*
%config(noreplace) %{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%{python_sitelib}/%{name}*
%{_bindir}/%{name}*

################################################################################

%changelog
* Thu Nov 15 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.7-0
- Updated to latest version

* Wed Sep 26 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.4-0
- Updated to latest version

* Fri Aug 31 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.3-0
- Updated to latest version

* Fri Jul 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.6.1-0
- Updated to latest version

* Sat Jun 09 2018 Anton Novojilov <andy@essentialkaos.com> - 2.5.4-0
- Updated to latest version

* Tue Feb 06 2018 Anton Novojilov <andy@essentialkaos.com> - 2.4.3.0-0
- Updated to latest version

* Thu Nov 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.4.1.0-0
- Updated to latest version

* Sat Sep 16 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.2.0-0
- Updated to latest version

* Sat Jul 08 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.1.0-0
- Updated to latest version

* Tue May 09 2017 Anton Novojilov <andy@essentialkaos.com> - 2.3.0.0-0
- Updated to latest version

* Sat Jan 21 2017 Anton Novojilov <andy@essentialkaos.com> - 2.2.1.0-0
- Updated to latest version

* Sun Oct 16 2016 Anton Novojilov <andy@essentialkaos.com> - 2.1.2.0-0
- Updated to latest version

* Mon Sep 05 2016 Anton Novojilov <andy@essentialkaos.com> - 2.1.1.0-0
- Updated to latest version

* Thu May 26 2016 Gleb Goncharov <inbox@gongled.ru> - 2.1.0.0-0
- Updated to latest version

* Mon May 23 2016 Gleb Goncharov <inbox@gongled.ru> - 2.0.2.0-0
- Updated to latest version

* Tue Mar 01 2016 Gleb Goncharov <inbox@gongled.ru> - 2.0.1.0-0
- Updated to latest version

* Sun Jan 31 2016 Gleb Goncharov <inbox@gongled.ru> - 2.0.0.1-0
- Initial build
