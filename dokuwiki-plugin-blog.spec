%define		subver	2023-10-24
%define		ver		%(echo %{subver} | tr -d -)
%define		plugin		blog
%define		php_min_version 5.3.0
Summary:	DokuWiki Blog Plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	%{ver}
Release:	1
License:	GPL v2
Group:		Applications/WWW
Source0:	https://github.com/dokufreaks/plugin-blog/archive/a23a795c008ce738c509615fa426436a04052827/%{plugin}-%{subver}.tar.gz
# Source0-md5:	27bbff2464337b6214130d0c9257c6cb
URL:		https://www.dokuwiki.org/plugin:blog
BuildRequires:	rpmbuild(find_lang) >= 1.41
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20131208
Requires:	php(core) >= %{php_min_version}
Requires:	dokuwiki-plugin-include
Requires:	dokuwiki-plugin-pagelist
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}

%description
The Blog Plugin makes blogs in your wiki easily possible. The blog
component shows the latest entries (pages) from a namespace in reverse
chronological order.

%prep
%setup -qc
mv plugin-%{plugin}-*/* .

%build
version=$(awk '/^date/{print $2}' plugin.info.txt)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
rm $RPM_BUILD_ROOT%{plugindir}/{COPYING,README,_template.txt}

# find locales
%find_lang %{name}.lang --with-dokuwiki

%clean
rm -rf $RPM_BUILD_ROOT

%post
# force css cache refresh
if [ -f %{dokuconf}/local.php ]; then
	touch %{dokuconf}/local.php
fi

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc README _template.txt
%dir %{plugindir}
%{plugindir}/*.css
%{plugindir}/*.php
%{plugindir}/*.txt
%{plugindir}/conf
%{plugindir}/syntax
