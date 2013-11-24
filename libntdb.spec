%if ! (0%{?fedora} > 12 || 0%{?rhel} > 5)
%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%endif
%{!?python_version: %global python_version %(%{__python} -c "from distutils.sysconfig import get_python_version; print(get_python_version())")}

Name: libntdb
Version: 1.0
Release: 0.1%{?dist}
Group: System Environment/Daemons
Summary: The ntdb library
License: LGPLv3+
URL: http://ntdb.samba.org/
Source: http://samba.org/ftp/ntdb/ntdb-%{version}.tar.gz
BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires: autoconf
BuildRequires: libxslt
BuildRequires: docbook-style-xsl
BuildRequires: python-devel
BuildRequires: doxygen

# Patches

%description
A library that implements a hierarchical allocator with destructors.

%package devel
Group: Development/Libraries
Summary: Developer tools for the Ntdb library
Requires: libntdb = %{version}-%{release}

%description devel
Header files needed to develop programs that link against the Ntdb library.

%package -n pyntdb
Group: Development/Libraries
Summary: Developer tools for the Ntdb library
Requires: libntdb = %{version}-%{release}
Obsoletes: pyntdb < %{version}-%{release}

%description -n pyntdb
Pyntdb libraries for creating python bindings using ntdb

%package -n pyntdb-devel
Group: Development/Libraries
Summary: Developer tools for the Ntdb library
Requires: pyntdb = %{version}-%{release}
Obsoletes: pyntdb-devel < %{version}-%{release}

%description -n pyntdb-devel
Development libraries for pyntdb

%prep
%setup -q -n ntdb-%{version}

%build
%configure --disable-rpath \
           --disable-rpath-install \
           --bundled-libraries=NONE \
           --builtin-libraries=replace \
           --disable-silent-rules

make %{?_smp_mflags} V=1
doxygen doxy.config

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

# Shared libraries need to be marked executable for
# rpmbuild to strip them and include them in debuginfo
find $RPM_BUILD_ROOT -name "*.so*" -exec chmod -c +x {} \;

rm -f $RPM_BUILD_ROOT%{_libdir}/libntdb.a
rm -f $RPM_BUILD_ROOT/usr/share/swig/*/ntdb.i

# Install API docs
cp -a doc/man/* $RPM_BUILD_ROOT/%{_mandir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%{_libdir}/libntdb.so.*

%files devel
%defattr(-,root,root,-)
%{_includedir}/ntdb.h
%{_libdir}/libntdb.so
%{_libdir}/pkgconfig/ntdb.pc
%{_mandir}/man3/ntdb*.3.gz
%{_mandir}/man3/libntdb*.3.gz

%files -n pyntdb
%defattr(-,root,root,-)
%{_libdir}/libpyntdb-util.so.*
%{python_sitearch}/ntdb.so

%files -n pyntdb-devel
%defattr(-,root,root,-)
%{_includedir}/pyntdb.h
%{_libdir}/pkgconfig/pyntdb-util.pc
%{_libdir}/libpyntdb-util.so

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

%post -n pyntdb -p /sbin/ldconfig
%postun -n pyntdb -p /sbin/ldconfig

%changelog
* Sun Nov 24 2013 Nico Kadel-Garcia <nkadel@gmail.com> - 1.0-0.1
- First libntdb package, based on libtalloc
