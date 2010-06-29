%define initdir %{_sysconfdir}/rc.d/init.d
%define auth %(test -f /etc/pam.d/system-auth && echo /etc/pam.d/system-auth || echo)

Summary: The Samba SMB server.
Name: samba
Version: 2.2.7
Release: 2_afstoken
License: GNU GPL Version 2
Group: System Environment/Daemons
URL: http://www.samba.org/

Source: ftp://us2.samba.org/pub/samba/%{name}-%{version}.tar.bz2

# Red Hat specific replacement-files
Source1: samba.log
Source2: samba.xinetd
Source3: swat.desktop
Source4: samba.sysconfig
Source5: smb.init
Source6: samba.pamd
Source7: smbprint
Source8: winbind.init

# Don't depend on Net::LDAP
Source999: filter-requires-samba.sh

# generic patches
Patch0: samba-2.2.4-smb.conf.patch
Patch1: samba-2.2.0-smbw.patch
Patch3: samba-2.0.5a-gawk.patch
Patch5: samba-2.0.7-krb5-1.2.patch
Patch6: samba-2.0.7-buildroot.patch
Patch7: samba-2.2.3a-smbpass.patch
Patch11: samba-2.2.0-logname.patch
Patch13: samba-2.2.2-winsfixes.patch
Patch14: samba-2.2.3-smbadduserloc.patch
Patch15: samba-2.2.7-lfsclient.patch
# Not used, but it have some patches which might be needed later...
Patch16: samba-2.2.2-smbadduser.patch
Patch17: samba-2.2.7-afstoken.patch

Requires: pam >= 0.64 %{auth} samba-common = %{version} 
Requires: logrotate >= 3.4 initscripts >= 5.54-1 
BuildRoot: %{_tmppath}/%{name}-%{version}-root
Prereq: /sbin/chkconfig /bin/mktemp /usr/bin/killall
Prereq: fileutils sed /etc/init.d 
BuildRequires: pam-devel, readline-devel, ncurses-devel, fileutils, libacl-devel


# Working around perl dependency problem from docs
%define __find_requires %{SOURCE999}

%description
Samba is the protocol by which a lot of PC-related machines share
files, printers, and other information (such as lists of available
files and printers). The Windows NT, OS/2, and Linux operating systems
support this natively, and add-on packages can enable the same thing
for DOS, Windows, VMS, UNIX of all kinds, MVS, and more. This package
provides an SMB server that can be used to provide network services to
SMB (sometimes called "Lan Manager") clients. Samba uses NetBIOS over
TCP/IP (NetBT) protocols and does NOT need the NetBEUI (Microsoft Raw
NetBIOS frame) protocol.

%package client
Summary: Samba (SMB) client programs.
Group: Applications/System
Requires: samba-common = %{version}
Obsoletes: smbfs

%description client
The samba-client package provides some SMB clients to compliment the
built-in SMB filesystem in Linux. These clients allow access of SMB
shares and printing to SMB printers.

%package common
Summary: Files used by both Samba servers and clients.
Group: Applications/System

%description common
Samba-common provides files necessary for both the server and client
packages of Samba.

%package swat
Summary: The Samba SMB server configuration program.
Group: Applications/System
Requires: samba = %{version} xinetd

%description swat
The samba-swat package includes the new SWAT (Samba Web Administration
Tool), for remotely managing Samba's smb.conf file using your favorite
Web browser.

%prep
%setup -q

# copy Red Hat specific scripts
cp %{SOURCE5} packaging/RedHat/
cp %{SOURCE6} packaging/RedHat/
cp %{SOURCE7} packaging/RedHat/
cp %{SOURCE8} packaging/RedHat/winbind.init

%patch0 -p1 -b .oldconf
%patch1 -p1 -b .smbw
%patch3 -p1 -b .gawk
%patch5 -p1 -b .krb5-1.2
%patch6 -p1 -b .buildroot
%patch7 -p1 -b .smbpass
%patch13 -p1 -b .winsfixes
%patch14 -p1 -b .locfix
%patch15 -p1 -b .lfs
%patch17 -p1 -b .afstoken

