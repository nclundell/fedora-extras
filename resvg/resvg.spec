%global debug_package %{nil}
%global crate resvg

Name:           resvg
Version:        0.45.1
Release:        %autorelease
Summary:        SVG rendering library
License:        Apache-2.0 OR MIT
URL:            https://crates.io/crates/resvg
Source:         %{crates_source}

BuildRequires:  cargo-rpm-macros

%description
An SVG rendering library.

%prep
%autosetup -n %{crate}-%{version} -p1

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
%license LICENSE-APACHE
%license LICENSE-MIT
%license LICENSE.dependencies
%doc README.md
%{_bindir}/resvg

%changelog
%autochangelog
