%undefine _debugsource_template
%define module ruff
%define oname ruff

# NOTE	Run create_vendored_crate_archive.sh script to create vendor archive-
# NOTE	when you update this package, submit archive to to abf and update-
# NOTE	Source1 & yml.

Name:		python-ruff
Version:	0.15.10
Release:	1
Summary:	An extremely fast Python linter and code formatter, written in Rust
License:	MIT
Group:		Development/Python
URL:		https://pypi.org/project/ruff/
Source0:	https://files.pythonhosted.org/packages/source/r/ruff/%{oname}-%{version}.tar.gz
Source1:	%{module}-%{version}-vendor.tar.xz
BuildSystem:	python

BuildRequires:	cargo
BuildRequires:	make
BuildRequires:	pkgconfig(python)
BuildRequires:	python
BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(maturin)
BuildRequires:	python%{pyver}dist(wheel)
BuildRequires:	rust-packaging

%description
An extremely fast Python linter and code formatter, written in Rust.

Ruff aims to be orders of magnitude faster than alternative tools while
integrating more functionality behind a single, common interface.

%prep
%autosetup -n %{module}-%{version} -p1 -a1
%cargo_prep -v vendor

cat >>.cargo/config <<EOF
[source.crates-io]
replace-with = "vendored-sources"

[source."git+https://github.com/astral-sh/lsp-types.git?rev=e15db0593f0ecbbd80599c3f5880e4bf5da1ca0c"]
git = "https://github.com/astral-sh/lsp-types.git"
rev = "e15db0593f0ecbbd80599c3f5880e4bf5da1ca0c"
replace-with = "vendored-sources"

[source."git+https://github.com/salsa-rs/salsa.git?rev=2f687a17ceea8ec7aaa605561ccbde938ccef086"]
git = "https://github.com/salsa-rs/salsa.git"
rev = "2f687a17ceea8ec7aaa605561ccbde938ccef086"
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"
EOF

%build -p
export CARGO_HOME=$PWD/.cargo
# sort out crate licenses
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%files
%license LICENSE LICENSES.dependencies
%{_bindir}/%{module}
%{python3_sitearch}/%{module}
%{python3_sitearch}/%{module}-%{version}.dist-info
