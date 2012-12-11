Summary:   NSS library for MySQL
Name:      nss-mysql
Version:   1.5
Release:   1
Source0:   http://prdownloads.sourceforge.net/libnss-mysql/libnss-mysql-%{version}.tar.gz
Patch1:    libnss-mysql-multiarch.patch
URL:       http://libnss-mysql.sourceforge.net
License:   GPLv2+
Group:     System/Libraries

BuildRequires: mysql-devel, libtool, autoconf, automake

%description
Store your UNIX user accounts in MySQL. "libnss-mysql" enables the following:

* System-wide authentication and name service using a MySQL database.
  Applications do not need to be MySQL-aware or modified in any way.

* Storing authentication information in a database instead of text files.

* Creation of a single authentication database for multiple servers.
  This is often referred to as the "Single Sign-on" problem.

* Writing data-modification routines (IE self-management web interface).

libnss-mysql is similar to NIS or LDAP. It provides the same centralized
authentication service through a database. What does this mean? Username,
uid, gid, password, etc comes from a MySQL database instead of
/etc/password, /etc/shadow, and /etc/group. A user configured in MySQL will
look and behave just like a user configured in /etc/passwd. Your
applications such as ls, finger, sendmail, qmail, exim, postfix, proftpd,
X, sshd, etc. will all 'see' these users!

%prep
%setup -q -n lib%{name}-%{version} -a 0
%patch1 -p1

%build
libtoolize -f
autoreconf -f
%configure2_5x
%make
# remove non linux samples
rm -rf sample/freebsd sample/solaris

%install
mkdir -p %{buildroot}/{etc,lib}
make DESTDIR=%{buildroot} install
rm -f %{buildroot}/%{_libdir}/libnss_mysql.so

%files
%{_libdir}/*.so.*
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/libnss-mysql.cfg
%attr(0600,root,root) %config(noreplace) %{_sysconfdir}/libnss-mysql-root.cfg
%doc README ChangeLog AUTHORS THANKS NEWS COPYING FAQ DEBUGGING UPGRADING TODO
%doc sample
