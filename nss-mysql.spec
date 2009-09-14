Summary:	MySQL NSS plugin
Name:		nss-mysql
Version:	1.0
Release:	%mkrel 5
URL:		http://www.nongnu.org/nss-mysql/
Group:		System/Libraries
License:	GPLv2+
Source0:	http://savannah.nongnu.org/download/nss-mysql/nss-mysql-%{version}.tar.gz
Source1:	http://savannah.nongnu.org/download/nss-mysql/nss-mysql-%{version}.tar.gz.sig
Patch0:		nss-mysql-build_against_the_shared_mysql_lib.diff
BuildRequires:	mysql-devel
BuildRequires:	libtool
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
NSS-MySQL allows you to authenticate UNIX groups and users using a MySQL
database. It uses the NSS API which provides an abstraction layer between the
UNIX authentication API and the related data. NSS-MySQL currently supports the
passwd, groups and shadow services. NSS-MySQL is highly configurable and
should work with most reasonable database designs.

%prep

%setup -q
%patch0 -p0

# lib64 fix
perl -pi -e "s|/lib\b|/%{_lib}|g" acinclude.m4

%build
rm -f configure
libtoolize --copy --force; aclocal; autoconf

%configure2_5x \
    --enable-group \
    --enable-debug \
    --enable-shadow \
    --with-mysql=%{_prefix}                                              

%make

%install
rm -rf %{buildroot}

%makeinstall_std

install -d %{buildroot}/%{_lib}
mv %{buildroot}%{_libdir}/lib* %{buildroot}/%{_lib}/

# cleanup
rm -f %{buildroot}/%{_lib}/lib*.so
rm -f %{buildroot}/%{_lib}/lib*.*a

%if %mdkversion < 200900
%post -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -p /sbin/ldconfig
%endif

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc AUTHORS COPYING NEWS README SHADOW THANKS TODO UPGRADE sample.sql
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/nss-mysql.conf
%attr(0640,root,root) %config(noreplace) %{_sysconfdir}/nss-mysql-root.conf
%attr(0755,root,root) /%{_lib}/libnss_mysql.so.*
