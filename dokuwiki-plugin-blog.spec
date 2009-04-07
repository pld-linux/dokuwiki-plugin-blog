%define		plugin		blog
Summary:	DokuWiki Blog Plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	20080718
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://www.chimeric.de/_src/plugin-blog.tgz
# Source0-md5:	772b602ffaf2270c1d8611e8a5243e3c
Source1:	dokuwiki-find-lang.sh
URL:		http://www.dokuwiki.org/plugin:blog
Requires:	dokuwiki >= 20061106
Requires:	dokuwiki-plugin-include
Requires:	dokuwiki-plugin-pagelist
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

%description
This plugin makes blogs in your wiki easily possible.

%prep
%setup -q -n %{plugin}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
rm -rf $RPM_BUILD_ROOT%{plugindir}/{blog.tar.gz,COPYING,README,VERSION}

# find locales
sh %{SOURCE1} %{name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README
%dir %{plugindir}
%{plugindir}/*.php
%{plugindir}/*.css
%{plugindir}/conf
%{plugindir}/syntax
