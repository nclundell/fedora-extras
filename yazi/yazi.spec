%global debug_package %{nil}

Name:    yazi
Version: 25.5.31
Release: %autorelease
Summary: Blazing Fast Terminal File Manager
License: MIT
URL:     https://crates.io/crates/yazi-cli
Source:  %{crates_source}

BuildRequires: cargo-rpm-macros

Recommends: fd-find
Recommends: file
Recommends: ffmpeg
Recommends: fzf
Recommends: git
Recommends: git-delta
Recommends: imagmagick
Recommends: jq
Recommends: mediainfo
Recommends: p7zip
Recommends: p7zip-plugins
Recommends: poppler-utils
Recommends: resvg
Recommends: ripgrep
Recommends: zoxide

%description
Yazi is a blazing fast terminal file manager written in Rust.

%prep
%autosetup -n %{crate}-%{version}

%__cargo vendor
%cargo_prep -v vendor

%build
%cargo_build
%{cargo_license} > LICENSE.dependencies

%install
%define cargo_install_lib 0
%cargo_install

%check
%cargo_test

%files -n %{crate}
%doc README.md
%license LICENSE
%license LICENSE.summary
%license LICENSE.dependencies
%{_bindir}/ya
%{_bindir}/yazi

%changelog
%autochangelog
