################################################################################

%global crc_check pushd ../SOURCES ; sha512sum -c %{SOURCE100} ; popd

################################################################################

Summary:              Radically simple IT automation
Name:                 ansible
Version:              2.11.12
Release:              0%{?dist}
URL:                  https://www.ansible.com
License:              GPLv3
Group:                Development/Libraries

Source0:              https://github.com/ansible/ansible/archive/refs/tags/v%{version}.tar.gz
Source100:            checksum.sha512

BuildRoot:            %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:            noarch

BuildRequires:        python3-devel python3-setuptools

Requires:             python36-PyYAML python3-setuptools python36-jinja2
Requires:             python36-crypto sshpass

Provides:             %{name} = %{version}-%{release}

################################################################################

%description

Ansible is a radically simple model-driven configuration management,
multi-node deployment, and orchestration engine. Ansible works
over SSH and does not require any software or daemons to be installed
on remote nodes. Extension modules can be written in any language and
are transferred to managed machines automatically.

################################################################################

%prep
%{crc_check}

%setup -q

%build
%{py3_build}

%install
rm -rf %{buildroot}

%{py3_install}

if expr x'%{python3_sitelib}' : 'x.*dist-packages/\?' ; then
  DEST_DIR='%{buildroot}%{python3_sitelib}'
  SOURCE_DIR=$(echo "$DEST_DIR" | sed 's/dist-packages/site-packages/g')

  if [[ -d "$SOURCE_DIR" && ! -d "$DEST_DIR" ]] ; then
    mv $SOURCE_DIR $DEST_DIR
  fi
fi

mkdir -p %{buildroot}%{_sysconfdir}/%{name}/
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_datadir}/%{name}

cp examples/ansible.cfg %{buildroot}%{_sysconfdir}/%{name}/

sed -i 's/#deprecation_warnings = True/deprecation_warnings = False/' \
       %{buildroot}%{_sysconfdir}/%{name}/%{name}.cfg

%clean
rm -rf %{buildroot}

################################################################################

%files
%defattr(-,root,root,-)
%doc README.rst COPYING licenses/*
%config(noreplace) %{_sysconfdir}/%{name}/%{name}.cfg
%dir %{_datadir}/%{name}
%{_bindir}/%{name}*
%{python3_sitelib}/%{name}*

################################################################################

%changelog
* Mon Feb 10 2020 Anton Novojilov <andy@essentialkaos.com> - 2.11.12-0
- Initial build for kaos repository
