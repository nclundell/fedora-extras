%global debug_package %{nil}

Name:    bluetui
Version: 0.6
Release: %autorelease
Summary: TUI for managing bluetooth on Linux
License: GPL-3.0-or-later
URL:     https://github.com/pythops/%{name}
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
TUI for managing bluetooth on Linux

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

%install
install -Dpm 0755 target/release/bluetui -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/bluetui --version

%files
%license LICENSE
%doc README.md
%{_bindir}/bluetui

%changelog
%autochangelog
