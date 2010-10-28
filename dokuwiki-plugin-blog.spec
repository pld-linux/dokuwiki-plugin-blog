%define		plugin		blog
Summary:	DokuWiki Blog Plugin
Name:		dokuwiki-plugin-%{plugin}
Version:	20090912
Release:	0.1
License:	GPL v2
Group:		Applications/WWW
Source0:	http://cloud.github.com/downloads/dokufreaks/plugin-blog/plugin-blog.tgz
# Source0-md5:	d722e48067ffccc6786b9ad25e9dcb4e
URL:		http://www.dokuwiki.org/plugin:blog
BuildRequires:	rpmbuild(macros) >= 1.520
Requires:	dokuwiki >= 20080505
Requires:	dokuwiki-plugin-include
Requires:	dokuwiki-plugin-pagelist
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dokuconf	/etc/webapps/dokuwiki
%define		dokudir		/usr/share/dokuwiki
%define		plugindir	%{dokudir}/lib/plugins/%{plugin}
%define		find_lang 	%{_usrlibrpm}/dokuwiki-find-lang.sh %{buildroot}

%description
The Blog Plugin makes blogs in your wiki easily possible. The blog
component shows the latest entries (pages) from a namespace in reverse
chronological order.

%prep
%setup -qc
mv %{plugin}/* .

version=$(cat VERSION)
if [ "$(echo "$version" | tr -d -)" != %{version} ]; then
	: %%{version} mismatch
	exit 1
fi

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{plugindir}
cp -a . $RPM_BUILD_ROOT%{plugindir}
rm $RPM_BUILD_ROOT%{plugindir}/{COPYING,README,VERSION,_template.txt}

# find locales
%find_lang %{name}.lang

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
%{plugindir}/*.php
%{plugindir}/*.css
%{plugindir}/conf
%{plugindir}/syntax
