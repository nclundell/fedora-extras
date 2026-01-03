%global debug_package %{nil}

Name:    yazi
Version: 25.12.29
Release: %autorelease
Summary: Blazing Fast Terminal File Manager
License: MIT
URL:            https://yazi-rs.github.io 
Source:         https://github.com/sxyazi/yazi/archive/refs/tags/v%{version}.tar.gz

BuildRequires: cargo-rpm-macros

Recommends: fd-find
Recommends: file
Recommends: ffmpeg
Recommends: fzf
Recommends: git
Recommends: git-delta
Recommends: imagmagick
Recommends: jq
Recommends: p7zip
Recommends: p7zip-plugins
Recommends: poppler-utils
Recommends: resvg
Recommends: ripgrep
Recommends: zoxide

%description
Yazi is a blazing fast terminal file manager written in Rust.

%prep
%autosetup -n %{name}-%{version}

%__cargo vendor
%cargo_prep -v vendor

%build
export YAZI_GEN_COMPLETIONS=1 
%cargo_build
%{cargo_license} > LICENSE.dependencies

%install
install -Dpm 0755 -t %{buildroot}%{_bindir} target/release/yazi target/release/ya 
install -Dpm 0644 yazi-boot/completions/%{name}.bash yazi-cli/completions/ya.bash -t %{buildroot}%{bash_completions_dir}
install -Dpm 0644 yazi-boot/completions/%{name}.fish yazi-cli/completions/ya.fish -t %{buildroot}%{fish_completions_dir}
install -Dpm 0644 yazi-boot/completions/%{name}.nu yazi-cli/completions/ya.nu -t %{buildroot}%{_datadir}/nushell/completions/
install -Dpm 0644 yazi-boot/completions/_%{name}     yazi-cli/completions/_ya     -t %{buildroot}%{zsh_completions_dir}

%if %{with check}
%check
%cargo_test
%endif

%files
%doc README.md
%license LICENSE
%license LICENSE.dependencies
%{_bindir}/ya
%{_bindir}/yazi
%{bash_completions_dir}/%{name}.bash
%{bash_completions_dir}/ya.bash
%{_datadir}/nushell/completions/%{name}.nu
%{_datadir}/nushell/completions/ya.nu
%{zsh_completions_dir}/_%{name}
%{zsh_completions_dir}/_ya
%{fish_completions_dir}/%{name}.fish
%{fish_completions_dir}/ya.fish

%changelog
%autochangelog
