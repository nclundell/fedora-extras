%global debug_package %{nil}

Name:    systemctl-tui
Version: 0.4.0
Release: %autorelease
Summary: A fast, simple TUI for interacting with systemd services and their logs.  

License: MIT
URL:     https://github.com/rgwood/%{name}
Source:  %{url}/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo
BuildRequires: rust

%description
systemctl-tui can quickly browse service status and logs, start/stop/restart/reload services, and view/edit unit files. It aims to do a small number of things well.

%prep
%autosetup -n %{name}-%{version}

%build
export RUSTFLAGS="%{build_rustflags}"
cargo build --release --locked

# Generate license documentation
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}' | sort -u > LICENSE.summary
cargo tree --workspace --edges no-build,no-dev,no-proc-macro --no-dedupe --prefix none --format '{l}: {p}' | sort -u > LICENSE.dependencies

%install
install -Dpm 0755 target/release/systemctl-tui -t %{buildroot}%{_bindir}/

%check
%{buildroot}%{_bindir}/systemctl-tui --version

%files
%doc README.md
%license LICENSE LICENSE.summary LICENSE.dependencies
%{_bindir}/systemctl-tui

%changelog
%autochangelog
