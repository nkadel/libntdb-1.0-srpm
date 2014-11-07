%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print(get_python_version())")}

Name: libntdb
Version: 1.0
Release: 0.2%{?dist}
Group: System Environment/Daemons
Summary: The ntdb library
License: LGPLv3+
URL: http://ntdb.samba.org/
Source: https://www.samba.org/ftp/ntdb/ntdb-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python-devel

# Patches

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Ntdb library
Requires: libntdb = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Ntdb library.

%package -n ntdb-tools
Group: Development/Libraries
Summary: Developer tools for the Ntdb library
Requires: libntdb = %{version}-%{release}

%description -n ntdb-tools
Tools to manage Ndb files

%prep
%setup -q -n ntdb-%{version}

%build
%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules

make V=1

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libntdb.a
rm -f $RPM_BUILD_ROOT/usr/share/swig/*/ntdb.i

# Hackery to install ntdb man pages
# Grab *ALL* man pages first, indiscriminately, so new categories
# error out
mkdir -p $RPM_BUILD_ROOT %{_mandir}
install -m 644 bin/default/man/*.* $RPM_BUILD_ROOT/%{_mandir}/

# Compress and deploy to mandir subdirectories as needed
mkdir -p $RPM_BUILD_ROOT %{_mandir}/man3
mv $RPM_BUILD_ROOT/%{_mandir}/*.3 $RPM_BUILD_ROOT/%{_mandir}/man3
gzip -9 $RPM_BUILD_ROOT/%{_mandir}/man3/*.3

mkdir -p $RPM_BUILD_ROOT %{_mandir}/man3
mv $RPM_BUILD_ROOT/%{_mandir}/*.8 $RPM_BUILD_ROOT/%{_mandir}/man8
gzip -9 $RPM_BUILD_ROOT/%{_mandir}/man8/*.8

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libntdb.so.*

%files -n ntdb-tools
%{_bindir}/ntdb*
%{_mandir}/man3/*
%{_mandir}/man8/*

%files devel
%defattr(-,root,root,-)
%{_includedir}/ntdb.h
%{_libdir}/*.so
%{_libdir}/ntdb/*.so
%{_libdir}/pkgconfig/ntdb.pc
%{python_sitearch}/ntdb.so

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%changelog
* Sun Mar 16 2014 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0-0.2
- Discard doxygen requirements and actions, wbscript cenerates man pages
- Manually deploy and compress man pages in correct target mandirs
- Discard pyntdb packaging from libtalloc
- Add ntdb-tools package

* Sun Nov 24 2013 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0-0.1
- First libntdb package, based on libtalloc