%build

cd source
%ifarch i386 sparc
RPM_OPT_FLAGS="$RPM_OPT_FLAGS -D_FILE_OFFSET_BITS=64"
%endif

#bug in 2.2.4
perl -pi -e "s|-symbolic||" Makefile.in

%configure \
	--libdir=%{_sysconfdir}/samba \
	--with-fhs \
	--with-privatedir=%{_sysconfdir}/samba \
	--with-lockdir=/var/cache/samba \
	--with-swatdir=%{_datadir}/swat \
	--with-codepagedir=%{_datadir}/samba/codepages \
	--without-automount \
	--without-smbmount \
	--without-pam \
	--without-mmap \
	--without-quotas \
	--without-smbwrapper \
	--without-libsmbclient \
	--without-utmp \
	--with-piddir=/var/run/samba \
	--without-acl-support \
	--with-afs \
	--with-ssl \
	--without-vfs
#	--without-pam_smbpass \


make  CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE" \
	all smbfilter nsswitch/libnss_wins.so debug2html

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT/sbin
mkdir -p $RPM_BUILD_ROOT/usr/{sbin,bin}
mkdir -p $RPM_BUILD_ROOT/%{initdir}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/{pam.d,logrotate.d}
mkdir -p $RPM_BUILD_ROOT/var/{log,spool}/samba
mkdir -p $RPM_BUILD_ROOT/var/cache/samba
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/swat/using_samba
mkdir -p $RPM_BUILD_ROOT/%{_datadir}/samba/codepages 

cd source

%makeinstall \
	BINDIR=$RPM_BUILD_ROOT%{_bindir} \
	BASEDIR=$RPM_BUILD_ROOT%{_prefix} \
	SBINDIR=$RPM_BUILD_ROOT%{_sbindir} \
	DATADIR=$RPM_BUILD_ROOT%{_datadir} \
	LOCKDIR=$RPM_BUILD_ROOT/var/cache/samba \
	PRIVATEDIR=$RPM_BUILD_ROOT%{_sysconfdir}/samba \
	LIBDIR=$RPM_BUILD_ROOT%{_sysconfdir}/samba \
	CONFIGDIR=$RPM_BUILD_ROOT%{_sysconfdir}/samba \
	VARDIR=$RPM_BUILD_ROOT/var/log/samba \
	CODEPAGEDIR=$RPM_BUILD_ROOT%{_datadir}/samba/codepages \
	SWATDIR=$RPM_BUILD_ROOT%{_datadir}/swat \
	SAMBABOOK=$RPM_BUILD_ROOT%{_datadir}/swat/using_samba \
	PIDDIR=$RPM_BUILD_ROOT/var/run/samba

cd ..

# Install other stuff
install -m644 packaging/RedHat/smb.conf $RPM_BUILD_ROOT%{_sysconfdir}/samba/smb.conf
install -m755 source/script/mksmbpasswd.sh $RPM_BUILD_ROOT%{_bindir}
install -m644 packaging/RedHat/smbusers $RPM_BUILD_ROOT/etc/samba/smbusers
install -m755 packaging/RedHat/smbprint $RPM_BUILD_ROOT%{_bindir}
install -m755 source/script/smbadduser $RPM_BUILD_ROOT%{_bindir}
install -m755 packaging/RedHat/smb.init $RPM_BUILD_ROOT%{initdir}/smb
install -m755 packaging/RedHat/winbind.init $RPM_BUILD_ROOT%{initdir}/winbind
ln -s ../..%{initdir}/smb  $RPM_BUILD_ROOT%{_sbindir}/samba
install -m644 packaging/RedHat/samba.pamd.stack $RPM_BUILD_ROOT/etc/pam.d/samba
install -m644 $RPM_SOURCE_DIR/samba.log $RPM_BUILD_ROOT/etc/logrotate.d/samba
echo 127.0.0.1 localhost > $RPM_BUILD_ROOT%{_sysconfdir}/samba/lmhosts

