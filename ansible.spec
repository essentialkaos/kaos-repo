################################################################################

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}

%if 0%{?rhel} == 5
%define __python /usr/bin/python26
%endif

################################################################################

Summary:              Radically simple IT automation
Name:                 ansible
Version:              2.1.0.0
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
%{__python} setup.py build


%install
rm -rf %{buildroot}

%{__python} setup.py install -O1 --prefix=%{_prefix} --root=%{buildroot}

if expr x'%{python_sitelib}' : 'x.*dist-packages/\?' ; then
    DEST_DIR='%{buildroot}%{python_sitelib}'
    SOURCE_DIR=$(echo "$DEST_DIR" | sed 's/dist-packages/site-packages/g')
    if [[ -d "$SOURCE_DIR" && ! -d "$DEST_DIR" ]] ; then
        mv $SOURCE_DIR $DEST_DIR
    fi
fi

%{__mkdir_p} %{buildroot}%{_sysconfdir}/%{name}/
%{__mkdir_p} %{buildroot}%{_mandir}/man1/
%{__mkdir_p} %{buildroot}%{_datadir}/%{name}

cp examples/hosts %{buildroot}%{_sysconfdir}/%{name}/
cp examples/ansible.cfg %{buildroot}%{_sysconfdir}/%{name}/
cp -v docs/man/man1/*.1 %{buildroot}%{_mandir}/man1/


%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.md PKG-INFO COPYING
%doc %{_mandir}/man1/%{name}*
%config(noreplace) %{_sysconfdir}/%{name}
%dir %{_datadir}/%{name}
%{python_sitelib}/%{name}*
%{_bindir}/%{name}*

################################################################################

%changelog
* Thu May 26 2016 Gleb Goncharov <inbox@gongled.ru> - 2.1.0.0-0
- Updated to latest version

* Mon May 23 2016 Gleb Goncharov <inbox@gongled.ru> - 2.0.2.0-0
- Updated to latest version

* Tue Mar 01 2016 Gleb Goncharov <inbox@gongled.ru> - 2.0.1.0-0
- Updated to latest version

* Sun Jan 31 2016 Gleb Goncharov <inbox@gongled.ru> - 2.0.0.1-0
- Initial build
