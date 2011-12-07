Name: compat-dapl
Epoch: 1
Version: 1.2.15
Release: 2.1%{?dist}
Summary: Library providing access to the DAT 1.2 API
Group: System Environment/Libraries
Obsoletes: udapl < 1.3, dapl < 1.2.2, compat-dapl-1.2.5 < 2.1
License: GPLv2 or BSD or CPL
Url: http://openfabrics.org/
Source0: http://www.openfabrics.org/downloads/dapl/%{name}-%{version}.tar.gz
Patch0: compat-dapl-1.2.15-pipe-leak.patch
Patch1: compat-dapl-1.2.15-cma-memleak-verbs-CQ-compl-chans-fix.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires(post): /sbin/ldconfig
Requires(postun): /sbin/ldconfig
BuildRequires: libibverbs-devel >= 1.1.3, librdmacm-devel >= 1.0.10
BuildRequires: autoconf, libtool dapl-devel
ExclusiveArch: i386 x86_64 ia64 ppc ppc64
%description
The DAT programming API provides a means of utilizing high performance
network technologies, such as InfiniBand and iWARP, without needing to
write your program to use those technologies directy.  This package
contains the libraries that implement version 1.2 of the DAT API.  The
current (and recommended version for any new code) is 2.0.  These 1.2
libraries are provided solely for backward compatibily.

%package devel
Summary: Development files for the dapl-1.2 compat libdat and libdapl libraries
Group: System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
Obsoletes: udapl-devel < 1.3, dapl-devel < 1.2.2, compat-dapl-devel-1.2.5 < 2.1
%description devel
Header files for the dapl-1.2 compat libdat and libdapl library.

%package static
Summary: Static libdat and libdapl libraries
Group: System Environment/Libraries
Requires: %{name}-devel = %{epoch}:%{version}-%{release}
Obsoletes: dapl-devel-static < 1.2.14, compat-dapl-static-1.2.5 < 2.1
%description static
Static versions of the dapl-1.2 compat libdat and libdapl libraries.

%package utils
Summary: Test suites for dapl 1.2 libraries
Group: System Environment/Libraries
Requires: %{name} = %{epoch}:%{version}-%{release}
%description utils
Useful test suites to validate the dapl library API's and operation.

%prep
%setup -q
%patch0 -p1 -b .pipe_leak
%patch1 -p1 -b .mem_leak
aclocal -I config && libtoolize --force --copy && autoheader && \
    automake --foreign --add-missing --copy && autoconf

%build
%configure CFLAGS="$CFLAGS -fno-strict-aliasing" --sysconfdir=%{_sysconfdir}/rdma/compat-dapl
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install
# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_libdir}/*.la %{buildroot}%{_mandir}/man5/*

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%{_libdir}/libdat.so.*
%{_libdir}/libdaplcma.so.*
%{_libdir}/libdaplscm.so.*
%config(noreplace) %{_sysconfdir}/rdma/compat-dapl/dat.conf
%doc AUTHORS ChangeLog COPYING README

%files devel
%defattr(-,root,root,-)
%{_libdir}/libdat.so
%{_libdir}/libdaplcma.so
%{_libdir}/libdaplscm.so
%dir %{_includedir}/dat
%{_includedir}/dat/*

%files static
%defattr(-,root,root,-)
%{_libdir}/libdat.a
%{_libdir}/libdaplcma.a
%{_libdir}/libdaplscm.a

%files utils
%defattr(-,root,root,-)
%{_bindir}/*1
%{_mandir}/man1/*1.1.gz

%changelog
* Mon Aug 01 2010 Jay Fenlason <fenlason@redhat.com> - 1:1.2.15-2.1.el6
- Include pipe-leak patch to close
  Resolves: rhbz619439 - OFED1.5.1: uDAPL - cma: memory leak of FD's (DB2 pureScale)
  This required some whitspace editing--apparently the patch was garbled
  somewhere in transit.
- Include the cma-memleak-verbs-CQ-compl-chans-fix patch to close
  Resolves: rhbz619443 - OFED1.5.1: uDAPL handles close on forked child exit (DB2 pureScale)

* Sun Mar 07 2010 Doug Ledford <dledford@redhat.com> - 1:1.2.15-2.el6
- Fix various rpmlint wanrings in spec file
- Version all of the obsoletes
- Now that this is no longer part of the dapl rpm, it needs its own
  doc macro so that the license and whatnot are on the system when the
  package is installed
- Related: bz555835

* Thu Jan 21 2010 Jay Fenlason <fenlason@redhat.com> 1:1.2.15-1.el5
- Change sysconfig file to /etc/rdma/compat-dapl to match the change in dapl
- Split out into separate source rpm from the dapl-2.0.25-2.el5.src.rpm
  Resolves: rhbz#557170 split compat-dapl into a separate srpm