# pam_smbpass
mkdir -p $RPM_BUILD_ROOT/lib/security
#mv $RPM_BUILD_ROOT%{_bindir}/pam_smbpass.so $RPM_BUILD_ROOT/lib/security/pam_smbpass.so
#cp -r source/pam_smbpass/ docs/
rm -f docs/pam_smbpass/*.*

# winbind
mkdir -p $RPM_BUILD_ROOT/lib
install -m 755 source/nsswitch/libnss_winbind.so $RPM_BUILD_ROOT/lib/libnss_winbind.so
install -m 755 source/nsswitch/libnss_wins.so $RPM_BUILD_ROOT/lib/libnss_wins.so
ln -s libnss_wins.so  $RPM_BUILD_ROOT/lib/libnss_wins.so.2
ln -s libnss_winbind.so  $RPM_BUILD_ROOT/lib/libnss_winbind.so.2

# VFS - recycling

# libsmbclient

mkdir -p $RPM_BUILD_ROOT/usr/{lib,include}


mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d
install -m644 %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/xinetd.d/swat

mkdir -p $RPM_BUILD_ROOT/usr/share/applications/
install -m644 %{SOURCE3} $RPM_BUILD_ROOT/usr/share/applications/samba-swat.desktop

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig
install -m644 %{SOURCE4} $RPM_BUILD_ROOT%{_sysconfdir}/sysconfig/samba

# remove this or it ends up in %doc
rm -rf docs/htmldocs/using_samba
rm -rf docs/faq/*sgml

# remove html'ized man pages:
rm -rf docs/htmldocs/*.[0-9].*

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/chkconfig --add smb


%preun
if [ $1 = 0 ] ; then
    /sbin/chkconfig --del smb
    /sbin/chkconfig --del winbind
    rm -rf /var/log/samba/* /var/cache/samba/*
    /sbin/service smb stop >/dev/null 2>&1
fi
exit 0

%postun
if [ "$1" -ge "1" ]; then
	%{initdir}/smb condrestart >/dev/null 2>&1
fi	

%post common
/sbin/chkconfig --add winbind

%preun common
if [ $1 = 0 ] ; then
    /sbin/chkconfig --del winbind
    /sbin/service winbind stop >/dev/null 2>&1
fi
exit 0

%triggerpostun -- samba < 1.9.18p7
if [ $1 != 0 ]; then
    /sbin/chkconfig --add smb
fi

%triggerpostun -- samba < 2.0.5a-3
if [ $1 != 0 ]; then
    [ ! -d /var/lock/samba ] && mkdir -m 0755 /var/lock/samba
    [ ! -d /var/spool/samba ] && mkdir -m 1777 /var/spool/samba
    chmod 644 /etc/services
    [ -f /etc/inetd.conf ] && chmod 644 /etc/inetd.conf
fi

%files
%defattr(-,root,root)
%doc README COPYING Manifest 
%doc WHATSNEW.txt Roadmap
%doc docs
%doc examples/autofs examples/LDAP examples/libsmbclient examples/misc examples/printer-accounting
%doc examples/printing

#attr(755,root,root) /lib/security/pam_smbpass.so
%{_sbindir}/smbd
%{_sbindir}/nmbd
%{_bindir}/make_unicodemap
%{_bindir}/mksmbpasswd.sh
%{_bindir}/smbcontrol
%{_bindir}/smbstatus
%{_bindir}/smbadduser
%{_bindir}/tdbbackup
%config(noreplace) %{_sysconfdir}/sysconfig/samba
%config(noreplace) %{_sysconfdir}/samba/smbusers
%attr(755,root,root) %config %{initdir}/smb
%config(noreplace) %{_sysconfdir}/logrotate.d/samba
%config(noreplace) %{_sysconfdir}/pam.d/samba

%dir /var/cache/samba
%dir /var/run/samba
%attr(0700,root,root) %dir /var/log/samba
%attr(1777,root,root) %dir /var/spool/samba

%files swat
%defattr(-,root,root)
/usr/share/applications/*
%config(noreplace) %{_sysconfdir}/xinetd.d/swat
%{_datadir}/swat
%{_sbindir}/swat

%files client
%defattr(-,root,root)
%{_bindir}/rpcclient
%{_bindir}/smbcacls
%{_bindir}/nmblookup
%{_bindir}/smbclient
%{_bindir}/smbprint
%{_bindir}/smbspool
%{_bindir}/smbtar

%files common
%defattr(-,root,root)
/lib/libnss_wins.so
/lib/libnss_wins.so.2
/lib/libnss_winbind.so
/lib/libnss_winbind.so.2
%{_bindir}/make_smbcodepage
%{_bindir}/testparm
%{_bindir}/testprns
%{_bindir}/smbpasswd
%{_bindir}/make_printerdef
%{_bindir}/wbinfo

%{_sbindir}/winbindd
%config(noreplace) %{_sysconfdir}/samba/smb.conf
%config(noreplace) %{_sysconfdir}/samba/lmhosts
%dir %{_datadir}/samba
%dir %{_datadir}/samba/codepages
%dir %{_sysconfdir}/samba
%{initdir}/winbind
%{_datadir}/samba/codepages/*

%changelog
* Wed Nov 20 2002 Bill Nottingham <notting@redhat.com> 2.2.7-2
- update to 2.2.7
- add patch for LFS in smbclient (<tcallawa@redhat.com>)

* Wed Aug 28 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-10
- logrotate fixes (#65007)

* Mon Aug 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-9
- /usr/lib was used in place of %%{_libdir} in three locations (#72554)

* Mon Aug  5 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-8
- Initscript fix (#70720)

* Fri Jul 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-7
- Enable VFS support and compile the "recycling" module (#69796)
- more selective includes of the examples dir 

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-6
- Fix the lpq parser for better handling of LPRng systems (#69352)

* Tue Jul 23 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-5
- desktop file fixes (#69505)

* Wed Jun 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-4
- Enable ACLs

* Tue Jun 25 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-3
- Make it not depend on Net::LDAP - those are doc files and examples

* Fri Jun 21 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Thu Jun 20 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.5-1
- 2.2.5

* Fri Jun 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.4-5
- Move the post/preun of winbind into the -common subpackage, 
  where the script is (#66128)

* Tue Jun  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.4-4
- Fix pidfile locations so it runs properly again (2.2.4 
  added a new directtive - #65007)

* Thu May 23 2002 Tim Powers <timp@redhat.com>
- automated rebuild

* Tue May 14 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.4-2
- Fix #64804

* Thu May  9 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.4-1
- 2.2.4
- Removed some zero-length and CVS internal files
- Make it build

* Wed Apr 10 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-6
- Don't use /etc/samba.d in smbadduser, it should be /etc/samba

* Thu Apr  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-5
- Add libsmbclient.a w/headerfile for KDE (#62202)

* Tue Mar 26 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-4
- Make the logrotate script look the correct place for the pid files 

* Thu Mar 14 2002 Nalin Dahyabhai <nalin@redhat.com> 2.2.3a-3
- include interfaces.o in pam_smbpass.so, which needs symbols from interfaces.o
  (patch posted to samba-list by Ilia Chipitsine)

* Thu Feb 21 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-2
- Rebuild

* Thu Feb  7 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3a-1
- 2.2.3a

* Mon Feb  4 2002 Trond Eivind Glomsrød <teg@redhat.com> 2.2.3-1
- 2.2.3

* Thu Nov 29 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-8
- New pam configuration file for samba

* Tue Nov 27 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-7
- Enable PAM session controll and password sync

* Tue Nov 13 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-6
- Move winbind files to samba-common. Add separate initscript for
  winbind 
- Fixes for winbind - protect global variables with mutex, use
  more secure getenv

* Thu Nov  8 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-5
- Teach smbadduser about "getent passwd" 
- Fix more pid-file references
- Add (conditional) winbindd startup to the initscript, configured in
  /etc/sysconfig/samba

* Wed Nov  7 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-4
- Fix pid-file reference in logrotate script
- include pam and nss modules for winbind

* Mon Nov  5 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-3
- Add "--with-utmp" to configure options (#55372)
- Include winbind, pam_smbpass.so, rpcclient and smbcacls
- start using /var/cache/samba, we need to keep state and there is
  more than just locks involved

* Sat Nov 03 2001 Florian La Roche <Florian.LaRoche@redhat.de> 2.2.2-2
- add "reload" to the usage string in the startup script

* Mon Oct 15 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.2-1
- 2.2.2

* Tue Sep 18 2001 Trond Eivind Glomsrød <teg@redhat.com> 2.2.1a-5
- Add patch from Jeremy Allison to fix IA64 alignment problems (#51497)

* Mon Aug 13 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Don't include smbpasswd in samba, it's in samba-common (#51598)
- Add a disabled "obey pam restrictions" statement - it's not
  active, as we use encrypted passwords, but if the admin turns
  encrypted passwords off the choice is available. (#31351)

* Wed Aug  8 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Use /var/cache/samba instead of /var/lock/samba 
- Remove "domain controller" keyword from smb.conf, it's 
  deprecated (from #13704)
- Sync some examples with smb.conf.default
- Fix password synchronization (#16987)

* Fri Jul 20 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Tweaks of BuildRequires (#49581)

* Wed Jul 11 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.2.1a bugfix release

* Tue Jul 10 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.2.1, which should work better for XP

* Sat Jun 23 2001 Trond Eivind Glomsrød <teg@redhat.com>
- 2.2.0a security fix
- Mark lograte and pam configuration files as noreplace

* Fri Jun 22 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add the /etc/samba directory to samba-common

* Thu Jun 21 2001 Trond Eivind Glomsrød <teg@redhat.com>
- Add improvements to the smb.conf as suggested in #16931

* Tue Jun 19 2001 Trond Eivind Glomsrød <teg@redhat.com>
  (these changes are from the non-head version)
- Don't include /usr/sbin/samba, it's the same as the initscript
- unset TMPDIR, as samba can't write into a TMPDIR owned 
  by root (#41193)
- Add pidfile: lines for smbd and nmbd and a config: line
  in the initscript  (#15343)
- don't use make -j
- explicitly include /usr/share/samba, not just the files in it

* Tue Jun 19 2001 Bill Nottingham <notting@redhat.com>
- mount.smb/mount.smbfs go in /sbin, *not* %%{_sbindir}

* Fri Jun  8 2001 Preston Brown <pbrown@redhat.com>
- enable encypted passwords by default

* Thu Jun  7 2001 Helge Deller <hdeller@redhat.de> 
- build as 2.2.0-1 release
- skip the documentation-directories docbook, manpages and yodldocs
- don't include *.sgml documentation in package
- moved codepage-directory to /usr/share/samba/codepages
- make it compile with glibc-2.2.3-10 and kernel-headers-2.4.2-2   

* Mon May 21 2001 Helge Deller <hdeller@redhat.de> 
- updated to samba 2.2.0
- moved codepages to %{_datadir}/samba/codepages
- use all available CPUs for building rpm packages
- use %{_xxx} defines at most places in spec-file
- "License:" replaces "Copyright:"
- dropped excludearch sparc
- de-activated japanese patches 100 and 200 for now 
  (they need to be fixed and tested wth 2.2.0)
- separated swat.desktop file from spec-file and added
  german translations
- moved /etc/sysconfig/samba to a separate source-file
- use htmlview instead of direct call to netscape in 
  swat.desktop-file

* Mon May  7 2001 Bill Nottingham <notting@redhat.com>
- device-remove security fix again (<tridge@samba.org>)

* Fri Apr 20 2001 Bill Nottingham <notting@redhat.com>
- fix tempfile security problems, officially (<tridge@samba.org>)
- update to 2.0.8

* Sun Apr  8 2001 Bill Nottingham <notting@redhat.com>
- turn of SSL, kerberos

* Thu Apr  5 2001 Bill Nottingham <notting@redhat.com>
- fix tempfile security problems (patch from <Marcus.Meissner@caldera.de>)

* Thu Mar 29 2001 Bill Nottingham <notting@redhat.com>
- fix quota support, and quotas with the 2.4 kernel (#31362, #33915)

* Mon Mar 26 2001 Nalin Dahyabhai <nalin@redhat.com>
- tweak the PAM code some more to try to do a setcred() after initgroups()
- pull in all of the optflags on i386 and sparc
- don't explicitly enable Kerberos support -- it's only used for password
  checking, and if PAM is enabled it's a no-op anyway

* Mon Mar  5 2001 Tim Waugh <twaugh@redhat.com>
- exit successfully from preun script (bug #30644).

* Fri Mar  2 2001 Nalin Dahyabhai <nalin@redhat.com>
- rebuild in new environment

* Wed Feb 14 2001 Bill Nottingham <notting@redhat.com>
- updated japanese stuff (#27683)

* Fri Feb  9 2001 Bill Nottingham <notting@redhat.com>
- fix trigger (#26859)

* Wed Feb  7 2001 Bill Nottingham <notting@redhat.com>
- add i18n support, japanese patch (#26253)

* Wed Feb  7 2001 Trond Eivind Glomsrød <teg@redhat.com>
- i18n improvements in initscript (#26537)

* Wed Jan 31 2001 Bill Nottingham <notting@redhat.com>
- put smbpasswd in samba-common (#25429)

* Wed Jan 24 2001 Bill Nottingham <notting@redhat.com>
- new i18n stuff

* Sun Jan 21 2001 Bill Nottingham <notting@redhat.com>
- rebuild

* Thu Jan 18 2001 Bill Nottingham <notting@redhat.com>
- i18n-ize initscript
- add a sysconfig file for daemon options (#23550)
- clarify smbpasswd man page (#23370)
- build with LFS support (#22388)
- avoid extraneous pam error messages (#10666)
- add Urban Widmark's bug fixes for smbmount (#19623)
- fix setgid directory modes (#11911)
- split swat into subpackage (#19706)

* Wed Oct 25 2000 Nalin Dahyabhai <nalin@redhat.com>
- set a default CA certificate path in smb.conf (#19010)
- require openssl >= 0.9.5a-20 to make sure we have a ca-bundle.crt file

* Mon Oct 16 2000 Bill Nottingham <notting@redhat.com>
- fix swat only_from line (#18726, others)
- fix attempt to write outside buildroot on install (#17943)

* Mon Aug 14 2000 Bill Nottingham <notting@redhat.com>
- add smbspool back in (#15827)
- fix absolute symlinks (#16125)

* Sun Aug 6 2000 Philipp Knirsch <pknirsch@redhat.com>
- bugfix for smbadduser script (#15148)

* Mon Jul 31 2000 Matt Wilson <msw@redhat.com>
- patch configure.ing (patch11) to disable cups test
- turn off swat by default

* Fri Jul 28 2000 Bill Nottingham <notting@redhat.com>
- fix condrestart stuff

* Fri Jul 21 2000 Bill Nottingham <notting@redhat.com>
- add copytruncate to logrotate file (#14360)
- fix init script (#13708)

* Sat Jul 15 2000 Bill Nottingham <notting@redhat.com>
- move initscript back
- remove 'Using Samba' book from %%doc 
- move stuff to /etc/samba (#13708)
- default configuration tweaks (#13704)
- some logrotate tweaks

* Wed Jul 12 2000 Prospector <bugzilla@redhat.com>
- automatic rebuild

* Tue Jul 11 2000 Bill Nottingham <notting@redhat.com>
- fix logrotate script (#13698)

* Thu Jul  6 2000 Bill Nottingham <notting@redhat.com>
- fix initscripts req (prereq /etc/init.d)

* Wed Jul 5 2000 Than Ngo <than@redhat.de>
- add initdir macro to handle the initscript directory
- add a new macro to handle /etc/pam.d/system-auth

* Thu Jun 29 2000 Nalin Dahyabhai <nalin@redhat.com>
- enable Kerberos 5 and SSL support
- patch for duplicate profile.h headers

* Thu Jun 29 2000 Bill Nottingham <notting@redhat.com>
- fix init script

* Tue Jun 27 2000 Bill Nottingham <notting@redhat.com>
- rename samba logs (#11606)

* Mon Jun 26 2000 Bill Nottingham <notting@redhat.com>
- initscript munging

* Fri Jun 16 2000 Bill Nottingham <notting@redhat.com>
- configure the swat stuff usefully
- re-integrate some specfile tweaks that got lost somewhere

* Thu Jun 15 2000 Bill Nottingham <notting@redhat.com>
- rebuild to get rid of cups dependency

* Wed Jun 14 2000 Nalin Dahyabhai <nalin@redhat.com>
- tweak logrotate configurations to use the PID file in /var/lock/samba

* Sun Jun 11 2000 Bill Nottingham <notting@redhat.com>
- rebuild in new environment

* Thu Jun  1 2000 Nalin Dahyabhai <nalin@redhat.com>
- change PAM setup to use system-auth

* Mon May  8 2000 Bill Nottingham <notting@redhat.com>
- fixes for ia64

* Sat May  6 2000 Bill Nottingham <notting@redhat.com>
- switch to %%configure

* Wed Apr 26 2000 Nils Philippsen <nils@redhat.de>
- version 2.0.7

* Sun Mar 26 2000 Florian La Roche <Florian.LaRoche@redhat.com>
- simplify preun

* Thu Mar 16 2000 Bill Nottingham <notting@redhat.com>
- fix yp_get_default_domain in autoconf
- only link against readline for smbclient
- fix log rotation (#9909)

* Fri Feb 25 2000 Bill Nottingham <notting@redhat.com>
- fix trigger, again.

* Mon Feb  7 2000 Bill Nottingham <notting@redhat.com>
- fix trigger.

* Fri Feb  4 2000 Bill Nottingham <notting@redhat.com>
- turn on quota support

* Mon Jan 31 2000 Cristian Gafton <gafton@redhat.com>
- rebuild to fox dependencies
- man pages are compressed

* Fri Jan 21 2000 Bill Nottingham <notting@redhat.com>
- munge post scripts slightly

* Wed Jan 19 2000 Bill Nottingham <notting@redhat.com>
- turn on mmap again. Wheee.
- ship smbmount on alpha

* Mon Dec  6 1999 Bill Nottingham <notting@redhat.com>
- turn off mmap. ;)

* Wed Dec  1 1999 Bill Nottingham <notting@redhat.com>
- change /var/log/samba to 0700
- turn on mmap support

* Thu Nov 11 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.6

* Fri Oct 29 1999 Bill Nottingham <notting@redhat.com>
- add a %defattr for -common

* Tue Oct  5 1999 Bill Nottingham <notting@redhat.com>
- shift some files into -client
- remove /home/samba from package.

* Tue Sep 28 1999 Bill Nottingham <notting@redhat.com>
- initscript oopsie. killproc <name> -HUP, not other way around.

* Sat Sep 26 1999 Bill Nottingham <notting@redhat.com>
- script cleanups. Again.

* Wed Sep 22 1999 Bill Nottingham <notting@redhat.com>
- add a patch to fix dropped reconnection attempts

* Mon Sep  6 1999 Jeff Johnson <jbj@redhat.com>
- use cp rather than mv to preserve /etc/services perms (#4938 et al).
- use mktemp to generate /etc/tmp.XXXXXX file name.
- add prereqs on sed/mktemp/killall (need to move killall to /bin).
- fix trigger syntax (i.e. "samba < 1.9.18p7" not "samba < samba-1.9.18p7")

* Mon Aug 30 1999 Bill Nottingham <notting@redhat.com>
- sed "s|nawk|gawk|" /usr/bin/convert_smbpasswd

* Sat Aug 21 1999 Bill Nottingham <notting@redhat.com>
- fix typo in mount.smb

* Fri Aug 20 1999 Bill Nottingham <notting@redhat.com>
- add a %trigger to work around (sort of) broken scripts in
  previous releases

* Mon Aug 16 1999 Bill Nottingham <notting@redhat.com>
- initscript munging

* Mon Aug  9 1999 Bill Nottingham <notting@redhat.com>
- add domain parsing to mount.smb

* Fri Aug  6 1999 Bill Nottingham <notting@redhat.com>
- add a -common package, shuffle files around.

* Fri Jul 23 1999 Bill Nottingham <notting@redhat.com>
- add a chmod in %postun so /etc/services & inetd.conf don't become unreadable

* Wed Jul 21 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.5
- fix mount.smb - smbmount options changed again.........
- fix postun. oops.
- update some stuff from the samba team's spec file.

* Fri Jun 18 1999 Bill Nottingham <notting@redhat.com>
- split off clients into separate package
- don't run samba by default

* Mon Jun 14 1999 Bill Nottingham <notting@redhat.com>
- fix one problem with mount.smb script
- fix smbpasswd on sparc with a really ugly kludge

* Thu Jun 10 1999 Dale Lovelace <dale@redhat.com>
- fixed logrotate script

* Tue May 25 1999 Bill Nottingham <notting@redhat.com>
- turn of 64-bit locking on 32-bit platforms

* Thu May 20 1999 Bill Nottingham <notting@redhat.com>
- so many releases, so little time
- explicitly uncomment 'printing = bsd' in sample config

* Tue May 18 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.4a
- fix mount.smb arg ordering

* Fri Apr 16 1999 Bill Nottingham <notting@redhat.com>
- go back to stop/start for restart (-HUP didn't work in testing)

* Fri Mar 26 1999 Bill Nottingham <notting@redhat.com>
- add a mount.smb to make smb mounting a little easier.
- smb filesystems apparently don't work on alpha. Oops.

* Thu Mar 25 1999 Bill Nottingham <notting@redhat.com>
- always create codepages

* Tue Mar 23 1999 Bill Nottingham <notting@redhat.com>
- logrotate changes

* Sun Mar 21 1999 Cristian Gafton <gafton@redhat.com> 
- auto rebuild in the new build environment (release 3)

* Fri Mar 19 1999 Preston Brown <pbrown@redhat.com>
- updated init script to use graceful restart (not stop/start)

* Tue Mar  9 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.3

* Thu Feb 18 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.2

* Mon Feb 15 1999 Bill Nottingham <notting@redhat.com>
- swat swat

* Tue Feb  9 1999 Bill Nottingham <notting@redhat.com>
- fix bash2 breakage in post script

* Fri Feb  5 1999 Bill Nottingham <notting@redhat.com>
- update to 2.0.0

* Mon Oct 12 1998 Cristian Gafton <gafton@redhat.com>
- make sure all binaries are stripped

* Thu Sep 17 1998 Jeff Johnson <jbj@redhat.com>
- update to 1.9.18p10.
- fix %triggerpostun.

* Tue Jul 07 1998 Erik Troan <ewt@redhat.com>
- updated postun triggerscript to check $0
- clear /etc/codepages from %preun instead of %postun

* Mon Jun 08 1998 Erik Troan <ewt@redhat.com>
- made the %postun script a tad less agressive; no reason to remove
  the logs or lock file (after all, if the lock file is still there,
  samba is still running)
- the %postun and %preun should only exectute if this is the final
  removal
- migrated %triggerpostun from Red Hat's samba package to work around
  packaging problems in some Red Hat samba releases

* Sun Apr 26 1998 John H Terpstra <jht@samba.anu.edu.au>
- minor tidy up in preparation for release of 1.9.18p5
- added findsmb utility from SGI package

* Wed Mar 18 1998 John H Terpstra <jht@samba.anu.edu.au>
- Updated version and codepage info.
- Release to test name resolve order

* Sat Jan 24 1998 John H Terpstra <jht@samba.anu.edu.au>
- Many optimisations (some suggested by Manoj Kasichainula <manojk@io.com>
- Use of chkconfig in place of individual symlinks to /etc/rc.d/init/smb
- Compounded make line
- Updated smb.init restart mechanism
- Use compound mkdir -p line instead of individual calls to mkdir
- Fixed smb.conf file path for log files
- Fixed smb.conf file path for incoming smb print spool directory
- Added a number of options to smb.conf file
- Added smbadduser command (missed from all previous RPMs) - Doooh!
- Added smbuser file and smb.conf file updates for username map

