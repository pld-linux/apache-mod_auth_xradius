#
%define		mod_name	auth_xradius
%define		apxs		%{_sbindir}/apxs
Summary:	Apache module:
Name:		apache-mod_%{mod_name}
Version:	0.4.6
Release:	5
License:	GPL
Group:		Networking/Daemons/HTTP
Source0:	http://www.outoforder.cc/downloads/mod_auth_xradius/mod_auth_xradius-%{version}.tar.bz2
# Source0-md5:	eeecc96f15dec9fe0a9c78c0b022903d
Source1:	%{name}.conf
Patch0:		mod_auth_xradius-unixd.patch
URL:		http://www.outoforder.cc/projects/apache/mod_auth_xradius/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.2
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
Requires:	apache-mod_auth_basic >= 2.2
Requires:	apache-mod_authz_user >= 2.2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
mod_auth_xradius provides high performance authentication against RFC
2865 RADIUS Servers. Features:
- Supports popular RADIUS Servers including OpenRADIUS, FreeRADIUS and
  commercial servers.
- Distributed Authentication Cache using apr_memcache.
- Local Authentication Cache using DBM.
- Uses standard HTTP Basic Authentication, unlike mod_auth_radius
  which uses cookies for sessions.

%prep
%setup -q -n mod_%{mod_name}-%{version}
%patch0 -p1

%build
%configure

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

%{__make} install \
        DESTDIR=$RPM_BUILD_ROOT

install %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_%{mod_name}.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/*_mod_%{mod_name}.conf
%attr(755,root,root) %{_pkglibdir}/*
